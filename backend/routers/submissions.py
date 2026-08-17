import os
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Submission, Course, Assignment, Scan
from backend.schemas.submission import SubmissionResponse, SubmissionDetailResponse
from backend.services.storage_service import StorageService
from backend.auth.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/api/submissions", tags=["Submissions"])

@router.post("/upload", response_model=SubmissionResponse)
async def upload_submission(
    student_name: str = Form(...),
    matric_number: str = Form(...),
    course_id: int = Form(...),
    assignment_id: Optional[int] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Selected course does not exist")

    # Read uploaded file content
    content_bytes = await file.read()
    if len(content_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds the 5MB limit")

    content_str = content_bytes.decode("utf-8", errors="replace")
    if not content_str.strip():
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    rel_path, source_hash, detected_language = StorageService.save_submission_file(
        student_matric=matric_number,
        filename=file.filename or "submission.txt",
        content=content_str
    )

    submission = Submission(
        student_name=student_name.strip(),
        matric_number=matric_number.strip().upper(),
        course_id=course_id,
        assignment_id=assignment_id if assignment_id and assignment_id > 0 else None,
        language=detected_language,
        file_name=StorageService.sanitize_filename(file.filename or "code.txt"),
        file_path=rel_path,
        source_hash=source_hash,
        source_code=content_str
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)

    return SubmissionResponse(
        id=submission.id,
        student_name=submission.student_name,
        matric_number=submission.matric_number,
        course_id=submission.course_id,
        assignment_id=submission.assignment_id,
        language=submission.language,
        file_name=submission.file_name,
        file_path=submission.file_path,
        source_hash=submission.source_hash,
        submitted_at=submission.submitted_at,
        course_code=course.course_code,
        assignment_title=submission.assignment.title if submission.assignment else None,
        latest_scan_similarity=None,
        latest_scan_id=None
    )

@router.get("", response_model=List[SubmissionResponse])
def get_submissions(
    course_id: Optional[int] = Query(None),
    language: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Submission)

    if course_id:
        query = query.filter(Submission.course_id == course_id)
    if language:
        query = query.filter(Submission.language.ilike(f"%{language}%"))
    if search:
        s_term = f"%{search.strip()}%"
        query = query.filter(
            (Submission.student_name.ilike(s_term)) |
            (Submission.matric_number.ilike(s_term)) |
            (Submission.file_name.ilike(s_term))
        )

    submissions = query.order_by(Submission.submitted_at.desc()).all()
    result = []
    for s in submissions:
        latest_scan = db.query(Scan).filter(Scan.submission_id == s.id).order_by(Scan.created_at.desc()).first()
        result.append(SubmissionResponse(
            id=s.id,
            student_name=s.student_name,
            matric_number=s.matric_number,
            course_id=s.course_id,
            assignment_id=s.assignment_id,
            language=s.language,
            file_name=s.file_name,
            file_path=s.file_path,
            source_hash=s.source_hash,
            submitted_at=s.submitted_at,
            course_code=s.course.course_code if s.course else None,
            assignment_title=s.assignment.title if s.assignment else None,
            latest_scan_similarity=latest_scan.overall_similarity if latest_scan else None,
            latest_scan_id=latest_scan.id if latest_scan else None
        ))
    return result

@router.get("/{submission_id}", response_model=SubmissionDetailResponse)
def get_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    latest_scan = db.query(Scan).filter(Scan.submission_id == sub.id).order_by(Scan.created_at.desc()).first()

    return SubmissionDetailResponse(
        id=sub.id,
        student_name=sub.student_name,
        matric_number=sub.matric_number,
        course_id=sub.course_id,
        assignment_id=sub.assignment_id,
        language=sub.language,
        file_name=sub.file_name,
        file_path=sub.file_path,
        source_hash=sub.source_hash,
        submitted_at=sub.submitted_at,
        course_code=sub.course.course_code if sub.course else None,
        assignment_title=sub.assignment.title if sub.assignment else None,
        latest_scan_similarity=latest_scan.overall_similarity if latest_scan else None,
        latest_scan_id=latest_scan.id if latest_scan else None,
        source_code=sub.source_code
    )

@router.get("/{submission_id}/source")
def get_submission_source(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return {
        "id": sub.id,
        "student_name": sub.student_name,
        "matric_number": sub.matric_number,
        "file_name": sub.file_name,
        "language": sub.language,
        "source_code": sub.source_code
    }

@router.delete("/{submission_id}")
def delete_submission(
    submission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub = db.query(Submission).filter(Submission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Remove physical file
    StorageService.delete_submission_file(sub.file_path)
    
    db.delete(sub)
    db.commit()
    return {"message": "Submission deleted successfully"}
