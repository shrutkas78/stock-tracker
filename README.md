# Stock Tracker

A lightweight stock price tracking system that fetches live market data, stores
it, and visualises price history through a dashboard. Built as a from-scratch
Python project with a full automated test suite and CI.

## Features

- **Live data** — pulls latest prices from Yahoo Finance via `yfinance`
- **Persistence** — stores every reading in a local SQLite database
- **Scheduling** — fetches on a configurable interval with APScheduler
- **Dashboard** — visualises price history per ticker with Streamlit
- **Tested** — unit tests with mocked network calls and an isolated in-memory DB
- **CI** — GitHub Actions runs the test suite on every push

## Tech stack

| Layer         | Tool                     |
|---------------|--------------------------|
| Data source   | yfinance (Yahoo Finance) |
| Storage       | SQLite + SQLAlchemy      |
| Scheduling    | APScheduler              |
| Dashboard     | Streamlit                |
| Testing       | pytest, pytest-mock      |
| CI            | GitHub Actions           |

## Getting started

```bash
# Clone and enter the project
git clone https://github.com/shrutkas78/stock-tracker.git
cd stock-tracker

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Fetch prices once and store them, then run on a 5-minute schedule:

```bash
python tracker.py
```

Launch the dashboard:

```bash
streamlit run app.py
```

Then open the local URL it prints (default http://localhost:8501).

The watchlist is defined in `tracker.py`. NSE tickers use the `.NS` suffix
(e.g. `RELIANCE.NS`), BSE tickers use `.BO`.

## Project structure
stock-tracker/
├── fetch.py # Retrieves the latest price for a ticker
├── db.py # SQLite schema + save/read helpers
├── tracker.py # Ties fetch + store together, on a schedule
├── app.py # Streamlit dashboard
├── requirements.txt
├── tests/
│ ├── test_fetch.py # Tests fetch logic with yfinance mocked
│ └── test_db.py # Tests storage with an in-memory database
└── .github/workflows/
└── tests.yml # CI: runs pytest on every push
## Testing strategy

The test suite is designed to be **fast, deterministic, and independent of
external state** — the same properties that matter for reliable automation in a
real pipeline:

- **Network is mocked.** `test_fetch.py` replaces `yfinance.Ticker` with a fake
  that returns a known DataFrame. Tests never call Yahoo Finance, so they don't
  depend on network availability or on markets being open, and they run in
  milliseconds.
- **The database is isolated.** `test_db.py` swaps the module's engine for an
  in-memory SQLite instance per test. Each test starts from a clean state and
  leaves no artifacts — the real `stocks.db` is never touched.
- **CI enforces it.** GitHub Actions installs dependencies and runs the full
  suite on every push, so regressions surface immediately.

Run the tests locally:

```bash
pytest -v
```
