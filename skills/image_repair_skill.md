# Structured Image Repair Skill

1. State the observed defect and its spatial scope.
2. Classify exactly one primary issue: `TEXT`, `FACT`, `LOCAL_DEFECT`, `COMPOSITION`, `BACKGROUND`, or `GLOBAL_FAILURE`.
3. Write preserve constraints before choosing an edit.
4. Prefer the smallest mask and local route that can satisfy the instruction.
5. Run visual QA and rule QA; if failed, record the reason before retrying.
6. Never claim model or human-quality evidence from a deterministic fixture.
