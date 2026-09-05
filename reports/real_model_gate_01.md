# REAL_MODEL_GATE_01

**Status: PASS (execution/provenance gate only; not a quality win).**

- Provider: `local-mflux`
- Model: `mlx-community/qwen-image-edit-2511-8bit`
- Runtime: MFlux 0.19.1 / MLX 0.32.2 / Apple M3 Max / 64 GiB
- Treatments: 3 cases x Full Regenerate + Local Repair = 6 real provider calls
- Input boundary: all inputs are `CONTROLLED_SYNTHETIC_TEST_IMAGE`
- Local mask boundary: `MASK_NOT_SUPPORTED`; the installed Qwen/MFlux CLI accepts image conditioning but no explicit mask flag
- Human review: `NOT_RUN`; review sheet is intentionally blank
- Simulator mixing: `NONE`; historical EXP-A/B/C/D files were not modified

## Case evidence

### case_02

- Full result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_01/full_regen.png`
- Local result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_01/local_repair.png`
- Full unrelated-region change proxy: `0.049`
- Local unrelated-region change proxy: `0.0529`
- Semantic target/text/product/layout fields: unverified; see `result.json`.

### case_00

- Full result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_02/full_regen.png`
- Local result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_02/local_repair.png`
- Full unrelated-region change proxy: `0.0301`
- Local unrelated-region change proxy: `0.0445`
- Semantic target/text/product/layout fields: unverified; see `result.json`.

### case_01

- Full result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_03/full_regen.png`
- Local result: `/Users/jingdong/Downloads/skill diff project/runs/REAL-EP03/case_03/local_repair.png`
- Full unrelated-region change proxy: `0.0434`
- Local unrelated-region change proxy: `0.0506`
- Semantic target/text/product/layout fields: unverified; see `result.json`.

## Interpretation boundary

The real model executed and produced inspectable outputs, but the local instruction path did not enforce a mask and OCR/VLM/human review was not run. The evidence supports saying that a real model was exercised on controlled inputs; it does not support saying Local Repair is better, text is correct, or preservation improved by a percentage.
