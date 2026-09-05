# Project context

This repository is an evidence-first lab for content-production stories about image repair agents. The claim under test is procedural: diagnosis and scoped repair should make failures observable and reduce unnecessary changes. The current fixtures are synthetic and deterministic so every pixel and manifest can be reproduced on a CPU-only machine.

Evidence labels used throughout the repository:

- `SYNTHETIC_DETERMINISTIC_SIMULATOR`: real local files, controlled fixture, no model quality claim.
- `REAL_MODEL_NOT_RUN`: no valid model/API run in this phase.
- `PRODUCTION_READY`: not claimed.
