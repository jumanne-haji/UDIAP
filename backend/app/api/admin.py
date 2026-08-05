from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.models.user import User, UserRole
from app.models.assessment import Assessment, Question
from app.schemas.user import UserOut, UserUpdate
from app.schemas.assessment import AssessmentCreate, AssessmentOut, QuestionCreate

router = APIRouter()


@router.get("/users", response_model=List[UserOut])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPERADMIN])),
):
    result = await db.execute(select(User).order_by(User.id))
    return result.scalars().all()


@router.patch("/users/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPERADMIN])),
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    await db.flush()
    await db.refresh(user)
    return user


@router.post("/assessments", response_model=AssessmentOut)
async def create_assessment(
    data: AssessmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPERADMIN, UserRole.RESEARCHER])),
):
    assessment = Assessment(
        title=data.title,
        description=data.description,
        category=data.category,
        difficulty=data.difficulty,
        estimated_minutes=data.estimated_minutes,
    )
    db.add(assessment)
    await db.flush()

    for q in data.questions or []:
        question = Question(
            assessment_id=assessment.id,
            question_text=q.question_text,
            context=q.context,
            constraints=q.constraints,
            expected_skills=q.expected_skills,
            order_index=q.order_index,
            max_score=q.max_score,
        )
        db.add(question)

    await db.flush()
    await db.refresh(assessment)
    # Reload with questions
    result = await db.execute(
        select(Assessment).where(Assessment.id == assessment.id)
    )
    return result.scalar_one()


@router.get("/monitoring")
async def ai_monitoring(
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.SUPERADMIN])),
):
    # Placeholder metrics – in production pull from real monitoring
    return {
        "model_accuracy": 0.87,
        "avg_processing_time_ms": 420,
        "error_rate": 0.012,
        "active_sessions": 0,
        "status": "healthy",
    }
