from datetime import datetime

import app


def test_in_session_boundaries():
    # Session-Grenzen als Strings: 07:00 bis **inkl.** 21:00 (UTC)
    start, end = "07:00", "21:00"

    assert not app.in_session(datetime(2025, 1, 1, 6, 59), start, end)
    assert app.in_session(datetime(2025, 1, 1, 7, 0), start, end)
    assert app.in_session(datetime(2025, 1, 1, 7, 1), start, end)
    assert app.in_session(datetime(2025, 1, 1, 20, 59), start, end)
    # 21:00 ist bei dir offenbar **offen**
    assert app.in_session(datetime(2025, 1, 1, 21, 0), start, end)
    assert not app.in_session(datetime(2025, 1, 1, 21, 1), start, end)
