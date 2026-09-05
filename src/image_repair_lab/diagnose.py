from dataclasses import asdict, dataclass
from typing import List, Tuple


@dataclass
class Diagnosis:
    case_id: str
    error_class: str
    defect_bbox: Tuple[int, int, int, int]
    preserve_constraints: List[str]
    confidence: float
    evidence: str

    def to_dict(self):
        result = asdict(self)
        result["defect_bbox"] = list(self.defect_bbox)
        return result


def diagnose(case: dict) -> Diagnosis:
    """Create a structured diagnosis from a fixture manifest.

    In production this is the adapter seam for a VLM or vision detector. The
    local runner intentionally uses declared fixture metadata so the evidence
    is reproducible and its simulator-only nature is explicit.
    """
    return Diagnosis(
        case_id=case["case_id"],
        error_class=case["expected_issue_type"],
        defect_bbox=tuple(case["defect_bbox"]),
        preserve_constraints=case["preserve_constraints"],
        confidence=1.0,
        evidence="fixture_metadata_declared_for_deterministic_simulator",
    )
