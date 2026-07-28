from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///stocks.db")

def init_db():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS prices (
                ticker TEXT, price REAL, ts TEXT
            )
        """))

def save_price(ticker, price, ts):
    with engine.begin() as conn:
        conn.execute(
            text("INSERT INTO prices VALUES (:t, :p, :ts)"),
            {"t": ticker, "p": price, "ts": ts}
        )

def get_latest_price(ticker):
    """Return the most recent stored price for a ticker, or None if none exists."""
    with engine.begin() as conn:
        result = conn.execute(
            text("""
                SELECT price FROM prices
                WHERE ticker = :t
                ORDER BY ts DESC
                LIMIT 1
            """),
            {"t": ticker}
        ).fetchone()
    return result[0] if result else None
