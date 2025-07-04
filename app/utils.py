from pathlib import Path
from datetime import datetime

LOG_PATH = Path("log.txt")

def log_to_file(message: str) -> None:
    """Append a timestamped message to log.txt."""
    timestamp = datetime.utcnow().isoformat(timespec="seconds")
    LOG_PATH.write_text(f"[{timestamp}] {message}\n", append=True)
