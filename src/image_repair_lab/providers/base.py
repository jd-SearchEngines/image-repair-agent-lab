from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class RealEditResult:
    provider: str
    model: str
    request_id: str
    timestamp: str
    input_path: str
    output_path: str
    instruction: str
    mode: str
    mask_path: Optional[str]
    seed: Optional[int]
    latency_seconds: float
    cost: Optional[float]
    raw_metadata_path: str
    success: bool
    error: Optional[str] = None
    mask_support: str = "UNKNOWN"

    def to_dict(self):
        return self.__dict__.copy()
