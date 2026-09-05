import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from image_repair_lab.providers import RealImageAdapter  # noqa: E402


def font(size):
    candidates = ["/System/Library/Fonts/STHeiti Light.ttc", "/System/Library/Fonts/Hiragino Sans GB.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf"]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def card(text, path, accent=(30, 70, 100)):
    image = Image.new("RGB", (1080, 420), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1080, 18), fill=accent)
    y = 54
    for line in text.splitlines():
        draw.text((54, y), line, fill=(25, 25, 25), font=font(30)); y += 48
    image.save(path)


def compare(before, after, path, skill):
    def labeled(source, label):
        canvas = Image.new("RGB", (1080, 1410), "white"); canvas.paste(ImageOps.fit(source.convert("RGB"), (1080, 1350)), (0, 60))
        ImageDraw.Draw(canvas).text((32, 16), label, fill=(15, 15, 15), font=font(34)); return canvas
    out = Image.new("RGB", (2160, 1410), "white")
    out.paste(labeled(before, "BEFORE"), (0, 0)); out.paste(labeled(after, "AFTER"), (1080, 0))
    ImageDraw.Draw(out).text((32, 1370), f"Qwen Image Edit | {skill} v1 | REAL RUN", fill=(80, 80, 80), font=font(20))
    out.save(path)


def make_text_variant():
    source = Image.open(ROOT / "data/mother_cases/product/product_master_4x5.png").convert("RGB")
    variant = source.copy(); draw = ImageDraw.Draw(variant)
    bbox = (150, 1040, 930, 1240)
    draw.rounded_rectangle(bbox, radius=24, fill=(250, 242, 225), outline=(120, 85, 55), width=5)
    draw.text((220, 1100), "秋季新口上市", fill=(40, 35, 30), font=font(66))
    out = ROOT / "data/controlled_variants"; out.mkdir(parents=True, exist_ok=True)
    variant.save(out / "product_text_before.png")
    (out / "product_text_ground_truth.json").write_text(json.dumps({"wrong_text": "秋季新口上市", "correct_text": "秋季新品上市", "text_bbox": list(bbox), "source": "deterministic PIL renderer", "input_type": "CONTROLLED_SYNTHETIC_TEST_VARIANT", "mother_case": "product_master_4x5.png"}, indent=2, ensure_ascii=False) + "\n")
    return out / "product_text_before.png"


CASES = [
    {"ep": "EP02", "family": "product", "skill": "Hero Product", "skill_path": "skills/hero_product/SKILL.md", "source": "data/mother_cases/product/product_master_4x5.png", "input_type": "PEXELS_CANONICAL_MOTHER_IMAGE", "prompt": "Turn this ordinary skincare product photo into a premium luxury studio advertisement. Improve studio lighting, controlled highlights, depth, and clean advertising background. Preserve the exact bottle silhouette, cap, proportions, physical product facts, and do not invent certification, ingredients, brand claims, or product text."},
    {"ep": "EP05", "family": "product", "skill": "Chinese Text Repair", "skill_path": "skills/text_repair/SKILL.md", "source": "data/controlled_variants/product_text_before.png", "input_type": "CONTROLLED_VARIANT_DERIVED_FROM_PEXELS_MOTHER", "prompt": "Correct only the Chinese promotion label from 秋季新口上市 to 秋季新品上市. Change only the text-safe label region. Preserve the exact product, bottle silhouette, background, layout, lighting, label geometry, and every unrelated pixel. Do not add claims."},
    {"ep": "EP06", "family": "scene", "skill": "Cinematic Scene", "skill_path": "skills/cinematic_scene/SKILL.md", "source": "data/mother_cases/scene/scene_master_4x5.png", "input_type": "PEXELS_CANONICAL_MOTHER_IMAGE", "prompt": "Transform this daytime old cafe street into a believable cinematic rainy evening scene with wet-road reflections, warm window light, restrained neon, and filmic contrast. Preserve the same storefront geometry, yellow door, windows, street perspective, and building identity; do not replace the building."},
]


def main():
    make_text_variant()
    adapter = RealImageAdapter(str(ROOT / ".real-model-venv/bin/mflux-generate-qwen-edit"), "/Users/jingdong/.cache/modelscope/qwen-image-edit-2511-8bit", steps=20, width=512, height=640)
    records = []
    for spec in CASES:
        run_dir = ROOT / "runs" / "skill_series" / spec["ep"]
        asset_dir = ROOT / "assets" / "skill_series" / spec["ep"].lower()
        run_dir.mkdir(parents=True, exist_ok=True); asset_dir.mkdir(parents=True, exist_ok=True)
        source = ROOT / spec["source"]
        before = Image.open(source).convert("RGB")
        model_input = ImageOps.fit(before, (512, 640), method=Image.Resampling.LANCZOS)
        model_input_path = run_dir / "model_input.png"; model_input.save(model_input_path)
        shutil.copy2(source, run_dir / "before.png")
        request = {"episode": spec["ep"], "family": spec["family"], "mother_case": "product_master_4x5.png" if spec["family"] == "product" else "scene_master_4x5.png", "input_path": str((run_dir / "before.png").relative_to(ROOT)), "input_type": spec["input_type"], "skill": spec["skill"], "skill_version": "v1", "skill_path": spec["skill_path"], "provider": adapter.provider, "model": adapter.model, "prompt": spec["prompt"], "attempt_budget": 3, "attempt": 1, "model_resolution": [512, 640], "content_resolution": [1080, 1350]}
        (run_dir / "request.json").write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n")
        result = adapter.edit(model_input_path, spec["prompt"], "skill_series", seed=7000 + len(records), output_path=run_dir / "model_output.png", metadata_dir=run_dir)
        (run_dir / "result.json").write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n")
        record = {"episode": spec["ep"], "skill": spec["skill"], "success": result.success, "attempts": 1, "run_dir": str(run_dir.relative_to(ROOT)), "skill_path": spec["skill_path"], "input_type": request["input_type"], "provider": adapter.provider, "model": adapter.model, "failed_attempts": [] if result.success else ["attempt_01"]}
        if result.success:
            after = Image.open(run_dir / "model_output.png").convert("RGB").resize((1080, 1350), Image.Resampling.LANCZOS)
            after.save(run_dir / "after.png")
            compare(before, after, run_dir / "compare_board.png", spec["skill"])
            compare(before, after, asset_dir / "compare_board.png", spec["skill"])
            shutil.copy2(run_dir / "before.png", asset_dir / "before.png"); shutil.copy2(run_dir / "after.png", asset_dir / "after.png")
        card(f"{spec['ep']}  |  {spec['skill']} v1\nModel: {adapter.model}\nProvider: {adapter.provider}\nAttempt: 01 / 03\nInput: controlled mother case", asset_dir / "run_card.png")
        card(Path(ROOT / spec["skill_path"]).read_text(), asset_dir / "skill_excerpt.png", accent=(100, 70, 35))
        (asset_dir / "content_notes.md").write_text(f"# {spec['ep']} {spec['skill']}\n\nReal model: `{adapter.model}` via `{adapter.provider}`.\n\nInput is a controlled mother image/variant, not a commercial ad asset. One canonical real attempt was run; raw metadata and result are in `runs/skill_series/{spec['ep']}/`. Human review and semantic judge were not run.\n\nDo not claim production lift or correctness from this output alone.\n")
        (asset_dir / "caption.md").write_text(f"同一套系列母图，{spec['skill']} v1，真实 Qwen Image Edit run。\n")
        records.append(record)
    (ROOT / "runs" / "skill_series" / "p0_manifest.json").write_text(json.dumps({"series": "AI修图 Skill 实验室", "gate": "P0", "same_model": adapter.model, "same_families": ["Product Master", "Scene Master"], "cases": records, "human_review": "NOT_RUN"}, indent=2, ensure_ascii=False) + "\n")
    status = [
        "# P0 same-series skill run",
        "",
        f"- Model: `{adapter.model}` via local `mflux` adapter",
        "- Input families: Pexels canonical Mother A/Product Master and Mother B/Scene Master; EP05 uses a controlled text variant derived from Mother A",
        "- Canonical output: one attempt per requested skill; human review is `NOT_RUN`",
        "",
    ]
    status.extend(f"- {r['episode']} {r['skill']}: {'PASS_EXECUTION' if r['success'] else 'FAIL'}; attempts={r['attempts']}" for r in records)
    status.extend(["", "All inputs are controlled mother images/variants. EP01/EP03/EP04/EP07 are `NOT_RUN` in this P0 stage. This is CONTENT DEMO / CONTROLLED EXPERIMENT evidence, not a benchmark or production-quality claim.", ""])
    (ROOT / "reports" / "p0_skill_series_status.md").write_text("\n".join(status))


if __name__ == "__main__":
    main()
