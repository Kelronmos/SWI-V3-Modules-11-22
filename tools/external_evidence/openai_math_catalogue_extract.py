#!/usr/bin/env python3
"""Deterministic catalogue extractor for openai/math (reference-only).

Does NOT download manuscript bodies.
Does NOT prove mathematical correctness.
Does NOT establish authority or authorization.

Usage (against a local checkout pinned to SOURCE_COMMIT):

  python tools/external_evidence/openai_math_catalogue_extract.py \
    --repo-root /path/to/openai/math \
    --out-dir /tmp/out

Expected freeze:
  source_commit = adc7f1241b42e322a6451854ab7e4b4c146bf78a
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

SOURCE_COMMIT_EXPECTED = "adc7f1241b42e322a6451854ab7e4b4c146bf78a"
FAMILY_RE = re.compile(r"\*\*(\d{3})\.\s+([^*]+?)\*\*")
PDF_RE = re.compile(r"\(preprints/([^)]+\.pdf)\)")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract(repo_root: Path) -> dict:
    contents = repo_root / "CONTENTS.md"
    formal = repo_root / "lean" / "formalization.yaml"
    if not contents.is_file():
        raise SystemExit(f"missing {contents}")
    text = contents.read_text(encoding="utf-8")
    fy = formal.read_text(encoding="utf-8") if formal.is_file() else ""

    matches = list(FAMILY_RE.finditer(text))
    families = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        pdfs = PDF_RE.findall(block)
        title = m.group(2).strip().rstrip(".")
        families.append(
            {
                "id": m.group(1),
                "title": title[:120],
                "ms": len(pdfs),
                "f": "U",
                "a": "NB",
                "z": "NA",
                "d": "B",
            }
        )

    # weak path-token formalization heuristic (PARTIAL only)
    fy_l = fy.lower()
    for fam, m in zip(families, matches):
        start = m.end()
        end = matches[matches.index(m) + 1].start() if matches.index(m) + 1 < len(matches) else len(text)
        block = text[start:end]
        pdfs = PDF_RE.findall(block)
        for p in pdfs:
            folder = p.split("/")[0].lower()
            if folder and folder in fy_l:
                fam["f"] = "P"
                break

    src_titles = re.findall(r'^\s+-\s+title:\s+"([^"]+)"', fy, re.M)
    ids = {f["id"] for f in families}
    id_ints = sorted(int(x) for x in ids)
    missing = [f"{i:03d}" for i in range(id_ints[0], id_ints[-1] + 1) if f"{i:03d}" not in ids]

    ndjson = "\n".join(json.dumps(f, ensure_ascii=False, separators=(",", ":")) for f in families) + "\n"
    return {
        "family_count": len(families),
        "unique_family_ids": len(ids),
        "manuscript_link_count": sum(f["ms"] for f in families),
        "formalization_source_entry_count": len(src_titles),
        "missing_ids_in_range": missing,
        "contents_sha256": sha256_file(contents),
        "formalization_yaml_sha256": sha256_file(formal) if formal.is_file() else None,
        "ndjson_sha256": hashlib.sha256(ndjson.encode()).hexdigest(),
        "ndjson": ndjson,
        "authority_status": "NOT_BOUND",
        "authorization_status": "NOT_AUTHORIZED",
        "mathematical_verification_status": "NOT_ESTABLISHED",
        "method": "contents_md_family_header_v1",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--out-dir", type=Path, required=True)
    ap.add_argument("--expect-commit", default=SOURCE_COMMIT_EXPECTED)
    args = ap.parse_args()

    head = args.repo_root / ".git"
    # commit check is advisory; caller must pin checkout
    result = extract(args.repo_root)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "families.ndjson").write_text(result["ndjson"], encoding="utf-8")
    meta = {k: v for k, v in result.items() if k != "ndjson"}
    meta["expected_source_commit"] = args.expect_commit
    meta["replay_status"] = "BASELINE_OR_LOCAL_RUN"
    meta["note"] = "Local extract is not dual-run REPLAY PASS. Math not proven."
    (args.out_dir / "extract_meta.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
