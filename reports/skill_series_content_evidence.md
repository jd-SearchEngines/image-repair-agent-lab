# Same-series content evidence index

This is `CONTENT DEMO / CONTROLLED EXPERIMENT` evidence, not a benchmark. The
table distinguishes v1, v2, first pass, second pass, deterministic
preprocessing/post-processing, and real-model output. EP02 and EP05 are locked
and were not rerun. EP07 remains `NOT_RUN`.

| Evidence | Mother / input lineage | Skill / pass | Real model call | Best comparison board | Status | Deterministic boundary and retained caveat |
|---|---|---|---:|---|---|---|
| EP01 v1 | Mother B / canonical scene | Vintage Poster v1 / first pass | 1 historical | `assets/skill_series/ep01/compare_board.png` | `PARTIAL` | Real model made the style change but generated malformed text; retained in `reports/content_qa_ep01.md`. |
| EP01 v2 | Mother B / canonical scene | Vintage Poster v2 / one real pass | 1 new | `assets/skill_series/ep01/compare_board_v2.png` | `CONTENT_USABLE` | Prompt forbids all generated text. PIL deterministic textured blank zones plus optional `OLD STREET CAFE` title; raw model output retained under `runs/skill_series/EP01/v2_text_free/`. |
| EP02 v1 | Mother A / product master | Hero Product v1 / first pass | 1 historical | `assets/skill_series/ep02/compare_board.png` | `CONTENT_USABLE` | Locked; not rerun. |
| EP03 v1 | Mother A / deterministic clutter variant | Background Cleanup v1 / first pass | 1 historical | `assets/skill_series/ep03/compare_board.png` | `PARTIAL` | Four clutter objects mostly removed but faint ghosts remained; retained in `reports/content_qa_ep03.md`. |
| EP03 v2 | EP03 v1 After as input | Background Cleanup / targeted second pass | 1 new | `assets/skill_series/ep03/final_compare_board.png` | `CONTENT_USABLE` | One Qwen second pass; feathered deterministic composite only in four declared residual regions. Bottle/cap/position/framing preserved from v1. |
| EP04 v1 | Mother A / deterministic scratch variant | Local Repair v1 / first pass | 1 historical | `assets/skill_series/ep04/compare_board.png` | `FAIL` | Scratch remains; MFlux had `MASK_NOT_SUPPORTED`. Failure retained. |
| EP04 backend gate | EP04 defect input + explicit mask | Qwen Diffusers inpaint backend / one smoke | 0 image inferences; 1 load attempt | `runs/skill_series/EP04/backend_smoke_qwen_diffusers/result.json` | `LOCAL_REPAIR_BACKEND_BLOCKED` | Pipeline exposes explicit `mask_image`, but local Qwen official text encoder is incomplete; failed before inference. No masked success claim. |
| EP05 v1 | Mother A / deterministic text variant | Chinese Text Repair v1 / first pass | 1 historical | `assets/skill_series/ep05/compare_board.png` | `CONTENT_USABLE` | Locked; not rerun; OCR evidence retained. |
| EP06 v1 | Mother B / canonical scene | Cinematic Scene v1 / first pass | 1 historical | `assets/skill_series/ep06/compare_board.png` | `CONTENT_UNUSABLE` | Cinematic change succeeded but malformed storefront text remained; retained. |
| EP06 v2 | Mother B / deterministic text-safe variant | Cinematic Scene v2 / one real pass | 1 new | `assets/skill_series/ep06/compare_board_v2.png` | `CONTENT_USABLE` | PIL controlled variant and disclosed signage mask precede Qwen; deterministic restoration/blur prevents malformed sign text. Not the original-photo lineage. |
| EP07 | Mixed | Multi-Skill Agent | 0 | `NOT_RUN` | `NOT_RUN` | Explicitly not run this turn. |

## Gate summary

- New real Qwen MFlux image calls this turn: `3` (EP01 v2, EP03 second pass, EP06 v2), exactly one each.
- EP04 backend smoke: `1` pipeline-load attempt, `0` image inferences; blocked before model inference.
- `CONTENT_USABLE_COUNT = 5 / 6`: EP01, EP02, EP03, EP05, EP06.
- `CONTENT_POLISH_GATE = PASS` for the three requested content repairs plus a resolved backend decision.
- `READY_FOR_EP07 = NO`: the 5/6 threshold is met, but EP07 was explicitly prohibited in this turn.

Canonical provenance is under `data/mother_cases/*/provenance.json`. Per-episode
request/result/raw metadata and run artifacts are under `runs/skill_series/`.
