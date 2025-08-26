import app


def test_load_bars_ms_string_and_duplicates(tmp_path):
    # Mini-CSV mit ms-Timestamps als STRING, inkl. Duplikat (letzter gewinnt)
    csv = tmp_path / "BTCUSDT_1m.csv"
    # t=open=high=low=close=volume  (t in ms, als String)
    # Zwei Zeilen mit gleichem t; die zweite (letzte) soll gewinnen
    csv.write_text(
        "t,open,high,low,close,volume\n"
        "1700000000000,1.0,1.0,1.0,1.0,10\n"
        "1700000060000,1.0,1.1,0.9,1.05,11\n"
        "1700000060000,2.0,2.2,1.8,2.1,22\n",  # Duplikat-Zeitstempel, letzter gewinnt
        encoding="utf-8",
    )

    # Aufrufen
    bars = app.load_bars_for_symbol(tmp_path, "BTCUSDT")

    # Erwartung: 2 eindeutige Kerzen (00:00:00 und 00:01:00), und bei der duplizierten gewinnt die letzte
    assert len(bars) == 2
    # erste Kerze (1.0 close)
    assert abs(bars[0].close - 1.0) < 1e-9
    # zweite Kerze sollte aus der letzten Duplikat-Zeile stammen (close=2.1, volume=22)
    assert abs(bars[1].close - 2.1) < 1e-9
    assert abs(bars[1].volume - 22.0) < 1e-9
