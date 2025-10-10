from pathlib import Path
from datetime import datetime

LOG_PATH = Path("log.txt")


def log_to_file(message: str) -> None:
    """Append a timestamped line to log.txt (UTF‑8)."""
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"[{timestamp}] {message}\n")
