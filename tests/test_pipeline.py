from PIL import Image
from image_repair_lab.qa import qa
from image_repair_lab.routing import route


def test_route_is_explicit():
    assert route({"error_class": "LOCAL_DEFECT"})["strategy"] == "local_inpaint"
    assert route({"error_class": "GLOBAL_FAILURE"})["scope"] == "global"


def test_qa_accepts_exact_local_repair():
    before = Image.new("RGB", (4, 4), "red")
    truth = Image.new("RGB", (4, 4), "red")
    after = truth.copy(); mask = Image.new("L", (4, 4), 0); mask.putpixel((1, 1), 255)
    assert qa(before, after, truth, mask)["status"] == "PASS"
