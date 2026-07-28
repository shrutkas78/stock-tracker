import pandas as pd
from sqlalchemy import create_engine, text
import db


def test_init_and_save(monkeypatch):
    # Swap the module's engine for an isolated in-memory DB
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(db, "engine", test_engine)

    db.init_db()
    db.save_price("TEST.NS", 123.45, "2026-01-01T10:00:00")

    result = pd.read_sql("SELECT * FROM prices", test_engine)

    assert len(result) == 1
    assert result.iloc[0]["ticker"] == "TEST.NS"
    assert result.iloc[0]["price"] == 123.45


def test_multiple_saves(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(db, "engine", test_engine)

    db.init_db()
    db.save_price("A.NS", 10.0, "t1")
    db.save_price("B.NS", 20.0, "t2")

    result = pd.read_sql("SELECT * FROM prices", test_engine)
    assert len(result) == 2
    assert set(result["ticker"]) == {"A.NS", "B.NS"}


def test_get_latest_price(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(db, "engine", test_engine)

    db.init_db()
    db.save_price("TEST.NS", 100.0, "2026-01-01T10:00:00")
    db.save_price("TEST.NS", 110.0, "2026-01-02T10:00:00")  # newer
    db.save_price("OTHER.NS", 50.0, "2026-01-02T10:00:00")

    # Should return the most recent price for that ticker
    assert db.get_latest_price("TEST.NS") == 110.0
    assert db.get_latest_price("OTHER.NS") == 50.0


def test_get_latest_price_missing(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(db, "engine", test_engine)

    db.init_db()
    # No rows for this ticker -> returns None
    assert db.get_latest_price("NOPE.NS") is None
