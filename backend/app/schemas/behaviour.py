from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, Dict, Any


class BehaviourLogCreate(BaseModel):
    session_id: str
    response_id: Optional[int] = None
    keystrokes: int = 0
    typing_speed_wpm: float = 0.0
    pause_time_ms: int = 0
    total_time_ms: int = 0
    thinking_pause_count: int = 0
    revision_count: int = 0
    deleted_chars: int = 0
    sentence_restructures: int = 0
    alternative_explorations: int = 0
    event_stream: Optional[Dict[str, Any]] = None


class BehaviourLogOut(BehaviourLogCreate):
    id: int
    user_id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
