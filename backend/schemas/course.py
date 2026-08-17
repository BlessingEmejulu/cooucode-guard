from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None

class AssignmentCreate(AssignmentBase):
    course_id: int

class AssignmentResponse(AssignmentBase):
    id: int
    course_id: int
    created_at: datetime
    submissions_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

class CourseBase(BaseModel):
    course_code: str
    course_title: str
    semester: Optional[str] = "First Semester"

class CourseCreate(CourseBase):
    pass

class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    assignments: List[AssignmentResponse] = []
    submissions_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)
