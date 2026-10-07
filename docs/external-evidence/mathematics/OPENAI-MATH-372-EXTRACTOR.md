# Catalogue extractor (reference-only)

**Tool:** `tools/external_evidence/openai_math_catalogue_extract.py`

**Status:** TOOL PRESENT · REPLAY NOT ESTABLISHED until dual-run hash match against frozen source.

```
Does NOT copy manuscript PDFs.
Does NOT prove mathematics.
Does NOT bind authority.
Does NOT authorize production.
```

## Freeze

`openai/math@adc7f1241b42e322a6451854ab7e4b4c146bf78a`

## Use

```bash
git clone https://github.com/openai/math.git
cd math && git checkout adc7f1241b42e322a6451854ab7e4b4c146bf78a
python /path/to/SWI/tools/external_evidence/openai_math_catalogue_extract.py \
  --repo-root . --out-dir /tmp/openai_math_extract
```

Compare `extract_meta.json` fields to `evidence/external/openai_math_372/catalogue_meta.json`.

OPEN-015 dual-run remains required for `REPLAY = PASS`.
