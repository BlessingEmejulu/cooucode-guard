import os
import shutil
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db, Base, engine
from backend.config import STORAGE_DIR, SUBMISSIONS_DIR, REPORTS_DIR, DATABASE_DIR, APP_VERSION, INSTITUTION_NAME
from backend.auth.dependencies import get_current_user
from backend.models.user import User
from backend.models import Submission, Scan, Course, Report

router = APIRouter(prefix="/api/system", tags=["System"])

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "system": "COOUCodeGuard",
        "version": APP_VERSION,
        "offline_mode": True,
        "institution": INSTITUTION_NAME
    }

@router.get("/statistics")
def get_system_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Calculate storage sizes
    def get_dir_size(path: Path) -> int:
        total = 0
        if path.exists():
            for p in path.rglob("*"):
                if p.is_file():
                    total += p.stat().st_size
        return total

    submissions_size_bytes = get_dir_size(SUBMISSIONS_DIR)
    reports_size_bytes = get_dir_size(REPORTS_DIR)
    db_size_bytes = get_dir_size(DATABASE_DIR)

    return {
        "institution": INSTITUTION_NAME,
        "version": APP_VERSION,
        "offline_first": True,
        "database_engine": "SQLite",
        "database_size_kb": round(db_size_bytes / 1024, 2),
        "submissions_storage_kb": round(submissions_size_bytes / 1024, 2),
        "reports_storage_kb": round(reports_size_bytes / 1024, 2),
        "counts": {
            "users": db.query(User).count(),
            "courses": db.query(Course).count(),
            "submissions": db.query(Submission).count(),
            "scans": db.query(Scan).count(),
            "reports": db.query(Report).count()
        }
    }

@router.post("/reset-demo-data")
def reset_demo_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    from backend.services.demo_data import seed_demo_data
    # Clear tables
    db.query(Report).delete()
    db.query(Scan).delete()
    db.query(Submission).delete()
    db.query(Course).delete()
    db.query(User).delete()
    db.commit()

    # Reseed
    seed_demo_data(db)
    return {"message": "Demo data successfully reset and seeded"}
