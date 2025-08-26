import importlib.util
import sys
from datetime import datetime, timedelta
from pathlib import Path

spec = importlib.util.spec_from_file_location("app", str(Path(__file__).resolve().parents[2] / "app.py"))
app = importlib.util.module_from_spec(spec)
sys.modules["app"] = app
spec.loader.exec_module(app)


def test_backtest_variant_entry_and_sl(monkeypatch):
    # CFG_RUN ohne days_back
    monkeypatch.setattr(app, "CFG_RUN", {})

    Bar = app.Bar
    t0 = datetime(2025, 1, 1, 10, 0)
    t1 = t0 + timedelta(minutes=1)
    t2 = t1 + timedelta(minutes=1)

    bars = [
        Bar(t=t0, open=1.0, high=1.0, low=1.0, close=1.0, volume=100.0),
        Bar(t=t1, open=1.0, high=1.2, low=1.0, close=1.2, volume=110.0),
        Bar(t=t2, open=1.0, high=1.05, low=0.5, close=0.5, volume=120.0),
    ]

    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *a, **k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *a, **k: True)

    class DummyGov:
        def __init__(self, *a, **k):
            pass

        def can_trade(self, *a, **k):
            return True

        def register_trade(self, *a, **k):
            pass

        def register_exit(self, *a, **k):
            pass

    monkeypatch.setattr(app, "Governor", DummyGov)

    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})

    class RS:
        def __init__(self, vol_window=20):
            pass

        def update(self, *a, **k):
            pass

        def vol_zscore(self):
            return 0.0

        def atr14_pct(self):
            return 0.0

        def ffill_step(self):
            pass

    monkeypatch.setattr(app, "RollingStats", RS)

    trades = app.backtest_variant(bars, "BTCUSDT", profile="SAFE", risk_perc=0.005)
    assert len(trades) == 1
    assert "SL" in trades[0]["reason"]
