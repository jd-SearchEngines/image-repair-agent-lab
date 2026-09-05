from pathlib import Path
from PIL import Image, ImageDraw


COLORS = [(232, 244, 255), (255, 240, 220), (238, 255, 232), (247, 235, 255)]
ISSUES = ["TEXT", "FACT", "LOCAL_DEFECT", "COMPOSITION", "BACKGROUND", "GLOBAL_FAILURE"]


def make_case(case_id, issue, index, root):
    w, h = 640, 400
    clean = Image.new("RGB", (w, h), COLORS[index % len(COLORS)])
    d = ImageDraw.Draw(clean)
    d.rounded_rectangle((145, 70, 495, 330), radius=28, fill=(35, 88, 120), outline=(15, 40, 60), width=6)
    d.ellipse((225, 105, 415, 295), fill=(245, 245, 235), outline=(15, 40, 60), width=5)
    d.rectangle((245, 180, 395, 235), fill=(250, 190, 55), outline=(110, 60, 10), width=4)
    d.text((278, 197), f"TEA-{index:02d}", fill=(50, 30, 5))
    d.text((20, 20), f"synthetic fixture {case_id}", fill=(25, 25, 25))
    bad = clean.copy()
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    if issue == "TEXT":
        d2 = ImageDraw.Draw(bad); d2.rectangle((245, 180, 395, 235), fill=(245, 90, 90)); d2.text((276, 197), "TEA-??", fill="white")
        md.rectangle((238, 174, 402, 241), fill=255)
    elif issue == "FACT":
        d2 = ImageDraw.Draw(bad); d2.rectangle((235, 170, 405, 245), fill=(55, 150, 80)); d2.text((270, 195), "COFFEE", fill="white")
        md.rectangle((228, 164, 412, 251), fill=255)
    elif issue == "LOCAL_DEFECT":
        d2 = ImageDraw.Draw(bad); d2.ellipse((330, 120, 390, 180), fill=(220, 40, 30)); d2.line((335, 125, 385, 175), fill="white", width=8)
        md.ellipse((320, 110, 400, 190), fill=255)
    elif issue == "COMPOSITION":
        d2 = ImageDraw.Draw(bad); d2.rectangle((0, 0, 120, 399), fill=(170, 50, 70)); d2.text((15, 190), "CROP", fill="white")
        md.rectangle((0, 0, 125, 399), fill=255)
    elif issue == "BACKGROUND":
        d2 = ImageDraw.Draw(bad); d2.rectangle((0, 0, 640, 55), fill=(55, 55, 55)); d2.text((20, 20), "WRONG BG", fill="white")
        md.rectangle((0, 0, 640, 62), fill=255)
    else:
        d2 = ImageDraw.Draw(bad); d2.rectangle((0, 0, 640, 400), fill=(110, 30, 90)); d2.text((230, 190), "GLOBAL FAILURE", fill="white")
        md.rectangle((0, 0, 640, 400), fill=255)
    case_dir = Path(root) / case_id
    case_dir.mkdir(parents=True, exist_ok=True)
    clean.save(case_dir / "clean.png"); bad.save(case_dir / "before.png"); mask.save(case_dir / "mask.png")
    return {"case_id": case_id, "source": "generated_controlled_fixture", "source_type": "synthetic", "instruction": f"Repair the {issue.lower()} issue while preserving all correct regions.", "expected_issue_type": issue, "preserve_constraints": ["preserve product silhouette", "preserve background outside defect", "preserve correct text and color"], "defect_bbox": list(mask.getbbox() or (0, 0, w, h)), "fixture_dir": str(Path("data/cases") / case_id), "output_files": ["before.png", "clean.png", "mask.png"], "run_id": "fixture_generation"}
