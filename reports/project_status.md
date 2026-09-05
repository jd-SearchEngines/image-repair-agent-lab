# Project status

**Status: PARTIAL / REAL MODEL GATE 01 PASS / HUMAN REVIEW BLOCKED**

## Verified in this checkout

- `python3 -m image_repair_lab.run_experiments --all` completed on 2026-09-05.
- EXP-A: 5 synthetic cases with before/baseline/structured outputs and boards.
- EXP-B: 3 synthetic cases with full-regenerate/local-repair outputs, masks and boards.
- EXP-C: 3 synthetic cases with v1/v2 outputs, boards and failure/reflection records.
- EXP-D: 20 synthetic cases with manifests, route distribution, batch chart and summary.
- `pytest -q`: expected 2 tests passing.
- REAL_MODEL_GATE_01: 3/3 cases completed with 6 real local Qwen/MFlux outputs; every output has request/result/raw metadata and a comparison board.

## Boundary and blockers

- `SYNTHETIC_DETERMINISTIC_SIMULATOR`: all current image evidence. It uses known clean fixture pixels to create controlled repair targets; it is not an image model.
- `REAL_MODEL_NOT_RUN`: no remote API was used; this gate used local Qwen/MFlux only.
- `HUMAN_REVIEW_NOT_RUN`: no blind human quality panel was performed; see `reports/ep03_human_review_sheet.md`.
- `MASK_NOT_SUPPORTED`: the installed Qwen/MFlux CLI has image conditioning but no explicit mask argument; Local Repair is instruction-based only.
- `PRODUCTION_READY`: not claimed.
- Initial editable installs on this macOS CommandLineTools Python failed because the bundled old pip/setuptools editable path attempted either a system-owned site-packages write or a venv subprocess without `pip`. The runner and tests pass via `PYTHONPATH=src`; the repository also includes standard `pyproject.toml` metadata and a CI workflow for a clean modern Python environment.

## Next gate

Add a versioned real-model adapter, run a 3-case smoke test with raw provenance, then add blind human review. Do not compare model quality using the current synthetic scores.
