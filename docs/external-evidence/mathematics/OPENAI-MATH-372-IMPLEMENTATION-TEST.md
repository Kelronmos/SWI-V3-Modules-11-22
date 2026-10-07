# OpenAI Math 372 — SWI Implementation Boundary Tests

These tests check whether SWI correctly **blocks** evidence→authority escalation.

| Test | Input | Expected |
|------|-------|----------|
| A | Lean document exists | AUTHORIZATION blocked |
| B | Machine proof passes | HUMAN_AUTHORITY not auto-bound |
| C | E(a) ≠ ∅ | Permit(a) not automatic |
| D | CI green | PRODUCTION_AUTHORIZED blocked |
| E | Signature present | AUTHORITY not automatic |
| F | Formalization | AUTHORIZATION blocked |
| G | Replay PASS | Legitimacy not automatic |

Executable coverage: `tests/external_evidence/test_openai_math_372_audit.py`
