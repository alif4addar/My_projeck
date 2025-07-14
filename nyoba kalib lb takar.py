import streamlit as st


if st.button("Tambah Data"):
  st.write("Why hello there")

left, right = st.columns(2)
if left.button("Menambah Data", use_container_width=True):
    left.markdown(".")
if right.button("Selanjutnya", icon=":material/mood:", use_container_width=True):
    right.markdown("You clicked the Material button.")

