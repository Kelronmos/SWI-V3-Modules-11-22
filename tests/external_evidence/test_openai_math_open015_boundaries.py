"""OPEN-015 negative boundary tests — observation is not authority."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REC = ROOT / "evidence" / "external" / "openai_math_372" / "open_015_execution_record.json"


def _rec():
    assert REC.is_file()
    return json.loads(REC.read_text())


def test_replay_pass_does_not_claim_mathematical_proof():
    r = _rec()
    assert r["replay_status"] == "PASS"
    assert r["mathematical_verification_status"] == "NOT_ESTABLISHED"
    assert r["proven"] is False


def test_count_match_does_not_claim_proof():
    r = _rec()
    for v in r["population_results"].values():
        assert v == "REPRODUCED"
    assert r["mathematical_verification_status"] == "NOT_ESTABLISHED"


def test_lean_link_does_not_bind_human_authority():
    r = _rec()
    assert r["populations"]["lean_linked_docs_count"] == 235
    assert r["authority_status"] == "NOT_BOUND"
    assert r["human_review"] == "NOT_ESTABLISHED"


def test_formalization_does_not_authorize():
    r = _rec()
    assert r["populations"]["formalization_source_entry_count"] == 162
    assert r["authorization_status"] == "NOT_AUTHORIZED"
    assert r["production_authorized"] is False


def test_observation_does_not_establish_governance_or_seal():
    r = _rec()
    assert r["governance_binding"] == "NOT_ESTABLISHED"
    assert r["sealed"] is False


def test_first_run_baseline_second_run_pass():
    r = _rec()
    assert r["first_run"]["status"] == "BASELINE_SET"
    assert r["second_run"]["status"] == "PASS"
    assert r["first_run"]["output_sha256"] == r["second_run"]["output_sha256"]


def test_readme_722_discrepancy_not_forced():
    r = _rec()
    d = r["readme_722_discrepancy"]
    assert d["readme_claim"] == 722
    assert d["unique_pdf_links_observed"] == 721
    assert d["action"] == "RECORDED_NOT_FORCED"


def test_input_hashes_verified():
    r = _rec()
    assert r["input_hashes_verified"] is True
    assert r["source_commit"] == "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
