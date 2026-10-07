#!/usr/bin/env python3
"""Generate 372-family NDJSON parts from frozen CONTENTS.md + formalization.yaml.

Preserves catalogue observation fields (ms, f) established by the
contents_md_family_header_v1 extractor. Does NOT prove mathematics,
authority, authorization, seal, or production readiness.
"""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re

CONTENTS = Path("CONTENTS.md")
FORMAL = Path("lean/formalization.yaml")
OUT = Path("evidence/external/openai_math_372")

FAMILY_RE = re.compile(r"\*\*(\d{3})\.\s+([^*]+?)\*\*")
PDF_RE = re.compile(r"\(preprints/([^)]+\.pdf)\)")

assert CONTENTS.is_file(), f"Missing {CONTENTS}"
assert FORMAL.is_file(), f"Missing {FORMAL}"

OUT.mkdir(parents=True, exist_ok=True)

text = CONTENTS.read_text(encoding="utf-8")
fy = FORMAL.read_text(encoding="utf-8")
fy_l = fy.lower()

matches = list(FAMILY_RE.finditer(text))
rows = []
seen = set()

for i, m in enumerate(matches):
    ident = m.group(1)
    if ident in seen:
        continue
    seen.add(ident)

    start = m.end()
    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
    block = text[start:end]
    pdfs = PDF_RE.findall(block)
    title = m.group(2).strip().rstrip(".")
    # title truncation matches extractor ([:120])
    title = title[:120]

    f_status = "U"
    for p in pdfs:
        folder = p.split("/")[0].lower()
        if folder and folder in fy_l:
            f_status = "P"
            break

    rows.append({
        "id": ident,
        "title": title,
        "ms": len(pdfs),
        "f": f_status,
        "a": "NB",
        "z": "NA",
        "d": "B",
    })

assert len(rows) == 372, f"expected 372 rows, got {len(rows)}"
assert len({r["id"] for r in rows}) == 372

def encode(items):
    return "".join(
        json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
        for row in items
    )

part_a = encode(rows[:186])
part_b = encode(rows[186:])
combined = part_a + part_b
digest = hashlib.sha256(combined.encode("utf-8")).hexdigest()

(OUT / "families_part_a.ndjson").write_text(part_a, encoding="utf-8")
(OUT / "families_part_b.ndjson").write_text(part_b, encoding="utf-8")

meta = {
    "format": "ndjson",
    "source_commit": "adc7f1241b42e322a6451854ab7e4b4c146bf78a",
    "source_file": "CONTENTS.md",
    "parser": "contents_md_family_header_v1",
    "row_count": 372,
    "part_a_rows": 186,
    "part_b_rows": 186,
    "sha256": digest,
    "fields": {
        "id": "family_id",
        "title": "title",
        "ms": "manuscript_count",
        "f": "formalization P=PARTIAL U=UNKNOWN",
        "a": "NB=NOT_BOUND",
        "z": "NA=NOT_AUTHORIZED",
        "d": "B=BLOCKED",
    },
    "authority_status": "NOT_BOUND",
    "authorization_status": "NOT_AUTHORIZED",
    "mathematical_verification_status": "NOT_ESTABLISHED",
}

(OUT / "families.ndjson.meta.json").write_text(
    json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
    encoding="utf-8",
)

print(json.dumps(meta, indent=2))
print("---")
print("ms sum:", sum(r["ms"] for r in rows))
print("f P count:", sum(1 for r in rows if r["f"] == "P"))
print("f U count:", sum(1 for r in rows if r["f"] == "U"))
