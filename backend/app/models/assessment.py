"""
Assessment and Question models.
"""

from datetime import datetime, timezone
from sqlalchemy import String, Text, Integer, Float, ForeignKey, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
from app.core.database import Base


class DifficultyLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class AssessmentCategory(str, enum.Enum):
    TECHNICAL = "technical"
    STRATEGIC = "strategic"
    ETHICAL = "ethical"
    OPERATIONAL = "operational"
    RESEARCH = "research"


class Assessment(Base):
    __tablename__ = "assessments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    category: Mapped[AssessmentCategory] = mapped_column(
        SAEnum(AssessmentCategory, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=AssessmentCategory.TECHNICAL
    )
    difficulty: Mapped[DifficultyLevel] = mapped_column(
        SAEnum(DifficultyLevel, native_enum=False, values_callable=lambda x: [e.value for e in x]), default=DifficultyLevel.INTERMEDIATE
    )
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=30)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    questions = relationship("Question", back_populates="assessment", cascade="all, delete-orphan")
    responses = relationship("Response", back_populates="assessment")

    def __repr__(self) -> str:
        return f"<Assessment id={self.id} title={self.title}>"


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessments.id"), nullable=False)
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    context: Mapped[str] = mapped_column(Text, nullable=True)
    constraints: Mapped[str] = mapped_column(Text, nullable=True)
    expected_skills: Mapped[str] = mapped_column(String(500), nullable=True)  # comma-separated
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    max_score: Mapped[float] = mapped_column(Float, default=100.0)

    assessment = relationship("Assessment", back_populates="questions")
    responses = relationship("Response", back_populates="question")

    def __repr__(self) -> str:
        return f"<Question id={self.id} assessment_id={self.assessment_id}>"
