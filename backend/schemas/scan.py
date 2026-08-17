from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict

class MatchingBlock(BaseModel):
    start_a: int
    end_a: int
    start_b: int
    end_b: int
    similarity: float
    block_type: Optional[str] = "structural"
    description: Optional[str] = None

class ComparisonResponse(BaseModel):
    id: int
    scan_id: int
    submission_a_id: int
    submission_b_id: int
    student_a_name: Optional[str] = None
    matric_a: Optional[str] = None
    student_b_name: Optional[str] = None
    matric_b: Optional[str] = None
    file_a_name: Optional[str] = None
    file_b_name: Optional[str] = None
    similarity_score: float
    ast_similarity: float
    token_similarity: float
    fingerprint_similarity: float
    normalized_similarity: float
    matching_blocks: Optional[List[Dict[str, Any]]] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ComparisonDetailResponse(ComparisonResponse):
    source_a_code: str
    source_b_code: str

class ScanCreate(BaseModel):
    submission_id: int
    scan_type: Optional[str] = "repository"
    target_submission_id: Optional[int] = None

class ScanResponse(BaseModel):
    id: int
    submission_id: int
    user_id: Optional[int] = None
    scan_type: str
    overall_similarity: float
    ast_similarity: float
    token_similarity: float
    fingerprint_similarity: float
    normalized_similarity: float
    ai_pattern_score: float
    ai_pattern_details: Optional[Dict[str, Any]] = None
    risk_level: str
    status: str
    created_at: datetime
    student_name: Optional[str] = None
    matric_number: Optional[str] = None
    course_code: Optional[str] = None
    assignment_title: Optional[str] = None
    file_name: Optional[str] = None
    language: Optional[str] = None
    top_matches: Optional[List[ComparisonResponse]] = []

    model_config = ConfigDict(from_attributes=True)
