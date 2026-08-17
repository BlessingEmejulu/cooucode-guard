from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SubmissionBase(BaseModel):
    student_name: str
    matric_number: str
    course_id: int
    assignment_id: Optional[int] = None
    language: str

class SubmissionCreate(SubmissionBase):
    file_name: str
    source_code: str

class SubmissionResponse(SubmissionBase):
    id: int
    file_name: str
    file_path: str
    source_hash: str
    submitted_at: datetime
    course_code: Optional[str] = None
    assignment_title: Optional[str] = None
    latest_scan_similarity: Optional[float] = None
    latest_scan_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

class SubmissionDetailResponse(SubmissionResponse):
    source_code: str
