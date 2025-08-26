import app


def test_build_variants_uses_cfg_when_present(monkeypatch):
    # Werte als Prozentangaben (werden in _build_variants_from_cfg durch 100 geteilt)
    custom_cfg = [("SAFE", 0.75), ("FAST", 1.25)]
    monkeypatch.setattr(app, "CFG_RUN", {**app.CFG_RUN, "variants": custom_cfg})
    vs = app._build_variants_from_cfg()
    assert vs == [("SAFE", 0.0075), ("FAST", 0.0125)]
