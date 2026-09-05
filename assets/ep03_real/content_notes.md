# EP03 real-model content notes

## What this pack supports

- Cover candidate: `hero_case_01_board.png`; the local-defect problem is immediately legible.
- All three boards show real Qwen Image Edit outputs from the same controlled synthetic inputs.
- Full Regenerate visibly reconstructs more of the image; Local Repair also changed unrelated text/header pixels in this run.

## What the evidence says

- The strongest honest observation is not that Local Repair won. It is that a real instruction-based edit can remove or alter a local visual issue while still damaging unrelated text and metadata-like regions.
- `MASK_NOT_SUPPORTED` is a central caveat: the installed Qwen/MFlux CLI did not accept an explicit mask, so the Local Repair treatment is instruction-based only.
- The rule proxy fields are in each `runs/REAL-EP03/*/result.json`; they are pixel proxies against a declared clean synthetic fixture, not semantic or human scores.

## Public wording

Safe: “我们用真实 Qwen Image Edit 跑了三个受控测试，并保留了 before / full / local / request / raw metadata 证据。”

Not safe yet: “Local Repair 一定更好”“文字已正确”“保留率提升 X%”“模型达到生产质量”。人工审核、OCR/VLM judge 和显式 mask provider 仍未完成。
