import streamlit as st
import pandas as pd
from db import engine

st.title("Stock Tracker")
df = pd.read_sql("SELECT * FROM prices", engine)

for ticker in df["ticker"].unique():
    st.subheader(ticker)
    sub = df[df.ticker == ticker].set_index("ts")["price"]
    st.line_chart(sub)
