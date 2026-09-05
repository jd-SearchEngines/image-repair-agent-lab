# EP04 Content QA

`P1_CONTENT_STATUS = FAIL`

- The declared red scratch is still visibly present in the After image.
- The bottle and surrounding background remain broadly recognizable, but the requested local repair objective was not met.
- The deterministic reference mask and bbox are preserved for evaluation.
- `MASK_NOT_SUPPORTED`: the installed Qwen/MFlux CLI has no explicit mask argument; the mask was recorded as a reference only.
- `inside_mask_change = 0.08373647928237915`; `outside_mask_change_proxy = 0.047631267458200455`.

The two RGB delta values are audit proxies, not quality scores. Attempts: 1; no retry was hidden or performed.
