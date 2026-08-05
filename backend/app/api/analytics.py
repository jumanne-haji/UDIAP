from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.genome import DecisionGenome
from app.models.response import Response
from app.models.report import AIReport

router = APIRouter()


@router.get("/dashboard")
async def analytics_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Latest genome
    genome_result = await db.execute(
        select(DecisionGenome)
        .where(DecisionGenome.user_id == current_user.id)
        .order_by(DecisionGenome.created_at.desc())
        .limit(1)
    )
    latest_genome = genome_result.scalar_one_or_none()

    # Score history
    history_result = await db.execute(
        select(DecisionGenome)
        .where(DecisionGenome.user_id == current_user.id)
        .order_by(DecisionGenome.created_at.asc())
        .limit(30)
    )
    history = history_result.scalars().all()

    # Recent assessments count
    count_result = await db.execute(
        select(func.count(Response.id)).where(
            Response.user_id == current_user.id, Response.is_submitted == True
        )
    )
    total_assessments = count_result.scalar() or 0

    return {
        "decision_intelligence_score": latest_genome.overall_score if latest_genome else None,
        "latest_genome": {
            "critical_thinking": latest_genome.critical_thinking_score if latest_genome else 0,
            "risk_management": latest_genome.risk_score if latest_genome else 0,
            "adaptability": latest_genome.adaptability_score if latest_genome else 0,
            "technical_reasoning": latest_genome.technical_reasoning if latest_genome else 0,
            "communication": latest_genome.communication_score if latest_genome else 0,
            "reflection": latest_genome.reflection_score if latest_genome else 0,
        } if latest_genome else None,
        "score_trend": [
            {
                "date": g.created_at.isoformat(),
                "score": g.overall_score,
            }
            for g in history
        ],
        "total_assessments": total_assessments,
    }
