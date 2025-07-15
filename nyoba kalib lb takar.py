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
