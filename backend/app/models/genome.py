"""
Decision Genome – the cognitive profile of a user.
Aggregated scores across multiple dimensions.
"""

from datetime import datetime, timezone
from sqlalchemy import Integer, Float, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class DecisionGenome(Base):
    __tablename__ = "decision_genome"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=True)

    # Core cognitive dimensions (0-100)
    critical_thinking_score: Mapped[float] = mapped_column(Float, default=0.0)
    risk_score: Mapped[float] = mapped_column(Float, default=0.0)
    adaptability_score: Mapped[float] = mapped_column(Float, default=0.0)
    technical_reasoning: Mapped[float] = mapped_column(Float, default=0.0)
    communication_score: Mapped[float] = mapped_column(Float, default=0.0)
    reflection_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Process scores
    decision_speed_score: Mapped[float] = mapped_column(Float, default=0.0)
    revision_quality_score: Mapped[float] = mapped_column(Float, default=0.0)

    overall_score: Mapped[float] = mapped_column(Float, default=0.0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="decision_genomes")

    def __repr__(self) -> str:
        return f"<DecisionGenome user={self.user_id} overall={self.overall_score}>"
