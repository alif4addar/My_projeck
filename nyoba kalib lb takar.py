import streamlit as st
import pandas as pd
import numpy as np
import math
import statistics

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

# Kontrol jumlah baris
if "rows" not in st.session_state:
    st.session_state.rows = 1

def add_row():
    st.session_state.rows += 1

def remove_row():
    if st.session_state.rows > 1:
        st.session_state.rows -= 1

col1, col2 = st.columns(2)
with col1:
    st.button("+ Tambah Baris", on_click=add_row)
with col2:
    st.button("- Hapus Baris", on_click=remove_row)

def_data = [["" for _ in range(len(cols))] for _ in range(st.session_state.rows)]
df = st.data_editor(pd.DataFrame(def_data, columns=cols), use_container_width=True, num_rows="dynamic")

# Input alat ukur tambahan
st.subheader("Input Data Alat Ukur")
st.markdown("Masukkan nilai satuan terkecil (NST), U95, dan K masing-masing alat ukur:")
col_nst, col_u95, col_k = st.columns(3)

with col_nst:
    nst = [st.number_input(f"NST {label}", value=0.0, key=f"nst{i}") for i, label in enumerate(cols)]
with col_u95:
    u95 = [st.number_input(f"U95 {label}", value=0.0, key=f"u95{i}") for i, label in enumerate(cols)]
with col_k:
    k_val = [st.number_input(f"K {label}", value=1.0, key=f"k{i}") for i, label in enumerate(cols)]

# Input LOP
lop = st.number_input("Masukkan Nilai LOP Timbangan", value=0.0)

# Tombol proses
if st.button("Hitung"):
    try:
        if df.isnull().values.any() or (df == "").values.any():
            st.error("❌ Semua kolom harus diisi sebelum menghitung!")
            st.stop()

        kosong = df["Bobot Kosong (g)"].astype(float).tolist()
        isi = df["Bobot Isi (g)"].astype(float).tolist()
        suhu_air = df["Suhu Air (C)"].astype(float).tolist()
        suhu_udara = df["Suhu Udara (C)"].astype(float).tolist()
        tekanan = df["Tekanan Udara (mmHg)"].astype(float).tolist()
        kelembaban = df["Kelembaban (%)"].astype(float).tolist()

        if not all(len(lst) == len(kosong) for lst in [isi, suhu_air, suhu_udara, tekanan, kelembaban]):
            st.error("❌ Jumlah data di semua kolom harus sama!")
            st.stop()

        hasil = [b - a for a, b in zip(kosong, isi)]

        rata = {
            "bobot_kosong": sum(kosong) / len(kosong),
            "bobot_isi": sum(isi) / len(isi),
            "isi": sum(hasil) / len(hasil),
            "suhu_air": sum(suhu_air) / len(suhu_air),
            "suhu_udara": sum(suhu_udara) / len(suhu_udara),
            "tekanan": sum(tekanan) / len(tekanan),
            "kelembaban": sum(kelembaban) / len(kelembaban)
        }

        T = rata["suhu_air"]
        dens_air = 0.999974 - (((T - 3.989)**2) * (T + 338.636)) / (563385.4 * (T + 72.45147))
        dens_udara = ((0.464554 * rata["tekanan"]) - rata["kelembaban"]*(0.00252*rata["suhu_udara"]-0.020582)) / ((237.15+rata["suhu_udara"])*1000)

        massa = sum(hasil)
        koef_muai = 1e-5
        v_20 = massa * (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)
        koreksi = v_20 - v_konven

        # Ketidakpastian U1
        k_neraca = (lop/(2*math.sqrt(3)))
        k_ulangan = statistics.stdev(hasil)/(math.sqrt(len(hasil)))
        U1 = math.sqrt(k_neraca**2 + k_ulangan**2)
        Cs1 = (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)

        # U2 suhu air
        U2 = u95[2]/k_val[2]
        Cs2 = massa * (-koef_muai) / (dens_air - dens_udara)

        # U3 densitas air
        Ut = u95[2]/k_val[2]
        Ci = -((5.32e-6 * T**2 + 1.20e-4*T + 2.82e-5) / ((T + 72.45147)**2))
        U3 = abs(Ut * Ci)
        Cs3 = -massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)

        # U4 densitas udara
        Uh = u95[5]/k_val[5]
        Up = u95[4]/k_val[4]
        Ut = u95[3]/k_val[3]
        Ch = (0.020582 - 0.00252*rata["suhu_udara"]) / ((237.15 + rata["suhu_udara"]) * 1000)
        Cp = (0.464554) / ((237.15 + rata["suhu_udara"]) * 1000)
        Ct = (-0.6182*rata["kelembaban"] - 0.46554*rata["tekanan"]) / (((237.15 + rata["suhu_udara"])**2) * 1000)
        U4 = math.sqrt((Uh*Ch)**2 + (Up*Cp)**2 + (Ut*Ct)**2)
        Cs4 = massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)

        # U5 koef muai
        U5 = (0.1 * koef_muai) / math.sqrt(3)
        Cs5 = massa * (20 - T) / (dens_air - dens_udara)

        # U6 meniskus
        U6 = (0.05 * nst[0]) / math.sqrt(3)
        Cs6 = 1

        Ugab = math.sqrt((U1*Cs1)**2 + (U2*Cs2)**2 + (U3*Cs3)**2 + (U4*Cs4)**2 + (U5*Cs5)**2 + (U6*Cs6)**2)
        U95_exp = Ugab * 2

        st.subheader("Hasil Perhitungan")
        st.write(f"Rata-rata Bobot Isi: **{rata['isi']:.4f} g**")
        st.write(f"Densitas Air: **{dens_air:.7f} g/mL**")
        st.write(f"Densitas Udara: **{dens_udara:.7f} g/mL**")
        st.write(f"Volume Sebenarnya (20°C): **{v_20:.7f} mL**")
        st.write(f"Koreksi terhadap Volume Konvensional: **{koreksi:+.6f} mL**")

        st.subheader("Ketidakpastian")
        st.write(f"Ugab (Gabungan): **{Ugab:.6f} mL**")
        st.write(f"Ketidakpastian Diperluas (U95): **{U95_exp:.6f} mL**")

    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
