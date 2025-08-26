import app


def test_load_bars_returns_empty_when_csv_missing(tmp_path):
    # Es gibt absichtlich KEINE ABCUSDT_1m.csv im tmp_path
    bars = app.load_bars_for_symbol(tmp_path, "ABCUSDT")
    assert bars == [], "Bei fehlender CSV sollte eine leere Liste zurückkommen."
