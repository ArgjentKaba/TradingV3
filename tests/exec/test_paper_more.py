from datetime import datetime

from exec.paper import PaperExec


def test_execute_trade_zero_equity_only():
    # Deckt den Zweig ab: equity_before == 0 -> account_pnl_pct = 0.0
    p = PaperExec(symbol="XRPUSDT", profile="SAFE", start_equity=0.0, sl_pct=6.0)
    t_entry = datetime(2025, 1, 3, 10, 0)
    t_exit = datetime(2025, 1, 3, 10, 15)
    p.execute_trade(
        side="LONG",
        entry_price=100.0,
        exit_price=95.0,
        time_entry=t_entry,
        time_exit=t_exit,
        reason="manual exit",
    )
    trade = p.trades[0]
    assert trade["account_pnl_pct"] == "0.0000"


def test_execute_trade_tp1_and_tp2_and_stopbe():
    p = PaperExec(symbol="BTCUSDT", profile="SAFE")
    t_entry = datetime(2025, 1, 5, 9, 0)
    t_exit = datetime(2025, 1, 5, 10, 0)

    # TP1 (33%)
    p.execute_trade("LONG", 100.0, 110.0, t_entry, t_exit, reason="tp1 hit")
    assert p.trades[-1]["leg"] == "TP1"
    assert p.trades[-1]["leg_fraction"] == "0.33"

    # TP2 (67%)
    p.execute_trade("LONG", 100.0, 110.0, t_entry, t_exit, reason="tp2 reached")
    assert p.trades[-1]["leg"] == "TP2"
    assert p.trades[-1]["leg_fraction"] == "0.67"

    # Stop-BE (BE, 67%)
    p.execute_trade("LONG", 100.0, 90.0, t_entry, t_exit, reason="stopBE triggered")
    assert p.trades[-1]["leg"] == "BE"
    assert p.trades[-1]["leg_fraction"] == "0.67"

    # TimeMax 90m (FULL)
    p.execute_trade("LONG", 100.0, 95.0, t_entry, t_exit, reason="timemax_90m_be")
    assert p.trades[-1]["leg"] == "FULL"
    assert p.trades[-1]["leg_fraction"] == "1.00"
