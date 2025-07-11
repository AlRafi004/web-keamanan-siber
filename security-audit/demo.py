#!/usr/bin/env python3
"""
Demo script untuk menjalankan security scanner dengan contoh website pemerintah daerah
"""

import os
import sys
import subprocess
from website_scanner import WebsiteSecurityScanner
from report_generator import SecurityReportGenerator

def main():
    """Demo script untuk kampanye keamanan siber"""
    print("🛡️  DEMO: Website Security Scanner")
    print("Kampanye Keamanan Siber Indonesia")
    print("="*60)
    
    # Contoh website pemerintah daerah (gunakan yang real untuk testing)
    demo_websites = [
        "https://jakarta.go.id",
        "https://bandung.go.id", 
        "https://surabaya.go.id",
        "https://jogja.go.id",
        "https://semarang.go.id"
    ]
    
    print("Pilih website untuk demo scan:")
    for i, website in enumerate(demo_websites, 1):
        print(f"{i}. {website}")
    print("6. Input manual")
    
    try:
        choice = input("\nPilihan (1-6): ").strip()
        
        if choice == "6":
            target_url = input("Masukkan URL website: ").strip()
        elif choice in ['1', '2', '3', '4', '5']:
            target_url = demo_websites[int(choice) - 1]
        else:
            print("Pilihan tidak valid!")
            return
        
        print(f"\n🔍 Scanning: {target_url}")
        print("-" * 60)
        
        # Run security scan
        scanner = WebsiteSecurityScanner(target_url)
        results = scanner.scan()
        
        # Show summary
        scanner.print_summary()
        
        # Save results
        json_file = scanner.save_results()
        
        # Generate PDF report
        print(f"\n📊 Generating PDF report...")
        generator = SecurityReportGenerator(json_file)
        pdf_file = generator.generate_report()
        
        print(f"\n✅ Demo completed!")
        print(f"📁 JSON Results: {json_file}")
        print(f"📄 PDF Report: {pdf_file}")
        
        # Open files (Windows)
        if os.name == 'nt':
            try:
                os.startfile(pdf_file)
                print(f"📖 Opening PDF report...")
            except:
                print("💡 Buka file PDF secara manual untuk melihat laporan")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo dibatalkan oleh user")
    except Exception as e:
        print(f"\n❌ Error during demo: {str(e)}")
        print("💡 Pastikan semua dependencies sudah terinstall:")
        print("   pip install -r requirements.txt")

if __name__ == "__main__":
    main()
