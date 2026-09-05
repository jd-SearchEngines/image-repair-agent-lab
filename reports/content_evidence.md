# Content evidence map

Every claim below points to local files and carries the synthetic evidence caveat.

| EP | Claim | Supporting run | Screenshot candidates | Caveat |
|---|---|---|---|---|
| EP01 | 一句 Prompt 会把修复范围变宽；结构化 skill 先写诊断和约束 | EXP-A | `assets/ep01/compare_board.png` | baseline/simulator are controlled, not a model comparison |
| EP02 | 先判断哪里坏了，再决定怎么修 | EXP-A | `assets/ep02/compare_board.png`, `code_snippet.md` | diagnosis comes from fixture metadata |
| EP03 | 局部错误不应整图重做 | EXP-B | `assets/ep03/compare_board.png`, `optional_mask.png` | no perceptual metric or human review |
| EP04 | QA 失败后，reflection can trigger a bounded second pass | EXP-C | `assets/ep04/compare_board.png` | retry uses known target in simulator |
| EP05 | 不同错误类型需要不同路由 | EXP-D | `assets/ep05/batch_statistics.png` | route distribution is fixture-designed |
| EP06 | 文字和商品事实应单独修复 | EXP-A/D | `assets/ep06/compare_board.png` | OCR/fact verification not run |
| EP07 | Skill -> Agent 是可观测的多阶段闭环 | EXP-D | `assets/ep07/batch_statistics.png`, manifests | production adapter remains blocked |

For each EP, the corresponding asset directory contains `key_takeaway.md` and `caption.txt`; before/after files are copied from the verified run outputs.
