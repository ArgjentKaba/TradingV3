import app


def test_load_bars_skips_malformed_rows(tmp_path):
    csv = tmp_path / "BTCUSDT_1m.csv"
    # t,open,high,low,close,volume  (t in ms)
    # 2 gültige Zeilen + 1 kaputte Zeile (non-numeric) -> soll übersprungen werden
    csv.write_text(
        "t,open,high,low,close,volume\n"
        "1700000000000,1.0,1.1,0.9,1.05,10\n"
        "1700000060000,foo,bar,baz,qux,spam\n"  # malformed -> skip
        "1700000120000,1.1,1.2,1.0,1.15,11\n",
        encoding="utf-8",
    )

    bars = app.load_bars_for_symbol(tmp_path, "BTCUSDT")
    # Erwartung: nur die 2 gültigen Zeilen
    assert len(bars) == 2
    assert abs(bars[0].close - 1.05) < 1e-9
    assert abs(bars[1].close - 1.15) < 1e-9
