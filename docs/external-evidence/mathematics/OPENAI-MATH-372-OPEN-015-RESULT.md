# OPEN-015 Result — Catalogue Population Replay

**Execution date:** 2026-10-07  
**Source:** `openai/math@adc7f1241b42e322a6451854ab7e4b4c146bf78a`

## Input hash verification

| File | Expected | Observed | Match |
|------|----------|----------|-------|
| CONTENTS.md | `c492802b…fb860bf9` | same | YES |
| lean/formalization.yaml | `2dcbd0d6…be166edb9` | same | YES |

## Methods (deterministic)

| Population | Method ID | Definition |
|------------|-----------|------------|
| 372 families | `contents_md_family_header_v1` | `**NNN. Title**` headers in CONTENTS.md |
| 721 PDF links | `contents_md_pdf_link_v1` | Unique `preprints/...pdf` links |
| 162 formalizations | `formalization_yaml_sources_v1` | `sources` list in formalization.yaml |
| 235 Lean-linked | `contents_md_lean_docs_link_v1` | Unique `lean/docs/N.md` paths in CONTENTS.md |
| 185 comparators | `formalization_yaml_status_main_results_v1` | `status.main_results` entries (each with `comparator_config`) |

Note: 185 main_results → **178** unique comparator JSON paths (recorded, not forced equal).

## Population results

| Population | Result |
|------------|--------|
| 372 | **REPRODUCED** |
| 721 | **REPRODUCED** |
| 162 | **REPRODUCED** |
| 235 | **REPRODUCED** |
| 185 | **REPRODUCED** |

## Replay

| Run | Structured-output SHA-256 |
|-----|---------------------------|
| 1 | `a2a8a5730f2357cd1f0dba718ea339a5d2cd4b43379dc57bb6fc1d6853f9f086` |
| 2 | `a2a8a5730f2357cd1f0dba718ea339a5d2cd4b43379dc57bb6fc1d6853f9f086` |

```
REPLAY = PASS
```

Scope: deterministic catalogue population extraction only. Same-process dual-run. Independent third-party clean-env replay is optional stronger evidence.

## Explicit non-claims

```
REPLAY PASS ≠ MATHEMATICS PROVEN
REPLAY PASS ≠ HUMAN REVIEW
REPLAY PASS ≠ AUTHORITY BOUND
REPLAY PASS ≠ AUTHORIZED
REPLAY PASS ≠ SEALED
REPLAY PASS ≠ PRODUCTION AUTHORIZED
```

Machine record: `evidence/external/openai_math_372/open_015_replay_record.json`
