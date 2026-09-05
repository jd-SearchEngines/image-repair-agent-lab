# image-repair-agent-lab

一个面向内容生产的、可审计的图像修复 Agent 实验室。

核心闭环：

```text
Input Image -> Diagnose -> Error Classify -> Repair Route -> Repair -> Visual/Rule QA -> PASS/FAIL -> Reflection/Retry
```

## 这个项目解决什么问题？

AI 图片坏掉时，直接追加一句 prompt 往往会把正确区域一起改掉，也无法回答“哪里坏了、为什么这样修、修完是否通过”。本项目把诊断、路由、修复和 QA 拆成可记录的阶段，并为每一次运行保留输入、策略、输出和结果。

## 当前状态

第一阶段已在本地执行：A/B/C/D 四组 synthetic 最小实验均有 PNG、manifest、comparison board 和报告；REAL-EP03 用本地缓存的 Qwen Image Edit 真实跑了 3 个 case、6 个 treatment；同系列 P0 又锁定两张 Pexels Mother Image，并完成 EP02/EP05/EP06 各 1 次真实模型 canonical run。真实输出仍来自受控 mother image/variant，不能直接解释为生产质量；人工评审、OCR 与结构化 judge 尚未运行。见 [reports/project_status.md](reports/project_status.md)、[reports/real_model_gate_01.md](reports/real_model_gate_01.md) 和 [reports/skill_series_content_evidence.md](reports/skill_series_content_evidence.md)。

## 快速开始

```bash
python3 -m venv .venv
.venv/bin/pip install -e '.[dev]'
PYTHONPATH=src .venv/bin/python -m image_repair_lab.run_experiments --all
PYTHONPATH=src .venv/bin/python -m pytest -q
```

若环境已有 Pillow、NumPy、pytest，也可以直接省略 venv 并执行 `PYTHONPATH=src python3 ...`。运行后会在 `runs/EXP-A` 到 `runs/EXP-D` 写出图片和 JSON 证据。默认不会下载模型、不调用付费 API，也不会把网络图片当作本地证据。

## 实验入口

| 实验 | 问题 | 输出 |
|---|---|---|
| A | 一句 prompt vs Structured Repair Skill | 5 cases、三列对照板、诊断/策略/QA |
| B | Full regenerate vs Local Repair | 3 cases、mask、preserve score、无必要改动记录 |
| C | First repair vs Reflection / Second Pass | 3 cases、v1/v2、失败原因与反思 |
| D | Small Batch Repair Agent | 20 cases、路由分布、通过率、attempts 图表 |

最适合直接截图的入口是 [reports/content_evidence.md](reports/content_evidence.md) 和 [reports/series_asset_index.md](reports/series_asset_index.md)。

## 架构

- `src/image_repair_lab/diagnose.py`：从 case instruction 和 fixture metadata 形成结构化诊断。
- `src/image_repair_lab/routing.py`：把错误类别映射到 repair strategy。
- `src/image_repair_lab/repair.py`：deterministic simulator；仅用于可审计的 synthetic fixture，不宣称是模型。
- `src/image_repair_lab/qa.py`：区域修复分数、保留区域变化率、规则 QA。
- `src/image_repair_lab/render.py`：对照板、mask 和批量统计图。
- `src/image_repair_lab/run_experiments.py`：生成 fixtures 并运行 A/B/C/D。

详细说明见 [docs/architecture.md](docs/architecture.md)。

## 后续扩展

下一阶段应接入一个明确版本、权重来源和硬件要求均已记录的真实 image-edit model adapter；在真实模型 smoke test、人工盲评和成本/延迟记录通过前，不升级为“内容生产质量”或“模型优于 baseline”的结论。

## License

MIT，项目中的外部参考仅链接到其官方仓库，不复制外部代码或权重。
