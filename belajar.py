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
