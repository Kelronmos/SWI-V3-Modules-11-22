"""372-family catalogue matrix tests (parser freeze + non-escalation).

Does NOT prove mathematical correctness of any family.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / "evidence" / "external" / "openai_math_372" / "catalogue_meta.json"
PART_A = ROOT / "evidence" / "external" / "openai_math_372" / "families_part_a.ndjson"
PART_B = ROOT / "evidence" / "external" / "openai_math_372" / "families_part_b.ndjson"
ND_META = ROOT / "evidence" / "external" / "openai_math_372" / "families.ndjson.meta.json"


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

    def test_authority_not_bound(self, meta):
        assert meta["authority_status"] == "NOT_BOUND"
        assert meta["authorization_status"] == "NOT_AUTHORIZED"

    def test_mathematical_verification_not_established(self, meta):
        assert meta["mathematical_verification_status"] == "NOT_ESTABLISHED"

    def test_open015_replay_pass_is_not_authorization(self, meta):
        # OPEN-015 may set replay PASS for catalogue extraction only
        assert meta.get("replay_status") in ("PASS", "NOT_ESTABLISHED")
        assert meta["authorization_status"] == "NOT_AUTHORIZED"
        assert meta["mathematical_verification_status"] == "NOT_ESTABLISHED"


class TestOptionalNdjsonMatrix:
    def test_parts_if_present(self, meta):
        if not (PART_A.is_file() and PART_B.is_file()):
            pytest.skip("NDJSON parts not yet on remote")
        lines = PART_A.read_text().splitlines() + PART_B.read_text().splitlines()
        assert len(lines) == 372
        ids = []
        for line in lines:
            row = json.loads(line)
            ids.append(row["id"])
            assert row["a"] == "NB"
            assert row["z"] == "NA"
            assert row["d"] == "B"
        assert len(ids) == len(set(ids))
        blob = "\n".join(lines) + "\n"
        digest = hashlib.sha256(blob.encode()).hexdigest()
        if ND_META.is_file():
            nd = json.loads(ND_META.read_text())
            assert digest == nd["sha256"]
        if meta.get("families_ndjson_sha256"):
            assert digest == meta["families_ndjson_sha256"]
