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
- SAME_SERIES_P0: Mother A/Product Master and Mother B/Scene Master are locked with original, canonical 1080x1350 assets and Pexels provenance; EP02/EP05/EP06 each completed one real local Qwen/MFlux canonical run using the same model family.

## Boundary and blockers

- `SYNTHETIC_DETERMINISTIC_SIMULATOR`: all current image evidence. It uses known clean fixture pixels to create controlled repair targets; it is not an image model.
- `REAL_MODEL_NOT_RUN`: no remote API was used; this gate used local Qwen/MFlux only.
- `HUMAN_REVIEW_NOT_RUN`: no blind human quality panel was performed; EP05 OCR and EP06 structural identity checks are also not run; see `reports/ep03_human_review_sheet.md` and `reports/skill_series_content_evidence.md`.
- `MASK_NOT_SUPPORTED`: the installed Qwen/MFlux CLI has image conditioning but no explicit mask argument; Local Repair is instruction-based only.
- `PRODUCTION_READY`: not claimed.
- Initial editable installs on this macOS CommandLineTools Python failed because the bundled old pip/setuptools editable path attempted either a system-owned site-packages write or a venv subprocess without `pip`. The runner and tests pass via `PYTHONPATH=src`; the repository also includes standard `pyproject.toml` metadata and a CI workflow for a clean modern Python environment.

## Next gate

Run the blind human/OCR/structural review for the P0 content pack, then decide whether EP01/EP03/EP04 should receive their one canonical attempt. Do not compare model quality using the current synthetic scores or promote the content pack to production claims.
