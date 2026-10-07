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

## Purpose

Map the repository’s mathematical result families against the SWI evidence ladder **without** treating formalization, machine checking, or repository presence as authorization.

## Important

This report does **NOT** establish the mathematical truth of every result.  
It records observable repository evidence and identifies gaps requiring further validation.

## SWI invariant

```
DATA ≠ EVIDENCE ≠ ADMISSION ≠ AUTHORIZATION ≠ ACTION
```

## Evidence ladder

| Level | Name |
|-------|------|
| F0 | Family |
| F1 | Claim |
| F2 | Manuscript |
| F3 | Formalization |
| F4 | Machine Check |
| F5 | Comparator |
| F6 | Reproducibility |
| F7 | Human Review |
| F8 | Governance |
| F9 | Authority |
| F10 | Authorization |

```
F0 ≠ F1 ≠ F2 ≠ F3 ≠ F4 ≠ F5 ≠ F6 ≠ F7 ≠ F8 ≠ F9 ≠ F10
```

## Repository-level observations

| Observation | Value | Status |
|-------------|-------|--------|
| Manuscripts (README) | 722 | OBSERVED |
| Result families (README) | 372 | OBSERVED |
| Lean-linked families (secondary count) | 235 | OBSERVED (external parse of CONTENTS.md) |
| Formalization source entries | 162 | OBSERVED (formalization.yaml reporting) |
| Comparator configurations | 185 | OBSERVED (secondary reporting) |
| Mixed verification stages | yes | OBSERVED (README) |
| All manuscripts formalized | no | OBSERVED (README) |
| Unformalized may have issues | yes | OBSERVED (README) |

These numbers are **not** interchangeable:

```
372 families
≠ 235 Lean-linked families
≠ 162 formalization entries
≠ 185 comparator configurations
≠ 372 verified mathematical results
≠ 372 human-reviewed results
≠ 372 authorized actions
```

## SWI drift test

Potential evidence drift occurs when a lower evidence state is interpreted as a higher authority state without an explicit gate.

```
repository entry
    ↓
manuscript
    ↓
formalization
    ↓
machine checking
    ↓
human interpretation
    ↓
governance
    ↓
authority
    ↓
authorization
    ↓
action
```

A successful transition at one layer does **not** automatically authorize the next layer.

```
Formalized ≠ Verified
Verified ≠ Human Accepted
Human Accepted ≠ Governed
Governed ≠ Authorized
Authorized ≠ Executed
Executed ≠ Legitimate
```

## Permit boundary

```
Permit(a) ⟺
  ∀ L,G,S,H:
    C(a) ⊆ L ∩ G ∩ S ∩ H
  ∧
    E(a) ≠ ∅
```

Interpretation:

- `E(a) ≠ ∅` means evidence exists.
- It does **not** mean E(a) is sufficient, establishes authority, establishes authorization, or permits consequential action.

Lean / formalization can strengthen `E(a)`. It does not automatically fill L, G, S, and H.

## Individual 372-row matrix

**Status:** NOT BUILT in this commit.

Portfolio observations are frozen. A full 372-row evidence matrix requires deterministic extraction from `CONTENTS.md` + `overview` against the frozen source commit and is recorded as an open gap.

## Conclusion

The audit establishes the existence and structure of the published repository evidence at the portfolio level.

It does **not** establish that all 372 mathematical result families are mathematically proven, independently reviewed, governance-bound, authorized, or suitable for consequential action.

```
Evidence remains evidence.
Authority remains a separate boundary.
```

```
REPORT_ADDED = YES
MATHEMATICS_VERIFIED = NOT ESTABLISHED
HUMAN_REVIEW = NOT ESTABLISHED
GOVERNANCE_BINDING = NOT ESTABLISHED
AUTHORITY_BOUND = NO
PRODUCTION_AUTHORIZATION = NO
```
