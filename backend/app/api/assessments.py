"""
Assessment endpoints: list, start, submit.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import uuid
from datetime import datetime, timezone

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.assessment import Assessment, Question
from app.models.response import Response
from app.schemas.assessment import (
    AssessmentOut,
    AssessmentListItem,
    StartAssessmentRequest,
    StartAssessmentResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
)
from ai_engine.coe.observer import coe
from ai_engine.scoring.engine import scoring_engine

router = APIRouter()


@router.get("/", response_model=List[AssessmentListItem])
async def list_assessments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Assessment).where(Assessment.is_active == True).order_by(Assessment.id)
    )
    return result.scalars().all()


@router.get("/{assessment_id}", response_model=AssessmentOut)
async def get_assessment(
    assessment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return assessment


@router.post("/start", response_model=StartAssessmentResponse)
async def start_assessment(
    data: StartAssessmentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.id == data.assessment_id, Assessment.is_active == True)
    )
    assessment = result.scalar_one_or_none()
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    session_id = coe.start_session(current_user.id, assessment.id)

    return StartAssessmentResponse(
        session_id=session_id,
        assessment=assessment,
    )


@router.post("/submit", response_model=SubmitAnswerResponse)
async def submit_answer(
    data: SubmitAnswerRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate question
    q_result = await db.execute(select(Question).where(Question.id == data.question_id))
    question = q_result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    # Extract behavioural features from COE
    features = coe.extract_features(data.session_id, total_time_ms=data.time_spent_seconds * 1000)

    # Score
    content = scoring_engine.score_content(data.answer_text, question.expected_skills)
    process = scoring_engine.score_process(features)
    final = scoring_engine.compute_final(content, process)

    response = Response(
        user_id=current_user.id,
        assessment_id=question.assessment_id,
        question_id=data.question_id,
        session_id=data.session_id,
        answer_text=data.answer_text,
        word_count=data.word_count,
        time_spent_seconds=data.time_spent_seconds,
        content_score=final["content_score"],
        process_score=final["process_score"],
        final_score=final["overall_score"],
        is_submitted=True,
        submitted_at=datetime.now(timezone.utc),
    )
    db.add(response)
    await db.flush()
    await db.refresh(response)

    return SubmitAnswerResponse(
        response_id=response.id,
        content_score=final["content_score"],
        process_score=final["process_score"],
        final_score=final["overall_score"],
    )
