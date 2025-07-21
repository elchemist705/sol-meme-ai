import os
import json
import random
import time
from datetime import datetime

# ----- File Setup -----
DEFAULT_MEMORY_FILE = "trade_memory.json"
FALLBACK_MEMORY_FILE = os.path.expanduser("~/degen_memory_backup.json")

# ----- Load & Save Memory -----
def load_memory(path=DEFAULT_MEMORY_FILE):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except Exception as e:
        print(f"⚠️ Error loading memory: {e}")
    return []

def save_memory(portfolio, path=DEFAULT_MEMORY_FILE):
    try:
        with open(path, "w") as f:
            json.dump(portfolio, f, indent=2)
        print(f"📁 Memory saved to {path}")
    except PermissionError:
        print(f"❌ Can't write to {path}. Falling back to: {FALLBACK_MEMORY_FILE}")
        try:
            with open(FALLBACK_MEMORY_FILE, "w") as f:
                json.dump(portfolio, f, indent=2)
            print(f"📁 Memory saved to fallback: {FALLBACK_MEMORY_FILE}")
        except Exception as e:
            print(f"🚫 Fallback save failed: {e}")

# ----- Scoring Functions -----
def rate_name(name):
    keywords = ['pepe', 'doge', 'moon', '420', 'elon', 'pump']
    return sum(word in name.lower() for word in keywords) * 10

def scale_volume(volume): return min(volume / 1000, 10)
def calculate_growth(wallets): return min(wallets / 100, 10)
def time_decay(age): return 10 if age < 60 else 5 if age < 120 else 2

def analyze_feature_correlation(trades):
    if len(trades) == 0:
        return {'name': 0.3, 'volume': 0.25, 'growth': 0.25, 'age': 0.2}

    name_scores, volume_scores, growth_scores, age_scores, profits = [], [], [], [], []

    for trade in trades:
        coin = {
            'name': trade['coin'],
            'volume': random.randint(100, 2000),
            'wallets': random.randint(20, 500),
            'age': random.randint(5, 180)
        }
        name_scores.append(rate_name(coin['name']))
        volume_scores.append(scale_volume(coin['volume']))
        growth_scores.append(calculate_growth(coin['wallets']))
        age_scores.append(time_decay(coin['age']))
        profits.append(trade['profit'])

    def correlate(values, profits):
        avg_x = sum(values) / len(values)
        avg_y = sum(profits) / len(profits)
        covariance = sum((x - avg_x) * (y - avg_y) for x, y in zip(values, profits))
        return max(covariance / len(values), 0.01)  # Prevent zero-weight

    weights = {
        'name': correlate(name_scores, profits),
        'volume': correlate(volume_scores, profits),
        'growth': correlate(growth_scores, profits),
        'age': correlate(age_scores, profits),
    }

    # Normalize to 1
    total = sum(weights.values())
    for key in weights:
        weights[key] = round(weights[key] / total, 3)

    print(f"\n🧠 Adaptive Weights Used: {weights}\n")
    return weights

# ----- Meme Scoring Engine -----
def meme_score(coin, weights):
    return (
        rate_name(coin['name']) * weights['name'] +
        scale_volume(coin['volume']) * weights['volume'] +
        calculate_growth(coin['wallets']) * weights['growth'] +
        time_decay(coin['age']) * weights['age']
    )

# ----- Coin Generator -----
def fetch_meme_coins():
    return [{
        'name': random.choice(['Pepe420Moon', 'ElonStonks', 'ZoomDoge', 'asdfcoin']),
        'volume': random.randint(100, 2000),
        'wallets': random.randint(20, 500),
        'age': random.randint(5, 180)
    } for _ in range(10)]

# ----- Trade Simulation -----
def simulate_trade(coin, score):
    buy_price = round(random.uniform(0.005, 0.02), 4)
    multiplier = random.uniform(0.6, 3.0) if score >= 7.5 else random.uniform(0.7, 1.1)
    sell_price = round(buy_price * multiplier, 4)
    profit = round(sell_price - buy_price, 4)
    now = time.time()
    readable_time = datetime.fromtimestamp(now).strftime("%Y-%m-%d %H:%M:%S")

    return {
        'coin': coin['name'],
        'score': round(score, 2),
        'buy_price': buy_price,
        'sell_price': sell_price,
        'profit': profit,
        'timestamp': now,
        'datetime': readable_time
    }

# ----- Bot Core -----
def run_bot(memory):
    weights = analyze_feature_correlation(memory)
    new_trades = []
    coins = fetch_meme_coins()

    for coin in coins:
        score = meme_score(coin, weights)
        print(f"🔍 {coin['name']} | Score: {score:.1f}")
        if score >= 7.5:
            trade = simulate_trade(coin, score)
            result = "🚀 GAIN" if trade['profit'] > 0 else "📉 LOSS"
            print(f"🧾 Trade: Bought @ {trade['buy_price']} → Sold @ {trade['sell_price']} | PnL: {trade['profit']} ({result})\n")
            new_trades.append(trade)
        else:
            print("❌ Skipped.\n")
    return memory + new_trades

# ----- Execute -----
if __name__ == "__main__":
    print("\n🤖 DegenGPT v4 — Adaptive Scoring Mode Activated\n")
    memory = load_memory()
    updated_memory = run_bot(memory)
    save_memory(updated_memory)
    print(f"\n📈 Trades saved: {len(updated_memory)} total\n")