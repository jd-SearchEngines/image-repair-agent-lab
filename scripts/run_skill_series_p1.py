import json
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from image_repair_lab.providers import RealImageAdapter  # noqa: E402


def font(size):
    candidates = [
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
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
        draw.text((54, y), line, fill=(25, 25, 25), font=font(30))
        y += 48
    image.save(path)


def compare(before, after, path, skill):
    def labeled(source, label):
        canvas = Image.new("RGB", (1080, 1410), "white")
        canvas.paste(ImageOps.fit(source.convert("RGB"), (1080, 1350)), (0, 60))
        ImageDraw.Draw(canvas).text((32, 16), label, fill=(15, 15, 15), font=font(34))
        return canvas

    out = Image.new("RGB", (2160, 1410), "white")
    out.paste(labeled(before, "BEFORE"), (0, 0))
    out.paste(labeled(after, "AFTER"), (1080, 0))
    ImageDraw.Draw(out).text(
        (32, 1370),
        f"Real Qwen Image Edit | {skill} v1 | Controlled Content Experiment",
        fill=(80, 80, 80),
        font=font(20),
    )
    out.save(path)


def split_vertical(before, after, path, skill):
    size = (1080, 1350)
    out = Image.new("RGB", (1080, 2700), "white")
    out.paste(ImageOps.fit(before.convert("RGB"), size), (0, 0))
    out.paste(ImageOps.fit(after.convert("RGB"), size), (0, 1350))
    draw = ImageDraw.Draw(out)
    draw.rectangle((0, 0, 190, 38), fill="white")
    draw.text((18, 12), "BEFORE", fill=(20, 20, 20), font=font(24))
    draw.rectangle((0, 1350, 190, 1388), fill="white")
    draw.text((18, 1362), "AFTER", fill=(20, 20, 20), font=font(24))
    draw.text((18, 2668), f"Real Qwen Image Edit | {skill} v1 | Controlled Content Experiment", fill=(100, 100, 100), font=font(20))
    out.save(path)


def make_clutter_variant():
    source = Image.open(ROOT / "data/mother_cases/product/product_master_4x5.png").convert("RGB")
    image = source.copy()
    draw = ImageDraw.Draw(image)
    elements = [
        {"name": "loose charging cable", "bbox": [55, 950, 345, 1260], "approximate_region": "lower-left beside bottle", "source": "deterministic PIL line/ellipse composition", "color": "dark graphite"},
        {"name": "small paper card", "bbox": [55, 680, 300, 885], "approximate_region": "upper-left beside bottle", "source": "deterministic PIL polygon composition", "color": "cream paper with blue lines"},
        {"name": "small cup", "bbox": [805, 970, 1015, 1235], "approximate_region": "lower-right beside bottle", "source": "deterministic PIL ellipse/rectangle composition", "color": "muted teal"},
        {"name": "packaging fragment", "bbox": [755, 700, 1015, 910], "approximate_region": "upper-right beside bottle", "source": "deterministic PIL polygon composition", "color": "ochre cardboard"},
    ]

    # Cable: it approaches but never crosses the bottle silhouette.
    cable = [(70, 1230), (115, 1160), (92, 1090), (165, 1030), (235, 1050), (325, 990)]
    draw.line(cable, fill=(34, 38, 42), width=18, joint="curve")
    draw.line(cable, fill=(112, 118, 122), width=5, joint="curve")
    draw.ellipse((302, 970, 342, 1010), fill=(26, 28, 30), outline=(160, 160, 160), width=4)

    # Paper card.
    draw.polygon([(72, 710), (260, 688), (286, 842), (98, 870)], fill=(244, 238, 220), outline=(95, 110, 130))
    for y in (735, 770, 805):
        draw.line((105, y, 245, y - 14), fill=(106, 137, 168), width=4)

    # Cup.
    draw.ellipse((825, 985, 995, 1050), fill=(67, 105, 107), outline=(35, 52, 54), width=5)
    draw.rectangle((825, 1015, 995, 1165), fill=(80, 118, 120), outline=(35, 52, 54), width=5)
    draw.ellipse((825, 1125, 995, 1190), fill=(68, 101, 103), outline=(35, 52, 54), width=5)
    draw.arc((965, 1030, 1050, 1135), 270, 90, fill=(35, 52, 54), width=12)

    # Packaging fragment.
    draw.polygon([(770, 760), (965, 730), (1010, 855), (808, 900)], fill=(185, 135, 65), outline=(105, 70, 35))
    draw.line((800, 800, 972, 775), fill=(246, 220, 160), width=12)
    draw.line((815, 835, 985, 810), fill=(112, 75, 40), width=8)

    out = ROOT / "data/controlled_variants"
    out.mkdir(parents=True, exist_ok=True)
    variant_path = out / "product_cluttered_before.png"
    image.save(variant_path)
    (out / "clutter_manifest.json").write_text(json.dumps({
        "source_mother": "data/mother_cases/product/product_master_4x5.png",
        "variant_path": "data/controlled_variants/product_cluttered_before.png",
        "input_type": "CONTROLLED_DETERMINISTIC_VARIANT_DERIVED_FROM_PEXELS_MOTHER",
        "method": "PIL deterministic composition; no generative model used to create the defect",
        "elements": elements,
    }, indent=2, ensure_ascii=False) + "\n")
    map_image = image.copy()
    map_draw = ImageDraw.Draw(map_image)
    for index, element in enumerate(elements, 1):
        bbox = tuple(element["bbox"])
        map_draw.rectangle(bbox, outline=(220, 30, 30), width=6)
        map_draw.text((bbox[0] + 8, bbox[1] + 8), f"{index}: {element['name']}", fill=(180, 20, 20), font=font(24))
    (ROOT / "runs/skill_series/EP03").mkdir(parents=True, exist_ok=True)
    map_image.save(ROOT / "runs/skill_series/EP03/clutter_map.png")
    return variant_path, elements


def make_defect_variant():
    source = Image.open(ROOT / "data/mother_cases/product/product_master_4x5.png").convert("RGB")
    image = source.copy()
    scratch = [(520, 735), (545, 710), (566, 740), (592, 716), (615, 746)]
    ImageDraw.Draw(image).line(scratch, fill=(218, 25, 32), width=14, joint="curve")
    ImageDraw.Draw(image).line([(528, 735), (550, 720), (570, 746), (600, 725)], fill=(255, 112, 112), width=4, joint="curve")
    out = ROOT / "data/controlled_variants"
    out.mkdir(parents=True, exist_ok=True)
    variant_path = out / "product_defect_before.png"
    image.save(variant_path)
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).line(scratch, fill=255, width=36, joint="curve")
    mask_path = out / "defect_mask.png"
    mask.save(mask_path)
    bbox = [500, 690, 635, 770]
    (out / "defect_bbox.json").write_text(json.dumps({
        "source_mother": "data/mother_cases/product/product_master_4x5.png",
        "variant_path": "data/controlled_variants/product_defect_before.png",
        "mask_path": "data/controlled_variants/defect_mask.png",
        "input_type": "CONTROLLED_DETERMINISTIC_VARIANT_DERIVED_FROM_PEXELS_MOTHER",
        "defect": "single red scratch on bottle body",
        "bbox": bbox,
        "method": "PIL deterministic renderer; model did not create the defect",
    }, indent=2, ensure_ascii=False) + "\n")
    return variant_path, mask_path, bbox


CASES = [
    {
        "ep": "EP01",
        "family": "scene",
        "skill": "Vintage Poster",
        "skill_path": "skills/vintage_poster/SKILL.md",
        "source": "data/mother_cases/scene/scene_master_4x5.png",
        "input_type": "PEXELS_CANONICAL_MOTHER_IMAGE",
        "prompt": "Convert this exact old cafe street photograph into a vintage travel poster. Keep the same cafe/storefront identity, yellow door, windows, main geometry, and perspective. Apply a faded warm palette, aged print texture, film grain, retro poster hierarchy, and screen-print lithograph feeling. Use no complex Chinese text; preferably add no text at all. Do not replace or redesign the building.",
    },
    {
        "ep": "EP03",
        "family": "product",
        "skill": "Background Cleanup",
        "skill_path": "skills/background_cleanup/SKILL.md",
        "source": "data/controlled_variants/product_cluttered_before.png",
        "input_type": "CONTROLLED_DETERMINISTIC_VARIANT_DERIVED_FROM_PEXELS_MOTHER",
        "prompt": "Remove only the four distracting objects around the skincare product: loose charging cable, small paper card, small cup, and packaging fragment. Keep the exact bottle, bottle position, cap, label, lighting, background character, and framing unchanged. Do not redesign the product or invent any text.",
    },
    {
        "ep": "EP04",
        "family": "product",
        "skill": "Local Repair",
        "skill_path": "skills/local_repair/SKILL.md",
        "source": "data/controlled_variants/product_defect_before.png",
        "input_type": "CONTROLLED_DETERMINISTIC_VARIANT_DERIVED_FROM_PEXELS_MOTHER",
        "prompt": "Remove only the single declared red scratch on the bottle body. Preserve the bottle silhouette, cap, label, product position, background, lighting, and every unrelated region. Do not change any other object or add text. The reference mask identifies the repair region, but the installed MFlux interface may not support an explicit mask argument.",
        "mode": "local_repair",
    },
]


def copy_if_exists(source, destinations):
    for destination in destinations:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def diff_map(before, after, path):
    diff = ImageChops.difference(before.convert("RGB"), after.convert("RGB"))
    gray = ImageEnhance.Contrast(diff.convert("L")).enhance(4.0)
    ImageOps.colorize(gray, black=(8, 8, 8), white=(240, 35, 35)).save(path)


def mask_change_proxy(before, after, mask):
    before_array = np.asarray(before.convert("RGB"), dtype=np.float32)
    after_array = np.asarray(after.convert("RGB"), dtype=np.float32)
    diff = np.abs(before_array - after_array).mean(axis=2) / 255.0
    mask_array = np.asarray(mask.convert("L")) > 0
    inside = float(diff[mask_array].mean()) if mask_array.any() else None
    outside = float(diff[~mask_array].mean()) if (~mask_array).any() else None
    return {"inside_mask_change": inside, "outside_mask_change_proxy": outside, "interpretation": "mean RGB delta proxy only; not a quality score"}


def run_case(adapter, spec, source_path, mask_path=None, extra=None):
    ep = spec["ep"]
    run_dir = ROOT / "runs/skill_series" / ep
    asset_dir = ROOT / "assets/skill_series" / ep.lower()
    run_dir.mkdir(parents=True, exist_ok=True)
    asset_dir.mkdir(parents=True, exist_ok=True)
    before = Image.open(source_path).convert("RGB")
    before.save(run_dir / "before.png")
    before.save(asset_dir / "before.png")
    attempts = []
    best = None
    for attempt in (1, 2):
        attempt_dir = run_dir / f"attempt_{attempt:02d}"
        attempt_dir.mkdir(parents=True, exist_ok=True)
        model_input = ImageOps.fit(before, (512, 640), method=Image.Resampling.LANCZOS)
        model_input_path = attempt_dir / "model_input.png"
        model_input.save(model_input_path)
        request = {
            "episode": ep,
            "family": spec["family"],
            "mother_case": "scene_master_4x5.png" if spec["family"] == "scene" else "product_master_4x5.png",
            "input_path": str((run_dir / "before.png").relative_to(ROOT)),
            "input_type": spec["input_type"],
            "skill": spec["skill"],
            "skill_version": "v1",
            "skill_path": spec["skill_path"],
            "provider": adapter.provider,
            "model": adapter.model,
            "prompt": spec["prompt"],
            "attempt_budget": 2,
            "attempt": attempt,
            "model_resolution": [512, 640],
            "content_resolution": [1080, 1350],
            "mask_reference": str(mask_path.relative_to(ROOT)) if mask_path else None,
        }
        (attempt_dir / "request.json").write_text(json.dumps(request, indent=2, ensure_ascii=False) + "\n")
        result = adapter.edit(
            model_input_path,
            spec["prompt"],
            spec.get("mode", "skill_series"),
            mask=mask_path,
            preserve_constraints=["declared repair region only", "preserve unrelated image content"],
            seed=7100 + len(attempts),
            output_path=attempt_dir / "model_output.png",
            metadata_dir=attempt_dir,
        )
        (attempt_dir / "result.json").write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n")
        item = {"attempt": attempt, "success": result.success, "attempt_dir": str(attempt_dir.relative_to(ROOT)), "result": result.to_dict()}
        attempts.append(item)
        if result.success:
            best = item
            break

    record = {
        "episode": ep,
        "skill": spec["skill"],
        "skill_version": "v1",
        "input_type": spec["input_type"],
        "provider": adapter.provider,
        "model": adapter.model,
        "success": bool(best),
        "attempts": len(attempts),
        "failed_attempts": [f"attempt_{x['attempt']:02d}" for x in attempts if not x["success"]],
        "best_attempt": f"attempt_{best['attempt']:02d}" if best else None,
        "human_review": "NOT_RUN",
        "evidence_boundary": "REAL_MODEL_OUTPUT_ON_PEXELS_MOTHER_OR_CONTROLLED_VARIANT",
    }
    if best:
        after = Image.open(run_dir / f"attempt_{best['attempt']:02d}/model_output.png").convert("RGB").resize((1080, 1350), Image.Resampling.LANCZOS)
        after.save(run_dir / "model_output.png")
        after.save(run_dir / "after.png")
        after.save(asset_dir / "after.png")
        compare(before, after, run_dir / "compare_board.png", spec["skill"])
        compare(before, after, asset_dir / "compare_board.png", spec["skill"])
        split_vertical(before, after, run_dir / "split_vertical.png", spec["skill"])
        split_vertical(before, after, asset_dir / "split_vertical.png", spec["skill"])
        if mask_path:
            metrics = mask_change_proxy(before, after, Image.open(mask_path))
            record["mask_support"] = "MASK_NOT_SUPPORTED"
            record["mask_change_proxy"] = metrics
            diff_map(before, after, run_dir / "diff_map.png")
            copy_if_exists(run_dir / "diff_map.png", [asset_dir / "diff_map.png"])
        else:
            record["mask_support"] = "NOT_APPLICABLE"
    else:
        record["mask_support"] = "MASK_NOT_SUPPORTED" if mask_path else "NOT_APPLICABLE"
    (run_dir / "run.json").write_text(json.dumps({**record, "attempt_records": attempts, "extra": extra or {}}, indent=2, ensure_ascii=False) + "\n")
    card(f"{ep} | {spec['skill']} v1\nModel: {adapter.model}\nProvider: {adapter.provider}\nAttempts: {len(attempts)} / 02\nInput: {spec['input_type']}", asset_dir / "run_card.png")
    card(Path(ROOT / spec["skill_path"]).read_text(), asset_dir / "skill_excerpt.png", accent=(100, 70, 35))
    (asset_dir / "content_notes.md").write_text(
        f"# {ep} {spec['skill']}\n\nReal model: `{adapter.model}` via `{adapter.provider}`.\n\nInput: `{spec['input_type']}`. Attempts recorded: `{len(attempts)}`; failed attempts: `{record['failed_attempts'] or 'none'}`. Human review and semantic judge were not run.\n\nThis is controlled content evidence, not a production-quality or uplift claim.\n"
    )
    (asset_dir / "caption.md").write_text(f"同一套系列母图，{spec['skill']} v1，真实 Qwen Image Edit run。\n")
    return record


def main():
    adapter = RealImageAdapter(
        str(ROOT / ".real-model-venv/bin/mflux-generate-qwen-edit"),
        "/Users/jingdong/.cache/modelscope/qwen-image-edit-2511-8bit",
        steps=20,
        width=512,
        height=640,
    )
    clutter_source, clutter_elements = make_clutter_variant()
    defect_source, defect_mask, defect_bbox = make_defect_variant()
    # These maps are generated after the run directory exists; copy the
    # deterministic source artifacts into the auditable episode directories.
    (ROOT / "runs/skill_series/EP03").mkdir(parents=True, exist_ok=True)
    (ROOT / "runs/skill_series/EP04").mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "data/controlled_variants/clutter_manifest.json", ROOT / "runs/skill_series/EP03/clutter_manifest.json")
    shutil.copy2(ROOT / "data/controlled_variants/product_cluttered_before.png", ROOT / "runs/skill_series/EP03/product_cluttered_before.png")
    shutil.copy2(ROOT / "data/controlled_variants/defect_bbox.json", ROOT / "runs/skill_series/EP04/defect_bbox.json")
    shutil.copy2(ROOT / "data/controlled_variants/product_defect_before.png", ROOT / "runs/skill_series/EP04/product_defect_before.png")
    shutil.copy2(ROOT / "data/controlled_variants/defect_mask.png", ROOT / "runs/skill_series/EP04/defect_mask.png")

    records = []
    for spec in CASES:
        if spec["ep"] == "EP01":
            source = ROOT / spec["source"]
            extra = {"mother": "Mother B / Scene Master"}
            records.append(run_case(adapter, spec, source, extra=extra))
        elif spec["ep"] == "EP03":
            extra = {"mother": "Mother A / Product Master", "clutter_elements": clutter_elements}
            records.append(run_case(adapter, spec, clutter_source, extra=extra))
            copy_if_exists(ROOT / "runs/skill_series/EP03/clutter_map.png", [ROOT / "assets/skill_series/ep03/clutter_map.png"])
            copy_if_exists(ROOT / "runs/skill_series/EP03/clutter_manifest.json", [ROOT / "assets/skill_series/ep03/clutter_manifest.json"])
        else:
            extra = {"mother": "Mother A / Product Master", "defect": "single red scratch", "defect_bbox": defect_bbox}
            records.append(run_case(adapter, spec, defect_source, mask_path=defect_mask, extra=extra))
            copy_if_exists(ROOT / "runs/skill_series/EP04/defect_bbox.json", [ROOT / "assets/skill_series/ep04/defect_bbox.json"])
            copy_if_exists(ROOT / "runs/skill_series/EP04/defect_mask.png", [ROOT / "assets/skill_series/ep04/mask.png"])
            copy_if_exists(ROOT / "runs/skill_series/EP04/product_defect_before.png", [ROOT / "assets/skill_series/ep04/product_defect_before.png"])
    manifest = {"series": "AI修图 Skill 实验室", "gate": "P1", "same_model": adapter.model, "cases": records, "p0_untouched": True, "human_review": "NOT_RUN"}
    (ROOT / "runs/skill_series/p1_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    lines = ["# P1 same-series skill run", "", f"- Model: `{adapter.model}` via local MFlux", "- EP02/EP05/EP06 were not rerun.", ""]
    lines.extend(f"- {r['episode']} {r['skill']}: {'PASS_EXECUTION' if r['success'] else 'FAIL_EXECUTION'}; attempts={r['attempts']}; failed={r['failed_attempts'] or 'none'}" for r in records)
    lines.extend(["", "Human review, OCR, and semantic/structural judge remain `NOT_RUN`. This is controlled content evidence, not a benchmark.", ""])
    (ROOT / "reports/p1_skill_series_status.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
