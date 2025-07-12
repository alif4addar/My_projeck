import streamlit as st

st.write("Hello, *World!* :🖕🖕:")


st.title("This is a title")
st.title("_Streamlit_ is :red[cool] :sunglasses:")

st.header("_Streamlit_ is :blue[cool] :sunglasses:", divider="gray")

st.subheader("_Streamlit_ is :blue[cool] :sunglasses:", divider="green")

st.markdown("*Streamlit* is **really** ***cool***.")

st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)

st.button("Reset", type="primary")
if st.button("Say hello"):
    st.write("Why hello there")

if st.button("Aloha", type="tertiary"):
    st.write("Ciao")

col1, col2, col3 = st.columns(3)

with col1:
    st.header("A cat")
    st.image("https://static.streamlit.io/examples/cat.jpg")

with col2:
    st.header("A dog")
    st.image("https://static.streamlit.io/examples/dog.jpg")

with col3:
    st.header("An owl")
    st.image("https://static.streamlit.io/examples/owl.jpg")

import time

with st.sidebar:
    with st.echo():
        st.write("This code will be printed to the sidebar.")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")
st.success('This is a success message!', icon="✅")
if not st.user.is_logged_in:
    if st.button("Log in"):
        st.login()
else:
    if st.button("Log out"):
        st.logout()
    st.write(f"Hello, {st.user.name}!")


