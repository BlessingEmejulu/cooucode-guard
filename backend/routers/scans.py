from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import Submission, Scan, Comparison, Report
from backend.schemas.scan import ScanCreate, ScanResponse, ComparisonResponse
from backend.auth.dependencies import get_current_user
from backend.models.user import User
from analysis_engine.similarity import SimilarityEngine
from analysis_engine.ai_pattern_detector import AIPatternDetector
from analysis_engine.report_generator import ReportGenerator

router = APIRouter(prefix="/api/scans", tags=["Scanning & Plagiarism"])

@router.post("", response_model=ScanResponse)
def run_scan(
    scan_in: ScanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    target_sub = db.query(Submission).filter(Submission.id == scan_in.submission_id).first()
    if not target_sub:
        raise HTTPException(status_code=404, detail="Target submission not found")

    # 1. Determine comparison candidate pool (same language, excluding self)
    query = db.query(Submission).filter(
        Submission.id != target_sub.id,
        Submission.language == target_sub.language
    )

    if scan_in.scan_type == "course" and target_sub.course_id:
        query = query.filter(Submission.course_id == target_sub.course_id)
    elif scan_in.scan_type == "assignment" and target_sub.assignment_id:
        query = query.filter(Submission.assignment_id == target_sub.assignment_id)
    elif scan_in.scan_type == "pairwise" and scan_in.target_submission_id:
        query = query.filter(Submission.id == scan_in.target_submission_id)

    candidates = query.all()

    # 2. AI Pattern Heuristic Analysis for the target code
    ai_analysis = AIPatternDetector.analyze(target_sub.source_code, target_sub.language)
    ai_score = ai_analysis.get("ai_pattern_score", 0.0)

    # 3. Pairwise comparisons across candidates
    highest_overall = 0.0
    highest_ast = 0.0
    highest_token = 0.0
    highest_fp = 0.0
    highest_norm = 0.0

    comparison_results: List[Dict[str, Any]] = []

    for peer in candidates:
        try:
            comp = SimilarityEngine.compare_pair(
                target_sub.source_code,
                peer.source_code,
                target_sub.language
            )

            if comp["overall_similarity"] > highest_overall:
                highest_overall = comp["overall_similarity"]
                highest_ast = comp["ast_similarity"]
                highest_token = comp["token_similarity"]
                highest_fp = comp["fingerprint_similarity"]
                highest_norm = comp["normalized_similarity"]

            comparison_results.append({
                "peer": peer,
                "comparison": comp
            })
        except Exception:
            # Gracefully handle single comparison failure without stopping scan
            continue

    # Sort comparisons by similarity descending
    comparison_results.sort(key=lambda x: x["comparison"]["overall_similarity"], reverse=True)

    risk_level = SimilarityEngine.classify_risk(highest_overall)

    # 4. Save Scan Record
    scan = Scan(
        submission_id=target_sub.id,
        user_id=current_user.id if current_user else None,
        scan_type=scan_in.scan_type or "repository",
        overall_similarity=highest_overall,
        ast_similarity=highest_ast,
        token_similarity=highest_token,
        fingerprint_similarity=highest_fp,
        normalized_similarity=highest_norm,
        ai_pattern_score=ai_score,
        ai_pattern_details=ai_analysis,
        risk_level=risk_level,
        status="completed"
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # 5. Save top comparison records
    top_matches_response: List[ComparisonResponse] = []
    report_matches = []

    for item in comparison_results:
        peer = item["peer"]
        comp = item["comparison"]
        c_record = Comparison(
            scan_id=scan.id,
            submission_a_id=target_sub.id,
            submission_b_id=peer.id,
            similarity_score=comp["overall_similarity"],
            ast_similarity=comp["ast_similarity"],
            token_similarity=comp["token_similarity"],
            fingerprint_similarity=comp["fingerprint_similarity"],
            normalized_similarity=comp["normalized_similarity"],
            matching_blocks=comp["matching_blocks"]
        )
        db.add(c_record)
        db.commit()
        db.refresh(c_record)

        resp_item = ComparisonResponse(
            id=c_record.id,
            scan_id=scan.id,
            submission_a_id=target_sub.id,
            submission_b_id=peer.id,
            student_a_name=target_sub.student_name,
            matric_a=target_sub.matric_number,
            student_b_name=peer.student_name,
            matric_b=peer.matric_number,
            file_a_name=target_sub.file_name,
            file_b_name=peer.file_name,
            similarity_score=c_record.similarity_score,
            ast_similarity=c_record.ast_similarity,
            token_similarity=c_record.token_similarity,
            fingerprint_similarity=c_record.fingerprint_similarity,
            normalized_similarity=c_record.normalized_similarity,
            matching_blocks=c_record.matching_blocks or [],
            created_at=c_record.created_at
        )
        top_matches_response.append(resp_item)

        report_matches.append({
            "submission_b": {
                "student_name": peer.student_name,
                "matric_number": peer.matric_number,
                "file_name": peer.file_name
            },
            "similarity_score": comp["overall_similarity"],
            "ast_similarity": comp["ast_similarity"],
            "token_similarity": comp["token_similarity"],
            "fingerprint_similarity": comp["fingerprint_similarity"],
            "normalized_similarity": comp["normalized_similarity"],
            "matching_blocks": comp["matching_blocks"]
        })

    # 6. Generate Standalone HTML Report
    try:
        report_html = ReportGenerator.generate_html_report(
            scan_data={
                "id": scan.id,
                "overall_similarity": scan.overall_similarity,
                "ast_similarity": scan.ast_similarity,
                "token_similarity": scan.token_similarity,
                "fingerprint_similarity": scan.fingerprint_similarity,
                "normalized_similarity": scan.normalized_similarity,
                "risk_level": scan.risk_level,
                "ai_pattern_score": scan.ai_pattern_score
            },
            student_info={
                "student_name": target_sub.student_name,
                "matric_number": target_sub.matric_number,
                "course_code": target_sub.course.course_code if target_sub.course else "N/A",
                "assignment_title": target_sub.assignment.title if target_sub.assignment else "General",
                "language": target_sub.language,
                "file_name": target_sub.file_name
            },
            comparison_matches=report_matches,
            ai_details=ai_analysis
        )
        report_path = ReportGenerator.save_report_file(scan.id, report_html)
        report_record = Report(
            scan_id=scan.id,
            title=f"Plagiarism Audit - {target_sub.student_name} ({target_sub.matric_number})",
            file_path=str(report_path),
            report_format="HTML",
            summary_data={"overall_similarity": scan.overall_similarity, "risk_level": scan.risk_level}
        )
        db.add(report_record)
        db.commit()
    except Exception:
        pass

    return ScanResponse(
        id=scan.id,
        submission_id=scan.submission_id,
        user_id=scan.user_id,
        scan_type=scan.scan_type,
        overall_similarity=scan.overall_similarity,
        ast_similarity=scan.ast_similarity,
        token_similarity=scan.token_similarity,
        fingerprint_similarity=scan.fingerprint_similarity,
        normalized_similarity=scan.normalized_similarity,
        ai_pattern_score=scan.ai_pattern_score,
        ai_pattern_details=scan.ai_pattern_details,
        risk_level=scan.risk_level,
        status=scan.status,
        created_at=scan.created_at,
        student_name=target_sub.student_name,
        matric_number=target_sub.matric_number,
        course_code=target_sub.course.course_code if target_sub.course else None,
        assignment_title=target_sub.assignment.title if target_sub.assignment else None,
        file_name=target_sub.file_name,
        language=target_sub.language,
        top_matches=top_matches_response
    )

@router.get("", response_model=List[ScanResponse])
def get_scans(
    risk_level: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Scan).join(Submission, Scan.submission_id == Submission.id)

    if risk_level:
        query = query.filter(Scan.risk_level.ilike(f"%{risk_level}%"))
    if search:
        s_term = f"%{search.strip()}%"
        query = query.filter(
            (Submission.student_name.ilike(s_term)) |
            (Submission.matric_number.ilike(s_term)) |
            (Submission.file_name.ilike(s_term))
        )

    scans = query.order_by(Scan.created_at.desc()).all()
    result = []
    for sc in scans:
        sub = sc.submission
        result.append(ScanResponse(
            id=sc.id,
            submission_id=sc.submission_id,
            user_id=sc.user_id,
            scan_type=sc.scan_type,
            overall_similarity=sc.overall_similarity,
            ast_similarity=sc.ast_similarity,
            token_similarity=sc.token_similarity,
            fingerprint_similarity=sc.fingerprint_similarity,
            normalized_similarity=sc.normalized_similarity,
            ai_pattern_score=sc.ai_pattern_score,
            ai_pattern_details=sc.ai_pattern_details,
            risk_level=sc.risk_level,
            status=sc.status,
            created_at=sc.created_at,
            student_name=sub.student_name if sub else None,
            matric_number=sub.matric_number if sub else None,
            course_code=sub.course.course_code if sub and sub.course else None,
            assignment_title=sub.assignment.title if sub and sub.assignment else None,
            file_name=sub.file_name if sub else None,
            language=sub.language if sub else None,
            top_matches=[]
        ))
    return result

@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sc = db.query(Scan).filter(Scan.id == scan_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Scan record not found")

    sub = sc.submission
    comps = db.query(Comparison).filter(Comparison.scan_id == sc.id).order_by(Comparison.similarity_score.desc()).all()
    
    top_matches = []
    for c in comps:
        sub_a = c.submission_a
        sub_b = c.submission_b
        top_matches.append(ComparisonResponse(
            id=c.id,
            scan_id=c.scan_id,
            submission_a_id=c.submission_a_id,
            submission_b_id=c.submission_b_id,
            student_a_name=sub_a.student_name if sub_a else None,
            matric_a=sub_a.matric_number if sub_a else None,
            student_b_name=sub_b.student_name if sub_b else None,
            matric_b=sub_b.matric_number if sub_b else None,
            file_a_name=sub_a.file_name if sub_a else None,
            file_b_name=sub_b.file_name if sub_b else None,
            similarity_score=c.similarity_score,
            ast_similarity=c.ast_similarity,
            token_similarity=c.token_similarity,
            fingerprint_similarity=c.fingerprint_similarity,
            normalized_similarity=c.normalized_similarity,
            matching_blocks=c.matching_blocks or [],
            created_at=c.created_at
        ))

    return ScanResponse(
        id=sc.id,
        submission_id=sc.submission_id,
        user_id=sc.user_id,
        scan_type=sc.scan_type,
        overall_similarity=sc.overall_similarity,
        ast_similarity=sc.ast_similarity,
        token_similarity=sc.token_similarity,
        fingerprint_similarity=sc.fingerprint_similarity,
        normalized_similarity=sc.normalized_similarity,
        ai_pattern_score=sc.ai_pattern_score,
        ai_pattern_details=sc.ai_pattern_details,
        risk_level=sc.risk_level,
        status=sc.status,
        created_at=sc.created_at,
        student_name=sub.student_name if sub else None,
        matric_number=sub.matric_number if sub else None,
        course_code=sub.course.course_code if sub and sub.course else None,
        assignment_title=sub.assignment.title if sub and sub.assignment else None,
        file_name=sub.file_name if sub else None,
        language=sub.language if sub else None,
        top_matches=top_matches
    )

@router.delete("/{scan_id}")
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sc = db.query(Scan).filter(Scan.id == scan_id).first()
    if not sc:
        raise HTTPException(status_code=404, detail="Scan record not found")
    db.delete(sc)
    db.commit()
    return {"message": "Scan record deleted successfully"}
