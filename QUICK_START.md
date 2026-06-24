# 🚀 Quick Start - Deploy ke Streamlit Cloud

## ⚡ Cara Cepat (5 Menit)

### 1️⃣ Persiapan Lokal
```bash
# Pastikan semua file sudah ter-commit
git status
git add .
git commit -m "Ready for Streamlit deployment"
git push
```

### 2️⃣ Deploy ke Streamlit Cloud
1. Buka https://streamlit.io/cloud
2. Login dengan GitHub
3. Klik "New app"
4. Pilih repository: `USERNAME/data-indo` (atau nama repo Anda)
5. Branch: `main`
6. File: `streamlit_app.py`
7. **KLIK DEPLOY!** ✨

### 3️⃣ Selesai! 🎉
URL aplikasi Anda:
```
https://[app-name]-[username].streamlit.app
```

---

## 🧪 Test Lokal Dulu (Optional)

```bash
pip install streamlit plotly
streamlit run streamlit_app.py
```
Aplikasi terbuka di: http://localhost:8501

---

## 📊 Yang Ada di Aplikasi Anda

✅ **Dashboard** - Statistik populasi terbaru
✅ **Grafik** - Visualisasi bar & line chart  
✅ **Prediksi** - ML predictions dengan 2 algorithms
✅ **Insight** - Analisis per kelompok umur

---

## ⚠️ PENTING!

✅ Pastikan file `.csv` sudah di-GitHub:
```bash
git add *.csv
git push
```

✅ Pastikan `requirements.txt` update dengan Streamlit:
```
streamlit==1.28.0
plotly==5.17.0
```

---

## 📖 Detail Lengkap?

Baca: `DEPLOYMENT_GUIDE.md`

---

## 🆘 Ada Error?

1. Check "Logs" di Streamlit Cloud (Settings)
2. Baca error message
3. Fix di code lokal
4. Push ke GitHub (auto redeploy)

---

**Good luck! 🚀**
