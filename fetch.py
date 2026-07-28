import yfinance as yf

def get_price(ticker):
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    return data["Close"].iloc[-1]

if __name__ == "__main__":
    print(get_price("RELIANCE.NS"))
