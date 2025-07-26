import streamlit as st

# Konfigurasi halaman
st.set_page_config(
    page_title="Web Identifikasi Custom",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)
PRIMARY = "#1e355e"        # biru tua edukatif
SECONDARY = "#f39c12"      # oranye aksen
SUCCESS = "#27ae60"        # hijau sukses
WARNING = "#e67e22"        # oranye peringatan
DANGER = "#c0392b"         # merah error
INFO = "#2980b9"           # biru info
LIGHT_BG_ALPHA = 0.90       # transparansi konten utama
MAX_WIDTH_PX = 900      

# CSS Styling agar mirip web asli
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    body {{
        background: url('https://github.com/alif4addar/My_projeck/blob/main/bg%20streamlit%20no%20wm.png') no-repeat center center fixed;
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

    h1, h2, h3, h4 {{
        color: {PRIMARY};
        font-family: 'Inter', sans-serif;
        font-weight: 700;
    }}

    .edu-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.25rem;
        color: white;
        background: {SECONDARY};
    }}

    .result-card {{
        background: white;
        border-left: 8px solid {SUCCESS};
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}

    .warning-card {{
        background: white;
        border-left: 8px solid {WARNING};
        padding: 1.25rem 1.5rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}

    .decision-path {{
        font-family: monospace;
        font-size: 0.85rem;
        background: rgba(0,0,0,0.05);
        padding: 0.5rem 0.75rem;
        border-radius: 6px;
        line-height: 1.3;
    }}

    /* ===== Sidebar ===== */
    section[data-testid="stSidebar"] > div:first-child {{
        background: rgba(255,255,255,0.95);
        backdrop-filter: blur(6px);
        padding-top: 1rem;
    }}

    /* Button pill group container */
    .nav-pill-container {{
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
        margin-bottom: 1.5rem;
    }}
    .nav-pill {{
        width: 100%;
        padding: 0.6rem 1rem;
        border-radius: 999px;
        border: 2px solid {PRIMARY}20;
        background: white;
        color: {PRIMARY};
        font-weight: 600;
        text-align: left;
        cursor: pointer;
        transition: all 0.15s ease-in-out;
    }}
    .nav-pill:hover {{
        border-color: {PRIMARY};
        transform: translateX(2px) scale(1.01);
    }}
    .nav-pill.active {{
        background: {PRIMARY};
        color: #fff;
        border-color: {PRIMARY};
        box-shadow: 0 0 0 2px {PRIMARY}40 inset;
    }}

    .nav-pill .emoji {{
        margin-right: 0.35rem;
    }}

    /* Theory cards */
    .theory-card {{
        background:#ffffff;
        border:1px solid #dfe4ea;
        border-radius:16px;
        padding:1.25rem 1.5rem;
        margin-bottom:1.25rem;
        box-shadow:0 1px 4px rgba(0,0,0,0.08);
    }}
    .theory-card h3 {{margin-top:0;}}
    .theory-grid {{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin-top:1rem;}}
    .theory-tag {{display:inline-block;padding:2px 8px;font-size:0.75rem;border-radius:4px;background:{PRIMARY}15;color:{PRIMARY};margin-right:4px;margin-bottom:4px;}}
    .safety-tag {{background:{DANGER}25;color:{DANGER};}}
    .tip-tag {{background:{SECONDARY}25;color:{SECONDARY};}}
    </style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("🔍 Navigasi")
st.sidebar.markdown("Pilih halaman atau fitur lain dari sini.")

# Konten utama
st.title("📐 Web Perhitungan Ketidakpastian Kalibrasi Alat")
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
