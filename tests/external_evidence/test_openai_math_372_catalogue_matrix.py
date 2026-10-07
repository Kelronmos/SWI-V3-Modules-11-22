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


class TestCatalogueMetaFreeze:
    def test_meta_family_count(self, meta):
        assert meta["family_count"] == 372
        assert meta["unique_family_ids"] == 372

    def test_missing_ids_recorded(self, meta):
        assert meta["missing_ids_in_range"] == ["045", "061", "070", "123", "163"]

    def test_contents_hash_frozen(self, meta):
        assert meta["contents_sha256"] == (
            "c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9"
        )

    def test_formalization_yaml_hash_frozen(self, meta):
        assert meta["formalization_yaml_sha256"] == (
            "2dcbd0d6e6a22475f53d49bfdfcac9b6d2b470653c332a9f56522f5be166edb9"
        )

    def test_manuscript_link_count_recorded(self, meta):
        assert meta["manuscript_link_count"] == 721
        assert meta["formalization_source_entry_count"] == 162

    def test_authority_not_bound(self, meta):
        assert meta["authority_status"] == "NOT_BOUND"
        assert meta["authorization_status"] == "NOT_AUTHORIZED"

    def test_mathematical_verification_not_established(self, meta):
        assert meta["mathematical_verification_status"] == "NOT_ESTABLISHED"

    def test_id_range(self, meta):
        assert meta["id_range"]["min"] == "001"
        assert meta["id_range"]["max"] == "377"


class TestOptionalFamiliesCsv:
    def test_csv_if_present_has_372_rows_and_blocks_auth(self):
        if not CSV.is_file():
            pytest.skip("families.csv not yet landed on remote; meta freeze still valid")
        with CSV.open(newline="", encoding="utf-8") as fp:
            rows = list(csv.DictReader(fp))
        assert len(rows) == 372
        ids = [r["family_id"] for r in rows]
        assert len(ids) == len(set(ids))
        for r in rows:
            assert r["authorization"] == "NOT_AUTHORIZED"
            assert r["authority"] == "NOT_BOUND"
            assert r["drift_status"] == "BLOCKED"
            assert r["human_review"] == "NOT_ESTABLISHED"
