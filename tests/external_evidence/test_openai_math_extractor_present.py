"""Extractor tool presence tests — not a replay execution."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TOOL = ROOT / "tools" / "external_evidence" / "openai_math_catalogue_extract.py"


def test_extractor_script_exists():
    assert TOOL.is_file()


def test_extractor_declares_non_authorization():
    text = TOOL.read_text(encoding="utf-8")
    assert "Does NOT prove mathematical correctness" in text
    assert "NOT_AUTHORIZED" in text or "authorization" in text.lower()
