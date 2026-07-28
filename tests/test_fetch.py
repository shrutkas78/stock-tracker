import pandas as pd
from unittest.mock import MagicMock
import fetch


def test_get_price_returns_latest_close(mocker):
    # Fake history dataframe with a known close price
    fake_df = pd.DataFrame({"Close": [100.0, 105.0, 110.0]})

    # Build a fake Ticker whose .history() returns our fake df
    fake_ticker = MagicMock()
    fake_ticker.history.return_value = fake_df

    # Replace yf.Ticker so no real network call happens
    mocker.patch.object(fetch.yf, "Ticker", return_value=fake_ticker)

    result = fetch.get_price("FAKE.NS")

    assert result == 110.0                      # last Close
    fetch.yf.Ticker.assert_called_once_with("FAKE.NS")
    fake_ticker.history.assert_called_once_with(period="1d")


def test_get_price_uses_last_row(mocker):
    fake_df = pd.DataFrame({"Close": [42.0]})
    fake_ticker = MagicMock()
    fake_ticker.history.return_value = fake_df
    mocker.patch.object(fetch.yf, "Ticker", return_value=fake_ticker)

    assert fetch.get_price("SINGLE.NS") == 42.0
