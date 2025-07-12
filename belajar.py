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

df = pd.DataFrame(np.random.randn(50, 20), columns=("col %d" % i for i in range(20)))

st.dataframe(df)  # Same as st.write(df)
