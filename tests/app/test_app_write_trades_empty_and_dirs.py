import app


def test_write_trades_creates_dirs_and_handles_empty(tmp_path):
    # tiefer, noch-nicht-existierender Pfad
    outdir = tmp_path / "deep" / "nested" / "dir"
    outfile = outdir / "trades_empty.csv"

    # keine Trades, aber Risk-Header erwarten
    app.write_trades([], str(outfile), use_risk_fields=True)

    # Ordner wurde erstellt und Datei existiert
    assert outfile.exists()

    text = outfile.read_text(encoding="utf-8")
    # Header enthält Risk-Felder (auch wenn keine Zeilen)
    assert "profile_run" in text and "risk_perc_run" in text and "equity_before" in text
    # keine Datenzeilen außer Header
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) == 1, f"Erwarte nur Header, bekam: {lines}"
