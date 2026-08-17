import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Report, Scan, Submission, Comparison
from backend.schemas.report import ReportResponse
from backend.auth.dependencies import get_current_user
from backend.models.user import User
from analysis_engine.report_generator import ReportGenerator

router = APIRouter(prefix="/api/reports", tags=["Reports"])

@router.get("", response_model=List[ReportResponse])
def get_reports(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return reports

@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rep = db.query(Report).filter(Report.id == report_id).first()
    if not rep:
        raise HTTPException(status_code=404, detail="Report not found")
    return rep

@router.get("/{report_id}/html", response_class=HTMLResponse)
def get_report_html(
    report_id: int,
    db: Session = Depends(get_db)
):
    rep = db.query(Report).filter(Report.id == report_id).first()
    if not rep or not rep.file_path or not os.path.exists(rep.file_path):
        raise HTTPException(status_code=404, detail="HTML Report file not found")
    
    with open(rep.file_path, "r", encoding="utf-8") as f:
        return f.read()

@router.post("/generate/{scan_id}", response_model=ReportResponse)
def generate_report(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sc = db.query(Scan).filter(Scan.id == scan_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Scan not found")

    target_sub = sc.submission
    comps = db.query(Comparison).filter(Comparison.scan_id == sc.id).order_by(Comparison.similarity_score.desc()).all()

    report_matches = []
    for c in comps:
        peer = c.submission_b
        report_matches.append({
            "submission_b": {
                "student_name": peer.student_name if peer else "Unknown",
                "matric_number": peer.matric_number if peer else "N/A",
                "file_name": peer.file_name if peer else "code"
            },
            "similarity_score": c.similarity_score,
            "ast_similarity": c.ast_similarity,
            "token_similarity": c.token_similarity,
            "fingerprint_similarity": c.fingerprint_similarity,
            "normalized_similarity": c.normalized_similarity,
            "matching_blocks": c.matching_blocks or []
        })

    report_html = ReportGenerator.generate_html_report(
        scan_data={
            "id": sc.id,
            "overall_similarity": sc.overall_similarity,
            "ast_similarity": sc.ast_similarity,
            "token_similarity": sc.token_similarity,
            "fingerprint_similarity": sc.fingerprint_similarity,
            "normalized_similarity": sc.normalized_similarity,
            "risk_level": sc.risk_level,
            "ai_pattern_score": sc.ai_pattern_score
        },
        student_info={
            "student_name": target_sub.student_name if target_sub else "Unknown",
            "matric_number": target_sub.matric_number if target_sub else "N/A",
            "course_code": target_sub.course.course_code if target_sub and target_sub.course else "N/A",
            "assignment_title": target_sub.assignment.title if target_sub and target_sub.assignment else "General",
            "language": target_sub.language if target_sub else "N/A",
            "file_name": target_sub.file_name if target_sub else "code"
        },
        comparison_matches=report_matches,
        ai_details=sc.ai_pattern_details or {}
    )

    report_path = ReportGenerator.save_report_file(sc.id, report_html)
    rep = Report(
        scan_id=sc.id,
        title=f"Plagiarism Audit - {target_sub.student_name} ({target_sub.matric_number})",
        file_path=str(report_path),
        report_format="HTML",
        summary_data={"overall_similarity": sc.overall_similarity, "risk_level": sc.risk_level}
    )
    db.add(rep)
    db.commit()
    db.refresh(rep)

    return rep
