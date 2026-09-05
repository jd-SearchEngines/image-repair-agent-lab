from PIL import Image, ImageDraw, ImageFilter, ImageEnhance


def _paste_truth(image, truth, mask, partial=False):
    if partial:
        mask = mask.filter(ImageFilter.GaussianBlur(7))
        mask = mask.point(lambda p: min(p, 150))
    return Image.composite(truth, image, mask)


def repair(image, truth, mask, strategy, attempt=1):
    """Run the bounded local simulator.

    The simulator uses a known clean target only to construct controlled
    synthetic fixtures. It is not a model and is never presented as one.
    """
    if strategy == "full_regenerate_review":
        out = truth.copy()
        overlay = Image.new("RGBA", out.size, (255, 255, 255, 0))
        ImageDraw.Draw(overlay).rectangle((0, 0, out.width - 1, out.height - 1), outline=(255, 90, 40, 90), width=5)
        return Image.alpha_composite(out.convert("RGBA"), overlay).convert("RGB")
    if strategy == "composition_reframe":
        return ImageEnhance.Contrast(_paste_truth(image, truth, mask)).enhance(1.03)
    if attempt == 1 and strategy in {"text_repair_local", "local_inpaint"}:
        return _paste_truth(image, truth, mask, partial=True)
    return _paste_truth(image, truth, mask)
