from exec.paper import PaperExec
from strategy.filters import FilterThresholds, RollingStats, passes_gate


def test_paper_exec_records_trade():
    pe = PaperExec("BTCUSDT")
    pe.execute_trade(
        side="LONG",
        entry_price=100.0,
        exit_price=108.0,
        time_entry="2024-01-01 00:00",
        time_exit="2024-01-01 01:00",
        reason="tp1",
    )
    assert len(pe.trades) == 1


def test_filters_gate_basic():
    th = FilterThresholds(
        mom_long_min=0.0,
        mom_short_max=0.0,
        vol_z_min=-1e9,
        atr14_pct_max=1e9,
    )
    assert passes_gate("LONG", mom_1m_pct=0.1, vol_z=0.0, atr_pct=0.0, oi_delta_5m_pct=0.0, thresholds=th)


def test_rollingstats_runs():
    rs = RollingStats(vol_window=5)
    rs.update(high=10.0, low=9.0, close=9.5, volume=100.0)
    assert isinstance(rs.vol_zscore(), float)
