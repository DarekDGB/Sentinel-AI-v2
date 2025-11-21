from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


@dataclass
class LoadedModel:
    """
    Placeholder container for a loaded model.

    In a real implementation this would wrap an ONNX / Torch / TF runtime.
    """

    path: Path
    hash: str


class ModelVerificationError(Exception):
    """Raised when a model fails integrity checks."""


def compute_file_hash(path: Path, algo: str = "sha3_256") -> str:
    """Compute a cryptographic hash of a file."""
    hasher = hashlib.new(algo)
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_and_verify_model(
    model_path: str,
    expected_hash: Optional[str] = None,
) -> LoadedModel:
    """
    Load a model from disk and verify its hash if provided.

    This function does *not* load an actual ML runtime; it only provides a
    safe, verifiable interface and leaves runtime binding up to the devs.
    """
    path = Path(model_path)
    if not path.exists():
        raise ModelVerificationError(f"Model file not found: {path}")

    actual_hash = compute_file_hash(path)

    if expected_hash is not None and actual_hash != expected_hash:
        raise ModelVerificationError(
            f"Model hash mismatch: expected {expected_hash}, got {actual_hash}"
        )

    return LoadedModel(path=path, hash=actual_hash)


def run_model_inference(model: LoadedModel, features: Any) -> float:
    """
    Placeholder for model inference.

    Returns a dummy risk score in [0.0, 1.0] so developers can integrate
    their own real AI runtime without changing the rest of the code.
    """
    _ = (model, features)
    return 0.5
