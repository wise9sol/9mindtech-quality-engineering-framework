# © 2026 Wise 9 Mind Solutions LLC. All rights reserved.
from pathlib import Path
from datetime import datetime


def artifact_path(prefix: str, suffix: str) -> Path:
    """Return a timestamped path inside the artifacts/ directory."""
    folder = Path("artifacts")
    folder.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return folder / f"{prefix}_{timestamp}{suffix}"
