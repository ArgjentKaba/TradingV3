import app


def test_write_trades_merges_heterogeneous_columns(tmp_path):
    out = tmp_path / "trades_hetero.csv"
    trades = [
        {
            "symbol": "BTCUSDT",
            "variant": "SAFE_005bp",
            "reason": "LEG1",
            "time_entry": 1700000000000,
            "time_exit": 1700000060000,
            "entry": 100.0,
            "exit": 108.0,
            "pnl_pct": 0.08,
            # keine Risk-Felder hier
        },
        {
            "symbol": "BTCUSDT",
            "variant": "SAFE_005bp",
            "reason": "LEG2",
            "time_entry": 1700000060000,
            "time_exit": 1700000120000,
            "entry": 108.0,
            "exit": 100.0,
            "pnl_pct": -0.074,
            # zusätzliche Felder, die im ersten Trade fehlen
            "profile_run": "SAFE",
            "risk_perc_run": 0.005,
            "account_pnl_usd": -7.4,
            "equity_before": 10000.0,
            "equity_after": 9992.6,
            "custom_extra": "X",
        },
    ]

    app.write_trades(trades, str(out), use_risk_fields=True)

    text = out.read_text(encoding="utf-8")
    # Header enthält Union aller Keys (inkl. custom_extra & risk-Felder)
    assert "custom_extra" in text
    assert "profile_run" in text and "risk_perc_run" in text
    # Daten beider Legs vorhanden
    assert "LEG1" in text and "LEG2" in text
