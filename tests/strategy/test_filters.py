from strategy.filters import FilterThresholds, RollingStats


def test_filterthresholds_defaults():
    ft = FilterThresholds()
    assert ft.vol_z_min == 0.0
    assert ft.spread_bps_max > 0


def test_rollingstats_basic_queue():
    rs = RollingStats(vol_window=2)
    rs.update(high=10, low=9, close=9.5, volume=100)
    rs.update(high=11, low=10, close=10.5, volume=200)
    rs.update(high=12, low=11, close=11.5, volume=300)
    # deque sollte auf Fenstergröße begrenzen
    assert len(rs.vols) == 2
    assert list(rs.vols)[-1] == 300
