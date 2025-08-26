from datetime import datetime, timedelta

import pytest

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


@pytest.mark.skip(reason="Wird später gezielt reaktiviert; Entry-Trigger der aktuellen Logik unbekannt.")
def test_timemax_be_path(monkeypatch):
    # Umgebung stabilisieren
    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)

    start = datetime(2025, 1, 1, 10, 0)
    b0 = _bar(start, 1.0, 1.0, 1.0, 1.0)
    t_entry = start + timedelta(minutes=1)
    b1 = _bar(t_entry, 1.0, 1.0, 1.0, 1.0)
    t_95 = t_entry + timedelta(minutes=95)
    b2 = _bar(t_95, 1.0005, 1.0005, 1.0005, 1.0005)
    t_96 = t_entry + timedelta(minutes=96)
    b3 = _bar(t_96, 1.0, 1.0002, 0.9998, 1.0)

    _ = app.backtest_variant([b0, b1, b2, b3], "BTCUSDT", profile="SAFE", risk_perc=0.005)
