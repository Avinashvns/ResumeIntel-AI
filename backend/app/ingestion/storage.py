from pathlib import Path
from uuid import uuid4


PROJECT_ROOT = Path(__file__).resolve().parents[3]

RESUME_STORAGE_DIR = PROJECT_ROOT / "data" / "resumes"

RESUME_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


def generate_stored_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()
    unique_id = uuid4().hex

    return f"{unique_id}{extension}"


def get_resume_path(stored_filename: str) -> Path:
    return RESUME_STORAGE_DIR / stored_filename