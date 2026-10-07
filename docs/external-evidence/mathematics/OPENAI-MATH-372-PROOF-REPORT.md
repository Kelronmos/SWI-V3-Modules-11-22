# OpenAI Math 372-Family Proof Report

## Proof target

This report proves only that the recorded **repository observations** can be grounded in the identified source snapshot.

It does **not** prove the mathematical truth of every result.

## PROOF-001

**Claim:** The source README states the catalogue contains 372 result families and 722 manuscripts.  
**Input:** `README.md` at `openai/math@adc7f124…`  
**Method:** Direct source text observation  
**Expected:** 372 families, 722 manuscripts  
**Observed:** 372 families, 722 manuscripts  
**Status:** SUPPORTED (repository observation)

**Not claimed:** Mathematical correctness of all 372 families.

## PROOF-002

**Claim:** The source README states not all manuscripts have Lean formalizations and some unformalized results could have issues.  
**Status:** SUPPORTED (repository observation)

## PROOF-003

**Claim:** Secondary reported counts (235 Lean-linked families, 162 formalization entries, 185 comparators) are distinct populations from 372 families.  
**Status:** SUPPORTED as inequality constraints in audit tests  
**Not claimed:** Re-parsed live from CONTENTS.md in this commit (OPEN-013).

## Boundary

```
Repository evidence is proof of the repository observation,
not proof of the underlying mathematical proposition.
```
