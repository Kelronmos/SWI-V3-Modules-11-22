# Optional 372-row NDJSON matrix status

**Status:** NOT LANDED ON REMOTE (stubs removed)

Incomplete `families_part_a.ndjson` / `families_part_b.ndjson` stubs were removed because they caused `test_parts_if_present` to FAIL (4 rows ≠ 372) instead of SKIP.

## How to regenerate complete parts (local)

```bash
# Pin openai/math@adc7f1241b42e322a6451854ab7e4b4c146bf78a
python tools/external_evidence/openai_math_catalogue_extract.py \
  --repo-root /path/to/openai/math \
  --out-dir /tmp/openai_math_extract
# Then split families.ndjson into part_a (186) + part_b (186)
```

Recorded complete-matrix sha256 (local generation 2026-10-07):
`749e92255d697b878b321ef49e4531d118c330292833391389e981a95cc3d5f5`

```
OPTIONAL MATRIX ON REMOTE = NO
OPEN-015 CORE REPLAY = PASS (independent of this matrix)
AUTHORITY = NOT_BOUND
```
