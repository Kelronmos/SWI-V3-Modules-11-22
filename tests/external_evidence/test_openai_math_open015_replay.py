"""OPEN-015 replay record tests — observation integrity only."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REC = ROOT / "evidence" / "external" / "openai_math_372" / "open_015_replay_record.json"
META = ROOT / "evidence" / "external" / "openai_math_372" / "catalogue_meta.json"


def test_replay_record_exists():
    assert REC.is_file()


def test_replay_pass_and_non_authorization():
    rec = json.loads(REC.read_text())
    assert rec["replay_status"] == "PASS"
    assert rec["authority_status"] == "NOT_BOUND"
    assert rec["authorization_status"] == "NOT_AUTHORIZED"
    assert rec["mathematical_verification_status"] == "NOT_ESTABLISHED"
    assert rec["proven"] is False
    assert rec["sealed"] is False
    assert rec["production_authorized"] is False


def test_populations_reproduced():
    rec = json.loads(REC.read_text())
    p = rec["populations"]
    assert p["family_count"] == 372
    assert p["unique_pdf_links"] == 721
    assert p["formalization_source_entry_count"] == 162
    assert p["lean_linked_docs_count"] == 235
    assert p["comparator_main_results_count"] == 185
    for k, v in rec["population_results"].items():
        assert v == "REPRODUCED"


def test_dual_run_hashes_match():
    rec = json.loads(REC.read_text())
    assert rec["run1_output_sha256"] == rec["run2_output_sha256"]
    assert rec["run1_output_sha256"] == (
        "a2a8a5730f2357cd1f0dba718ea339a5d2cd4b43379dc57bb6fc1d6853f9f086"
    )


def test_input_hashes_match_freeze():
    rec = json.loads(REC.read_text())
    assert rec["input_hashes_verified"] is True
    assert rec["input_hashes"]["CONTENTS.md"].startswith("c492802b")


def test_meta_aligned():
    meta = json.loads(META.read_text())
    assert meta.get("open_015_replay_status") == "PASS"
    assert meta["lean_linked_docs_count"] == 235
    assert meta["comparator_main_results_count"] == 185
