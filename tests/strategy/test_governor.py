from datetime import datetime, timedelta

from strategy.governor import Governor


def test_trade_count_blocks_after_max_for_day():
    g = Governor(profile="SAFE", trades_min_per_day=0, trades_max_per_day=2, cooldown_minutes=30)
    t0 = datetime(2025, 1, 1, 9, 0, 0)

    # noch keine Trades -> erlaubt
    assert g.can_trade(t0, "BTCUSDT")

    # zwei Trades am selben Tag registrieren
    g.register_trade(t0)
    g.register_trade(t0 + timedelta(minutes=1))

    # dritter Trade am selben Tag darf nicht mehr
    assert not g.can_trade(t0 + timedelta(minutes=2), "BTCUSDT")


def test_cooldown_per_symbol():
    g = Governor(profile="SAFE", cooldown_minutes=30)
    t0 = datetime(2025, 1, 1, 10, 0, 0)

    # Exit auf BTC -> Cooldown startet
    g.register_exit(t0, "BTCUSDT")

    # vor Ablauf der 30 Minuten blockiert
    assert not g.can_trade(t0 + timedelta(minutes=15), "BTCUSDT")

    # nach Ablauf erlaubt
    assert g.can_trade(t0 + timedelta(minutes=31), "BTCUSDT")

    # anderer Markt war nie im Cooldown
    assert g.can_trade(t0 + timedelta(minutes=15), "ETHUSDT")
