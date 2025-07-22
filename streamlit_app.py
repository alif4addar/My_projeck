import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Web Identifikasi Custom",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# CSS Styling agar mirip web asli
st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }



    body {{
        background: url('https://raw.githubusercontent.com/Raixhaa/blank-app/main/dreamina-2025-07-15-91470000000000.png') no-repeat center center fixed;
        background-size: cover;
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: rgba(255,255,255,{LIGHT_BG_ALPHA});
        padding: 2rem 2rem 5rem 2rem;
        border-radius: 24px;
        max-width: {MAX_WIDTH_PX}px;
        margin: auto;
        box-shadow: 0 4px 40px rgba(0,0,0,0.15);
    }}

    .appview-container .main .block-container {
        max-width: 900px;
        padding: 2rem 1rem;
        margin: auto;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    button[kind="primary"] {
        background-color: #3a86ff;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }

    button[kind="primary"]:hover {
        background-color: #265dc3;
        color: #fff;
    }

    h1, h2 {
        color: #0a3d62;
    }

    [data-testid="stSidebar"] > div:first-child {
        background-color: #e9f0ff;
        padding: 1rem;
        border-right: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Navigasi")
st.sidebar.markdown("Pilih halaman atau fitur lain dari sini.")

# Konten utama
st.title("🔬 Web Identifikasi Custom")
st.markdown("""
Selamat datang di aplikasi identifikasi berbasis web!  
Silakan ubah bagian ini sesuai kebutuhan Anda (bisa untuk pendidikan, analisis senyawa, deteksi sifat fisik, dan lainnya).
""")

# Contoh input awal
col1, col2 = st.columns(2)
with col1:
    opsi1 = st.selectbox("Pilih Opsi 1:", ["-", "Pilihan A", "Pilihan B", "Pilihan C"])
with col2:
    opsi2 = st.selectbox("Pilih Opsi 2:", ["-", "Ya", "Tidak"])

# Tombol proses
if st.button("Proses Identifikasi"):
    if opsi1 == "Pilihan A" and opsi2 == "Ya":
        st.success("✅ Hasil: Golongan X terdeteksi")
    elif opsi1 == "Pilihan B":
        st.info("ℹ️ Hasil: Kemungkinan besar Golongan Y")
    else:
        st.warning("⚠️ Data tidak cukup untuk menentukan hasil")

# Footer
st.markdown("---")
st.caption("© 2025 - Web identifikasi ini bersifat editable untuk keperluan pendidikan dan pengembangan.")
