import app


def test_write_trades_with_risk_fields(tmp_path):
    out = tmp_path / "trades_risk.csv"
    trades = [
        {
            "symbol": "BTCUSDT",
            "variant": "SAFE_010bp",
            "reason": "TEST_RISK",
            "time_entry": 1700000000000,
            "time_exit": 1700000060000,
            "entry": 100.0,
            "exit": 101.2,
            "pnl_pct": 0.012,
            # Risk/Account Felder (Branch use_risk_fields=True)
            "profile_run": "SAFE",
            "risk_perc_run": 0.01,
            "R_multiple": 0.2,
            "account_pnl_pct": 0.12,
            "account_pnl_usd": 12.0,
            "equity_before": 10000.0,
            "equity_after": 10012.0,
            "qty": 1.0,
            "notional_usd": 100.0,
            # Zeit-Exit Felder (falls in Schema vorhanden)
            "time_limit_applied": False,
            "time_limit_minutes": 90,
            "unrealized_pct_at_90m": 0.0,
            "be_armed": False,
        }
    ]

    # echten Pfad schreiben lassen – Branch use_risk_fields=True
    app.write_trades(trades, str(out), use_risk_fields=True)

    text = out.read_text(encoding="utf-8")
    # Header- und Werte-Prüfungen inkl. Risk-Felder
    assert "profile_run" in text and "risk_perc_run" in text
    assert "equity_before" in text and "equity_after" in text
    assert "account_pnl_usd" in text
    assert "SAFE_010bp" in text and "TEST_RISK" in text
