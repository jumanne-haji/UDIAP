"""
User response to assessment questions.
"""

from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class Response(Base):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, default=0)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0)

    # Scores (filled by scoring engine)
    content_score: Mapped[float] = mapped_column(Float, nullable=True)
    process_score: Mapped[float] = mapped_column(Float, nullable=True)
    final_score: Mapped[float] = mapped_column(Float, nullable=True)

    is_submitted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="responses")
    assessment = relationship("Assessment", back_populates="responses")
    question = relationship("Question", back_populates="responses")

    def __repr__(self) -> str:
        return f"<Response id={self.id} user={self.user_id} score={self.final_score}>"
