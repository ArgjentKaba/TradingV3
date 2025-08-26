import pytest


@pytest.mark.skip(reason="OI-Map wird in app.main() aktuell nicht geladen – wird später separat behandelt.")
def test_main_uses_oi_loader_when_provided():
    pass
