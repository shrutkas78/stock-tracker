from fetch import get_history
from db import init_db, save_price
from config import WATCHLIST

init_db()

for ticker in WATCHLIST:
    try:
        rows = get_history(ticker, period="6mo")
        for r in rows:
            save_price(r["ticker"], r["price"], r["ts"])
        print(f"{ticker}: saved {len(rows)} rows")
    except Exception as e:
        print(f"{ticker}: failed - {e}")

print("Backfill complete.")
