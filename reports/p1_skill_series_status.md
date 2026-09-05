# P1 same-series skill run

- Model: `mlx-community/qwen-image-edit-2511-8bit` via local MFlux
- EP02/EP05/EP06 were not rerun.

- EP01 Vintage Poster: PASS_EXECUTION; attempts=1; failed=none
- EP03 Background Cleanup: PASS_EXECUTION; attempts=1; failed=none
- EP04 Local Repair: PASS_EXECUTION; attempts=1; failed=none

Content QA: EP01 `PARTIAL`, EP03 `PARTIAL`, EP04 `FAIL`. EP02/EP05/EP06 were not rerun; their QA is recorded in `reports/content_qa_ep02.md`, `reports/content_qa_ep05.md`, and `reports/content_qa_ep06.md`.

`P1_CONTENT_GATE = PARTIAL`

`READY_FOR_EP07 = NO`

EP07 remains stopped until the content QA decisions are accepted and the local-repair failure is either intentionally retained as a failure case or followed by an explicitly authorized next experiment. This is controlled content evidence, not a benchmark.

## Content polish gate

- EP01 v2: `CONTENT_USABLE`
- EP03 second pass: `CONTENT_USABLE`
- EP06 v2: `CONTENT_USABLE`
- EP04 local repair backend: `LOCAL_REPAIR_BACKEND_BLOCKED`; original `FAIL` retained
- EP02 and EP05 were not rerun
- EP07 was not run

`CONTENT_POLISH_GATE = PASS`

`CONTENT_USABLE_COUNT = 5 / 6` (EP01, EP02, EP03, EP05, EP06)

`READY_FOR_EP07 = NO` because this turn explicitly keeps EP07 stopped even though the 5/6 content threshold is now met.
