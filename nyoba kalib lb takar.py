

import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Aplikasi Kalibrasi Volume", layout="wide")
st.title("Aplikasi Kalibrasi Volume - Labu Takar")

# Input volume konvensional
v_konven = st.number_input("Masukkan Volume Konvensional (mL)", min_value=0.0, step=0.1)

# Template input tabel kosong
st.subheader("Input Data Pengukuran")
cols = [
    "Bobot Kosong (g)",
    "Bobot Isi (g)",
    "Suhu Air (C)",
    "Suhu Udara (C)",
    "Tekanan Udara (mmHg)",
    "Kelembaban (%)"
]
def_data = [["" for _ in range(len(cols))] for _ in range(5)]  # 5 baris kosong
df = st.data_editor(pd.DataFrame(def_data, columns=cols), use_container_width=True)

# Tombol proses
if st.button("Hitung"):
    try:
        # Validasi input kosong
        if df.isnull().values.any() or (df == "").values.any():
            st.error("❌ Semua kolom harus diisi sebelum menghitung!")
            st.stop()

        # Ambil data dari dataframe
        kosong = df["Bobot Kosong (g)"].astype(float).tolist()
        isi = df["Bobot Isi (g)"].astype(float).tolist()
        suhu_air = df["Suhu Air (C)"].astype(float).tolist()
        suhu_udara = df["Suhu Udara (C)"].astype(float).tolist()
        tekanan = df["Tekanan Udara (mmHg)"].astype(float).tolist()
        kelembaban = df["Kelembaban (%)"].astype(float).tolist()

        # Validasi panjang data sama
        if not all(len(lst) == len(kosong) for lst in [isi, suhu_air, suhu_udara, tekanan, kelembaban]):
            st.error("❌ Jumlah data di semua kolom harus sama!")
            st.stop()

        # Hitung bobot isi
        hasil = [b - a for a, b in zip(kosong, isi)]

        # Hitung rata-rata
        rata = {
            "bobot_kosong": sum(kosong) / len(kosong),
            "bobot_isi": sum(isi) / len(isi),
            "isi": sum(hasil) / len(hasil),
            "suhu_air": sum(suhu_air) / len(suhu_air),
            "suhu_udara": sum(suhu_udara) / len(suhu_udara),
            "tekanan": sum(tekanan) / len(tekanan),
            "kelembaban": sum(kelembaban) / len(kelembaban)
        }

        # Hitung densitas air
        T = rata["suhu_air"]
        dens_air = 0.999974 - (((T - 3.989)**2) * (T + 338.636)) / (563385.4 * (T + 72.45147))

        # Hitung densitas udara
        dens_udara = ((0.464554 * rata["tekanan"]) - rata["kelembaban"]*(0.00252*rata["suhu_udara"]-0.020582)) / ((237.15+rata["suhu_udara"])*1000)

        # Hitung volume sebenarnya
        massa = sum(hasil)
        koef_muai = 1e-5
        v_20 = massa * (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)

        koreksi = v_20 - v_konven

        # Output hasil
        st.subheader("Hasil Perhitungan")
        st.write(f"Rata-rata Bobot Isi: **{rata['isi']:.4f} g**")
        st.write(f"Densitas Air: **{dens_air:.7f} g/mL**")
        st.write(f"Densitas Udara: **{dens_udara:.7f} g/mL**")
        st.write(f"Volume Sebenarnya (20°C): **{v_20:.7f} mL**")
        st.write(f"Koreksi terhadap Volume Konvensional: **{koreksi:+.6f} mL**")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
