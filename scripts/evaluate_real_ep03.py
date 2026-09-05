import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def proxy_metrics(before_path, truth_path, mask_path, output_path):
    before = Image.open(before_path).convert("RGB")
    truth = Image.open(truth_path).convert("RGB").resize(Image.open(output_path).size)
    output = Image.open(output_path).convert("RGB")
    mask = Image.open(mask_path).convert("L").resize(output.size, Image.Resampling.NEAREST)
    a = np.asarray(before.resize(output.size)).astype(float)
    b = np.asarray(output).astype(float)
    t = np.asarray(truth).astype(float)
    m = np.asarray(mask) > 127
    delta = np.abs(a - b).mean(axis=2)
    target_error = np.abs(t - b).mean(axis=2)
    outside = ~m
    return {
        "rule_judge": "PIXEL_PROXY_ONLY_NOT_SEMANTIC",
        "target_issue_fixed": "UNVERIFIED_NO_OCR_OR_VLM",
        "target_region_similarity_to_declared_clean_fixture": round(float(1 - target_error[m].mean() / 255), 4) if m.any() else None,
        "unrelated_region_changed": round(float((delta[outside] > 8).mean()), 4) if outside.any() else None,
        "product_identity_preserved": "UNVERIFIED_MANUAL_REVIEW_REQUIRED",
        "layout_preserved": "UNVERIFIED_MANUAL_REVIEW_REQUIRED",
        "text_preserved": "UNVERIFIED_OCR_NOT_RUN",
        "obvious_new_artifact": "MANUAL_REVIEW_REQUIRED",
    }


def main():
    run_root = ROOT / "runs" / "REAL-EP03"
    report_rows = []
    for case_dir in sorted(p for p in run_root.iterdir() if p.is_dir()):
        case_id = json.loads((case_dir / "request.json").read_text())["case_id"]
        source_dir = ROOT / "data" / "cases" / case_id
        full_result = json.loads((case_dir / "full_result.json").read_text())
        local_result = json.loads((case_dir / "local_result.json").read_text())
        full_metrics = proxy_metrics(case_dir / "before.png", source_dir / "clean.png", case_dir / "mask.png", case_dir / "full_regen.png")
        local_metrics = proxy_metrics(case_dir / "before.png", source_dir / "clean.png", case_dir / "mask.png", case_dir / "local_repair.png")
        result = {"case_id": case_id, "evidence_boundary": "REAL_MODEL_OUTPUT_ON_CONTROLLED_SYNTHETIC_INPUT", "full_regenerate": {"provider_result": full_result, "evaluation": full_metrics}, "local_repair": {"provider_result": local_result, "evaluation": local_metrics}, "human_review": "NOT_RUN"}
        (case_dir / "result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
        report_rows.append(result)
    report = ["# REAL_MODEL_GATE_01", "", "**Status: PASS (execution/provenance gate only; not a quality win).**", "", "- Provider: `local-mflux`", "- Model: `mlx-community/qwen-image-edit-2511-8bit`", "- Runtime: MFlux 0.19.1 / MLX 0.32.2 / Apple M3 Max / 64 GiB", "- Treatments: 3 cases x Full Regenerate + Local Repair = 6 real provider calls", "- Input boundary: all inputs are `CONTROLLED_SYNTHETIC_TEST_IMAGE`", "- Local mask boundary: `MASK_NOT_SUPPORTED`; the installed Qwen/MFlux CLI accepts image conditioning but no explicit mask flag", "- Human review: `NOT_RUN`; review sheet is intentionally blank", "- Simulator mixing: `NONE`; historical EXP-A/B/C/D files were not modified", "", "## Case evidence", ""]
    for row in report_rows:
        report += [f"### {row['case_id']}", "", f"- Full result: `{row['full_regenerate']['provider_result']['output_path']}`", f"- Local result: `{row['local_repair']['provider_result']['output_path']}`", f"- Full unrelated-region change proxy: `{row['full_regenerate']['evaluation']['unrelated_region_changed']}`", f"- Local unrelated-region change proxy: `{row['local_repair']['evaluation']['unrelated_region_changed']}`", "- Semantic target/text/product/layout fields: unverified; see `result.json`.", ""]
    report += ["## Interpretation boundary", "", "The real model executed and produced inspectable outputs, but the local instruction path did not enforce a mask and OCR/VLM/human review was not run. The evidence supports saying that a real model was exercised on controlled inputs; it does not support saying Local Repair is better, text is correct, or preservation improved by a percentage.", ""]
    (ROOT / "reports" / "real_model_gate_01.md").write_text("\n".join(report))
    (ROOT / "assets" / "ep03_real" / "content_notes.md").write_text("# EP03 real-model content notes\n\n## What this pack supports\n\n- Cover candidate: `hero_case_01_board.png`; the local-defect problem is immediately legible.\n- All three boards show real Qwen Image Edit outputs from the same controlled synthetic inputs.\n- Full Regenerate visibly reconstructs more of the image; Local Repair also changed unrelated text/header pixels in this run.\n\n## What the evidence says\n\n- The strongest honest observation is not that Local Repair won. It is that a real instruction-based edit can remove or alter a local visual issue while still damaging unrelated text and metadata-like regions.\n- `MASK_NOT_SUPPORTED` is a central caveat: the installed Qwen/MFlux CLI did not accept an explicit mask, so the Local Repair treatment is instruction-based only.\n- The rule proxy fields are in each `runs/REAL-EP03/*/result.json`; they are pixel proxies against a declared clean synthetic fixture, not semantic or human scores.\n\n## Public wording\n\nSafe: “我们用真实 Qwen Image Edit 跑了三个受控测试，并保留了 before / full / local / request / raw metadata 证据。”\n\nNot safe yet: “Local Repair 一定更好”“文字已正确”“保留率提升 X%”“模型达到生产质量”。人工审核、OCR/VLM judge 和显式 mask provider 仍未完成。\n")


if __name__ == "__main__":
    main()
