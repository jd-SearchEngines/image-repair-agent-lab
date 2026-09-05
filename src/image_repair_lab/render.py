from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def _font(size=22):
    for path in ["/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def labeled(image, label):
    canvas = Image.new("RGB", (image.width, image.height + 44), "white")
    canvas.paste(image, (0, 44))
    ImageDraw.Draw(canvas).text((12, 10), label, fill=(20, 20, 20), font=_font())
    return canvas


def board(images, labels, path):
    tiles = [labeled(img.convert("RGB"), label) for img, label in zip(images, labels)]
    out = Image.new("RGB", (sum(i.width for i in tiles), max(i.height for i in tiles)), "white")
    x = 0
    for tile in tiles:
        out.paste(tile, (x, 0))
        x += tile.width
    out.save(path)


def save_mask(mask, path):
    mask.convert("L").save(path)


def stats_chart(stats, path):
    """Render a small dependency-free chart for content use."""
    width, height = 760, 420
    out = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(out)
    draw.text((28, 20), "EXP-D | Small Batch Repair Agent", fill=(20, 20, 20), font=_font(28))
    values = [("pass before", stats["pass_before"]), ("repaired", stats["repaired_successfully"]), ("still failed", stats["still_failed"])]
    colors = [(72, 140, 220), (70, 170, 105), (215, 90, 80)]
    max_value = max(1, stats["total_cases"])
    for i, ((label, value), color) in enumerate(zip(values, colors)):
        x = 70 + i * 225; bar_h = int(260 * value / max_value)
        draw.rectangle((x, 350 - bar_h, x + 130, 350), fill=color)
        draw.text((x, 365), label, fill=(30, 30, 30), font=_font(18))
        draw.text((x + 48, 325 - bar_h), str(value), fill=(30, 30, 30), font=_font(22))
    draw.text((28, 398), "Synthetic deterministic simulator; not model-quality evidence", fill=(110, 70, 30), font=_font(16))
    out.save(path)
