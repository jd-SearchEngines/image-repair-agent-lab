# Results summary

All values below are from `SYNTHETIC_DETERMINISTIC_SIMULATOR` fixtures and are reproducibility evidence, not model quality.

| Run | Cases | Result |
|---|---:|---|
| EXP-A | 5 | structured route keeps a local scope; baseline is broad by construction |
| EXP-B | 3 | local repair reports preserve score; full regenerate is intentionally global |
| EXP-C | 3 | first-pass failures are recorded and second pass is attempted when QA fails |
| EXP-D | 20 | 5 pass before, 17 repaired successfully, 3 still failed, avg attempts 1.35 |

EXP-D route distribution: `text_repair_local=4`, `fact_repair_local=4`, `local_inpaint=3`, `composition_reframe=3`, `background_repair=3`, `full_regenerate_review=3`.

The canonical machine-readable source is [runs/EXP-D/manifest.json](../runs/EXP-D/manifest.json). The content-friendly chart is [runs/EXP-D/batch_statistics.png](../runs/EXP-D/batch_statistics.png).

## REAL-EP03

`REAL_MODEL_GATE_01` is `PASS` for execution/provenance: local MFlux 0.19.1 ran `mlx-community/qwen-image-edit-2511-8bit` on 3 controlled synthetic inputs, with Full Regenerate and Local Repair treatments. The strongest preservation proxy did not favor Local Repair consistently, and semantic/OCR/human judging remains unverified. See [reports/real_model_gate_01.md](real_model_gate_01.md).
