import hashlib
import json
import urllib.request
from datetime import date
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
TODAY = str(date.today())
LICENSE_URL = "https://www.pexels.com/license/"
MOTHERS = {
    "product": {
        "pexels_photo_id": "8533212",
        "page_title": "Close Up shot of Cosmetic Product",
        "photographer": "Hanna Pad",
        "source_page_url": "https://www.pexels.com/photo/close-up-shot-of-cosmetic-product-8533212/",
        "download_url": "https://images.pexels.com/photos/8533212/pexels-photo-8533212.jpeg?cs=srgb&dl=pexels-anna-nekrashevich-8533212.jpg&fm=jpg",
    },
    "scene": {
        "pexels_photo_id": "4995025",
        "page_title": "Exterior of old cafe on street",
        "photographer": "Lisa Fotios",
        "source_page_url": "https://www.pexels.com/photo/exterior-of-old-cafe-on-street-4995025/",
        "download_url": "https://images.pexels.com/photos/4995025/pexels-photo-4995025.jpeg?cs=srgb&dl=pexels-fotios-photos-4995025.jpg&fm=jpg",
    },
}


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    for name, info in MOTHERS.items():
        dest = ROOT / "data" / "mother_cases" / name
        dest.mkdir(parents=True, exist_ok=True)
        original = dest / f"{name}_master_original.jpg"
        request = urllib.request.Request(info["download_url"], headers={"User-Agent": "Mozilla/5.0 image-repair-agent-lab/0.1"})
        with urllib.request.urlopen(request) as response, original.open("wb") as handle:
            handle.write(response.read())
        with Image.open(original) as image:
            original_size = list(image.size)
            canonical = ImageOps.fit(image.convert("RGB"), (1080, 1350), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
            canonical.save(dest / f"{name}_master_4x5.png")
        record = {
            **info,
            "source": "Pexels official page",
            "license_page": LICENSE_URL,
            "license_observed_on_source_page": "Free to use",
            "retrieval_date": TODAY,
            "original_path": str(original.relative_to(ROOT)),
            "canonical_path": str((dest / f"{name}_master_4x5.png").relative_to(ROOT)),
            "original_size": original_size,
            "canonical_size": [1080, 1350],
            "canonical_transform": "crop + resize only; no generative modification",
            "sha256": sha256(original),
        }
        (dest / "provenance.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "data" / "mother_cases" / "README.md").write_text("# Same-series mother images\n\nThese two Pexels images are the only canonical sources for the content series. See each family directory's `provenance.json`; canonical PNGs are 1080x1350 and use crop/resize only.\n")


if __name__ == "__main__":
    main()
