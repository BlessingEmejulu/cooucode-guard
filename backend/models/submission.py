from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(150), nullable=False, index=True)
    matric_number = Column(String(50), nullable=False, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    assignment_id = Column(Integer, ForeignKey("assignments.id"), nullable=True)
    language = Column(String(50), nullable=False) # Python, Java, C++
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    source_hash = Column(String(64), nullable=False, index=True) # SHA-256
    source_code = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

    course = relationship("Course", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")
    scans = relationship("Scan", back_populates="submission", cascade="all, delete-orphan")
