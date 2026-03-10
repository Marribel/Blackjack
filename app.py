import streamlit as st
import numpy as np
import pandas as pd

st.title("Hello from WSL 🎉")
st.markdown("Hello!")	
st.write("Streamlit is working!")

with st.sidebar:
 st.header("User Info")
name = st.text_input("Name")
age = st.slider("Age", 0, 100, 25)

st.divider()

with st.sidebar:
	with st.expander("Chart Settings"):
		points = st.slider("Number of points", 10, 200, 50)
		show_b = st.checkbox("Show Line B")

st.divider()
st.header("Theme")
theme = st.radio("Choose a Theme", ["Light", "Dark"])

with st.sidebar:
	st.header("Output")

	st.write("Name:", name)
	st.write("Age: ", age)
	st.write("Theme: ", theme)

df = pd.DataFrame({
"A": np.random.randn(points).cumsum(),
"B": np.random.randn(points).cumsum()
})

if show_b:
	st.line_chart(df)
else:
	st.line_chart(df["A"])
