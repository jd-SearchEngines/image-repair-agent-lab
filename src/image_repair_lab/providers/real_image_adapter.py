import json
import shutil
import subprocess
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .base import RealEditResult


class RealImageAdapter:
    """Subprocess adapter for the locally cached MLX Qwen Image Edit model.

    This adapter deliberately records the CLI invocation and raw process
    output. It never calls the deterministic simulator and never fabricates an
    output when the provider fails.
    """

    provider = "local-mflux"
    model = "mlx-community/qwen-image-edit-2511-8bit"

    def __init__(self, executable: str, model_path: str, steps: int = 20, width: int = 512, height: int = 320):
        self.executable = executable
        self.model_path = model_path
        self.steps = steps
        self.width = width
        self.height = height

    def edit(self, image, instruction, mode, mask=None, preserve_constraints=None, seed=None, output_path=None, metadata_dir=None):
        request_id = f"real-{uuid.uuid4()}"
        started = time.monotonic()
        timestamp = datetime.now(timezone.utc).isoformat()
        output_path = Path(output_path)
        metadata_dir = Path(metadata_dir or output_path.parent)
        metadata_dir.mkdir(parents=True, exist_ok=True)
        raw_path = metadata_dir / f"{request_id}.raw.json"
        cmd = [self.executable, "--model", self.model_path, "--base-model", "qwen-image-edit", "--image-paths", str(image), "--prompt", instruction, "--width", str(self.width), "--height", str(self.height), "--steps", str(self.steps), "--seed", str(seed or 0), "--low-ram", "--no-metadata", "--output", str(output_path)]
        if mode == "local_repair":
            # Qwen Image Edit through the installed MFlux CLI has no mask flag.
            # Keep the mask path in the record, but fail closed on the claim.
            mask_support = "MASK_NOT_SUPPORTED"
        else:
            mask_support = "NOT_APPLICABLE"
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        latency = round(time.monotonic() - started, 3)
        payload = {
            "request_id": request_id, "provider": self.provider, "model": self.model,
            "model_path": self.model_path, "command": cmd, "timestamp": timestamp,
            "stdout": result.stdout, "stderr": result.stderr, "returncode": result.returncode,
            "preserve_constraints": preserve_constraints or [], "mask_support": mask_support,
            "mask_path": str(mask) if mask else None, "seed": seed, "latency_seconds": latency,
        }
        raw_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
        success = result.returncode == 0 and output_path.exists() and output_path.stat().st_size > 0
        error = None if success else (result.stderr[-1000:] or f"provider_exit_{result.returncode}")
        return RealEditResult(
            provider=self.provider, model=self.model, request_id=request_id, timestamp=timestamp,
            input_path=str(image), output_path=str(output_path), instruction=instruction, mode=mode,
            mask_path=str(mask) if mask else None, seed=seed, latency_seconds=latency, cost=None,
            raw_metadata_path=str(raw_path), success=success, error=error, mask_support=mask_support,
        )
