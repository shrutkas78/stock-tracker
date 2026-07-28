import streamlit as st
import pandas as pd
from db import engine
from portfolio import compute_watchlist, compute_portfolio
from config import HOLDINGS, WATCHLIST

st.set_page_config(page_title="Stock Tracker", layout="wide")
st.title("Stock Tracker")

# --- Combined watchlist + portfolio table ---
st.header("Watchlist & Portfolio")

rows = compute_watchlist(WATCHLIST, HOLDINGS)

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

# --- Price history charts (whole watchlist) ---
st.header("Price History")

df = pd.read_sql("SELECT * FROM prices", engine)
if df.empty:
    st.info("No price history yet. Run `python backfill.py` to load it.")
else:
    df["ts"] = pd.to_datetime(df["ts"]).dt.date
    for ticker in WATCHLIST:
        sub = df[df["ticker"] == ticker]
        if sub.empty:
            continue
        series = sub.groupby("ts")["price"].mean()
        st.caption(ticker)
        st.line_chart(series)
