import os

# Which environment we're running as. Defaults to dev for safety.
APP_ENV = os.environ.get("APP_ENV", "dev")

_CONFIGS = {
    "dev": {
        "db_path": "stocks_dev.db",
        "watchlist": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
        "fetch_interval_minutes": 5,
    },
    "qa": {
        "db_path": "stocks_qa.db",
        "watchlist": ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "SBIN.NS"],
        "fetch_interval_minutes": 5,
    },
    "staging": {
        "db_path": "stocks_staging.db",
        "watchlist": [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
            "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "WIPRO.NS",
        ],
        "fetch_interval_minutes": 10,
    },
    "prod": {
        "db_path": "stocks.db",
        "watchlist": [
            "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
            "SBIN.NS", "BHARTIARTL.NS", "ITC.NS", "LT.NS", "WIPRO.NS",
            "HINDUNILVR.NS", "AXISBANK.NS", "KOTAKBANK.NS", "MARUTI.NS", "TITAN.NS",
        ],
        "fetch_interval_minutes": 15,
    },
}

if APP_ENV not in _CONFIGS:
    raise ValueError(f"Unknown APP_ENV '{APP_ENV}'. Must be one of {list(_CONFIGS)}")

_cfg = _CONFIGS[APP_ENV]

DB_PATH = _cfg["db_path"]
WATCHLIST = _cfg["watchlist"]
FETCH_INTERVAL_MINUTES = _cfg["fetch_interval_minutes"]

# Holdings (P&L) — same across envs for now
HOLDINGS = [
    {"ticker": "RELIANCE.NS", "quantity": 10, "buy_price": 1200.0},
    {"ticker": "TCS.NS",      "quantity": 5,  "buy_price": 2000.0},
    {"ticker": "INFY.NS",     "quantity": 8,  "buy_price": 1050.0},
]
