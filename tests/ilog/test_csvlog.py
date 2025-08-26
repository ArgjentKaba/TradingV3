from pathlib import Path

from ilog.csvlog import ORDERED_FIELDS, _normalize_row, csvlog, write_trades


def test_normalize_row_adds_missing_fields():
    row = {"symbol": "BTCUSDT", "profile": "SAFE", "risk_perc": "0.5"}
    norm = _normalize_row(row)
    assert norm["symbol"] == "BTCUSDT"
    assert norm["profile_run"] == "SAFE"
    assert norm["risk_perc_run"] == "0.5"
    for f in ORDERED_FIELDS:
        assert f in norm


def test_write_trades_creates_csv(tmp_path: Path):
    trades = [
        {
            "symbol": "BTCUSDT",
            "side": "LONG",
            "entry": "100",
            "exit": "110",
            "profile": "SAFE",
            "risk_perc": "0.5",
        }
    ]
    file = tmp_path / "out.csv"
    write_trades(trades, str(file))
    text = file.read_text(encoding="utf-8")
    assert "symbol" in text and "BTCUSDT" in text


def test_write_trades_with_empty_list(tmp_path: Path):
    file = tmp_path / "empty.csv"
    write_trades([], str(file))
    lines = file.read_text(encoding="utf-8").splitlines()
    assert lines[0].startswith("time_entry")
    assert len(lines) == 1


def test_write_trades_empty(tmp_path: Path):
    path = tmp_path / "empty.csv"
    csvlog.write_trades([], str(path))
    assert path.exists()
    content = path.read_text(encoding="utf-8")
    # Datei enthält nur Headerzeile
    assert "time_entry" in content and "\n" in content


def test_write_trades_with_extra_field(tmp_path: Path):
    path = tmp_path / "extra.csv"
    trades = [
        {
            "time_entry": "t1",
            "time_exit": "t2",
            "symbol": "BTC",
            "side": "LONG",
            "entry": "100",
            "exit": "110",
            "reason": "tp1",
            "custom_field": "extra_value",
        }
    ]
    csvlog.write_trades(trades, str(path))
    text = path.read_text(encoding="utf-8")
    # custom_field muss als Spalte enthalten sein
    assert "custom_field" in text
    assert "extra_value" in text
