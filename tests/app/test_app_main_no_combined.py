from datetime import datetime, timedelta
from pathlib import Path

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=1.0)


def test_main_no_combined_when_disabled(monkeypatch, tmp_path):
    # Eine Variante reicht
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005)])

    # Universe + Output (save_combined=False)
    symfile = tmp_path / "symbols.txt"
    symfile.write_text("BTCUSDT\n", encoding="utf-8")
    outdir = tmp_path / "runs"
    monkeypatch.setattr(
        app,
        "CFG_RUN",
        {
            "universe_file": str(symfile),
            "output": {"dir": str(outdir), "save_combined": False},
        },
    )

    # Bars vorhanden
    t0 = datetime(2025, 1, 1, 0, 0)
    bars = [_bar(t0, 1, 1, 1, 1), _bar(t0 + timedelta(minutes=1), 1, 1, 1, 1)]
    monkeypatch.setattr(app, "load_bars_for_symbol", lambda *a, **k: bars)

    # backtest_variant liefert 1 Trade
    monkeypatch.setattr(
        app,
        "backtest_variant",
        lambda *_a, **_k: [{"symbol": "BTCUSDT", "variant": "SAFE_005bp", "pnl": 0.001, "reason": "TEST"}],
    )

    # write_trades spy
    calls = []
    real_write = app.write_trades

    def spy_write(trades, path, use_risk_fields=True):
        calls.append(Path(path).name)
        return real_write(trades, path, use_risk_fields=use_risk_fields)

    monkeypatch.setattr(app, "write_trades", spy_write)

    # run
    app.main()

    # Erwartung: nur Varianten-Datei, KEINE combined
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in calls), calls
    assert "trades_all_variants.csv" not in calls, calls
