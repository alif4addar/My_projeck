"""
# simpan sebagai app.py

import streamlit as st

st.title("Perhitungan Bobot Labu Takar")

st.header("1. Input Data Bobot Labu Takar Kosong")
lb_kosong = []
i = 1
while True:
    value = st.text_input(f"Bobot Labu Kosong ke-{i} (gram):", key=f"kosong_{i}")
    if value == "":
        break
    try:
        lb_kosong.append(float(value))
        i += 1
    except:
        st.error("Masukkan angka yang valid")
        break

st.header("2. Input Data Bobot Labu Takar + Isi")
lb_isi = []
i = 1
while True:
    value = st.text_input(f"Bobot Labu Isi ke-{i} (gram):", key=f"isi_{i}")
    if value == "":
        break
    try:
        lb_isi.append(float(value))
        i += 1
    except:
        st.error("Masukkan angka yang valid")
        break

if st.button("Hitung"):
    if len(lb_kosong) != len(lb_isi):
        st.error("Jumlah data kosong dan isi tidak sama!")
    else:
        hasil = [isi - kosong for kosong, isi in zip(lb_kosong, lb_isi)]
        st.subheader("Hasil Bobot Isi:")
        for idx, val in enumerate(hasil, 1):
            st.write(f"Hasil ke-{idx}: {val:.4f} gram")

        st.subheader("Rata-Rata:")
        xx = ["Bobot Labu Kosong", "Bobot Labu Isi", "Bobot Isi"]
        yy = [lb_kosong, lb_isi, hasil]
        for nama, data in zip(xx, yy):
            st.write(f"Rata-rata {nama}: {sum(data)/len(data):.4f} gram")

st.header("3. Input Nilai Satuan Terkecil Alat Ukur")
alat_ukur = {}
aa = ["Timbangan", "Termometer Air", "Termometer Udara", "Barometer Udara", "Hygrometer"]
bb = ["mg", "C", "C", "mmHg", "%"]

for m, n in zip(aa, bb):
    nilai = st.text_input(f"{m} ({n})", key=m)
    alat_ukur[m] = nilai

"""







import streamlit as st
import pandas as pd

st.set_page_config(page_title="Aplikasi Kalibrasi Volume", layout="wide")
st.title("Aplikasi Kalibrasi Volume - Labu Takar")

# Input volume konvensional
v_konven = st.number_input("Masukkan Volume Konvensional (mL)", min_value=0.0, step=0.1)

# Template input tabel
st.subheader("Input Data Pengukuran")
cols = [
    "Bobot Kosong (g)",
    "Bobot Isi (g)",
    "Suhu Air (C)",
    "Suhu Udara (C)",
    "Tekanan Udara (mmHg)",
    "Kelembaban (%)"
]
def_data = [[1.0, 49.9999, 25.0, 27.0, 759.0, 68.0] for _ in range(3)]
df = st.data_editor(pd.DataFrame(def_data, columns=cols), use_container_width=True)

# Tombol proses
if st.button("Hitung"):
    try:
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

