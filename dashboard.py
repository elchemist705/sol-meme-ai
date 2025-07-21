import streamlit as st
import json
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

MEMORY_FILE = "trade_memory.json"
fallback = os.path.expanduser("~/degen_memory_backup.json")

# ---- Load Trades ----
def load_trades():
    if os.path.exists(MEMORY_FILE):
        file = MEMORY_FILE
    elif os.path.exists(fallback):
        file = fallback
    else:
        return pd.DataFrame()
    with open(file, "r") as f:
        data = json.load(f)
    return pd.DataFrame(data)

# ---- Dashboard UI ----
st.set_page_config(page_title="DegenGPT Dashboard", layout="wide")
st.title("🧠 DegenGPT Trade Dashboard")

df = load_trades()

if df.empty:
    st.warning("No trades found in memory.")
else:
    st.subheader("📋 Trade History")
    st.dataframe(df.sort_values("timestamp", ascending=False))

    st.subheader("📈 Profit Over Time")
    df["datetime"] = pd.to_datetime(df["datetime"])
    df["cumulative_profit"] = df["profit"].cumsum()

    fig, ax = plt.subplots()
    ax.plot(df["datetime"], df["cumulative_profit"], marker="o")
    ax.set_ylabel("Cumulative SOL")
    ax.set_xlabel("Time")
    st.pyplot(fig)

    st.subheader("🔥 Top Trades")
    top = df.sort_values("profit", ascending=False).head(5)
    st.table(top[["coin", "buy_price", "sell_price", "profit", "datetime"]])
