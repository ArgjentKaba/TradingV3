from datetime import datetime, timedelta
from pathlib import Path

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=1.0)


def test_main_variant_only_when_no_combined(monkeypatch, tmp_path):
    # 1) Umgebung: eine Variante, save_combined=False
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005)])
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

    # 2) Bars vorhanden
    t0 = datetime(2025, 1, 1, 0, 0)
    bars = [_bar(t0, 1, 1, 1, 1), _bar(t0 + timedelta(minutes=1), 1, 1, 1, 1)]
    monkeypatch.setattr(app, "load_bars_for_symbol", lambda *a, **k: bars)

    # 3) backtest liefert Dummy-Trade
    dummy_trade = {"symbol": "BTCUSDT", "variant": "SAFE_005bp", "pnl": 0.001, "reason": "TEST"}
    monkeypatch.setattr(app, "backtest_variant", lambda *a, **k: [dummy_trade])

    # 4) write_trades abfangen
    calls = []

    def fake_write(trades, path, use_risk_fields=True):
        calls.append((len(trades), Path(path).name, use_risk_fields))

    monkeypatch.setattr(app, "write_trades", fake_write)

    # 5) Run
    app.main()

    # 6) Prüfen: Variantendatei JA, Combined NEIN
    names = [n for _, n, _ in calls]
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in names), names
    assert "trades_all_variants.csv" not in names, names
