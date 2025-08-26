from datetime import datetime

from core.timeutil import in_session


def test_in_session_true():
    t = datetime(2025, 1, 1, 10, 30)
    assert in_session(t, "09:00", "11:00") is True


def test_in_session_false():
    t = datetime(2025, 1, 1, 8, 59)
    assert in_session(t, "09:00", "11:00") is False


def test_in_session_edge_cases():
    t_start = datetime(2025, 1, 1, 9, 0)
    t_end = datetime(2025, 1, 1, 11, 0)
    assert in_session(t_start, "09:00", "11:00") is True
    assert in_session(t_end, "09:00", "11:00") is True
