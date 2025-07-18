import streamlit as st

st.set_page_config(
    page_title="Panduan Kalibrasi Volume",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Panduan Penggunaan Aplikasi Kalibrasi Volume")

st.markdown("""
Selamat datang di **Aplikasi Kalibrasi Volume Labu Takar**. Berikut ini adalah langkah-langkah penggunaannya:

### 📌 Langkah-Langkah Penggunaan

1. Masukkan volume konvensional labu takar.
2. Isi data pengukuran pada tabel yang disediakan.
3. Tekan tombol **"Hitung Rata-rata Data Pengukuran"**.
4. Masukkan data alat ukur: **NST, U95, dan K**.
5. Tekan tombol **"Hitung Volume & Ketidakpastian"** untuk mendapatkan hasil akhir kalibrasi.

### 📎 Tips:
- Pastikan semua kolom pada tabel dan input terisi.
- Gunakan nilai yang sesuai dengan satuan masing-masing alat ukur.
- Data ketidakpastian seperti LOP neraca dan nilai K harus akurat untuk hasil yang tepat.

👉 Silakan buka tab **"Kalibrasi Volume"** di sidebar untuk mulai melakukan perhitungan.
""")

st.info("Untuk akurasi terbaik, gunakan data hasil pengamatan nyata dan alat ukur yang telah dikalibrasi.")
