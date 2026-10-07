# OPEN-015 — Catalogue Replay Plan

**Status:** PLAN RECORDED · **NOT EXECUTED**  
**Authority:** NONE  
**SWI Authorization:** NOT GRANTED  
**Date recorded:** 2026-10-07

```
REPLAY = NOT ESTABLISHED
MATHEMATICS_VERIFIED = NOT ESTABLISHED
AUTHORITY_BOUND = NO
PRODUCTION_AUTHORIZED = NO
```

## Purpose

Reproduce **observation counts** from a **frozen** external source with a
**deterministic method** and **recorded hashes**.

```
NOT PURPOSE:
  prove mathematics
  establish human authority
  grant authorization
  seal SWI
```

## Freeze (inputs)

| Field | Value |
|-------|--------|
| SOURCE_REPOSITORY | `openai/math` |
| SOURCE_COMMIT | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| AUDIT_DATE | 2026-10-07 |
| PRIMARY FILES | `CONTENTS.md`, `README.md`, `lean/formalization.yaml` |
| OPTIONAL | Lean-link patterns in CONTENTS; comparator paths under `lean/` |

**Rule:** Do not rebind to a newer `main` without a new freeze and a new OPEN-015 run.

## Method versions

| Method ID | Target | Procedure |
|-----------|--------|-----------|
| `contents_md_family_header_v1` | Families | Parse `**NNN. Title**` headers in CONTENTS.md |
| `contents_md_pdf_link_v1` | Manuscript PDF links | Extract unique `preprints/...pdf` links |
| `formalization_yaml_sources_v1` | Formalization entries | Count `sources` title entries in `lean/formalization.yaml` |
| `contents_lean_link_v1` | Lean-linked families | **TBD** — only if a deterministic rule is defined from CONTENTS; else **UNKNOWN** |
| `comparator_config_v1` | Comparators | **TBD** — only if a deterministic path/glob is defined; else **UNKNOWN** |

### Prior parse baseline (not dual-run replay)

| Metric | Observed | Note |
|--------|----------|------|
| CONTENTS.md sha256 | `c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9` | Input freeze |
| formalization.yaml sha256 | `2dcbd0d6e6a22475f53d49bfdfcac9b6d2b470653c332a9f56522f5be166edb9` | Input freeze |
| Family count | 372 | Unique IDs 001–377; missing 045, 061, 070, 123, 163 |
| PDF links | 721 | vs README 722 — delta recorded |
| Formalization titles | 162 | From yaml |
| Lean-linked (235) | **NOT SEALED** | Needs `contents_lean_link_v1` or UNKNOWN |
| Comparators (185) | **NOT SEALED** | Needs `comparator_config_v1` or UNKNOWN |

## Replay procedure

```
1. Obtain tree at SOURCE_COMMIT only
2. Verify file hashes = catalogue_meta.json
3. Run method_id with fixed parser version / no network
4. Emit structured output (JSON/CSV metadata only — no manuscript bodies)
5. Hash the output artifact
6. Compare to EXPECTED_HASH
   (first run: record as baseline → status BASELINE_SET, not PASS)
7. Second independent run (clean env) → same hash → REPLAY = PASS
   else REPLAY = FAIL
```

```
FROZEN SOURCE
     ↓
SAME METHOD
     ↓
SAME INPUT
     ↓
SAME OUTPUT
     ↓
SAME HASH
```

Until step 7 succeeds:

```
REPLAY = NOT ESTABLISHED
```

## Outputs (reference-only)

| Artifact | Content |
|----------|---------|
| `catalogue_meta.json` | Counts, methods, input hashes, authority NOT_BOUND |
| `families.csv` (or equivalent) | family_id, title, refs, classifications — **no PDF text** |
| `replay_record.json` | Input SHA, method version, env, expected/observed output hash, result |

**Do not copy:** manuscript PDFs, large sections, reasoning traces.

## Pass / fail criteria

| Claim | PASS means | Does **not** mean |
|-------|------------|-------------------|
| Family count 372 | Parser reproduces 372 unique IDs | Theorems true |
| Formalization 162 | Yaml source titles = 162 | All results machine-checked in this run |
| PDF links 721 | Unique preprint links = 721 | README 722 reconciled |
| Lean 235 | Method defined + count matches | Authorization |
| Comparators 185 | Method defined + count matches | Authorization |
| Replay | Two clean runs, identical output hash | Legitimacy / production |

## Negative gates (must remain)

```
REPLAY PASS     ↛  LEGITIMACY
COUNT MATCH     ↛  MATHEMATICAL PROOF
LEAN LINK       ↛  HUMAN AUTHORITY
FORMALIZATION   ↛  AUTHORIZATION
UNKNOWN METHOD  ↛  INVENTED COUNT
```

If a population cannot be extracted deterministically:

```
STATUS = UNKNOWN
ACTION = do not publish as fact
CONSEQUENCE = OPEN-015 remains open for that population
```

## Execution order (when authorized)

1. Re-fetch **only** frozen commit; verify input hashes
2. Re-run family / pdf / formalization methods
3. Define or reject methods for 235 and 185
4. Write `replay_record.json` (first run = baseline)
5. Second clean run → set REPLAY PASS/FAIL
6. Update open gaps; **no** status promotion to PROVEN / SEALED / AUTHORIZED

## Stop conditions

- License/attribution unclear for anything beyond metadata → **no corpus copy**
- Method for 235/185 ambiguous → **UNKNOWN**, do not force
- Hash mismatch → **REPLAY FAIL**; do not silently change expected
- Pressure to mark PROVEN from green counts → **STOP**

## Expected posture after a successful *execution* of this plan

```
CATALOGUE 372/721/162:  REPRODUCED (if hashes match)
235 / 185:              REPRODUCED or UNKNOWN
REPLAY:                 PASS only after dual-run hash match
MATH OF 372:            NOT PROVEN
AUTHORITY:              NOT BOUND
AUTHORIZATION:          NOT AUTHORIZED
PRODUCTION:             NOT AUTHORIZED
```

**This document is a plan, not a run.**
