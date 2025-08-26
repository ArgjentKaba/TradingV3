from datetime import datetime, timedelta
from pathlib import Path

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=1.0)


def test_main_mixed_universe_some_missing(monkeypatch, tmp_path, capsys):
    # Zwei Varianten, damit wir sicher den Aggregationspfad treffen
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005), ("FAST", 0.010)])

    # Universe: A ohne Daten, B mit Daten
    symfile = tmp_path / "symbols.txt"
    symfile.write_text("NODATA\nBTCUSDT\n", encoding="utf-8")
    outdir = tmp_path / "runs"
    monkeypatch.setattr(
        app,
        "CFG_RUN",
        {
            "universe_file": str(symfile),
            "output": {"dir": str(outdir), "save_combined": True},
        },
    )

    # load_bars: NODATA -> [], BTCUSDT -> 2 Bars
    t0 = datetime(2025, 1, 1, 0, 0)
    bars_ok = [_bar(t0, 1, 1, 1, 1), _bar(t0 + timedelta(minutes=1), 1, 1, 1, 1)]

    def fake_load_bars(path, symbol):
        return [] if symbol == "NODATA" else bars_ok

    monkeypatch.setattr(app, "load_bars_for_symbol", fake_load_bars)

    # backtest: ein Dummy-Trade pro Variante (nur für BTCUSDT)
    def fake_backtest_variant(_bars, symbol, profile, risk_perc, **_kw):
        return [
            {"symbol": symbol, "variant": f"{profile}_{int(risk_perc * 1000):03d}bp", "pnl": 0.001, "reason": "TEST"}
        ]

    monkeypatch.setattr(app, "backtest_variant", fake_backtest_variant)

    # write_trades: echte Funktion sichern, dann Spy setzen
    real_write = app.write_trades
    written = []

    def spy_write(trades, path, use_risk_fields=True):
        written.append((len(trades), Path(path).name))
        return real_write(trades, path, use_risk_fields=use_risk_fields)

    monkeypatch.setattr(app, "write_trades", spy_write)

    # run
    app.main()
    out = capsys.readouterr().out

    # Assertions:
    # 1) Hinweis auf fehlende Daten für NODATA
    assert "Keine Daten" in out or "keine Daten" in out

    # 2) Variantendateien für BTCUSDT (SAFE & FAST) + Combined
    names = [n for _, n in written]
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in names), names
    assert any(n.startswith("trades_FAST_") and n.endswith("bp.csv") for n in names), names
    assert "trades_all_variants.csv" in names, names

    # 3) Combined enthält Summe aller Trades (=2, je 1 pro Variante)
    combined_counts = [cnt for cnt, n in written if n == "trades_all_variants.csv"]
    assert combined_counts and combined_counts[0] == 2, combined_counts
