# Step-by-Step Security Scan Website Pemerintah

## 🚀 **PERSIAPAN ENVIRONMENT**

### Step 1: Masuk ke Directory Security Audit

```powershell
cd "c:\Kampanye Keamanan Siber\security-audit"
```

### Step 2: Aktivasi Virtual Environment (Opsional tapi Recommended)

```powershell
# Buat virtual environment jika belum ada
python -m venv .venv

# Aktivasi virtual environment
.venv\Scripts\activate

# Verify Python version
python --version
```

### Step 3: Install Dependencies

```powershell
# Install semua package yang dibutuhkan
pip install -r requirements.txt

# Atau install manual jika ada masalah:
pip install requests beautifulsoup4 reportlab cryptography urllib3
```

### Step 4: Verify Installation

```powershell
# Test import modules
python -c "import requests, bs4, reportlab; print('All modules installed successfully')"
```

---

## 🔍 **MENJALANKAN SECURITY SCAN**

### Step 5: Scan Website Target

```powershell
# Format dasar:
python website_scanner.py [URL_WEBSITE]

# Contoh scan website pemerintah:
python website_scanner.py https://kotimkab.go.id
python website_scanner.py https://pemkabbogor.go.id
python website_scanner.py https://jakarta.go.id
python website_scanner.py https://bandung.go.id

# Untuk website dengan subdomain:
python website_scanner.py https://diskominfo.kotimkab.go.id
```

### Step 6: Monitor Progress Scan

```powershell
# Scan akan menampilkan progress seperti:
# [INFO] Starting security scan for: https://kotimkab.go.id
# [INFO] Checking SSL certificate...
# [INFO] Analyzing security headers...
# [INFO] Scanning for vulnerabilities...
# [INFO] Generating report...
# [SUCCESS] Scan completed successfully!
```

---

## 📊 **MELIHAT HASIL SCAN**

### Step 7: Check Hasil JSON

```powershell
# File hasil scan akan tersimpan dengan format:
# security_scan_[domain]_[timestamp].json

# Lihat daftar file hasil scan:
dir security_scan_*.json

# Baca hasil scan terakhir:
type security_scan_kotimkab.go.id_*.json

# Atau dengan PowerShell untuk formatting yang lebih baik:
Get-Content security_scan_kotimkab.go.id_*.json | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## 📄 **GENERATE LAPORAN PDF**

### Step 8: Buat Professional Report

```powershell
# Generate PDF report dari hasil JSON
python report_generator.py security_scan_kotimkab.go.id_20250712_*.json

# Atau specify file JSON tertentu:
python report_generator.py "security_scan_kotimkab.go.id_20250712_154530.json"
```

### Step 9: Buka Laporan PDF

```powershell
# File PDF akan tersimpan dengan format:
# security_report_[domain]_[timestamp].pdf

# Buka PDF report:
start security_report_kotimkab.go.id_*.pdf

# Atau lihat daftar semua report:
dir security_report_*.pdf
```

---

## 🎯 **CONTOH SCAN MULTIPLE WEBSITES**

### Step 10: Batch Scan Multiple Sites

```powershell
# Buat list website yang akan di-scan
$websites = @(
    "https://kotimkab.go.id",
    "https://pemkabbogor.go.id",
    "https://jakarta.go.id",
    "https://bandung.go.id",
    "https://surabaya.go.id"
)

# Loop scan semua website
foreach ($site in $websites) {
    Write-Host "Scanning: $site" -ForegroundColor Green
    python website_scanner.py $site
    Start-Sleep -Seconds 5  # Jeda 5 detik antar scan
}
```

### Step 11: Generate All Reports

```powershell
# Generate PDF untuk semua hasil scan
Get-ChildItem security_scan_*.json | ForEach-Object {
    Write-Host "Generating report for: $($_.Name)" -ForegroundColor Yellow
    python report_generator.py $_.Name
}
```

---

## 🛠️ **TROUBLESHOOTING**

### Jika Ada Error SSL Certificate:

```powershell
# Tambahkan parameter untuk skip SSL verification (hanya untuk testing)
python website_scanner.py https://kotimkab.go.id --skip-ssl-verify
```

### Jika Website Lambat/Timeout:

```powershell
# Tingkatkan timeout (default 10 detik)
python website_scanner.py https://kotimkab.go.id --timeout 30
```

### Jika Ada Error Permission:

```powershell
# Jalankan PowerShell sebagai Administrator, atau:
# Ubah execution policy sementara
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Jika Module Error:

```powershell
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt --upgrade
```

---

## 📋 **QUICK REFERENCE COMMANDS**

### Scan Single Website:

```powershell
python website_scanner.py https://[domain].go.id
```

### View JSON Results:

```powershell
type security_scan_*.json
```

### Generate PDF Report:

```powershell
python report_generator.py security_scan_*.json
```

### Open Latest Report:

```powershell
start security_report_*.pdf
```

### Clean Old Files:

```powershell
# Hapus file scan lama (opsional)
del security_scan_*.json
del security_report_*.pdf
```

---

## 🎯 **WEBSITE PEMERINTAH YANG BISA DI-TEST**

### Website Kabupaten/Kota:

- https://kotimkab.go.id (Timika)
- https://pemkabbogor.go.id (Bogor)
- https://bandung.go.id (Bandung)
- https://jakarta.go.id (Jakarta)
- https://surabaya.go.id (Surabaya)

### Website Provinsi:

- https://jabarprov.go.id (Jawa Barat)
- https://jatengprov.go.id (Jawa Tengah)
- https://jatimprov.go.id (Jawa Timur)

### Website Kementerian:

- https://kominfo.go.id
- https://kemenkeu.go.id
- https://kemendagri.go.id

---

## ⚡ **ONE-LINER COMMANDS**

### Quick Scan + Report:

```powershell
python website_scanner.py https://kotimkab.go.id; python report_generator.py security_scan_kotimkab.go.id_*.json; start security_report_kotimkab.go.id_*.pdf
```

### Scan with Timestamp:

```powershell
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"; python website_scanner.py https://kotimkab.go.id; echo "Scan completed at: $timestamp"
```

---

**📝 Note:**

- Pastikan koneksi internet stabil
- Beberapa website pemerintah mungkin memiliki rate limiting
- Hasil scan disimpan otomatis dengan timestamp
- Gunakan VPN jika ada blocking dari website tertentu
- Scan membutuhkan waktu 1-3 menit per website tergantung ukuran dan response time
