# Local Repair Skill v1

- Diagnose one explicit defect and preserve all other regions.
- Use a defect mask when the provider supports one; otherwise record `MASK_NOT_SUPPORTED`.
- Measure outside-mask pixel-change proxy, but do not call it semantic preservation.
- Keep failed attempts and never claim production quality without human review.
