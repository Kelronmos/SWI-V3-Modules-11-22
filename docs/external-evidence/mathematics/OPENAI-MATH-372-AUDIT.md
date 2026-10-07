# OpenAI Math — 372 Result-Family Evidence Audit

**Status:** OBSERVATION / EXTERNAL EVIDENCE  
**Authority:** NONE  
**SWI Authorization:** NOT GRANTED  
**Audit date:** 2026-10-07  
**Source commit:** `adc7f1241b42e322a6451854ab7e4b4c146bf78a` (`openai/math` main)

## Source

OpenAI Math repository: https://github.com/openai/math

## Catalogue statement (source README)

722 manuscripts covering 372 result families.

## Parser freeze (CONTENTS.md)

| Metric | Value |
|--------|-------|
| Parser | `contents_md_family_header_v1` |
| CONTENTS.md sha256 | `c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9` |
| formalization.yaml sha256 | `2dcbd0d6e6a22475f53d49bfdfcac9b6d2b470653c332a9f56522f5be166edb9` |
| Family headers matched | **372** |
| Unique family IDs | **372** |
| ID range | 001–377 |
| Missing IDs in range | 045, 061, 070, 123, 163 |
| Manuscript PDF links | **721** (vs README 722 — delta recorded) |
| Formalization source entries | **162** |

Artifact: `evidence/external/openai_math_372/catalogue_meta.json`

## Purpose

Map the repository’s mathematical result families against the SWI evidence ladder **without** treating formalization, machine checking, or repository presence as authorization.

## Important

This report does **NOT** establish the mathematical truth of every result.

## SWI invariant

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

## Evidence ladder

F0 Family → F1 Claim → F2 Manuscript → F3 Formalization → F4 Machine Check → F5 Comparator → F6 Reproducibility → F7 Human Review → F8 Governance → F9 Authority → F10 Authorization

```
F0 ≠ F1 ≠ … ≠ F10
```

## Repository-level observations

```
372 families
≠ 162 formalization entries
≠ 721 manuscript links
≠ 372 verified mathematical results
≠ 372 human-reviewed results
≠ 372 authorized actions
```

## SWI drift test

```
Formalized ≠ Verified ≠ Human Accepted ≠ Governed ≠ Authorized ≠ Executed ≠ Legitimate
```

## Permit boundary

```
Permit(a) ⟺ ∀ L,G,S,H: C(a) ⊆ L ∩ G ∩ S ∩ H  ∧  E(a) ≠ ∅
```

`E(a) ≠ ∅` does **not** mean sufficient, authority, authorization, or action.

## Individual 372-row matrix

**Parser-produced local matrix exists** (372 rows; all `NOT_AUTHORIZED` / `NOT_BOUND` / `BLOCKED`).  
**Remote `families.csv` upload:** in progress / partial (size-constrained transfer).  
**Do not treat absence of remote CSV as absence of the meta freeze.**

## Conclusion

```
REPORT_ADDED = YES
CATALOGUE_PARSER_FREEZE = YES
MATHEMATICS_VERIFIED = NOT ESTABLISHED
AUTHORITY_BOUND = NO
PRODUCTION_AUTHORIZATION = NO
```
