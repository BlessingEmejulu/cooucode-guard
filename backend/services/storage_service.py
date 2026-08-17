import hashlib
import os
import re
from pathlib import Path
from typing import Tuple
from fastapi import UploadFile, HTTPException
from backend.config import SUBMISSIONS_DIR, MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS

class StorageService:
    @classmethod
    def sanitize_filename(cls, filename: str) -> str:
        """Sanitizes filename to prevent path traversal and invalid characters."""
        filename = os.path.basename(filename)
        # Remove dangerous chars
        clean_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)
        return clean_name or "submission.txt"

    @classmethod
    def get_file_hash(cls, content: str) -> str:
        """Computes SHA-256 hash of code content."""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    @classmethod
    def detect_language(cls, filename: str) -> str:
        ext = Path(filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(ALLOWED_EXTENSIONS.keys())}"
            )
        return ALLOWED_EXTENSIONS[ext]

    @classmethod
    def save_submission_file(
        cls,
        student_matric: str,
        filename: str,
        content: str
    ) -> Tuple[str, str, str]:
        """
        Saves source code file to local disk under storage/submissions.
        Returns (relative_file_path, file_hash, detected_language).
        """
        clean_filename = cls.sanitize_filename(filename)
        clean_matric = re.sub(r'[^a-zA-Z0-9_\-]', '_', student_matric)
        language = cls.detect_language(clean_filename)

        matric_dir = SUBMISSIONS_DIR / clean_matric
        matric_dir.mkdir(parents=True, exist_ok=True)

        target_path = matric_dir / clean_filename
        
        # Write to disk
        with open(target_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(content)

        file_hash = cls.get_file_hash(content)
        rel_path = str(target_path.relative_to(SUBMISSIONS_DIR.parent))

        return rel_path, file_hash, language

    @classmethod
    def read_submission_file(cls, rel_path: str) -> str:
        """Reads file from storage safely."""
        full_path = (SUBMISSIONS_DIR.parent / rel_path).resolve()
        # Security check: ensure path is within STORAGE_DIR
        if not str(full_path).startswith(str(SUBMISSIONS_DIR.parent.resolve())):
            raise HTTPException(status_code=403, detail="Unauthorized file path access")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="Submission file not found on disk")

        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    @classmethod
    def delete_submission_file(cls, rel_path: str) -> bool:
        full_path = (SUBMISSIONS_DIR.parent / rel_path).resolve()
        if full_path.exists() and str(full_path).startswith(str(SUBMISSIONS_DIR.parent.resolve())):
            try:
                os.remove(full_path)
                return True
            except Exception:
                return False
        return False
