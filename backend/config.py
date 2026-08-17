import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent.parent
STORAGE_DIR = BASE_DIR / "storage"
SUBMISSIONS_DIR = STORAGE_DIR / "submissions"
REPORTS_DIR = STORAGE_DIR / "reports"
DATABASE_DIR = BASE_DIR / "database"

# Ensure essential directories exist
for directory in [STORAGE_DIR, SUBMISSIONS_DIR, REPORTS_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Application configurations
APP_NAME = os.getenv("APP_NAME", "COOUCodeGuard")
APP_TITLE = "COOUCodeGuard - Offline Source Code Plagiarism Detection System"
APP_VERSION = "1.0.0"
SECRET_KEY = os.getenv("SECRET_KEY", "coou-secure-offline-secret-key-salt-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")) # 24 hours

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_DIR / 'cooucode_guard.db'}")

INSTITUTION_NAME = os.getenv("INSTITUTION_NAME", "Chukwuemeka Odumegwu Ojukwu University")
INSTITUTION_CAMPUS = os.getenv("INSTITUTION_CAMPUS", "Uli Campus, Anambra State, Nigeria")
INSTITUTION_DEPT = os.getenv("INSTITUTION_DEPT", "Department of Computer Science")

ALLOWED_EXTENSIONS = {
    ".py": "Python",
    ".java": "Java",
    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".h": "C++",
    ".hpp": "C++"
}

# Max upload size: 5MB per file
MAX_UPLOAD_SIZE = 5 * 1024 * 1024
