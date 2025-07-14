import streamlit as st


st.button("Reset")
if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")
