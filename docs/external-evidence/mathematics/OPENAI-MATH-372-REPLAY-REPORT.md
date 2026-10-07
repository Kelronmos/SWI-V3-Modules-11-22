# OpenAI Math 372 — Replay Report

## Freeze

| Field | Value |
|-------|-------|
| Source repo | openai/math |
| Source commit | `adc7f1241b42e322a6451854ab7e4b4c146bf78a` |
| Parser | `contents_md_family_header_v1` |
| CONTENTS.md sha256 | `c492802b53fb4c4161e45fc678bb67bd526add72ca2635493a367ff7fb860bf9` |
| formalization.yaml sha256 | `2dcbd0d6e6a22475f53d49bfdfcac9b6d2b470653c332a9f56522f5be166edb9` |

## Observed parser output (this audit)

| Metric | Value |
|--------|-------|
| Family headers matched | 372 |
| Unique family IDs | 372 |
| ID range | 001–377 |
| Missing IDs in range | 045, 061, 070, 123, 163 |
| Manuscript PDF links | 721 |
| Formalization source titles | 162 |

## Replay procedure

1. Obtain source commit `adc7f124…`
2. Load `CONTENTS.md` and `lean/formalization.yaml`
3. Verify sha256 against catalogue_meta.json
4. Run family-header parser
5. Expect family_count = 372, unique IDs = 372
6. Compare generated families.csv hash to recorded artifact

## Status

```
REPLAY_METADATA = RECORDED
INDEPENDENT_THIRD_PARTY_REPLAY = NOT_YET_RUN
MATHEMATICS_VERIFIED = NOT ESTABLISHED
AUTHORITY_BOUND = NO
AUTHORIZATION = NOT_AUTHORIZED
```

Replay PASS would prove **catalogue reproducibility**, not mathematical truth.
