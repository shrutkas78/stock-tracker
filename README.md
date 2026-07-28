# stock-tracker

A small tool I built to track stock prices over time. It grabs the latest price
for a list of tickers, saves each reading to a local database, and shows the
history in a simple dashboard. Mostly a way to get a full little system working
end to end — data in, stored, scheduled, displayed, and tested.

Right now the watchlist is a few NSE stocks (Reliance, TCS, Infosys), but you
can point it at anything Yahoo Finance covers.

## What it uses

- yfinance for the price data
- SQLite (via SQLAlchemy) to store readings
- APScheduler to re-fetch on an interval
- Streamlit for the dashboard
- pytest for the tests, GitHub Actions to run them on every push

## Running it

```bash
git clone https://github.com/shrutkas78/stock-tracker.git
cd stock-tracker

python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

To start fetching (runs once, then every 5 minutes):

```bash
python tracker.py
```

To see the dashboard:

```bash
streamlit run app.py
```

It'll print a local URL, usually http://localhost:8501.

The list of tickers lives at the top of `tracker.py`. NSE symbols need `.NS`
on the end, BSE ones need `.BO`.

## How it's laid out
fetch.py - gets the latest price for one ticker
db.py - database setup and save/read helpers
tracker.py - runs fetch + save for the whole watchlist, on a schedule
app.py - the Streamlit dashboard
tests/ - the test suite
## Notes on the tests

The tests don't hit the network or the real database. `test_fetch.py` fakes out
yfinance so it returns a known price instead of calling Yahoo — otherwise the
tests would break whenever the market's closed or the connection's flaky.
`test_db.py` uses an in-memory SQLite database so each test starts clean and
never touches the real `stocks.db`.

```bash
pytest -v
```

One thing worth knowing: prices only change during NSE trading hours, so if you
run it overnight the numbers stay flat. That's expected, not a bug — took me a
minute to figure out.
