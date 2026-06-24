# 📱 Panduan Deploy ke Streamlit Cloud

Aplikasi Anda sudah siap untuk di-deploy ke Streamlit Cloud! Ikuti langkah-langkah di bawah ini.

## 📋 Prasyarat

✅ GitHub account (gratis di https://github.com)
✅ Code sudah di-commit ke GitHub repository
✅ Streamlit Cloud account (gratis di https://streamlit.io/cloud)

---

## 🚀 Langkah-langkah Deployment

### Step 1: Push Kode ke GitHub

Pastikan semua file sudah ter-push ke GitHub repository Anda:

```bash
# Jika belum ada git repository
git init
git add .
git commit -m "Add Streamlit app"
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git push -u origin main

# Jika sudah ada
git add streamlit_app.py .streamlit/config.toml requirements.txt
git commit -m "Convert to Streamlit app"
git push
```

**Pastikan file-file ini ada di repository:**
- ✅ `streamlit_app.py` (file utama Streamlit)
- ✅ `requirements.txt` (dependencies)
- ✅ `.streamlit/config.toml` (konfigurasi)
- ✅ Semua file `.csv` (data files)
- ✅ `.gitignore` (optional tapi recommended)

---

### Step 2: Deploy ke Streamlit Cloud

1. **Login ke Streamlit Cloud**
   - Buka https://streamlit.io/cloud
   - Klik "Sign in"
   - Login dengan GitHub account Anda

2. **Create New App**
   - Klik "New app" (tombol berwarna biru)
   - Pilih repository Anda
   - Pilih branch: `main` atau `master`
   - Masukkan path ke file: `streamlit_app.py`

3. **Selesai!**
   - Tunggu proses build (beberapa menit)
   - URL aplikasi Anda akan muncul (format: `https://appname-username.streamlit.app`)

---

## 📊 Screenshoot Proses

### A. Di GitHub
```
data-indo/
├── streamlit_app.py          ← File utama Streamlit
├── requirements.txt          ← Dependencies
├── .streamlit/
│   └── config.toml          ← Konfigurasi Streamlit
├── app.py                   ← File lama (Flask) - boleh dihapus
├── *.csv                    ← Data files (PENTING: harus ada di repo!)
└── ...
```

### B. Di Streamlit Cloud Deploy Config
```
Repository: USERNAME/data-indo
Branch: main
File: streamlit_app.py
```

---

## ⚠️ Hal Penting untuk Diperhatikan

### 1. **Data Files**
   ⚠️ Semua file `.csv` HARUS ada di GitHub repository!
   ```bash
   git add data_penduduk_konsolidasi_2019_2025.csv
   git add "Jumlah Penduduk Menurut Kelompok Umur*"
   git commit -m "Add data files"
   git push
   ```

### 2. **File Size Limit**
   - GitHub: Max 100MB per file (file CSV Anda harus OK)
   - Jika ada yang terlalu besar, gunakan `.gitignore`:
   ```
   # .gitignore
   __pycache__/
   *.pyc
   .env
   .DS_Store
   venv/
   ```

### 3. **Secrets Management** (Opsional)
   Jika ada credentials/API keys, gunakan Streamlit Secrets:
   1. Buka Settings aplikasi di Streamlit Cloud
   2. Klik "Secrets" 
   3. Tambahkan secrets dalam format TOML

---

## 🐛 Troubleshooting

### Error: "File not found: data_penduduk_konsolidasi_2019_2025.csv"
**Solusi:** Pastikan file CSV ada di repository dan di-commit.
```bash
git status  # Lihat apakah file CSV ada
git add data_penduduk_konsolidasi_2019_2025.csv
git push
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"
**Solusi:** Pastikan `requirements.txt` berisi `streamlit==1.28.0` dan sudah di-push.

### Aplikasi berjalan lambat
**Solusi:** Streamlit Cloud free tier terbatas resources. Anda bisa:
- Upgrade ke paid plan
- Optimize code untuk lebih cepat
- Cache data lebih agresif dengan `@st.cache_data`

### Aplikasi crash/error saat load
**Solusi:** 
1. Buka Logs di Streamlit Cloud (Settings → Logs)
2. Cari error message
3. Fix code dan push ke GitHub
4. Refresh aplikasi (otomatis redeployed)

---

## 📱 Testing Lokal Sebelum Deploy

Sebelum deploy ke production, test aplikasi Streamlit di lokal Anda:

```bash
# Install dependencies
pip install -r requirements.txt

# Run aplikasi Streamlit
streamlit run streamlit_app.py
```

Aplikasi akan terbuka di http://localhost:8501

---

## ✅ Checklist Sebelum Deploy

- [ ] File `streamlit_app.py` sudah dibuat
- [ ] File `.streamlit/config.toml` sudah ada
- [ ] `requirements.txt` berisi Streamlit dan Plotly
- [ ] Semua file `.csv` sudah di-commit ke GitHub
- [ ] Git repository sudah di-push ke GitHub
- [ ] Test lokal berjalan lancar (tanpa error)
- [ ] Streamlit Cloud account sudah siap
- [ ] Sudah siap deploy! 🚀

---

## 📞 Support

Jika ada masalah:
1. Check Logs di Streamlit Cloud
2. Baca dokumentasi Streamlit: https://docs.streamlit.io
3. Cek GitHub repository structure

---

## 🎉 Selamat!

Aplikasi Anda sekarang online dan bisa diakses oleh siapa saja! 

**Share link Anda:**
- Format: `https://app-name-username.streamlit.app`
- Bisa di-share ke social media, email, atau website Anda

---

## 💡 Improvement Ideas (Opsional)

Untuk membuat aplikasi lebih baik:
1. **Add Download Button** - Export prediksi ke Excel
2. **Add Comparison** - Bandingkan beberapa daerah sekaligus
3. **Add Custom Slider** - User bisa pilih tahun prediksi
4. **Add Comments** - Insight/penjelasan tentang data
5. **Add Authentication** - Login untuk fitur premium

