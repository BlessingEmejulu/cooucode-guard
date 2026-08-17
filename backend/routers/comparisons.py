from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Comparison, Submission
from backend.schemas.scan import ComparisonDetailResponse
from backend.auth.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/api/comparisons", tags=["Comparisons"])

@router.get("/{comparison_id}", response_model=ComparisonDetailResponse)
def get_comparison(
    comparison_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    comp = db.query(Comparison).filter(Comparison.id == comparison_id).first()
    if not comp:
        raise HTTPException(status_code=404, detail="Comparison record not found")

    sub_a = comp.submission_a
    sub_b = comp.submission_b

    return ComparisonDetailResponse(
        id=comp.id,
        scan_id=comp.scan_id,
        submission_a_id=comp.submission_a_id,
        submission_b_id=comp.submission_b_id,
        student_a_name=sub_a.student_name if sub_a else "Student A",
        matric_a=sub_a.matric_number if sub_a else "N/A",
        student_b_name=sub_b.student_name if sub_b else "Student B",
        matric_b=sub_b.matric_number if sub_b else "N/A",
        file_a_name=sub_a.file_name if sub_a else "source_a",
        file_b_name=sub_b.file_name if sub_b else "source_b",
        similarity_score=comp.similarity_score,
        ast_similarity=comp.ast_similarity,
        token_similarity=comp.token_similarity,
        fingerprint_similarity=comp.fingerprint_similarity,
        normalized_similarity=comp.normalized_similarity,
        matching_blocks=comp.matching_blocks or [],
        created_at=comp.created_at,
        source_a_code=sub_a.source_code if sub_a else "",
        source_b_code=sub_b.source_code if sub_b else ""
    )
