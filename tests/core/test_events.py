from datetime import datetime

from core.events import Bar


def test_bar_fields_are_set_correctly():
    t = datetime(2025, 1, 1, 10, 0)
    b = Bar(t=t, open=1.0, high=2.0, low=0.5, close=1.5, volume=100)
    assert b.t == t
    assert b.open == 1.0
    assert b.high == 2.0
    assert b.low == 0.5
    assert b.close == 1.5
    assert b.volume == 100
