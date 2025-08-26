import importlib.util
from pathlib import Path

# app.py als Modul laden (unabhängig von sys.path)
APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
spec = importlib.util.spec_from_file_location("app", APP_PATH)
app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app)


def test_main_runs_with_mocks(monkeypatch, tmp_path):
    # Dummy-Daten
    dummy_symbols = ["BTCUSDT", "ETHUSDT"]
    dummy_trades = [{"symbol": "BTCUSDT"}, {"symbol": "ETHUSDT"}]

    # Mocks
    monkeypatch.setattr(app, "load_symbols", lambda path: dummy_symbols)
    monkeypatch.setattr(app, "load_bars_for_symbol", lambda data_path, sym: ["BAR"])
    monkeypatch.setattr(app, "backtest_variant", lambda bars, sym, profile, risk_perc: dummy_trades)
    written = {}

    def fake_write_trades(trades, path, use_risk_fields=True):
        written[path] = list(trades)

    monkeypatch.setattr(app, "write_trades", fake_write_trades)

    # Mock CFG_RUN und VARIANTS
    monkeypatch.setattr(app, "CFG_RUN", {"universe_file": "ignore", "output": {"dir": str(tmp_path)}})
    monkeypatch.setattr(app, "VARIANTS", [("SAFE", 0.005)])

    app.main()

    # Prüfen, ob Dateien „geschrieben“ wurden
    assert any("trades_SAFE" in p for p in written)
    assert any("trades_all_variants" in p for p in written)
    assert all(isinstance(v, list) for v in written.values())
