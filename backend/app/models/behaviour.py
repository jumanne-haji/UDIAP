"""
Cognitive Observer Engine – Behaviour Logs.
Captures temporal and behavioural features during assessment.
"""

from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base


class BehaviourLog(Base):
    __tablename__ = "behaviour_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    session_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    response_id: Mapped[int] = mapped_column(ForeignKey("responses.id"), nullable=True)

    # Temporal features
    keystrokes: Mapped[int] = mapped_column(Integer, default=0)
    typing_speed_wpm: Mapped[float] = mapped_column(Float, default=0.0)
    pause_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    total_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    thinking_pause_count: Mapped[int] = mapped_column(Integer, default=0)

    # Behaviour features
    revision_count: Mapped[int] = mapped_column(Integer, default=0)
    deleted_chars: Mapped[int] = mapped_column(Integer, default=0)
    sentence_restructures: Mapped[int] = mapped_column(Integer, default=0)
    alternative_explorations: Mapped[int] = mapped_column(Integer, default=0)

    # Raw event stream (optional detailed log)
    event_stream: Mapped[dict] = mapped_column(JSON, nullable=True)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    user = relationship("User", back_populates="behaviour_logs")

    def __repr__(self) -> str:
        return f"<BehaviourLog session={self.session_id} speed={self.typing_speed_wpm}>"
