# OPEN-015 — Catalogue Replay Plan

**Status:** EXECUTED · REPLAY PASS (catalogue extraction only)  
**Authority:** NONE  
**SWI Authorization:** NOT GRANTED  
**Date recorded:** 2026-10-07  
**Execution record:** `evidence/external/openai_math_372/open_015_execution_record.json`

```
REPLAY = PASS
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
| CONTENTS.md sha256 | `c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9` |
| formalization.yaml sha256 | `2dcbd0d6e6a22475f53d49bfdfcac9b6d2b470653c332a9f56522f5be166edb9` |

Input hashes: **VERIFIED** on execution.

## Methods executed

| Method ID | Target | Result |
|-----------|--------|--------|
| `contents_md_family_header_v1` | Families | **372 REPRODUCED** |
| `contents_md_pdf_link_v1` | PDF links | **721 REPRODUCED** (README claims 722; delta recorded) |
| `formalization_yaml_sources_v1` | Formalization sources | **162 REPRODUCED** |
| `contents_md_lean_docs_link_v1` | Lean-linked docs | **235 REPRODUCED** |
| `formalization_yaml_status_main_results_v1` | Comparator main_results | **185 REPRODUCED** (178 unique JSON paths) |

## Replay

| Run | Status | Output SHA-256 |
|-----|--------|----------------|
| First | BASELINE_SET | `f3c1238ac5dd112b509d3dd223143e57d7301aad8c39c711b9ecf4155e55b0d2` |
| Second | PASS | `f3c1238ac5dd112b509d3dd223143e57d7301aad8c39c711b9ecf4155e55b0d2` |

```
REPLAY = PASS
```

## Explicit non-claims

```
REPLAY_PASS ↛ MATHEMATICAL_PROOF
COUNT_MATCH ↛ MATHEMATICAL_PROOF
LEAN_LINK ↛ HUMAN_AUTHORITY
FORMALIZATION ↛ AUTHORIZATION
CI_GREEN ↛ PRODUCTION_AUTHORIZATION
OBSERVATION ↛ AUTHORITY
```
