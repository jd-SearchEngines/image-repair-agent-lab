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
