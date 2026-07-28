import yfinance as yf

def get_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    return data["Close"].iloc[-1]

def get_history(ticker, period="6mo"):
    """Return a list of {ticker, price, ts} dicts for past daily closes."""
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    rows = []
    for ts, row in data.iterrows():
        rows.append({
            "ticker": ticker,
            "price": float(row["Close"]),
            "ts": ts.isoformat(),
        })
    return rows

if __name__ == "__main__":
    print(get_price("RELIANCE.NS"))
