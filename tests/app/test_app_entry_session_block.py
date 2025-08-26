from datetime import datetime, timedelta

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=100.0)


class DummyGov:
    def __init__(self, *a, **k):
        pass

    def can_trade(self, *a, **k):
        return True

    def register_trade(self, *a, **k):
        pass

    def register_exit(self, *a, **k):
        pass


class DummyRS:
    def __init__(self, *a, **k):
        pass

    def update(self, *a, **k):
        pass

    def vol_zscore(self):
        return 0.0

    def atr14_pct(self):
        return 0.0

    def ffill_step(self):
        return


def test_no_trade_outside_session(monkeypatch):
    # Umgebung fixieren
    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: False)  # Session blockiert
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)

    t0 = datetime(2025, 1, 1, 9, 0)
    bars = [
        _bar(t0, 1, 1, 1, 1),
        _bar(t0 + timedelta(minutes=1), 1, 1, 1, 1),
    ]
    trades = app.backtest_variant(bars, "BTCUSDT", profile="SAFE", risk_perc=0.005)
    assert trades == []
