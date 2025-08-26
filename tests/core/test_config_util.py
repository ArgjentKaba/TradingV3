import json
from pathlib import Path

from core.config_util import load_config


def test_load_config_with_json(tmp_path: Path):
    file = tmp_path / "test.json"
    file.write_text(json.dumps({"a": 1}))
    default = {"a": 0, "b": 2}
    cfg = load_config(str(file), default)
    assert cfg["a"] == 1
    assert cfg["b"] == 2


def test_load_config_with_yaml(tmp_path: Path):
    file = tmp_path / "test.yaml"
    file.write_text("a: 5\nb: 6")
    default = {"a": 0, "b": 2, "c": 3}
    cfg = load_config(str(file), default)
    assert cfg["a"] == 5
    assert cfg["b"] == 6
    assert cfg["c"] == 3


def test_load_config_missing_file_returns_default(tmp_path: Path):
    missing = tmp_path / "missing.yaml"
    default = {"x": 1}
    cfg = load_config(str(missing), default)
    assert cfg == default


def test_load_config_invalid_content_returns_default(tmp_path: Path):
    file = tmp_path / "test.txt"
    file.write_text("::: invalid :::")
    default = {"z": 9}
    cfg = load_config(str(file), default)
    assert cfg == default
