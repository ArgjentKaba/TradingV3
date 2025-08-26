from pathlib import Path

import app


def test_main_no_data(monkeypatch, tmp_path, capsys):
    # Variants klein halten (nur 1 Lauf)
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005)])
    # Symbols-Datei im tmp erzeugen
    symfile = tmp_path / "symbols.txt"
    symfile.write_text("BTCUSDT\n", encoding="utf-8")

    # CFG_RUN überschreiben: eigenes symbols-file + output-dir im tmp + save_combined=True
    monkeypatch.setattr(
        app,
        "CFG_RUN",
        {
            "universe_file": str(symfile),
            "output": {"dir": str(tmp_path / "runs"), "save_combined": True},
        },
    )

    # Keine Daten für alle Symbole
    monkeypatch.setattr(app, "load_bars_for_symbol", lambda *a, **k: [])

    # write_trades Calls mitzählen statt echte Dateien zu schreiben
    calls = []

    def fake_write_trades(trades, path, use_risk_fields=True):
        calls.append((len(trades), Path(path).name))

    monkeypatch.setattr(app, "write_trades", fake_write_trades)

    # Run
    app.main()
    # Ausgabe prüfen (Warnung pro Symbol)
    out = capsys.readouterr().out
    assert "Keine Daten für BTCUSDT gefunden" in out

    # Es sollte mindestens 2 write_trades-Aufrufe geben:
    # - trades_SAFE_005bp.csv (variant)
    # - trades_all_variants.csv (combined)
    names = [n for _, n in calls]
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in names)
    assert "trades_all_variants.csv" in names
