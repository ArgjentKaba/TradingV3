from strategy.filters import FilterThresholds, RollingStats, divergence_ok, passes_gate


def test_passes_gate_long_short_and_thresholds():
    th = FilterThresholds(
        mom_long_min=0.5,
        mom_short_max=-0.5,
        oi_long_min=0.2,
        oi_short_max=-0.2,
        vol_z_min=1.0,
        atr14_pct_max=5.0,
    )
    # LONG fail mom
    assert passes_gate("LONG", 0.2, vol_z=2.0, atr_pct=1.0, oi_delta_5m_pct=0.5, thresholds=th) is False
    # LONG fail oi
    assert passes_gate("LONG", 0.8, vol_z=2.0, atr_pct=1.0, oi_delta_5m_pct=0.1, thresholds=th) is False
    # SHORT fail mom
    assert passes_gate("SHORT", -0.2, vol_z=2.0, atr_pct=1.0, oi_delta_5m_pct=-0.5, thresholds=th) is False
    # SHORT fail oi
    assert passes_gate("SHORT", -1.0, vol_z=2.0, atr_pct=1.0, oi_delta_5m_pct=-0.1, thresholds=th) is False
    # vol_z fail
    assert passes_gate("LONG", 1.0, vol_z=0.5, atr_pct=1.0, oi_delta_5m_pct=0.5, thresholds=th) is False
    # atr_pct fail
    assert passes_gate("LONG", 1.0, vol_z=2.0, atr_pct=10.0, oi_delta_5m_pct=0.5, thresholds=th) is False
    # All ok LONG
    assert passes_gate("LONG", 1.0, vol_z=2.0, atr_pct=1.0, oi_delta_5m_pct=0.5, thresholds=th) is True


def test_ffill_step_updates_vols():
    rs = RollingStats()
    # prev_close ist None -> nichts passiert
    rs.ffill_step()
    assert len(rs.vols) == 0
    # prev_close setzen
    rs.update(2.0, 1.0, 1.5, 100.0)
    before = len(rs.vols)
    rs.ffill_step()
    after = len(rs.vols)
    assert after == before + 1


def test_divergence_ok_allow_true_cases():
    th = FilterThresholds(allow_divergence=True, div_min_abs_oi=0.5, div_max_abs_mom=1.0)
    # oi None -> False
    assert divergence_ok(mom_1m_pct=0.2, oi_delta_5m_pct=None, thresholds=th) is False
    # |oi| hoch genug und |mom| klein genug -> True
    assert divergence_ok(mom_1m_pct=0.3, oi_delta_5m_pct=-0.6, thresholds=th) is True
    # |mom| zu groß -> False
    assert divergence_ok(mom_1m_pct=1.5, oi_delta_5m_pct=0.8, thresholds=th) is False


def test_divergence_ok_allow_false_cases():
    th = FilterThresholds(allow_divergence=False)
    # oi None -> True
    assert divergence_ok(mom_1m_pct=0.2, oi_delta_5m_pct=None, thresholds=th) is True
    # gleiches Vorzeichen -> True
    assert divergence_ok(mom_1m_pct=-0.4, oi_delta_5m_pct=-0.7, thresholds=th) is True
