import streamlit as st
import pandas as pd
import numpy as np
import math
import statistics

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Aplikasi Kalibrasi Volume",
    page_icon="🧪",
    layout="wide", # Menggunakan layout wide agar ada lebih banyak ruang
    initial_sidebar_state="collapsed"
)

# --- CSS Kustom (untuk meniru gaya TBHX.net) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
        color: #333; /* Warna teks umum */
    }

    .stApp {
        background-color: #f8f8f8; /* Latar belakang aplikasi */
        padding: 20px; /* Padding keseluruhan */
    }

    /* Header */
    .header-section {
        padding: 20px 0;
        text-align: center;
        background-color: #ffffff;
        border-bottom: 1px solid #eee;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .header-section h1 {
        color: #2193b0; /* Warna biru khas */
        font-weight: 700;
        margin: 0;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(to right, #6dd5ed, #2193b0); /* Gradien biru */
        color: white;
        padding: 60px 30px;
        text-align: center;
        border-radius: 10px;
        margin-bottom: 40px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .hero-section h2 {
        font-size: 2.8em;
        font-weight: 700;
        margin-bottom: 15px;
        line-height: 1.2;
        color: white; /* Pastikan judul di hero putih */
    }
    .hero-section p {
        font-size: 1.1em;
        margin-bottom: 20px;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }

    /* General Card/Container Style */
    .app-card {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 30px;
    }
    .app-card h3, .app-card h4 {
        color: #2193b0; /* Warna biru untuk subheader */
        font-weight: 600;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .stNumberInput label, .stTextInput label, .stTextArea label {
        font-weight: 600;
        color: #555;
        margin-bottom: 5px;
        display: block;
    }
    .stNumberInput input, .stTextInput input, .stTextArea textarea {
        border-radius: 5px;
        border: 1px solid #ddd;
        padding: 8px 12px;
        width: 100%;
        box-sizing: border-box;
    }
    .stNumberInput input:focus, .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #2193b0;
        box-shadow: 0 0 0 0.1rem rgba(33, 147, 176, 0.25);
        outline: none;
    }

    /* Buttons */
    .stButton > button {
        background-color: #2193b0;
        color: white;
        border: none;
        padding: 10px 25px;
        border-radius: 5px;
        font-size: 1.0em;
        cursor: pointer;
        transition: background-color 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background-color: #1a7a90; /* Warna biru lebih gelap saat hover */
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    /* Style for the "Add Row" and "Remove Row" buttons */
    .stButton > button[data-testid="stFormSubmitButton"] { /* Target specific buttons if needed */
        background-color: #28a745; /* Green for add */
    }
    .stButton > button[data-testid="stFormSubmitButton"]:hover {
        background-color: #218838;
    }
    .stButton > button[data-testid="stFormSubmitButton"] + div .stButton > button { /* Target remove button */
        background-color: #dc3545; /* Red for remove */
    }
    .stButton > button[data-testid="stFormSubmitButton"] + div .stButton > button:hover {
        background-color: #c82333;
    }


    /* Data Editor */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden; /* Ensures rounded corners apply */
        border: 1px solid #ddd;
    }
    .stDataFrame .data-grid {
        border-radius: 8px;
    }
    /* Specific styling for table headers */
    .stDataFrame .data-grid-header {
        background-color: #f0f0f0;
        color: #333;
        font-weight: 600;
    }

    /* Info/Warning/Error messages */
    .stAlert {
        border-radius: 8px;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .stAlert.info {
        background-color: #e0f7fa;
        color: #00796b;
        border-left: 5px solid #00bcd4;
    }
    .stAlert.warning {
        background-color: #fff3e0;
        color: #e65100;
        border-left: 5px solid #ff9800;
    }
    .stAlert.error {
        background-color: #ffebee;
        color: #c62828;
        border-left: 5px solid #ef5350;
    }

    /* Divider */
    .stDivider {
        margin: 40px 0;
        border-top: 1px solid #eee;
    }

    /* Footer */
    .footer-section {
        text-align: center;
        padding: 30px 0;
        margin-top: 50px;
        border-top: 1px solid #eee;
        color: #777;
        font-size: 0.9em;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-section"><h1>Aplikasi Kalibrasi Volume Labu Takar</h1></div>', unsafe_allow_html=True)

# --- Hero Section (Deskripsi Aplikasi) ---
st.markdown("""
    <div class="hero-section">
        <h2>Hitung Volume Sebenarnya dan Ketidakpastian Labu Takar Anda</h2>
        <p>Alat komprehensif ini membantu Anda melakukan perhitungan kalibrasi volume labu takar secara akurat, termasuk analisis ketidakpastian sesuai standar metrologi.</p>
    </div>
""", unsafe_allow_html=True)

# --- Bagian Input Volume Konvensional ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.subheader("1. Input Volume Konvensional")
v_konven = st.number_input("Masukkan Volume Konvensional (mL)", min_value=0.0, step=0.1, key="v_konven_input")
st.markdown('</div>', unsafe_allow_html=True)


# --- Bagian Input Data Pengukuran ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.subheader("2. Input Data Pengukuran")
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

col_add_row, col_remove_row = st.columns(2)
with col_add_row:
    st.button("+ Tambah Baris", on_click=add_row, use_container_width=True)
with col_remove_row:
    st.button("- Hapus Baris", on_click=remove_row, use_container_width=True)

def_data = [["" for _ in range(len(cols))] for _ in range(st.session_state.rows)]
df = st.data_editor(pd.DataFrame(def_data, columns=cols), use_container_width=True, num_rows="dynamic")

if st.button("Hitung Rata-rata Data Pengukuran", key="hitung_rata_rata_btn"):
    try:
        # Memastikan semua sel diisi sebelum perhitungan
        # Check if any cell is empty or contains non-numeric data
        if df.isnull().values.any() or (df == "").values.any():
            st.warning("⚠️ Semua sel harus diisi sebelum menghitung rata-rata.")
        else:
            # Convert all columns to numeric, handling potential errors
            try:
                df_numeric = df.astype(float)
            except ValueError:
                st.error("Pastikan semua input data pengukuran adalah angka yang valid.")
                st.stop() # Stop execution if conversion fails

            kosong = df_numeric["Bobot Kosong (g)"].tolist()
            isi = df_numeric["Bobot Isi (g)"].tolist()
            suhu_air = df_numeric["Suhu Air (C)"].tolist()
            suhu_udara = df_numeric["Suhu Udara (C)"].tolist()
            tekanan = df_numeric["Tekanan Udara (mmHg)"].tolist()
            kelembaban = df_numeric["Kelembaban (%)"].tolist()

            # Menghitung bobot isi (hasil)
            hasil = [b - a for a, b in zip(kosong, isi)]

            # Menghitung rata-rata untuk setiap kolom dan SEM untuk bobot isi
            rata = {
                "Bobot Kosong (g)": sum(kosong)/len(kosong),
                "Bobot Isi (g)": sum(isi)/len(isi),
                "Bobot Isi (Hasil) (g)": sum(hasil)/len(hasil),
                "Suhu Air (C)": sum(suhu_air)/len(suhu_air),
                "Suhu Udara (C)": sum(suhu_udara)/len(suhu_udara),
                "Tekanan Udara (mmHg)": sum(tekanan)/len(tekanan),
                "Kelembaban (%)": sum(kelembaban)/len(kelembaban),
                "SEM Bobot Isi (g)": statistics.stdev(hasil) / math.sqrt(len(hasil)) if len(hasil) > 1 else 0.0 # Handle case with single data point
            }

            # Menyimpan rata-rata ke session_state agar bisa diakses di tombol lain
            st.session_state.rata_pengukuran = rata

            st.subheader("Rata-rata Data Pengukuran")
            st.markdown('<div class="app-card">', unsafe_allow_html=True) # Nested card for results
            for k, v in rata.items():
                st.write(f"**{k}:** `{v:.4f}`")
            st.markdown('</div>', unsafe_allow_html=True)

    except ValueError:
        st.error("Pastikan semua input data pengukuran adalah angka yang valid.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat menghitung rata-rata: {e}")
st.markdown('</div>', unsafe_allow_html=True) # Close app-card for data input


# --- Bagian Input Alat Ukur ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.subheader("3. Input Alat Ukur")
lop = st.number_input("Masukkan Nilai LOP Timbangan", value=0.0, format="%.4f", key="lop_input") # Format untuk presisi
st.markdown("Masukkan nilai NST, U95, dan K untuk alat ukur:")

CC = ["Timbangan","Termometer Air","Termometer Udara","Barometer Udara","Hygrometer"]

# Menggunakan kolom untuk input NST, U95, dan K agar lebih rapi
col_nst, col_u95, col_k = st.columns(3)
nst = []
u95 = []
nilai_k = []

with col_nst:
    
    for i, label in enumerate(CC):
        nst.append(st.number_input(f"NST {label}", value=0.0, key=f"nst_{i}", format="%.4f"))
with col_u95:
    st.markdown("#### U95")
    for i, label in enumerate(CC):
        u95.append(st.number_input(f"U95 {label}", value=0.0, key=f"u95_{i}", format="%.4f"))
with col_k:
    st.markdown("#### K")
    for i, label in enumerate(CC):
        nilai_k.append(st.number_input(f"K {label}", value=1.0, key=f"kval_{i}", format="%.4f"))
st.markdown('</div>', unsafe_allow_html=True) # Close app-card for instrument input


# --- Bagian Perhitungan Volume & Ketidakpastian ---
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.subheader("4. Perhitungan Volume & Ketidakpastian")

# Tombol khusus menghitung ketidakpastian
if "rata_pengukuran" in st.session_state:
    rata = st.session_state.rata_pengukuran

    if st.button("Hitung Volume & Ketidakpastian", key="hitung_volume_ketidakpastian_btn"):
        try:
            # Mengambil nilai dari rata-rata pengukuran
            T = rata["Suhu Air (C)"]
            massa = rata["Bobot Isi (Hasil) (g)"]
            suhu_udara = rata["Suhu Udara (C)"]
            tekanan = rata["Tekanan Udara (mmHg)"]
            kelembaban = rata["Kelembaban (%)"]

            # Perhitungan Densitas Air (berdasarkan formula tertentu)
            # Formula densitas air yang lebih akurat (dari literatur metrologi)
            # Ini adalah pendekatan, formula eksak bisa sangat kompleks
            dens_air = 0.999974 - (((T - 3.989)**2) * (T + 338.636)) / (563385.4 * (T + 72.45147))

            # Perhitungan Densitas Udara (berdasarkan formula tertentu)
            # Formula densitas udara (misal dari CIPM 1981/91)
            # Ini adalah pendekatan, formula eksak bisa sangat kompleks
            dens_udara = ((0.464554 * tekanan) - kelembaban*(0.00252*suhu_udara-0.020582)) / ((237.15+suhu_udara)*1000)

            # Koefisien muai termal gelas (contoh nilai umum)
            koef_muai = 1e-5 # Koefisien muai termal gelas (per °C)

            # Volume sebenarnya pada 20°C (V20)
            # Rumus kalibrasi volume labu takar
            v_20 = massa * (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)
            koreksi = v_20 - v_konven

            # --- Perhitungan Ketidakpastian ---

            # Ketidakpastian massa air (U1)
            # k_neraca: ketidakpastian dari timbangan (distribusi persegi)
            k_neraca = (lop / (2 * math.sqrt(3)))
            # k_ulangan: ketidakpastian dari pengulangan pengukuran (SEM)
            k_ulangan = rata["SEM Bobot Isi (g)"]
            U1 = math.sqrt(k_neraca**2 + k_ulangan**2)
            # Koefisien sensitivitas Cs1 = dV/dm
            Cs1 = (1 - koef_muai * (T - 20)) / (dens_air - dens_udara)

            # Ketidakpastian suhu air (U2)
            # U2: ketidakpastian standar dari termometer air (U95/k)
            U2 = u95[1] / nilai_k[1] if nilai_k[1] != 0 else 0 # Hindari pembagian nol
            # Koefisien sensitivitas Cs2 = dV/dT
            Cs2 = massa * (-koef_muai) / (dens_air - dens_udara)

            # Ketidakpastian densitas air (U3)
            # Ut: ketidakpastian suhu air yang mempengaruhi densitas air
            Ut_dens_air = U2 # Menggunakan U2 karena suhu air adalah input untuk densitas air
            # Ci: turunan densitas air terhadap suhu
            # Ini adalah turunan parsial dari dens_air terhadap T
            # (5.32e-6 * T**2 + 1.20e-4*T + 2.82e-5) / ((T + 72.45147)**2) adalah penyederhanaan turunan
            # Sebaiknya hitung turunan numerik atau gunakan formula turunan yang tepat
            # Untuk tujuan demonstrasi, kita gunakan pendekatan ini:
            Ci = -((5.32e-6 * T**2 + 1.20e-4*T + 2.82e-5) / ((T + 72.45147)**2))
            U3 = abs(Ut_dens_air * Ci)
            # Koefisien sensitivitas Cs3 = dV/d(dens_air)
            Cs3 = -massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)

            # Ketidakpastian densitas udara (U4)
            # Uh: ketidakpastian higrometer
            Uh = u95[4] / nilai_k[4] if nilai_k[4] != 0 else 0
            # Up: ketidakpastian barometer
            Up = u95[3] / nilai_k[3] if nilai_k[3] != 0 else 0
            # Ut_udara: ketidakpastian termometer udara
            Ut_udara = u95[2] / nilai_k[2] if nilai_k[2] != 0 else 0

            # Koefisien sensitivitas untuk densitas udara
            # Ch = d(dens_udara)/d(kelembaban)
            Ch = (0.020582 - 0.00252*suhu_udara) / ((237.15 + suhu_udara) * 1000)
            # Cp = d(dens_udara)/d(tekanan)
            Cp = (0.464554) / ((237.15 + suhu_udara) * 1000)
            # Ct = d(dens_udara)/d(suhu_udara)
            Ct = (-0.6182*kelembaban - 0.46554*tekanan) / (((237.15 + suhu_udara)**2) * 1000)
            U4 = math.sqrt((Uh*Ch)**2 + (Up*Cp)**2 + (Ut_udara*Ct)**2)
            # Koefisien sensitivitas Cs4 = dV/d(dens_udara)
            Cs4 = massa * (1 - koef_muai*(T - 20)) / ((dens_air - dens_udara)**2)

            # Ketidakpastian Koefisien Muai Volume (U5)
            # U5: ketidakpastian koefisien muai (distribusi persegi, misal 10% dari nilai)
            U5 = (0.1 * koef_muai) / math.sqrt(3)
            # Koefisien sensitivitas Cs5 = dV/d(koef_muai)
            Cs5 = massa * (20 - T) / (dens_air - dens_udara)

            # Ketidakpastian Miniskus (U6)
            # U6: ketidakpastian dari pembacaan miniskus (distribusi persegi, misal 0.05 * NST)
            U6 = (0.05 * nst[0]) / math.sqrt(3)
            # Koefisien sensitivitas Cs6 = dV/d(miniskus)
            Cs6 = 1 # Asumsi miniskus langsung menambah/mengurangi volume

            # Ketidakpastian Gabungan (Ugab)
            # Menggabungkan semua komponen ketidakpastian
            Ugab = math.sqrt(
                (U1*Cs1)**2 +
                (U2*Cs2)**2 +
                (U3*Cs3)**2 +
                (U4*Cs4)**2 +
                (U5*Cs5)**2 +
                (U6*Cs6)**2
            )

            # Ketidakpastian Diperluas (U95)
            # Faktor cakupan k=2 untuk tingkat kepercayaan 95%
            U95_exp = Ugab * 2

            st.subheader("Hasil Perhitungan")
            st.markdown('<div class="app-card">', unsafe_allow_html=True) # Nested card for results
            st.write(f"**Densitas Air:** `{dens_air:.7f} g/mL`")
            st.write(f"**Densitas Udara:** `{dens_udara:.7f} g/mL`")
            st.write(f"**Volume Sebenarnya (20°C):** `{v_20:.7f} mL`")
            st.write(f"**Koreksi Volume Konvensional:** `{koreksi:+.6f} mL`")
            st.markdown('</div>', unsafe_allow_html=True)

            st.subheader("Ketidakpastian")
            st.markdown('<div class="app-card">', unsafe_allow_html=True) # Nested card for uncertainty results
            st.write(f"**Ketidakpastian Standar Gabungan (Ugab):** `{Ugab:.6f} mL`")
            st.write(f"**Ketidakpastian Diperluas (U95, k=2):** `{U95_exp:.6f} mL`")
            st.markdown('</div>', unsafe_allow_html=True)

        except ZeroDivisionError:
            st.error("Terjadi pembagian dengan nol. Pastikan nilai 'K' tidak nol untuk alat ukur yang relevan dan densitas air tidak sama dengan densitas udara.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat perhitungan lanjutan: {e}")
else:
    st.info("Silakan masukkan data pengukuran dan klik 'Hitung Rata-rata Data Pengukuran' terlebih dahulu.")

st.markdown('</div>', unsafe_allow_html=True) # Close app-card for calculation section

# --- Footer ---
st.markdown('<div class="footer-section">© 2023 Aplikasi Kalibrasi Volume. Semua Hak Dilindungi.</div>', unsafe_allow_html=True)
