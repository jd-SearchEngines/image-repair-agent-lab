import numpy as np


def qa(before, after, truth, mask, preserve_threshold=0.015, repair_threshold=0.92):
    a = np.asarray(before).astype(float)
    b = np.asarray(after).astype(float)
    t = np.asarray(truth).astype(float)
    m = np.asarray(mask).astype(bool)[..., None]
    changed = np.abs(a - b).mean(axis=2)
    target_error = np.abs(b - t).mean(axis=2)
    preserve_change_rate = float((changed[~m[..., 0]] > 2.0).mean()) if (~m[..., 0]).any() else 0.0
    defect_error = float(target_error[m[..., 0]].mean()) if m[..., 0].any() else 0.0
    max_error = 255.0 * 3.0
    repair_score = max(0.0, 1.0 - defect_error / 255.0)
    passed = repair_score >= repair_threshold and preserve_change_rate <= preserve_threshold
    return {
        "status": "PASS" if passed else "FAIL",
        "repair_score": round(repair_score, 4),
        "preserve_change_rate": round(preserve_change_rate, 4),
        "preserve_score": round(1.0 - preserve_change_rate, 4),
        "thresholds": {"repair_score": repair_threshold, "preserve_change_rate": preserve_threshold},
        "qa_scope": "pixel_rule_on_synthetic_fixture",
    }
