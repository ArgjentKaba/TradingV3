import pytest

import app


def test_main_raises_when_universe_file_missing(monkeypatch, tmp_path):
    missing = tmp_path / 'does_not_exist.txt'
    outdir = tmp_path / 'runs'

    monkeypatch.setattr(
        app,
        'CFG_RUN',
        {
            'universe_file': str(missing),
            'output': {'dir': str(outdir), 'save_combined': True},
        },
    )
    monkeypatch.setattr(app, 'VARIANTS', [('SAFE', 0.005)])

    # Erwartung: FileNotFoundError aus load_symbols()
    with pytest.raises(FileNotFoundError):
        app.main()
