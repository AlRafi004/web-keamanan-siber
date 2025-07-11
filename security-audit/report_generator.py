#!/usr/bin/env python3
"""
Report Generator untuk Security Audit
Membuat laporan PDF dari hasil scan keamanan website
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
import json
from datetime import datetime
import os

class SecurityReportGenerator:
    def __init__(self, scan_results_file):
        """Initialize report generator with scan results"""
        with open(scan_results_file, 'r', encoding='utf-8') as f:
            self.results = json.load(f)
        
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
        
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.lightgrey,
            borderPadding=5
        ))
        
        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            textColor=colors.darkgreen
        ))
        
        self.styles.add(ParagraphStyle(
            name='VulnHigh',
            parent=self.styles['Normal'],
            textColor=colors.red,
            fontSize=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='VulnMedium',
            parent=self.styles['Normal'],
            textColor=colors.orange,
            fontSize=10
        ))
        
        self.styles.add(ParagraphStyle(
            name='VulnLow',
            parent=self.styles['Normal'],
            textColor=colors.green,
            fontSize=10
        ))

    def generate_report(self, output_filename=None):
        """Generate complete security assessment report"""
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = self.results['target'].replace('https://', '').replace('http://', '').replace('/', '_')
            output_filename = f"security_report_{domain}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        story = []
        
        # Build report content
        story.extend(self.create_title_page())
        story.append(PageBreak())
        
        story.extend(self.create_executive_summary())
        story.append(PageBreak())
        
        story.extend(self.create_vulnerability_details())
        story.append(PageBreak())
        
        story.extend(self.create_technical_findings())
        story.append(PageBreak())
        
        story.extend(self.create_recommendations())
        story.append(PageBreak())
        
        story.extend(self.create_appendix())
        
        # Build PDF
        doc.build(story)
        print(f"📊 Security report generated: {output_filename}")
        return output_filename

    def create_title_page(self):
        """Create report title page"""
        story = []
        
        # Title
        story.append(Paragraph("LAPORAN AUDIT KEAMANAN WEBSITE", self.styles['CustomTitle']))
        story.append(Spacer(1, 30))
        
        # Target info
        story.append(Paragraph("Target Website:", self.styles['SectionHeader']))
        story.append(Paragraph(self.results['target'], self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Scan info
        scan_time = datetime.fromisoformat(self.results['scan_time']).strftime("%d %B %Y, %H:%M WIB")
        
        info_data = [
            ['Tanggal Scan:', scan_time],
            ['Response Code:', str(self.results.get('response_code', 'N/A'))],
            ['Response Time:', f"{self.results.get('response_time', 0):.2f} detik"],
            ['Total Vulnerabilities:', str(len(self.results['vulnerabilities']))],
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(info_table)
        story.append(Spacer(1, 40))
        
        # Campaign info
        story.append(Paragraph("KAMPANYE KEAMANAN SIBER INDONESIA", self.styles['SectionHeader']))
        story.append(Paragraph(
            "Laporan ini merupakan bagian dari Kampanye Keamanan Siber untuk meningkatkan "
            "awareness dan implementasi keamanan website pemerintah daerah.",
            self.styles['Normal']
        ))
        
        return story

    def create_executive_summary(self):
        """Create executive summary section"""
        story = []
        
        story.append(Paragraph("RINGKASAN EKSEKUTIF", self.styles['SectionHeader']))
        
        # Summary statistics
        total_vulns = len(self.results['vulnerabilities'])
        severity_count = {'high': 0, 'medium': 0, 'low': 0}
        
        for vuln in self.results['vulnerabilities']:
            severity_count[vuln['severity']] += 1
        
        # Overall security rating
        security_score = self.calculate_security_score()
        security_rating = self.get_security_rating(security_score)
        
        summary_text = f"""
        Audit keamanan website telah dilakukan terhadap {self.results['target']} pada tanggal {datetime.fromisoformat(self.results['scan_time']).strftime("%d %B %Y")}.
        
        <b>Hasil Keseluruhan:</b>
        • Total vulnerabilities ditemukan: {total_vulns}
        • Tingkat keamanan: {security_rating} ({security_score}/100)
        • SSL/TLS Status: {'Aktif' if self.results['ssl_info'].get('has_ssl') else 'Tidak Aktif'}
        • Security Headers: {len(self.results['security_headers'])}/7 diimplementasikan
        
        <b>Distribusi Severity:</b>
        • High Risk: {severity_count['high']} item
        • Medium Risk: {severity_count['medium']} item  
        • Low Risk: {severity_count['low']} item
        """
        
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Recommendations summary
        if severity_count['high'] > 0:
            priority_text = "Perlu tindakan segera untuk mengatasi vulnerabilities dengan tingkat risiko tinggi."
        elif severity_count['medium'] > 0:
            priority_text = "Disarankan untuk mengatasi vulnerabilities dengan tingkat risiko menengah dalam waktu dekat."
        else:
            priority_text = "Keamanan website sudah cukup baik, lakukan monitoring rutin."
        
        story.append(Paragraph(f"<b>Prioritas Tindakan:</b> {priority_text}", self.styles['Normal']))
        
        return story

    def create_vulnerability_details(self):
        """Create detailed vulnerability section"""
        story = []
        
        story.append(Paragraph("DETAIL VULNERABILITIES", self.styles['SectionHeader']))
        
        if not self.results['vulnerabilities']:
            story.append(Paragraph("✅ Tidak ditemukan vulnerability yang signifikan.", self.styles['Normal']))
            return story
        
        # Group by severity
        vulns_by_severity = {'high': [], 'medium': [], 'low': []}
        for vuln in self.results['vulnerabilities']:
            vulns_by_severity[vuln['severity']].append(vuln)
        
        # High severity
        if vulns_by_severity['high']:
            story.append(Paragraph("🔴 HIGH RISK VULNERABILITIES", self.styles['SubHeader']))
            for i, vuln in enumerate(vulns_by_severity['high'], 1):
                story.append(Paragraph(f"{i}. <b>{vuln['type']}</b>", self.styles['VulnHigh']))
                story.append(Paragraph(f"   {vuln['description']}", self.styles['Normal']))
                story.append(Spacer(1, 8))
        
        # Medium severity
        if vulns_by_severity['medium']:
            story.append(Paragraph("🟡 MEDIUM RISK VULNERABILITIES", self.styles['SubHeader']))
            for i, vuln in enumerate(vulns_by_severity['medium'], 1):
                story.append(Paragraph(f"{i}. <b>{vuln['type']}</b>", self.styles['VulnMedium']))
                story.append(Paragraph(f"   {vuln['description']}", self.styles['Normal']))
                story.append(Spacer(1, 8))
        
        # Low severity
        if vulns_by_severity['low']:
            story.append(Paragraph("🟢 LOW RISK VULNERABILITIES", self.styles['SubHeader']))
            for i, vuln in enumerate(vulns_by_severity['low'], 1):
                story.append(Paragraph(f"{i}. <b>{vuln['type']}</b>", self.styles['VulnLow']))
                story.append(Paragraph(f"   {vuln['description']}", self.styles['Normal']))
                story.append(Spacer(1, 8))
        
        return story

    def create_technical_findings(self):
        """Create technical findings section"""
        story = []
        
        story.append(Paragraph("TEMUAN TEKNIS", self.styles['SectionHeader']))
        
        # SSL/TLS Information
        story.append(Paragraph("🔒 SSL/TLS Configuration", self.styles['SubHeader']))
        if self.results['ssl_info'].get('has_ssl'):
            ssl_data = [
                ['SSL Status:', '✅ Aktif'],
                ['Certificate Issuer:', self.results['ssl_info'].get('issuer', {}).get('organizationName', 'N/A')],
                ['Valid Until:', self.results['ssl_info'].get('not_after', 'N/A')],
                ['Cipher Suite:', self.results['ssl_info'].get('cipher_suite', 'N/A')]
            ]
        else:
            ssl_data = [['SSL Status:', '❌ Tidak Aktif']]
        
        ssl_table = Table(ssl_data, colWidths=[2*inch, 3*inch])
        ssl_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(ssl_table)
        story.append(Spacer(1, 15))
        
        # Security Headers
        story.append(Paragraph("🛡️ Security Headers", self.styles['SubHeader']))
        
        important_headers = [
            'X-Frame-Options', 'X-Content-Type-Options', 'X-XSS-Protection',
            'Strict-Transport-Security', 'Content-Security-Policy',
            'Referrer-Policy', 'Permissions-Policy'
        ]
        
        header_data = []
        for header in important_headers:
            status = '✅ Implemented' if header in self.results['security_headers'] else '❌ Missing'
            value = self.results['security_headers'].get(header, 'Not Set')[:50]
            header_data.append([header, status, value])
        
        header_table = Table(header_data, colWidths=[2*inch, 1.5*inch, 2*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 15))
        
        # Server Information
        story.append(Paragraph("🖥️ Server Information", self.styles['SubHeader']))
        server_data = [
            ['Server:', self.results['server_info'].get('server', 'Unknown')],
            ['Powered By:', self.results['server_info'].get('powered_by', 'Unknown')],
            ['Technology Stack:', ', '.join(self.results['server_info'].get('technology_stack', ['Unknown']))]
        ]
        
        server_table = Table(server_data, colWidths=[2*inch, 3*inch])
        server_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(server_table)
        
        return story

    def create_recommendations(self):
        """Create recommendations section"""
        story = []
        
        story.append(Paragraph("REKOMENDASI PERBAIKAN", self.styles['SectionHeader']))
        
        if not self.results['recommendations']:
            story.append(Paragraph("Tidak ada rekomendasi khusus saat ini.", self.styles['Normal']))
            return story
        
        # Group recommendations by priority
        rec_by_priority = {'High': [], 'Medium': [], 'Low': []}
        for rec in self.results['recommendations']:
            rec_by_priority[rec['priority']].append(rec)
        
        for priority in ['High', 'Medium', 'Low']:
            if rec_by_priority[priority]:
                priority_emoji = {'High': '🔴', 'Medium': '🟡', 'Low': '🟢'}
                story.append(Paragraph(f"{priority_emoji[priority]} PRIORITAS {priority.upper()}", self.styles['SubHeader']))
                
                for i, rec in enumerate(rec_by_priority[priority], 1):
                    story.append(Paragraph(f"{i}. <b>{rec['category']}</b>", self.styles['Normal']))
                    story.append(Paragraph(f"   {rec['recommendation']}", self.styles['Normal']))
                    story.append(Spacer(1, 8))
                
                story.append(Spacer(1, 15))
        
        # Implementation timeline
        story.append(Paragraph("📅 TIMELINE IMPLEMENTASI", self.styles['SubHeader']))
        timeline_text = """
        <b>Prioritas Tinggi:</b> 1-2 minggu
        • Implementasi SSL/TLS jika belum ada
        • Perbaikan vulnerability dengan risiko tinggi
        
        <b>Prioritas Menengah:</b> 1-2 bulan  
        • Implementasi security headers
        • Perbaikan konfigurasi server
        
        <b>Prioritas Rendah:</b> 2-6 bulan
        • Optimisasi tambahan
        • Monitoring dan maintenance rutin
        """
        story.append(Paragraph(timeline_text, self.styles['Normal']))
        
        return story

    def create_appendix(self):
        """Create appendix section"""
        story = []
        
        story.append(Paragraph("LAMPIRAN", self.styles['SectionHeader']))
        
        # Forms analysis
        if self.results['forms_analysis']:
            story.append(Paragraph("📋 Analisis Form", self.styles['SubHeader']))
            
            form_data = [['Action', 'Method', 'CSRF Protection', 'Input Count']]
            for form in self.results['forms_analysis']:
                csrf_status = '✅ Yes' if form['has_csrf_token'] else '❌ No'
                form_data.append([
                    form['action'][:30] + '...' if len(form['action']) > 30 else form['action'],
                    form['method'],
                    csrf_status,
                    str(len(form['inputs']))
                ])
            
            form_table = Table(form_data, colWidths=[2*inch, 1*inch, 1.5*inch, 1*inch])
            form_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(form_table)
            story.append(Spacer(1, 15))
        
        # External links
        if self.results['external_links']:
            story.append(Paragraph("🔗 External Links Found", self.styles['SubHeader']))
            story.append(Paragraph(f"Total external links: {len(self.results['external_links'])}", self.styles['Normal']))
            
            # Show first 10 external links
            for i, link in enumerate(self.results['external_links'][:10], 1):
                story.append(Paragraph(f"{i}. {link[:60]}{'...' if len(link) > 60 else ''}", self.styles['Normal']))
            
            if len(self.results['external_links']) > 10:
                story.append(Paragraph(f"... dan {len(self.results['external_links']) - 10} link lainnya", self.styles['Normal']))
        
        # About this scan
        story.append(Spacer(1, 30))
        story.append(Paragraph("TENTANG SCAN INI", self.styles['SubHeader']))
        about_text = """
        Scan keamanan ini menggunakan Website Security Scanner yang dikembangkan khusus untuk 
        Kampanye Keamanan Siber Indonesia. Scanner ini melakukan pemeriksaan otomatis terhadap:
        
        • Konfigurasi SSL/TLS
        • Security headers HTTP
        • Informasi server yang terekspos
        • Vulnerability umum (directory traversal, SQL injection)
        • Analisis form dan CSRF protection
        • Directory listing dan file backup yang terekspos
        
        <b>Disclaimer:</b> Hasil scan ini bersifat informatif dan tidak menggantikan audit keamanan 
        profesional yang komprehensif. Disarankan untuk melakukan penetration testing oleh ahli 
        keamanan siber untuk analisis yang lebih mendalam.
        """
        story.append(Paragraph(about_text, self.styles['Normal']))
        
        return story

    def calculate_security_score(self):
        """Calculate overall security score"""
        score = 100
        
        # Deduct points for vulnerabilities
        for vuln in self.results['vulnerabilities']:
            if vuln['severity'] == 'high':
                score -= 15
            elif vuln['severity'] == 'medium':
                score -= 8
            elif vuln['severity'] == 'low':
                score -= 3
        
        # Deduct points for missing SSL
        if not self.results['ssl_info'].get('has_ssl'):
            score -= 20
        
        # Deduct points for missing security headers
        important_headers = ['X-Frame-Options', 'X-Content-Type-Options', 'Strict-Transport-Security']
        for header in important_headers:
            if header not in self.results['security_headers']:
                score -= 5
        
        return max(0, score)

    def get_security_rating(self, score):
        """Convert score to rating"""
        if score >= 90:
            return "Excellent"
        elif score >= 80:
            return "Good"
        elif score >= 70:
            return "Fair"
        elif score >= 60:
            return "Poor"
        else:
            return "Critical"

def main():
    """Main function for command-line usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate PDF report from security scan results')
    parser.add_argument('scan_file', help='JSON file from security scan')
    parser.add_argument('-o', '--output', help='Output PDF filename')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.scan_file):
        print(f"❌ Scan file not found: {args.scan_file}")
        return
    
    print("📊 Generating security report...")
    
    generator = SecurityReportGenerator(args.scan_file)
    output_file = generator.generate_report(args.output)
    
    print(f"✅ Report generated successfully: {output_file}")

if __name__ == "__main__":
    main()
