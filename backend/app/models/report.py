"""
AI Generated Decision Intelligence Report.
"""

from datetime import datetime, timezone
from sqlalchemy import Integer, Text, ForeignKey, DateTime, String, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class AIReport(Base):
    __tablename__ = "ai_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=True)
    genome_id: Mapped[int] = mapped_column(ForeignKey("decision_genome.id"), nullable=True)

    summary: Mapped[str] = mapped_column(Text, nullable=False)
    strengths: Mapped[list] = mapped_column(JSON, default=list)          # list of strings
    weaknesses: Mapped[list] = mapped_column(JSON, default=list)
    recommendations: Mapped[list] = mapped_column(JSON, default=list)

    # HDPM stage analysis
    hdpm_analysis: Mapped[dict] = mapped_column(JSON, nullable=True)

    # Full structured report payload
    full_report: Mapped[dict] = mapped_column(JSON, nullable=True)

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="ai_reports")

    def __repr__(self) -> str:
        return f"<AIReport id={self.id} user={self.user_id}>"
