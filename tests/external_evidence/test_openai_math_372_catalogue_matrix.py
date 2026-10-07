"""372-family catalogue matrix tests (parser freeze + non-escalation).

Does NOT prove mathematical correctness of any family.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "evidence" / "external" / "openai_math_372" / "catalogue_meta.json"
CSV = ROOT / "evidence" / "external" / "openai_math_372" / "families.csv"


@pytest.fixture(scope="module")
def meta():
    assert META.is_file()
    return json.loads(META.read_text())


@pytest.fixture(scope="module")
def rows():
    assert CSV.is_file(), "families.csv missing — matrix not landed"
    with CSV.open(newline="", encoding="utf-8") as fp:
        return list(csv.DictReader(fp))


class TestCatalogueMatrix:
    def test_meta_family_count(self, meta):
        assert meta["family_count"] == 372
        assert meta["unique_family_ids"] == 372

    def test_csv_row_count(self, rows):
        assert len(rows) == 372

    def test_family_ids_unique(self, rows):
        ids = [r["family_id"] for r in rows]
        assert len(ids) == len(set(ids))

    def test_missing_ids_recorded(self, meta):
        assert meta["missing_ids_in_range"] == ["045", "061", "070", "123", "163"]

    def test_no_row_is_authorized(self, rows):
        for r in rows:
            assert r["authorization"] == "NOT_AUTHORIZED"
            assert r["authority"] == "NOT_BOUND"
            assert r["drift_status"] == "BLOCKED"

    def test_no_row_claims_human_review_complete(self, rows):
        for r in rows:
            assert r["human_review"] == "NOT_ESTABLISHED"

    def test_partial_formalization_does_not_authorize(self, rows):
        partial = [r for r in rows if r["formalization"] == "PARTIAL"]
        assert len(partial) >= 1
        for r in partial:
            assert r["authorization"] == "NOT_AUTHORIZED"

    def test_contents_hash_frozen(self, meta):
        assert meta["contents_sha256"] == (
            "c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9"
        )

    def test_mathematical_verification_not_established(self, meta):
        assert meta["mathematical_verification_status"] == "NOT_ESTABLISHED"
