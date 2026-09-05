import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def make_split(before, after, path, skill):
    size = (1080, 1350)
    canvas = Image.new("RGB", (1080, 2700), "white")
    canvas.paste(ImageOps.fit(before.convert("RGB"), size), (0, 0)); canvas.paste(ImageOps.fit(after.convert("RGB"), size), (0, 1350))
    draw = ImageDraw.Draw(canvas); font = ImageFont.load_default()
    draw.rectangle((0, 0, 190, 34), fill="white"); draw.text((18, 12), "BEFORE", fill=(20, 20, 20), font=font)
    draw.rectangle((0, 1350, 190, 1384), fill="white"); draw.text((18, 1362), "AFTER", fill=(20, 20, 20), font=font)
    draw.text((18, 2670), f"Qwen Image Edit | {skill} v1 | REAL RUN", fill=(100, 100, 100), font=font)
    canvas.save(path)


def make_text_zoom(image, path):
    # The controlled variant declares this text region; keep the crop fixed so
    # before/after inspection is directly comparable and reproducible.
    crop = image.crop((100, 980, 980, 1280)).convert("RGB")
    crop.save(path)


def main():
    manifest = json.loads((ROOT / "runs/skill_series/p0_manifest.json").read_text())
    for row in manifest["cases"]:
        ep = row["episode"]; run_dir = ROOT / row["run_dir"]; asset_dir = ROOT / "assets" / "skill_series" / ep.lower()
        before = Image.open(run_dir / "before.png"); after = Image.open(run_dir / "after.png")
        make_split(before, after, run_dir / "split_vertical.png", row["skill"]); make_split(before, after, asset_dir / "split_vertical.png", row["skill"])
        if ep == "EP05":
            make_text_zoom(before, run_dir / "zoom_before.png")
            make_text_zoom(after, run_dir / "zoom_after.png")
            make_text_zoom(before, asset_dir / "zoom_before.png")
            make_text_zoom(after, asset_dir / "zoom_after.png")
        request = json.loads((run_dir / "request.json").read_text()); result = json.loads((run_dir / "result.json").read_text())
        (run_dir / "run.json").write_text(json.dumps({"episode": ep, "skill": row["skill"], "skill_version": "v1", "provider": row["provider"], "model": row["model"], "input_type": row["input_type"], "request": request, "result": result, "evidence_boundary": "REAL_MODEL_OUTPUT_ON_PEXELS_MOTHER_OR_CONTROLLED_VARIANT", "human_review": "NOT_RUN"}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
