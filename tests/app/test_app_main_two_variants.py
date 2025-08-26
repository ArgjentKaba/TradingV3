from datetime import datetime, timedelta
from pathlib import Path

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=1.0)


def test_main_two_variants_combined(monkeypatch, tmp_path):
    # 1) Zwei Varianten aktivieren
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005), ("FAST", 0.010)])

    # 2) Universe & Output setzen
    symfile = tmp_path / "symbols.txt"
    symfile.write_text("BTCUSDT\n", encoding="utf-8")
    outdir = tmp_path / "runs"
    monkeypatch.setattr(
        app,
        "CFG_RUN",
        {
            "universe_file": str(symfile),
            "output": {"dir": str(outdir), "save_combined": True},
        },
    )

    # 3) Bars vorhanden
    t0 = datetime(2025, 1, 1, 0, 0)
    bars = [_bar(t0, 1, 1, 1, 1), _bar(t0 + timedelta(minutes=1), 1, 1, 1, 1)]
    monkeypatch.setattr(app, "load_bars_for_symbol", lambda *a, **k: bars)

    # 4) backtest_variant liefert je Variante genau einen Trade
    def fake_backtest_variant(_bars, symbol, profile, risk_perc, **_kw):
        return [
            {"symbol": symbol, "variant": f"{profile}_{int(risk_perc * 1000):03d}bp", "pnl": 0.001, "reason": "TEST"}
        ]

    monkeypatch.setattr(app, "backtest_variant", fake_backtest_variant)

    # 5) write_trades abfangen
    calls = []

    def fake_write(trades, path, use_risk_fields=True):
        calls.append((len(trades), Path(path).name))

    monkeypatch.setattr(app, "write_trades", fake_write)

    # 6) Run
    app.main()

    # 7) Asserts: beide Varianten + Combined enthalten
    names = [n for _, n in calls]
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in names), names
    assert any(n.startswith("trades_FAST_") and n.endswith("bp.csv") for n in names), names
    assert "trades_all_variants.csv" in names, names

    # Combined sollte die Summe aller Trades enthalten (=2)
    combined_sizes = [cnt for cnt, n in calls if n == "trades_all_variants.csv"]
    assert combined_sizes and combined_sizes[0] == 2, combined_sizes
