from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Course, Assignment, Submission
from backend.schemas.course import CourseCreate, CourseResponse, AssignmentCreate, AssignmentResponse
from backend.auth.dependencies import get_current_user
from backend.models.user import User

router = APIRouter(prefix="/api/courses", tags=["Courses & Assignments"])

@router.get("", response_model=List[CourseResponse])
def get_courses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    courses = db.query(Course).all()
    result = []
    for c in courses:
        sub_count = db.query(Submission).filter(Submission.course_id == c.id).count()
        asgs = []
        for a in c.assignments:
            a_subs = db.query(Submission).filter(Submission.assignment_id == a.id).count()
            asgs.append(AssignmentResponse(
                id=a.id,
                course_id=a.course_id,
                title=a.title,
                description=a.description,
                deadline=a.deadline,
                created_at=a.created_at,
                submissions_count=a_subs
            ))
        result.append(CourseResponse(
            id=c.id,
            course_code=c.course_code,
            course_title=c.course_title,
            semester=c.semester,
            created_at=c.created_at,
            assignments=asgs,
            submissions_count=sub_count
        ))
    return result

@router.post("", response_model=CourseResponse)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Course).filter(Course.course_code == course_in.course_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course code already exists")

    course = Course(
        course_code=course_in.course_code.upper().strip(),
        course_title=course_in.course_title.strip(),
        semester=course_in.semester
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return CourseResponse(
        id=course.id,
        course_code=course.course_code,
        course_title=course.course_title,
        semester=course.semester,
        created_at=course.created_at,
        assignments=[],
        submissions_count=0
    )

@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    sub_count = db.query(Submission).filter(Submission.course_id == course.id).count()
    return CourseResponse(
        id=course.id,
        course_code=course.course_code,
        course_title=course.course_title,
        semester=course.semester,
        created_at=course.created_at,
        assignments=[AssignmentResponse.from_orm(a) for a in course.assignments],
        submissions_count=sub_count
    )

@router.delete("/{course_id}")
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()
    return {"message": "Course and related assignments deleted successfully"}

# Assignments router under courses
@router.post("/assignments", response_model=AssignmentResponse)
def create_assignment(
    asg_in: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    course = db.query(Course).filter(Course.id == asg_in.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    asg = Assignment(
        course_id=asg_in.course_id,
        title=asg_in.title.strip(),
        description=asg_in.description,
        deadline=asg_in.deadline
    )
    db.add(asg)
    db.commit()
    db.refresh(asg)
    return AssignmentResponse(
        id=asg.id,
        course_id=asg.course_id,
        title=asg.title,
        description=asg.description,
        deadline=asg.deadline,
        created_at=asg.created_at,
        submissions_count=0
    )

@router.delete("/assignments/{assignment_id}")
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    asg = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not asg:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(asg)
    db.commit()
    return {"message": "Assignment deleted successfully"}
