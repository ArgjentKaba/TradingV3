from datetime import datetime

from exec.paper import PaperExec


def test_execute_trade_full_leg():
    p = PaperExec(symbol="BTCUSDT", profile="SAFE", start_equity=10000)
    t_entry = datetime(2025, 1, 1, 10, 0)
    t_exit = datetime(2025, 1, 1, 11, 0)
    p.execute_trade(
        side="LONG", entry_price=100.0, exit_price=110.0, time_entry=t_entry, time_exit=t_exit, reason="TP2 hit"
    )
    assert len(p.trades) == 1
    trade = p.trades[0]
    assert trade["symbol"] == "BTCUSDT"
    assert float(trade["equity_after"]) > float(trade["equity_before"])


def test_execute_trade_stop_loss():
    p = PaperExec(symbol="ETHUSDT", profile="FAST", start_equity=5000)
    t_entry = datetime(2025, 1, 2, 9, 0)
    t_exit = datetime(2025, 1, 2, 9, 30)
    p.execute_trade(
        side="SHORT",
        entry_price=200.0,
        exit_price=180.0,
        time_entry=t_entry,
        time_exit=t_exit,
        reason="stopBE triggered",
        be_armed=True,
    )
    assert len(p.trades) == 1
    trade = p.trades[0]
    assert "BE" in trade["leg"]
