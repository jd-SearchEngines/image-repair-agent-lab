import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
MODEL = Path("/Users/jingdong/.cache/modelscope/Qwen-Image-Edit-2511")
PYTHON_ENV = Path("/Users/jingdong/Downloads/Google_image/qa_judge_dpo/.venvs/sft-bench-hf")
INPUT = ROOT / "data/controlled_variants/product_defect_before.png"
MASK = ROOT / "data/controlled_variants/defect_mask.png"
RUN = ROOT / "runs/skill_series/EP04/backend_smoke_qwen_diffusers"
ASSET = ROOT / "assets/skill_series/ep04"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def font(size):
    for candidate in (
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def comparison(before, after, path):
    size = (1080, 1350)
    board = Image.new("RGB", (2160, 1410), "white")
    for x, image, label in ((0, before, "BEFORE"), (1080, after, "MASKED INPAINT SMOKE")):
        fitted = ImageOps.fit(image.convert("RGB"), size)
        board.paste(fitted, (x, 60))
        ImageDraw.Draw(board).text((x + 30, 17), label, fill=(15, 15, 15), font=font(32))
    ImageDraw.Draw(board).text((30, 1370), "EP04 | Qwen Diffusers explicit-mask backend smoke | not content promotion", fill=(80, 80, 80), font=font(20))
    board.save(path)


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    ASSET.mkdir(parents=True, exist_ok=True)
    started = time.time()
    metadata = {
        "episode": "EP04",
        "status": "RUNNING",
        "backend": "QWEN_DIFFUSERS_INPAINT_PIPELINE",
        "pipeline": "diffusers.QwenImageEditInpaintPipeline",
        "model_path": str(MODEL),
        "python_environment": str(PYTHON_ENV),
        "input": str(INPUT.relative_to(ROOT)),
        "mask": str(MASK.relative_to(ROOT)),
        "mask_semantics": "white pixels are repainted; black pixels are preserved",
        "input_sha256": sha256(INPUT),
        "mask_sha256": sha256(MASK),
        "parameters": {
            "prompt": "Remove only the single red scratch inside the provided mask. Preserve the bottle silhouette, cap, label, product position, background, lighting, and every unrelated region. Do not add text or objects.",
            "height": 512,
            "width": 640,
            "num_inference_steps": 8,
            "true_cfg_scale": 4.0,
            "strength": 0.9,
            "seed": 8804,
        },
        "cost": None,
        "started_at_epoch": started,
    }
    (RUN / "request.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    try:
        import diffusers
        import torch

        metadata["versions"] = {"diffusers": diffusers.__version__, "torch": torch.__version__}
        if not torch.backends.mps.is_available():
            raise RuntimeError("MPS is unavailable in the selected environment")
        from diffusers import QwenImageEditInpaintPipeline

        metadata["device"] = "mps"
        load_started = time.time()
        pipe = QwenImageEditInpaintPipeline.from_pretrained(
            str(MODEL),
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True,
        )
        metadata["load_seconds"] = round(time.time() - load_started, 3)
        pipe.to("mps")
        source = Image.open(INPUT).convert("RGB")
        mask = Image.open(MASK).convert("L")
        output_started = time.time()
        generator = torch.Generator(device="cpu").manual_seed(8804)
        result = pipe(
            image=source,
            mask_image=mask,
            prompt=metadata["parameters"]["prompt"],
            height=512,
            width=640,
            num_inference_steps=8,
            true_cfg_scale=4.0,
            strength=0.9,
            generator=generator,
        )
        output = result.images[0].convert("RGB")
        metadata["inference_seconds"] = round(time.time() - output_started, 3)
        output.save(RUN / "model_output_512x640.png")
        final = output.resize((1080, 1350), Image.Resampling.LANCZOS)
        final.save(RUN / "after.png")
        final.save(ASSET / "backend_smoke_after.png")
        comparison(source, final, RUN / "compare_board.png")
        comparison(source, final, ASSET / "backend_smoke_compare_board.png")
        metadata["status"] = "PASS"
        metadata["success"] = True
        metadata["output"] = str((RUN / "after.png").relative_to(ROOT))
    except Exception as exc:
        metadata["status"] = "LOCAL_REPAIR_BACKEND_BLOCKED"
        metadata["success"] = False
        metadata["error_type"] = type(exc).__name__
        metadata["error"] = str(exc)
        metadata["traceback"] = traceback.format_exc()
    metadata["elapsed_seconds"] = round(time.time() - started, 3)
    (RUN / "result.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({k: metadata.get(k) for k in ("status", "success", "error_type", "error", "elapsed_seconds", "output")}, ensure_ascii=False))
    return 0 if metadata["success"] else 2


if __name__ == "__main__":
    sys.exit(main())
