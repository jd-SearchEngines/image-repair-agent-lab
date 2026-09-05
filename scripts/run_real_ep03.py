import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from image_repair_lab.providers import RealImageAdapter  # noqa: E402


def vertical_board(images, labels, path, size=(512, 320)):
    from PIL import ImageDraw, ImageFont
    font = ImageFont.load_default()
    tiles = []
    for image, label in zip(images, labels):
        tile = ImageOps.fit(image.convert("RGB"), size)
        canvas = Image.new("RGB", (size[0], size[1] + 36), "white")
        canvas.paste(tile, (0, 36)); ImageDraw.Draw(canvas).text((12, 10), label, fill=(15, 15, 15), font=font)
        tiles.append(canvas)
    board = Image.new("RGB", (size[0], sum(t.height for t in tiles)), "white")
    y = 0
    for tile in tiles:
        board.paste(tile, (0, y)); y += tile.height
    board.save(path)


CASES = [
    ("case_02", "Remove only the small red scratch artifact near the top of the tea package. Preserve the product silhouette, background, label, colors, and composition everywhere else."),
    ("case_00", "Replace the incorrect product label text TEA-?? with TEA-00. Preserve the label geometry, product silhouette, background, colors, and all unrelated regions."),
    ("case_01", "Correct the wrong product fact on the label from COFFEE to TEA-01. Preserve the product identity, label geometry, background, colors, and all unrelated regions."),
]


def main():
    out_root = ROOT / "runs" / "REAL-EP03"
    asset_root = ROOT / "assets" / "ep03_real"
    out_root.mkdir(parents=True, exist_ok=True); asset_root.mkdir(parents=True, exist_ok=True)
    adapter = RealImageAdapter(
        executable=str(ROOT / ".real-model-venv" / "bin" / "mflux-generate-qwen-edit"),
        model_path="/Users/jingdong/.cache/modelscope/qwen-image-edit-2511-8bit",
        steps=20, width=512, height=320,
    )
    all_results = []
    for idx, (case_id, local_instruction) in enumerate(CASES, 1):
        case_src = ROOT / "data" / "cases" / case_id
        case_out = out_root / f"case_{idx:02d}"; case_out.mkdir(parents=True, exist_ok=True)
        before_path = case_out / "before.png"; mask_path = case_out / "mask.png"
        shutil.copy2(case_src / "before.png", before_path); shutil.copy2(case_src / "mask.png", mask_path)
        full_instruction = "Regenerate the entire image as a clean premium tea product image. " + local_instruction
        constraints = ["preserve product identity", "preserve layout", "preserve unrelated correct regions"]
        full = adapter.edit(before_path, full_instruction, "full_regenerate", seed=4100 + idx, output_path=case_out / "full_regen.png", metadata_dir=case_out)
        local = adapter.edit(before_path, local_instruction, "local_repair", mask=mask_path, preserve_constraints=constraints, seed=4200 + idx, output_path=case_out / "local_repair.png", metadata_dir=case_out)
        for result in (full, local):
            (case_out / ("full_result.json" if result.mode == "full_regenerate" else "local_result.json")).write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n")
        (case_out / "request.json").write_text(json.dumps({"case_id": case_id, "input_image": "CONTROLLED_SYNTHETIC_TEST_IMAGE", "provider": adapter.provider, "model": adapter.model, "full_instruction": full_instruction, "local_instruction": local_instruction, "mask_path": "mask.png", "mask_support_local": "MASK_NOT_SUPPORTED", "preserve_constraints": constraints}, indent=2, ensure_ascii=False) + "\n")
        (case_out / "notes.md").write_text(f"# REAL-EP03 case {idx:02d}\n\nInput: `CONTROLLED_SYNTHETIC_TEST_IMAGE` from `{case_id}`.\n\nProvider outputs are real local Qwen/MFlux executions. The local treatment used instruction-based local editing because the installed CLI does not support an explicit mask; this is recorded as `MASK_NOT_SUPPORTED`.\n\nHuman review: not performed in this run.\n")
        valid = [Image.open(before_path), Image.open(case_out / "full_regen.png"), Image.open(case_out / "local_repair.png")]
        vertical_board(valid, ["BEFORE", "FULL REGENERATE", "LOCAL REPAIR"], case_out / "comparison_board.png")
        all_results.append({"case_id": case_id, "case_dir": str(case_out.relative_to(ROOT)), "full": full.to_dict(), "local": local.to_dict(), "comparison_board": str((case_out / "comparison_board.png").relative_to(ROOT)), "evidence_boundary": "REAL_MODEL_OUTPUT_ON_CONTROLLED_SYNTHETIC_INPUT"})
    (out_root / "manifest.json").write_text(json.dumps({"gate": "REAL_MODEL_GATE_01", "provider": adapter.provider, "model": adapter.model, "model_path": adapter.model_path, "steps": adapter.steps, "resolution": [adapter.width, adapter.height], "cases": all_results, "human_review": "NOT_RUN", "simulator_mixing": "NONE"}, indent=2, ensure_ascii=False) + "\n")
    best = all_results[0]
    for source, name in [("comparison_board.png", "hero_case_01_board.png"), ("before.png", "best_before.png"), ("full_regen.png", "best_full_regen.png"), ("local_repair.png", "best_local_repair.png"), ("mask.png", "best_mask.png")]:
        shutil.copy2(out_root / "case_01" / source, asset_root / name)
    (asset_root / "content_notes.md").write_text("# EP03 real-model content notes\n\nThis pack contains three real local Qwen Image Edit outputs generated from controlled synthetic inputs. It is not a benchmark and has no human quality score.\n\n- Cover candidate: `hero_case_01_board.png` (local defect case; the before/after question is immediately legible).\n- Largest visual difference: to be decided after human review; do not infer from file existence or model self-report.\n- Full Regenerate risk: assess whether product identity, layout, label, or background changed outside the issue.\n- Local Repair: the model received a local-edit instruction, but explicit masks are unsupported by this MFlux CLI, so preservation is unverified.\n- Publicly safe: the pipeline called a real local model on controlled synthetic inputs and preserved raw metadata.\n- Not publicly safe yet: claims that Local Repair is better, text is correct, or quality improved by a percentage.\n")
    (asset_root / "hero_case_01_caption.txt").write_text("Real Qwen Image Edit on a controlled synthetic input: BEFORE / FULL REGENERATE / LOCAL REPAIR. Explicit mask unsupported by the installed CLI; preservation awaits human review.\n")


if __name__ == "__main__":
    main()
