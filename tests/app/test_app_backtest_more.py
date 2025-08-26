from datetime import datetime, timedelta

import pytest

import app


def make_bar(ts, price):
    return app.Bar(t=ts, open=price, high=price, low=price, close=price, volume=100.0)


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


@pytest.mark.parametrize("scenario", ["tp1_tp2", "be", "timemax"])
def test_backtest_variant_special_paths(monkeypatch, scenario):
    # Ensure no cutoff by days_back
    monkeypatch.setattr(app, "CFG_RUN", {})

    # Dummies / always-true gates
    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)

    start = datetime(2025, 1, 1, 10, 0)
    bars = [make_bar(start, 1.0)]

    # Entry-Bar: close = 1.05 -> entry_price = 1.05
    entry_bar_time = start + timedelta(minutes=1)
    bars.append(make_bar(entry_bar_time, 1.05))

    # TP1-Bar: high deutlich über TP1 (TP1 = 1.05 * 1.08 = 1.134)
    tp1_time = entry_bar_time + timedelta(minutes=1)
    bars.append(app.Bar(t=tp1_time, open=1.05, high=1.20, low=1.05, close=1.10, volume=100.0))

    if scenario == "tp1_tp2":
        # TP2-Bar: high deutlich über TP2 (TP2 = 1.05 * 1.12 = 1.176)
        tp2_time = tp1_time + timedelta(minutes=1)
        bars.append(app.Bar(t=tp2_time, open=1.10, high=1.25, low=1.10, close=1.20, volume=100.0))
    elif scenario == "be":
        # BE-Bar: nach TP1 fällt low auf/unter entry_price (1.05) -> StopBE
        be_time = tp1_time + timedelta(minutes=1)
        bars.append(app.Bar(t=be_time, open=1.06, high=1.06, low=1.00, close=1.03, volume=100.0))
    elif scenario == "timemax":
        # 90m nach Entry (entry um 10:01) -> 11:36+ reicht; close > entry -> TimeMax_90m_Profit
        timemax_time = entry_bar_time + timedelta(minutes=95)
        bars.append(app.Bar(t=timemax_time, open=1.05, high=1.07, low=1.05, close=1.06, volume=100.0))

    trades = app.backtest_variant(bars, "BTCUSDT", profile="SAFE", risk_perc=0.005)
    assert trades, f"Expected trades for scenario {scenario}"


def test_gap_handling(monkeypatch):
    monkeypatch.setattr(app, "CFG_RUN", {})
    monkeypatch.setattr(app, "Governor", DummyGov)
    monkeypatch.setattr(app, "RollingStats", DummyRS)
    monkeypatch.setattr(app, "load_oi_map", lambda *a, **k: {})
    monkeypatch.setattr(app, "in_session", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "passes_gate", lambda *_a, **_k: True)
    monkeypatch.setattr(app, "divergence_ok", lambda *_a, **_k: True)

    start = datetime(2025, 1, 1, 10, 0)
    bars = [
        make_bar(start, 1.0),
        make_bar(start + timedelta(minutes=4), 1.1),  # Gap > 2m -> lock
        make_bar(start + timedelta(minutes=5), 1.12),
        make_bar(start + timedelta(minutes=6), 1.15),
        make_bar(start + timedelta(minutes=7), 1.20),
        make_bar(start + timedelta(minutes=8), 1.25),
        make_bar(start + timedelta(minutes=9), 1.30),
    ]
    trades = app.backtest_variant(bars, "BTCUSDT", profile="SAFE", risk_perc=0.005)
    # Nur Robustheit: es darf nicht crashen; Einstieg kann verzögert sein
    assert isinstance(trades, list)
