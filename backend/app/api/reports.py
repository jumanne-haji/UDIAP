from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.response import Response
from app.models.genome import DecisionGenome
from app.models.report import AIReport
from app.schemas.report import AIReportOut, GenerateReportRequest
from ai_engine.scoring.report_generator import report_generator
from ai_engine.coe.observer import coe

router = APIRouter()


@router.post("/generate", response_model=AIReportOut)
async def generate_report(
    data: GenerateReportRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Fetch the latest response for this session
    result = await db.execute(
        select(Response)
        .where(
            Response.session_id == data.session_id,
            Response.user_id == current_user.id,
            Response.is_submitted == True,
        )
        .order_by(Response.id.desc())
        .limit(1)
    )
    response = result.scalar_one_or_none()
    if not response:
        raise HTTPException(status_code=404, detail="No submitted response found for this session")

    # Behaviour features
    features = coe.extract_features(data.session_id, total_time_ms=response.time_spent_seconds * 1000)

    # Generate report
    report_data = report_generator.generate(
        answer_text=response.answer_text,
        behaviour_features=features,
        user_name=current_user.name,
    )

    scores = report_data["scores"]

    # Persist Decision Genome
    genome = DecisionGenome(
        user_id=current_user.id,
        assessment_id=response.assessment_id,
        session_id=data.session_id,
        critical_thinking_score=scores.get("critical_thinking", 0),
        risk_score=scores.get("risk_management", 0),
        adaptability_score=scores.get("adaptability", scores.get("adaptability_process", 0)),
        technical_reasoning=scores.get("technical_reasoning", 0),
        communication_score=scores.get("communication", 0),
        reflection_score=scores.get("reflection", scores.get("reflection_score", 0)),
        decision_speed_score=scores.get("decision_speed_score", 0),
        revision_quality_score=scores.get("revision_quality_score", 0),
        overall_score=scores.get("overall_score", 0),
    )
    db.add(genome)
    await db.flush()

    # Persist AI Report
    ai_report = AIReport(
        user_id=current_user.id,
        assessment_id=response.assessment_id,
        session_id=data.session_id,
        genome_id=genome.id,
        summary=report_data["summary"],
        strengths=report_data["strengths"],
        weaknesses=report_data["weaknesses"],
        recommendations=report_data["recommendations"],
        hdpm_analysis=report_data["hdpm_analysis"],
        full_report=report_data["full_report"],
    )
    db.add(ai_report)
    await db.flush()
    await db.refresh(ai_report)

    # End COE session
    coe.end_session(data.session_id)

    return ai_report


@router.get("/{report_id}", response_model=AIReportOut)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AIReport).where(AIReport.id == report_id, AIReport.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/", response_model=list[AIReportOut])
async def list_my_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(AIReport)
        .where(AIReport.user_id == current_user.id)
        .order_by(AIReport.generated_at.desc())
        .limit(20)
    )
    return result.scalars().all()
