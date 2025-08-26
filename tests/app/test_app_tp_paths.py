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


@pytest.mark.skip(reason="Wird später Schritt-für-Schritt aktiviert (Entry/TP-Logik).")
def test_tp1_then_tp2(monkeypatch):
    monkeypatch.setattr(app, "TP1_PCT", 0.0010, raising=False)
    monkeypatch.setattr(app, "TP2_PCT", 0.0020, raising=False)

    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)

    t0 = datetime(2025, 1, 1, 12, 0)
    entry = 1.0000
    b0 = _bar(t0, entry, entry, entry, entry)
    b1 = _bar(t0 + timedelta(minutes=1), entry, entry, entry, entry)
    b2 = _bar(t0 + timedelta(minutes=2), entry * 1.0002, entry * 1.0011, entry * 0.9998, entry * 1.0005)
    b3 = _bar(t0 + timedelta(minutes=3), entry * 1.0021, entry * 1.0022, entry * 1.0015, entry * 1.0020)

    _ = app.backtest_variant([b0, b1, b2, b3], "BTCUSDT", profile="SAFE", risk_perc=0.005)
