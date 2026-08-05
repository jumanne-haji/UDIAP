from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional, Dict, Any


class AIReportOut(BaseModel):
    id: int
    user_id: int
    assessment_id: Optional[int]
    session_id: Optional[str]
    summary: str
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    hdpm_analysis: Optional[Dict[str, Any]]
    full_report: Optional[Dict[str, Any]]
    generated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GenerateReportRequest(BaseModel):
    session_id: str
    assessment_id: Optional[int] = None
