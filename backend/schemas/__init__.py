from backend.schemas.user import UserBase, UserCreate, UserLogin, UserResponse, Token
from backend.schemas.course import CourseBase, CourseCreate, CourseResponse, AssignmentBase, AssignmentCreate, AssignmentResponse
from backend.schemas.submission import SubmissionBase, SubmissionCreate, SubmissionResponse, SubmissionDetailResponse
from backend.schemas.scan import ScanCreate, ScanResponse, ComparisonResponse, ComparisonDetailResponse, MatchingBlock
from backend.schemas.report import ReportCreate, ReportResponse

__all__ = [
    "UserBase", "UserCreate", "UserLogin", "UserResponse", "Token",
    "CourseBase", "CourseCreate", "CourseResponse", "AssignmentBase", "AssignmentCreate", "AssignmentResponse",
    "SubmissionBase", "SubmissionCreate", "SubmissionResponse", "SubmissionDetailResponse",
    "ScanCreate", "ScanResponse", "ComparisonResponse", "ComparisonDetailResponse", "MatchingBlock",
    "ReportCreate", "ReportResponse"
]
