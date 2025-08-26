import csv
import importlib.util
import sys
from datetime import datetime
from pathlib import Path

# KORRIGIERT: zwei Ebenen hoch zum Repo-Root → app.py
spec = importlib.util.spec_from_file_location("app", str(Path(__file__).resolve().parents[2] / "app.py"))
app = importlib.util.module_from_spec(spec)
sys.modules["app"] = app
spec.loader.exec_module(app)


def test_load_bars_for_symbol_reads_and_dedup(tmp_path):
    fn = tmp_path / "BTCUSDT_1m.csv"
    fieldnames = ["time", "open", "high", "low", "close", "volume"]
    rows = [
        {
            "time": str(int(datetime(2025, 1, 1, 10, 0).timestamp() * 1000)),
            "open": "1",
            "high": "2",
            "low": "0.5",
            "close": "1.5",
            "volume": "100",
        },
        {
            "time": str(int(datetime(2025, 1, 1, 10, 1).timestamp() * 1000)),
            "open": "2",
            "high": "3",
            "low": "1.0",
            "close": "2.5",
            "volume": "200",
        },
    ]
    with fn.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    bars = app.load_bars_for_symbol(str(tmp_path), "BTCUSDT")
    assert len(bars) == 2
    assert bars[0].open == 1.0
    assert bars[1].close == 2.5
    assert app.load_bars_for_symbol(str(tmp_path), "XXX") == []


def test_load_oi_map_reads_and_handles(tmp_path):
    oi_dir = tmp_path / "oi"
    oi_dir.mkdir()
    fn = oi_dir / "BTCUSDT_oi_1m.csv"
    fieldnames = ["time", "open_interest"]
    rows = [
        {"time": str(int(datetime(2025, 1, 1, 10, 0).timestamp() * 1000)), "open_interest": "1000"},
        {"time": str(int(datetime(2025, 1, 1, 10, 5).timestamp() * 1000)), "open_interest": "1100"},
    ]
    with fn.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    oi_map = app.load_oi_map(str(tmp_path), "BTCUSDT")
    assert any(isinstance(v, float) for v in oi_map.values())
    assert app.load_oi_map(str(tmp_path), "XXX") == {}
