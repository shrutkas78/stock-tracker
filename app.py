import streamlit as st
import pandas as pd
from db import engine, get_latest_price
from portfolio import compute_watchlist, compute_portfolio
from config import HOLDINGS, WATCHLIST

st.set_page_config(page_title="Stock Tracker", layout="wide")
st.title("Stock Tracker")

# --- Combined watchlist + portfolio table ---
st.header("Watchlist & Portfolio")

rows = compute_watchlist(WATCHLIST, HOLDINGS, price_fn=get_latest_price)

table = pd.DataFrame([
    {
        "Ticker": r["ticker"],
        "Owned": "✓" if r["owned"] else "",
        "Qty": r["quantity"],
        "Buy Price": r["buy_price"],
        "Current Price": round(r["current_price"], 2),
        "Value": round(r["current_value"], 2) if r["current_value"] is not None else None,
        "Gain": round(r["gain"], 2) if r["gain"] is not None else None,
        "Gain %": round(r["gain_pct"], 2) if r["gain_pct"] is not None else None,
    }
    for r in rows
])
st.dataframe(table, use_container_width=True, hide_index=True)

# --- Totals (owned holdings only) ---
summary = compute_portfolio(HOLDINGS)
col1, col2, col3 = st.columns(3)
col1.metric("Total Cost", f"₹{summary['total_cost']:,.2f}")
col2.metric("Total Value", f"₹{summary['total_value']:,.2f}")
col3.metric(
    "Total Gain",
    f"₹{summary['total_gain']:,.2f}",
    delta=f"{(summary['total_gain'] / summary['total_cost'] * 100):.2f}%",
)

# --- Price history: pick one ticker to chart ---
st.header("Price History")

df = pd.read_sql("SELECT * FROM prices", engine)
if df.empty:
    st.info("No price history yet. Run `python backfill.py` to load it.")
else:
    df["ts"] = pd.to_datetime(df["ts"]).dt.date
    available = [t for t in WATCHLIST if t in df["ticker"].unique()]
    if available:
        choice = st.selectbox("Select a stock", available)
        series = df[df["ticker"] == choice].groupby("ts")["price"].mean()
        st.line_chart(series)
    else:
        st.info("No history for the current watchlist yet.")
