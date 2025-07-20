import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import numpy as np
import math
import statistics
from pathlib import Path

st.set_page_config(page_title="Kalibrasi Volume", layout="wide")
v_konven = st.number_input(" Masukkan Volume Konvensional (mL)", min_value=0.0, step=25.0,  format="%.2f")

ketelitian_lb = st.number_input(" Masukkan Ketelitian Labu Takar (mL)", min_value=0.0, step=0.001, format="%.4f")

# --------------------------- Inisialisasi ---------------------------
if "rows" not in st.session_state:
    st.session_state.rows = 3

if "data_pengukuran" not in st.session_state:
    st.session_state.data_pengukuran = pd.DataFrame(
        [["" for _ in range(6)] for _ in range(st.session_state.rows)],
        columns=[
            "Bobot Kosong (g)",
            "Bobot Isi (g)",
            "Suhu Air (C)",
            "Suhu Udara (C)",
            "Tekanan Udara (mmHg)",
            "Kelembaban (%)"
        ]
    )

# --------------------------- Fungsi ---------------------------
def add_row():
    new_row = ["" for _ in range(6)]
    st.session_state.rows += 1
    st.session_state.data_pengukuran.loc[len(st.session_state.data_pengukuran)] = new_row

def remove_row():
    if st.session_state.rows > 1:
        st.session_state.rows -= 1
        st.session_state.data_pengukuran.drop(index=st.session_state.data_pengukuran.index[-1], inplace=True)
        st.session_state.data_pengukuran.reset_index(drop=True, inplace=True)

def reset_data():
    st.session_state.rows = 3
    st.session_state.data_pengukuran = pd.DataFrame(
        [["" for _ in range(6)] for _ in range(3)],
        columns=[
            "Bobot Kosong (g)",
            "Bobot Isi (g)",
            "Suhu Air (C)",
            "Suhu Udara (C)",
            "Tekanan Udara (mmHg)",
            "Kelembaban (%)"
        ]
    )

# --------------------------- Tampilan ---------------------------
st.markdown("""
    <h3 style='color:#5F6F65;'>Input Data Pengukuran</h3>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([3, 6, 3])
with col1:
    st.button(" + Tambah Baris", on_click=add_row)
with col3:
    st.button(" - Hapus Baris", on_click=remove_row)

# Editor
edited_df = st.data_editor(
    st.session_state.data_pengukuran,
    use_container_width=True,
    num_rows="dynamic",
    key="data_editor"
)

# Update data_pengukuran jika ada perubahan
st.session_state.data_pengukuran = edited_df

# Tombol reset
if st.button("🗑️ Hapus Semua Inputan"):
    reset_data()
    st.success("Semua data berhasil dihapus.")

# Hitung Rata-rata
if st.button("Hitung Rata-rata Data Pengukuran"):
    df = st.session_state.data_pengukuran.copy()

    # Validasi
    if (df == "").any().any() or df.isnull().any().any():
        st.warning("⚠️ Semua sel harus diisi sebelum menghitung rata-rata.")
    else:
        try:
            kosong = df["Bobot Kosong (g)"].astype(float).tolist()
            isi = df["Bobot Isi (g)"].astype(float).tolist()
            suhu_air = df["Suhu Air (C)"].astype(float).tolist()
            suhu_udara = df["Suhu Udara (C)"].astype(float).tolist()
            tekanan = df["Tekanan Udara (mmHg)"].astype(float).tolist()
            kelembaban = df["Kelembaban (%)"].astype(float).tolist()

            hasil = [b - a for a, b in zip(kosong, isi)]

            rata = {
                "Bobot Kosong (g)": sum(kosong)/len(kosong),
                "Bobot Isi (g)": sum(isi)/len(isi),
                "Bobot Isi (Hasil) (g)": sum(hasil)/len(hasil),
                "Suhu Air (C)": sum(suhu_air)/len(suhu_air),
                "Suhu Udara (C)": sum(suhu_udara)/len(suhu_udara),
                "Tekanan Udara (mmHg)": sum(tekanan)/len(tekanan),
                "Kelembaban (%)": sum(kelembaban)/len(kelembaban),
                "SEM Bobot Isi (g)": statistics.stdev(hasil) / math.sqrt(len(hasil)) if len(hasil) > 1 else 0
            }

            st.session_state.rata_pengukuran = rata

            st.subheader("Rata-rata Data Pengukuran")
            for k, v in rata.items():
                st.write(f"{k}: **{v:.4f}**")

        except Exception as e:
            st.error(f"Terjadi kesalahan saat menghitung rata-rata: {e}")

# Input untuk ketidakpastian
CC = ["Timbangan","Termometer Air","Termometer Udara","Barometer Udara","Hygrometer"]
satuan = ["g", "C", "C", "mmHg", "%"]
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.markdown("<h3 style='color:#5F6F65;'>Input Alat Ukur</h3>", unsafe_allow_html=True)
lop = st.number_input("Masukkan Nilai LOP Timbangan", value=0.0000, step=0.0001, format="%.4f")
st.markdown("Masukkan nilai NST, U95, dan K untuk alat ukur:")

col_nst, col_u95, col_k = st.columns(3)
with col_nst:
        st.markdown("<h3 style='color:#5F6F65; font-size: 24px;'>NST</h3>", unsafe_allow_html=True)
        nst = [st.number_input(f" {label} ( {satuan[i]} )", value=0.0000, key=f"nst_{i}", step=0.0001, format="%.4f") for i, label in enumerate(CC)]
with col_u95:
        st.markdown("<h3 style='color:#5F6F65; font-size: 24px;'>U95</h3>", unsafe_allow_html=True)
        u95 = [st.number_input(f" {label}", value=0.0000, key=f"u95_{i}", step=0.0001, format="%.4f") for i, label in enumerate(CC)]
with col_k:
        st.markdown("<h3 style='color:#5F6F65; font-size: 24px;'>K</h3>", unsafe_allow_html=True)
        nilai_k = [st.number_input(f" {label}", value=2.0, key=f"kval_{i}", step=0.0001, format="%.4f") for i, label in enumerate(CC)]
    
    
    
    
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.markdown("<h3 style='color:#5F6F65;'>Perhitungan Ketidakpastian</h3>", unsafe_allow_html=True)
    
    # Tombol ngitung ketidakpastian
if "rata_pengukuran" in st.session_state:
        rata = st.session_state.rata_pengukuran
    
        st.divider()
        st.subheader("Perhitungan Volume dan Ketidakpastian")
    
        if st.button("Hitung Volume & Ketidakpastian"):
            try:
                T = rata["Suhu Air (C)"]
                massa = rata["Bobot Isi (Hasil) (g)"]
                suhu_udara = rata["Suhu Udara (C)"]
                tekanan = rata["Tekanan Udara (mmHg)"]
                kelembaban = rata["Kelembaban (%)"]
    
                dens_air = 0.999974 - (((T - 3.989)**2) * (T + 338.636)) / (563385.4 * (T + 72.45147))
                dens_udara = ((0.464554 * tekanan) - kelembaban*(0.00252*suhu_udara-0.020582)) / ((237.15+suhu_udara)*1000)
    
                koef_muai = 1e-5
                v_20 = massa * (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)
                koreksi = abs(v_20 - v_konven)
    
            # Ketidakpastian massa air (U1)
                k_neraca = (lop/(2*math.sqrt(3)))
                k_ulangan = rata["SEM Bobot Isi (g)"]
                U1 = math.sqrt(k_neraca**2 + k_ulangan**2)
                Cs1 = (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)
    
            #Ketidakpastian suhu air (U2)
                U2 = u95[1] / nilai_k[1]
                Cs2 = massa * (-koef_muai) / (dens_air - dens_udara)
    
            #Ketidakpastian densitas air(U3)
                Ut = U2
                Ci = -((5.32e-6 * T**2 + 1.20e-4*T + 2.82e-5) / ((T + 72.45147)**2))
                U3 = abs(Ut * Ci)
                Cs3 = -massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)
    
            #Ketidakpastian densitas udara(U4)
                Uh = u95[4]/nilai_k[4]
                Up = u95[3]/nilai_k[3]
                Ut = u95[2]/nilai_k[2]
                Ch = (0.020582 - 0.00252*suhu_udara) / ((237.15 + suhu_udara) * 1000)
                Cp = (0.464554) / ((237.15 + suhu_udara) * 1000)
                Ct = (-0.6182*kelembaban - 0.46554*tekanan) / (((237.15 + suhu_udara)**2) * 1000)
                U4 = math.sqrt((Uh*Ch)**2 + (Up*Cp)**2 + (Ut*Ct)**2)
                Cs4 = massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)
    
            #Ketidakpastian KMV(U5)
                U5 = (0.1 * koef_muai) / math.sqrt(3)
                Cs5 = massa * (20 - T) / (dens_air - dens_udara)
    
            #Ketidakpastian miniskus(U6)
                U6 = (0.05 * ketelitian_lb) / math.sqrt(3)
                Cs6 = 1
    
            #Ketidakpastian gabungan(Ugab)
                Ugab = math.sqrt((U1*Cs1)**2 + (U2*Cs2)**2 + (U3*Cs3)**2 + (U4*Cs4)**2 + (U5*Cs5)**2 + (U6*Cs6)**2)
            
            #Ketidakpastian Diperluas
                U95_exp = Ugab * 2
    
                st.subheader("Hasil Perhitungan")
                st.write(f"Densitas Air: **{dens_air:.7f} g/mL**")
                st.write(f"Densitas Udara: **{dens_udara:.7f} g/mL**")
                st.write(f"Volume Sebenarnya (20°C): **{v_20:.7f} mL**")
                st.write(f"Koreksi Volume Konvensional: **{koreksi:+.6f} mL**")
    
                st.subheader("Ketidakpastian")
                st.write(f"Ugab (Gabungan): **{Ugab:.6f} mL**")
                st.write(f"Ketidakpastian Diperluas (U95): **{U95_exp:.6f} mL**")
            except Exception as e:
                st.error(f"Terjadi kesalahan saat perhitungan lanjutan: {e}")


