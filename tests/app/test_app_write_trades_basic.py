import app


def test_write_trades_basic(tmp_path):
    out = tmp_path / "trades_min.csv"
    trades = [
        {
            "symbol": "BTCUSDT",
            "variant": "SAFE_005bp",
            "pnl": 0.001,
            "reason": "TEST",
            "time_entry": 1700000000000,  # optional Felder mitgeben schadet nicht
            "time_exit": 1700000060000,
        }
    ]

    # echten Pfad schreiben lassen – nicht mocken
    app.write_trades(trades, str(out), use_risk_fields=False)

    # Datei existiert und enthält die erwarteten Spaltennamen/Zeilen
    text = out.read_text(encoding="utf-8")
    assert "symbol" in text and "variant" in text and "reason" in text
    assert "BTCUSDT" in text and "SAFE_005bp" in text and "TEST" in text
