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
