#!/usr/bin/env python3
"""
Website Security Scanner
Kampanye Keamanan Siber - Tool untuk basic security assessment website pemerintah daerah
"""

import requests
import ssl
import socket
import urllib3
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import warnings
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class WebsiteSecurityScanner:
    def __init__(self, target_url, timeout=10):
        self.target_url = target_url.rstrip('/')
        self.timeout = timeout
        self.domain = urlparse(target_url).netloc
        self.results = {
            'target': target_url,
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities': [],
            'security_headers': {},
            'ssl_info': {},
            'server_info': {},
            'forms_analysis': [],
            'external_links': [],
            'recommendations': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Security-Scanner/1.0 (Cybersecurity Education Campaign)'
        })

    def scan(self):
        """Main scanning function"""
        print(f"🔍 Starting security scan for: {self.target_url}")
        print("=" * 60)
        
        try:
            # Basic connectivity test
            response = self.session.get(self.target_url, timeout=self.timeout, verify=False)
            self.results['response_code'] = response.status_code
            self.results['response_time'] = response.elapsed.total_seconds()
            
            if response.status_code == 200:
                print("✅ Website accessible")
                
                # Run all security checks
                self.check_ssl_security()
                self.check_security_headers(response)
                self.check_server_information(response)
                self.analyze_html_content(response)
                self.check_common_vulnerabilities()
                self.check_directory_listing()
                self.check_backup_files()
                self.generate_recommendations()
                
                print("\n✅ Scan completed successfully!")
            else:
                print(f"❌ Website returned status code: {response.status_code}")
                self.results['vulnerabilities'].append({
                    'severity': 'medium',
                    'type': 'HTTP Response',
                    'description': f'Website returned non-200 status code: {response.status_code}'
                })
                
        except requests.RequestException as e:
            print(f"❌ Error accessing website: {str(e)}")
            self.results['vulnerabilities'].append({
                'severity': 'high',
                'type': 'Connectivity',
                'description': f'Cannot access website: {str(e)}'
            })
        
        return self.results

    def check_ssl_security(self):
        """Check SSL/TLS configuration"""
        print("🔒 Checking SSL/TLS security...")
        
        try:
            # Parse domain from URL
            parsed_url = urlparse(self.target_url)
            hostname = parsed_url.netloc
            port = 443 if parsed_url.scheme == 'https' else 80
            
            if parsed_url.scheme == 'https':
                # Get SSL certificate info
                context = ssl.create_default_context()
                with socket.create_connection((hostname, port), timeout=self.timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        cipher = ssock.cipher()
                        
                        self.results['ssl_info'] = {
                            'has_ssl': True,
                            'issuer': dict(x[0] for x in cert['issuer']),
                            'subject': dict(x[0] for x in cert['subject']),
                            'version': cert['version'],
                            'not_before': cert['notBefore'],
                            'not_after': cert['notAfter'],
                            'cipher_suite': cipher[0] if cipher else None,
                            'protocol': cipher[1] if cipher else None
                        }
                
                # Check certificate expiry
                expiry_date = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_until_expiry = (expiry_date - datetime.now()).days
                
                if days_until_expiry < 30:
                    self.results['vulnerabilities'].append({
                        'severity': 'high',
                        'type': 'SSL Certificate',
                        'description': f'SSL certificate expires in {days_until_expiry} days'
                    })
                elif days_until_expiry < 90:
                    self.results['vulnerabilities'].append({
                        'severity': 'medium',
                        'type': 'SSL Certificate',
                        'description': f'SSL certificate expires in {days_until_expiry} days'
                    })
                
                print("✅ SSL certificate validated")
            else:
                self.results['ssl_info']['has_ssl'] = False
                self.results['vulnerabilities'].append({
                    'severity': 'high',
                    'type': 'SSL/TLS',
                    'description': 'Website does not use HTTPS encryption'
                })
                print("❌ No SSL/TLS encryption detected")
                
        except Exception as e:
            self.results['vulnerabilities'].append({
                'severity': 'medium',
                'type': 'SSL Check',
                'description': f'Unable to verify SSL configuration: {str(e)}'
            })
            print(f"⚠️  SSL check failed: {str(e)}")

    def check_security_headers(self, response):
        """Check for important security headers"""
        print("🛡️  Checking security headers...")
        
        security_headers = {
            'X-Frame-Options': 'Prevents clickjacking attacks',
            'X-Content-Type-Options': 'Prevents MIME type sniffing',
            'X-XSS-Protection': 'Basic XSS protection',
            'Strict-Transport-Security': 'Enforces HTTPS connections',
            'Content-Security-Policy': 'Prevents various injection attacks',
            'Referrer-Policy': 'Controls referrer information leakage',
            'Permissions-Policy': 'Controls browser feature permissions'
        }
        
        headers_found = {}
        for header, description in security_headers.items():
            if header in response.headers:
                headers_found[header] = response.headers[header]
                print(f"✅ {header}: {response.headers[header]}")
            else:
                self.results['vulnerabilities'].append({
                    'severity': 'medium',
                    'type': 'Missing Security Header',
                    'description': f'Missing {header} header - {description}'
                })
                print(f"❌ Missing: {header}")
        
        self.results['security_headers'] = headers_found
        
        # Check for sensitive information disclosure
        if 'Server' in response.headers:
            server_info = response.headers['Server']
            if any(tech in server_info.lower() for tech in ['apache', 'nginx', 'iis']):
                if '/' in server_info:  # Version information disclosed
                    self.results['vulnerabilities'].append({
                        'severity': 'low',
                        'type': 'Information Disclosure',
                        'description': f'Server version disclosed: {server_info}'
                    })

    def check_server_information(self, response):
        """Analyze server information and technology stack"""
        print("🖥️  Analyzing server information...")
        
        self.results['server_info'] = {
            'server': response.headers.get('Server', 'Unknown'),
            'powered_by': response.headers.get('X-Powered-By', 'Unknown'),
            'technology_stack': []
        }
        
        # Detect technologies from headers and HTML
        tech_indicators = {
            'PHP': ['X-Powered-By', 'Set-Cookie'],
            'ASP.NET': ['X-AspNet-Version', 'X-Powered-By'],
            'Apache': ['Server'],
            'Nginx': ['Server'],
            'IIS': ['Server'],
            'WordPress': ['wp-content', 'wp-includes'],
            'Drupal': ['X-Generator', 'drupal'],
            'Joomla': ['X-Content-Encoded-By']
        }
        
        detected_tech = []
        for tech, indicators in tech_indicators.items():
            for indicator in indicators:
                if indicator in response.headers:
                    header_value = response.headers[indicator].lower()
                    if tech.lower() in header_value:
                        detected_tech.append(tech)
                        break
        
        self.results['server_info']['technology_stack'] = detected_tech

    def analyze_html_content(self, response):
        """Analyze HTML content for security issues"""
        print("📄 Analyzing HTML content...")
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Check for forms and their security
            forms = soup.find_all('form')
            for form in forms:
                form_analysis = {
                    'action': form.get('action', ''),
                    'method': form.get('method', 'GET').upper(),
                    'has_csrf_token': False,
                    'inputs': []
                }
                
                # Check for CSRF protection
                csrf_indicators = ['csrf', 'token', '_token', 'authenticity_token']
                inputs = form.find_all('input')
                
                for input_tag in inputs:
                    input_info = {
                        'type': input_tag.get('type', 'text'),
                        'name': input_tag.get('name', ''),
                        'required': input_tag.has_attr('required')
                    }
                    form_analysis['inputs'].append(input_info)
                    
                    # Check for CSRF tokens
                    if any(indicator in input_tag.get('name', '').lower() for indicator in csrf_indicators):
                        form_analysis['has_csrf_token'] = True
                
                # Security recommendations for forms
                if form_analysis['method'] == 'POST' and not form_analysis['has_csrf_token']:
                    self.results['vulnerabilities'].append({
                        'severity': 'medium',
                        'type': 'CSRF Protection',
                        'description': f'Form without CSRF protection: {form_analysis["action"]}'
                    })
                
                self.results['forms_analysis'].append(form_analysis)
            
            # Check for external links
            links = soup.find_all('a', href=True)
            external_links = []
            
            for link in links:
                href = link['href']
                if href.startswith('http') and self.domain not in href:
                    external_links.append(href)
            
            self.results['external_links'] = list(set(external_links))
            
            # Check for sensitive comments
            comments = soup.find_all(string=lambda text: isinstance(text, str) and '<!--' in text)
            for comment in comments:
                if any(keyword in comment.lower() for keyword in ['password', 'api', 'key', 'secret', 'admin']):
                    self.results['vulnerabilities'].append({
                        'severity': 'low',
                        'type': 'Information Disclosure',
                        'description': 'Sensitive information found in HTML comments'
                    })
            
        except Exception as e:
            print(f"⚠️  HTML analysis failed: {str(e)}")

    def check_common_vulnerabilities(self):
        """Check for common web vulnerabilities"""
        print("🎯 Testing for common vulnerabilities...")
        
        # Test for directory traversal
        traversal_payloads = ['../../../etc/passwd', '..\\..\\..\\windows\\system32\\drivers\\etc\\hosts']
        for payload in traversal_payloads:
            try:
                test_url = f"{self.target_url}/{payload}"
                response = self.session.get(test_url, timeout=5, verify=False)
                if 'root:' in response.text or 'localhost' in response.text:
                    self.results['vulnerabilities'].append({
                        'severity': 'high',
                        'type': 'Directory Traversal',
                        'description': f'Possible directory traversal vulnerability detected'
                    })
                    break
            except:
                continue
        
        # Test for SQL injection (basic)
        sql_payloads = ["'", "' OR 1=1--", "'; DROP TABLE users;--"]
        for payload in sql_payloads:
            try:
                test_url = f"{self.target_url}?id={payload}"
                response = self.session.get(test_url, timeout=5, verify=False)
                if any(error in response.text.lower() for error in ['sql', 'mysql', 'oracle', 'postgresql', 'sqlite']):
                    self.results['vulnerabilities'].append({
                        'severity': 'high',
                        'type': 'SQL Injection',
                        'description': 'Possible SQL injection vulnerability detected'
                    })
                    break
            except:
                continue

    def check_directory_listing(self):
        """Check for directory listing vulnerabilities"""
        print("📂 Checking for directory listing...")
        
        common_dirs = [
            '/admin/', '/administrator/', '/wp-admin/', '/cpanel/',
            '/phpmyadmin/', '/backup/', '/uploads/', '/files/',
            '/documents/', '/downloads/', '/temp/', '/tmp/'
        ]
        
        for directory in common_dirs:
            try:
                test_url = f"{self.target_url}{directory}"
                response = self.session.get(test_url, timeout=5, verify=False)
                
                if 'Index of' in response.text or 'Directory Listing' in response.text:
                    self.results['vulnerabilities'].append({
                        'severity': 'medium',
                        'type': 'Directory Listing',
                        'description': f'Directory listing enabled: {directory}'
                    })
            except:
                continue

    def check_backup_files(self):
        """Check for exposed backup and configuration files"""
        print("📋 Checking for exposed sensitive files...")
        
        sensitive_files = [
            '/robots.txt', '/.htaccess', '/web.config', '/sitemap.xml',
            '/backup.sql', '/backup.zip', '/database.sql', '/config.php',
            '/.env', '/wp-config.php', '/configuration.php', '/settings.php'
        ]
        
        for file_path in sensitive_files:
            try:
                test_url = f"{self.target_url}{file_path}"
                response = self.session.get(test_url, timeout=5, verify=False)
                
                if response.status_code == 200:
                    if file_path in ['/robots.txt', '/sitemap.xml']:
                        # These are normal files
                        continue
                    else:
                        self.results['vulnerabilities'].append({
                            'severity': 'medium',
                            'type': 'Exposed File',
                            'description': f'Sensitive file accessible: {file_path}'
                        })
            except:
                continue

    def generate_recommendations(self):
        """Generate security recommendations based on findings"""
        print("💡 Generating security recommendations...")
        
        recommendations = []
        
        # SSL recommendations
        if not self.results['ssl_info'].get('has_ssl', False):
            recommendations.append({
                'priority': 'High',
                'category': 'Encryption',
                'recommendation': 'Implement SSL/TLS encryption (HTTPS) for all website traffic'
            })
        
        # Security headers recommendations
        missing_headers = []
        important_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security']
        
        for header in important_headers:
            if header not in self.results['security_headers']:
                missing_headers.append(header)
        
        if missing_headers:
            recommendations.append({
                'priority': 'Medium',
                'category': 'Security Headers',
                'recommendation': f'Implement missing security headers: {", ".join(missing_headers)}'
            })
        
        # Form security recommendations
        if self.results['forms_analysis']:
            forms_without_csrf = [form for form in self.results['forms_analysis'] 
                                if form['method'] == 'POST' and not form['has_csrf_token']]
            if forms_without_csrf:
                recommendations.append({
                    'priority': 'Medium',
                    'category': 'CSRF Protection',
                    'recommendation': 'Implement CSRF protection for all POST forms'
                })
        
        # General recommendations
        recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Server Configuration',
                'recommendation': 'Hide server version information to prevent information disclosure'
            },
            {
                'priority': 'Low',
                'category': 'Content Security',
                'recommendation': 'Implement Content Security Policy (CSP) headers'
            },
            {
                'priority': 'Low',
                'category': 'Monitoring',
                'recommendation': 'Set up security monitoring and logging for suspicious activities'
            }
        ])
        
        self.results['recommendations'] = recommendations

    def save_results(self, filename=None):
        """Save scan results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"security_scan_{self.domain}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        
        print(f"📁 Results saved to: {filename}")
        return filename

    def print_summary(self):
        """Print scan summary"""
        print("\n" + "="*60)
        print("🔍 SECURITY SCAN SUMMARY")
        print("="*60)
        print(f"Target: {self.target_url}")
        print(f"Scan Time: {self.results['scan_time']}")
        print(f"Total Vulnerabilities: {len(self.results['vulnerabilities'])}")
        
        # Count by severity
        severity_count = {'high': 0, 'medium': 0, 'low': 0}
        for vuln in self.results['vulnerabilities']:
            severity_count[vuln['severity']] += 1
        
        print(f"  - High: {severity_count['high']}")
        print(f"  - Medium: {severity_count['medium']}")
        print(f"  - Low: {severity_count['low']}")
        
        print(f"\nSSL/TLS: {'✅ Enabled' if self.results['ssl_info'].get('has_ssl') else '❌ Disabled'}")
        print(f"Security Headers: {len(self.results['security_headers'])}/7 implemented")
        print(f"Forms Found: {len(self.results['forms_analysis'])}")
        print(f"External Links: {len(self.results['external_links'])}")
        
        if self.results['vulnerabilities']:
            print("\n🚨 TOP VULNERABILITIES:")
            for i, vuln in enumerate(self.results['vulnerabilities'][:5], 1):
                severity_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
                print(f"{i}. {severity_emoji[vuln['severity']]} {vuln['type']}: {vuln['description']}")
        
        print("\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(self.results['recommendations'][:3], 1):
            priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
            print(f"{i}. {priority_emoji[rec['priority']]} {rec['category']}: {rec['recommendation']}")

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Website Security Scanner for Cybersecurity Campaign')
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('-o', '--output', help='Output filename for results')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='Request timeout in seconds')
    
    args = parser.parse_args()
    
    # Validate URL
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    print("🛡️  Website Security Scanner")
    print("Kampanye Keamanan Siber Indonesia")
    print("="*60)
    
    scanner = WebsiteSecurityScanner(args.url, timeout=args.timeout)
    results = scanner.scan()
    
    scanner.print_summary()
    
    # Save results
    output_file = scanner.save_results(args.output)
    
    print(f"\n📊 Detailed results saved to: {output_file}")
    print("\n🔐 Gunakan hasil scan ini untuk meningkatkan keamanan website Anda!")

if __name__ == "__main__":
    main()
