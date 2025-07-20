import streamlit as st
import pandas as pd
import math
import statistics

st.set_page_config(page_title="Kalibrasi Volume", layout="wide")

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
