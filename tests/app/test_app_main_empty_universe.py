from pathlib import Path

import app


def test_main_with_empty_universe_file(monkeypatch, tmp_path):
    # Universe-Datei: nur Kommentare/Leerzeilen
    symfile = tmp_path / "symbols.txt"
    symfile.write_text("# kommentiert\n\n   \n# noch ein kommentar\n", encoding="utf-8")

    outdir = tmp_path / "runs"
    monkeypatch.setattr(
        app,
        "CFG_RUN",
        {
            "universe_file": str(symfile),
            "output": {"dir": str(outdir), "save_combined": True},
        },
    )
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005)])

    calls = []

    def fake_write(trades, path, use_risk_fields=True):
        calls.append((len(trades), Path(path).name))

    monkeypatch.setattr(app, "write_trades", fake_write)

    try:
        app.main()
    except SystemExit:
        pass

    # Deine Implementierung: trotz leerem Universe → 2 Dateien, beide mit 0 Zeilen
    assert len(calls) == 2, calls
    names = [n for _, n in calls]
    assert any(n.startswith("trades_SAFE_") and n.endswith("bp.csv") for n in names), names
    assert "trades_all_variants.csv" in names, names
    for cnt, _ in calls:
        assert cnt == 0
