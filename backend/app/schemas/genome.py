from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class DecisionGenomeOut(BaseModel):
    id: int
    user_id: int
    assessment_id: Optional[int]
    session_id: Optional[str]
    critical_thinking_score: float
    risk_score: float
    adaptability_score: float
    technical_reasoning: float
    communication_score: float
    reflection_score: float
    decision_speed_score: float
    revision_quality_score: float
    overall_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GenomeSummary(BaseModel):
    overall_score: float
    critical_thinking: float
    risk_management: float
    adaptability: float
    technical_reasoning: float
    communication: float
    reflection: float
