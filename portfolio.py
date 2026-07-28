from fetch import get_price


def compute_pnl(ticker, quantity, buy_price):
    current_price = get_price(ticker)
    cost_basis = quantity * buy_price
    current_value = quantity * current_price
    gain = current_value - cost_basis
    gain_pct = (gain / cost_basis) * 100 if cost_basis else 0.0
    return {
        "ticker": ticker,
        "quantity": quantity,
        "buy_price": buy_price,
        "current_price": current_price,
        "cost_basis": cost_basis,
        "current_value": current_value,
        "gain": gain,
        "gain_pct": gain_pct,
    }


def compute_portfolio(holdings):
    results = [
        compute_pnl(h["ticker"], h["quantity"], h["buy_price"])
        for h in holdings
    ]
    total_cost = sum(r["cost_basis"] for r in results)
    total_value = sum(r["current_value"] for r in results)
    return {
        "holdings": results,
        "total_cost": total_cost,
        "total_value": total_value,
        "total_gain": total_value - total_cost,
    }


def compute_watchlist(watchlist, holdings):
    """One row per watchlist stock. P&L filled in only for owned stocks."""
    owned = {h["ticker"]: h for h in holdings}
    rows = []
    for ticker in watchlist:
        current_price = get_price(ticker)
        if ticker in owned:
            h = owned[ticker]
            cost_basis = h["quantity"] * h["buy_price"]
            current_value = h["quantity"] * current_price
            gain = current_value - cost_basis
            rows.append({
                "ticker": ticker,
                "owned": True,
                "quantity": h["quantity"],
                "buy_price": h["buy_price"],
                "current_price": current_price,
                "current_value": current_value,
                "gain": gain,
                "gain_pct": (gain / cost_basis * 100) if cost_basis else 0.0,
            })
        else:
            rows.append({
                "ticker": ticker,
                "owned": False,
                "quantity": None,
                "buy_price": None,
                "current_price": current_price,
                "current_value": None,
                "gain": None,
                "gain_pct": None,
            })
    return rows
