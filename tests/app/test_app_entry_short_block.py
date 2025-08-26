from datetime import datetime, timedelta

import app


def _bar(ts, o, h, line, c):
    return app.Bar(t=ts, open=o, high=h, low=line, close=c, volume=100.0)


class DummyGov:
    def __init__(self, *a, **k):
        pass

    def can_trade(self, *a, **k):
        return True  # Governor erlaubt

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


def test_short_side_is_blocked(monkeypatch):
    # Umgebung: alles „grün“ – aber Momentum negativ -> SHORT -> Long-only blockiert Entry
    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})

    t0 = datetime(2025, 1, 1, 10, 0)
    # Bar0 hoch, Bar1 tieferer Close -> Momentum < 0 => side == SHORT
    b0 = _bar(t0, 100, 100, 100, 100)
    b1 = _bar(t0 + timedelta(minutes=1), 99.5, 99.6, 99.4, 99.5)
    # Noch ein Bar, damit Loop >=2 hat
    b2 = _bar(t0 + timedelta(minutes=2), 99.4, 99.6, 99.3, 99.4)

    trades = app.backtest_variant([b0, b1, b2], "BTCUSDT", profile="SAFE", risk_perc=0.005)
    assert trades == [], "Long-only Logik sollte SHORT-Entries blockieren."
