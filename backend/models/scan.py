from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    scan_type = Column(String(50), default="repository") # repository, course, pairwise
    overall_similarity = Column(Float, default=0.0)
    ast_similarity = Column(Float, default=0.0)
    token_similarity = Column(Float, default=0.0)
    fingerprint_similarity = Column(Float, default=0.0)
    normalized_similarity = Column(Float, default=0.0)
    ai_pattern_score = Column(Float, default=0.0)
    ai_pattern_details = Column(JSON, nullable=True)
    risk_level = Column(String(50), default="Low") # Low, Moderate, High, Critical
    status = Column(String(50), default="completed")
    created_at = Column(DateTime, default=datetime.utcnow)

    submission = relationship("Submission", back_populates="scans")
    user = relationship("User", back_populates="scans")
    comparisons = relationship("Comparison", back_populates="scan", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="scan", cascade="all, delete-orphan")

class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    submission_a_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    submission_b_id = Column(Integer, ForeignKey("submissions.id"), nullable=False)
    similarity_score = Column(Float, default=0.0)
    ast_similarity = Column(Float, default=0.0)
    token_similarity = Column(Float, default=0.0)
    fingerprint_similarity = Column(Float, default=0.0)
    normalized_similarity = Column(Float, default=0.0)
    matching_blocks = Column(JSON, nullable=True) # list of {start_a, end_a, start_b, end_b, score, type}
    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("Scan", back_populates="comparisons")
    submission_a = relationship("Submission", foreign_keys=[submission_a_id])
    submission_b = relationship("Submission", foreign_keys=[submission_b_id])

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("scans.id"), nullable=False)
    title = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)
    report_format = Column(String(50), default="HTML") # HTML, PDF
    summary_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    scan = relationship("Scan", back_populates="reports")
