import app


def test_build_variants_default_when_cfg_empty(monkeypatch):
    # Varianten im CFG leeren, damit der Default-Branch greift
    monkeypatch.setattr(app, "CFG_RUN", {**app.CFG_RUN, "variants": []})
    vs = app._build_variants_from_cfg()
    assert vs == [("SAFE", 0.005), ("SAFE", 0.010), ("FAST", 0.005), ("FAST", 0.010)]
