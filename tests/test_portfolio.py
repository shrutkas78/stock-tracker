import portfolio


def test_compute_pnl_gain(mocker):
    # Pretend the current price is 1280
    mocker.patch("portfolio.get_price", return_value=1280.0)

    result = portfolio.compute_pnl("RELIANCE.NS", quantity=10, buy_price=1200.0)

    assert result["cost_basis"] == 12000.0
    assert result["current_value"] == 12800.0
    assert result["gain"] == 800.0
    assert round(result["gain_pct"], 2) == 6.67


def test_compute_pnl_loss(mocker):
    mocker.patch("portfolio.get_price", return_value=1100.0)

    result = portfolio.compute_pnl("RELIANCE.NS", quantity=10, buy_price=1200.0)

    assert result["gain"] == -1000.0
    assert round(result["gain_pct"], 2) == -8.33


def test_compute_portfolio_totals(mocker):
    # Two holdings, fixed prices
    mocker.patch("portfolio.get_price", side_effect=[1280.0, 2300.0])

    holdings = [
        {"ticker": "RELIANCE.NS", "quantity": 10, "buy_price": 1200.0},
        {"ticker": "TCS.NS", "quantity": 5, "buy_price": 2000.0},
    ]
    summary = portfolio.compute_portfolio(holdings)

    # Reliance: cost 12000, value 12800 -> +800
    # TCS:      cost 10000, value 11500 -> +1500
    assert summary["total_cost"] == 22000.0
    assert summary["total_value"] == 24300.0
    assert summary["total_gain"] == 2300.0


def test_compute_pnl_includes_inputs(mocker):
    mocker.patch("portfolio.get_price", return_value=1280.0)
    result = portfolio.compute_pnl("RELIANCE.NS", quantity=10, buy_price=1200.0)
    assert result["quantity"] == 10
    assert result["buy_price"] == 1200.0


def test_compute_watchlist_merges_holdings(mocker):
    # Prices for RELIANCE, TCS, HDFCBANK in that order
    mocker.patch("portfolio.get_price", side_effect=[1280.0, 2300.0, 1500.0])

    watchlist = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    holdings = [
        {"ticker": "RELIANCE.NS", "quantity": 10, "buy_price": 1200.0},
        {"ticker": "TCS.NS",      "quantity": 5,  "buy_price": 2000.0},
    ]

    rows = portfolio.compute_watchlist(watchlist, holdings)

    assert len(rows) == 3

    # Owned stock: full P&L
    reliance = next(r for r in rows if r["ticker"] == "RELIANCE.NS")
    assert reliance["owned"] is True
    assert reliance["quantity"] == 10
    assert reliance["gain"] == 800.0

    # Not owned: price present, P&L fields are None
    hdfc = next(r for r in rows if r["ticker"] == "HDFCBANK.NS")
    assert hdfc["owned"] is False
    assert hdfc["current_price"] == 1500.0
    assert hdfc["quantity"] is None
    assert hdfc["gain"] is None


def test_compute_watchlist_custom_price_source():
    # Pass an explicit price function instead of hitting the network
    prices = {"RELIANCE.NS": 1280.0, "TCS.NS": 2300.0}
    price_fn = lambda t: prices[t]

    watchlist = ["RELIANCE.NS", "TCS.NS"]
    holdings = [{"ticker": "RELIANCE.NS", "quantity": 10, "buy_price": 1200.0}]

    rows = portfolio.compute_watchlist(watchlist, holdings, price_fn=price_fn)

    reliance = next(r for r in rows if r["ticker"] == "RELIANCE.NS")
    assert reliance["current_price"] == 1280.0
    assert reliance["gain"] == 800.0
