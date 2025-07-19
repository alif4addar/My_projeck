
import streamlit as st
import pandas as pd
import numpy as np
import math
import statistics

st.set_page_config(
    page_title="Aplikasi Kalibrasi Volume",
    page_icon="📖",
    layout="wide", 
    initial_sidebar_state="collapsed"
)


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
        background-color: #F4F8D3;
        border-bottom: 1px solid #eee;
        margin-bottom: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .header-section h1 {
        color: #5F6F65;
        font-weight: 700;
        margin: 0;
    }

    /* Hero Section */
    .hero-section {
        background: linear-gradient(to right, #CAE8BD, #B0DB9C); /* Gradien biru */
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
    
    .hero-section h3 {
        font-size: 28px;
        font-weight: 750;
        margin-bottom: 15px;
        line-height: 1.2;
        color: #5F6F65;
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
        color: #2193b0; 
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

    /* Buttons  */
    .stButton > button {
        background-color: #BAD8B6;
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
        background-color: #E1EACD;
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

    /* Warna untuk kolom input seperti NST, U95, K */
    input[type="number"] {
        background-color: #393E46 !important;
        color: #FDFAF6 !important;
        border: 2px solid #819A91 !important;
        border-radius: 6px;
        padding: 8px;
    }

    /* Warna untuk teks label input */
    label {
        color: #FDFAF6 !important;
    }

    /* Warna header tabel Data Editor */
    .st-emotion-cache-13k62yr {
        background-color: #393E46 !important;
        color: #FDFAF6 !important;
        border: 2px solid #819A91 !important;
    }

    /* Warna sel data editor */
    [data-testid="stDataFrame"] input {
        background-color: #393E46 !important;
        color: #FDFAF6 !important;
        border: 2px solid #819A91 !important;
        border-radius: 6px !important;
        padding: 6px;
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

    /* Paksa latar belakang utama aplikasi jadi putih */
    html, body, [class*="stApp"] {
        background-color: white !important;
        color: black !important;
    }

    /* Paksa latar belakang semua container jadi putih juga */
    .st-emotion-cache-1r6slb0 {
        background-color: white !important;
    }

    /* Warna header dan elemen lain juga bisa disesuaikan */
    .st-emotion-cache-13k62yr {
        background-color: white !important;
        color: black !important;
    }
    
    </style>
""", unsafe_allow_html=True)


# Inisialisasi halaman
if "page" not in st.session_state:
    st.session_state.page = 1

# Fungsi navigasi
def next_page():
    st.session_state.page += 1
    
def next_page_2():
    st.session_state.page += 2

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1
def prev_page_2():
    if st.session_state.page > 1:
        st.session_state.page -= 2


if st.session_state.page == 1:
# --- Header ---
    st.markdown('<div class="header-section"><h1>Aplikasi Kalibrasi Volume Labu Takar</h1></div>', unsafe_allow_html=True)

    col_pp, col_space, col_next = st.columns([3, 6, 2])
    with col_pp:
        if st.button("Petunjuk Penggunaan"): next_page()
            st.stop()
    with col_next:
        if st.button("Mulai"): next_page_2()
  

#====PP===
elif st.session_state.page == 2:
    st.markdown('<div class="header-section"><h1>Cara Penggunaan</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="app-card"><p>pada halaman pertana</p></div>', unsafe_allow_html=True)
    if st.button("Mulai"):
        next_page()


elif st.session_state.page == 3:
    st.markdown("""
        <div class="hero-section">
            <p>Alat komprehensif ini membantu Anda melakukan perhitungan kalibrasi volume labu takar secara akurat, termasuk analisis ketidakpastian sesuai standar metrologi.</p>           
        </div>
    """, unsafe_allow_html=True)

    col_kembali, col_space, col_lanjut = st.columns([2, 6, 2])
    with col_kembali:
        if st.button("Back"): prev_page_2()
            st.stop()
    with col_lanjut:
        if st.button("Next"): next_page()


elif st.session_state.page == 4:
    # Bagian Input VKonvensional
    st.markdown("<h1 style='color:#5F6F65;'>Aplikasi Kalibrasi Volume - Labu Takar</h1>", unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    # Input volume konvensional
    v_konven = st.number_input("Masukkan Volume Konvensional (mL)", min_value=0.0, step=25.0,  format="%.2f")

    ketelitian_lb = st.number_input("Masukkan Ketelitian Labu Takar (mL)", min_value=0.0, step=0.001, format="%.4f")

    # Template input tabel
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color:#5F6F65;'>Input Data Pengukuran</h3>", unsafe_allow_html=True)
    cols = [
        "Bobot Kosong (g)",
        "Bobot Isi (g)",
        "Suhu Air (C)",
        "Suhu Udara (C)",
        "Tekanan Udara (mmHg)",
        "Kelembaban (%)"
    ]
    
    # jmlh baris
    if "rows" not in st.session_state:
        st.session_state.rows = 1
    
    def add_row():
        st.session_state.rows += 1
    
    def remove_row():
        if st.session_state.rows > 1:
            st.session_state.rows -= 1
    
    col1, col2, col3 = st.columns([3, 6, 3])
    with col1:
        st.button(" + Tambah Baris", on_click=add_row)
    with col3:
        st.button(" - Hapus Baris", on_click=remove_row)
    
    
    def_data = [["" for _ in range(len(cols))] for _ in range(st.session_state.rows)]
    df = st.data_editor(pd.DataFrame(def_data, columns=cols), use_container_width=True, num_rows="dynamic")
    
    if st.button("Hitung Rata-rata Data Pengukuran"):
        try:
            if df.isnull().values.any() or (df == "").values.any():
                st.warning("⚠️ Semua sel harus diisi sebelum menghitung rata-rata.")
            else:
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
                    "SEM Bobot Isi (g)": statistics.stdev(hasil) / math.sqrt(len(hasil))
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

    col_kembali, col_space, col_lanjut = st.columns([2, 6, 2])
    with col_lanjut:
        if st.button("Next"): next_page()
            st.stop()
    with col_kembali:
        if st.button("Back"): prev_page()
            

elif st.session_state.page == 5:
    st.markdown('<div class="header-section"><h1>Terimakasih</h1></div>', unsafe_allow_html=True)    

    
    
