from typing import Dict, Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.database import get_db
from backend.models import Submission, Scan, Course, Assignment, Comparison
from backend.auth.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/statistics")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    total_submissions = db.query(Submission).count()
    total_scans = db.query(Scan).count()

    # Similarity classifications
    critical_cases = db.query(Scan).filter(Scan.overall_similarity >= 80.0).count()
    high_cases = db.query(Scan).filter(Scan.overall_similarity >= 60.0, Scan.overall_similarity < 80.0).count()
    medium_cases = db.query(Scan).filter(Scan.overall_similarity >= 30.0, Scan.overall_similarity < 60.0).count()
    low_cases = db.query(Scan).filter(Scan.overall_similarity < 30.0).count()

    # Average similarity
    avg_score = db.query(func.avg(Scan.overall_similarity)).scalar() or 0.0

    # Language distribution
    lang_dist_query = db.query(Submission.language, func.count(Submission.id)).group_by(Submission.language).all()
    lang_distribution = {lang: count for lang, count in lang_dist_query}

    # Similarity breakdown ranges for Chart.js
    similarity_distribution = {
        "0-29% (Low)": low_cases,
        "30-59% (Moderate)": medium_cases,
        "60-79% (High)": high_cases,
        "80-100% (Critical)": critical_cases
    }

    # AI Pattern distribution
    ai_high = db.query(Scan).filter(Scan.ai_pattern_score >= 60.0).count()
    ai_mod = db.query(Scan).filter(Scan.ai_pattern_score >= 30.0, Scan.ai_pattern_score < 60.0).count()
    ai_low = db.query(Scan).filter(Scan.ai_pattern_score < 30.0).count()

    return {
        "total_submissions": total_submissions,
        "total_scans": total_scans,
        "critical_cases": critical_cases,
        "high_cases": high_cases,
        "medium_cases": medium_cases,
        "low_cases": low_cases,
        "average_similarity": round(float(avg_score), 1),
        "language_distribution": lang_distribution,
        "similarity_distribution": similarity_distribution,
        "ai_distribution": {
            "High Indication": ai_high,
            "Moderate Indication": ai_mod,
            "Low Indication": ai_low
        }
    }

@router.get("/recent-submissions")
def get_recent_submissions(
    limit: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    submissions = db.query(Submission).order_by(Submission.submitted_at.desc()).limit(limit).all()
    result = []
    for s in submissions:
        latest_scan = db.query(Scan).filter(Scan.submission_id == s.id).order_by(Scan.created_at.desc()).first()
        result.append({
            "id": s.id,
            "student_name": s.student_name,
            "matric_number": s.matric_number,
            "course_code": s.course.course_code if s.course else "N/A",
            "assignment_title": s.assignment.title if s.assignment else "General",
            "language": s.language,
            "file_name": s.file_name,
            "submitted_at": s.submitted_at,
            "latest_similarity": latest_scan.overall_similarity if latest_scan else None,
            "latest_risk_level": latest_scan.risk_level if latest_scan else "Unscanned",
            "latest_scan_id": latest_scan.id if latest_scan else None
        })
    return result

@router.get("/recent-scans")
def get_recent_scans(
    limit: int = 6,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[Dict[str, Any]]:
    scans = db.query(Scan).order_by(Scan.created_at.desc()).limit(limit).all()
    result = []
    for sc in scans:
        sub = sc.submission
        result.append({
            "id": sc.id,
            "submission_id": sc.submission_id,
            "student_name": sub.student_name if sub else "Unknown",
            "matric_number": sub.matric_number if sub else "N/A",
            "course_code": sub.course.course_code if sub and sub.course else "N/A",
            "language": sub.language if sub else "N/A",
            "overall_similarity": sc.overall_similarity,
            "ast_similarity": sc.ast_similarity,
            "token_similarity": sc.token_similarity,
            "fingerprint_similarity": sc.fingerprint_similarity,
            "ai_pattern_score": sc.ai_pattern_score,
            "risk_level": sc.risk_level,
            "created_at": sc.created_at
        })
    return result
