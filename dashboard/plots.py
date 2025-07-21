import matplotlib.pyplot as plt

def plot_cumulative_profit(df):
    df["cumulative_profit"] = df["profit"].cumsum()
    fig, ax = plt.subplots()
    ax.plot(df["datetime"], df["cumulative_profit"], marker="o")
    ax.set_ylabel("Cumulative SOL")
    ax.set_xlabel("Time")
    return fig

def plot_trade_distribution(df):
    gain_count = (df["profit"] > 0).sum()
    loss_count = (df["profit"] <= 0).sum()
    fig, ax = plt.subplots()
    ax.bar(["Gain", "Loss"], [gain_count, loss_count], color=["green", "red"])
    ax.set_title("Trade Outcome Distribution")
    return fig