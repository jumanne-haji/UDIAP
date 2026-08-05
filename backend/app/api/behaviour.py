from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.behaviour import BehaviourLog
from app.schemas.behaviour import BehaviourLogCreate, BehaviourLogOut
from ai_engine.coe.observer import coe

router = APIRouter()


@router.post("/log", response_model=BehaviourLogOut)
async def log_behaviour(
    data: BehaviourLogCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Also feed the in-memory COE
    coe.log_event(data.session_id, {
        "type": "batch",
        "keystrokes": data.keystrokes,
        "pause": data.pause_time_ms,
        "revision": data.revision_count,
    })

    log = BehaviourLog(
        user_id=current_user.id,
        session_id=data.session_id,
        response_id=data.response_id,
        keystrokes=data.keystrokes,
        typing_speed_wpm=data.typing_speed_wpm,
        pause_time_ms=data.pause_time_ms,
        total_time_ms=data.total_time_ms,
        thinking_pause_count=data.thinking_pause_count,
        revision_count=data.revision_count,
        deleted_chars=data.deleted_chars,
        sentence_restructures=data.sentence_restructures,
        alternative_explorations=data.alternative_explorations,
        event_stream=data.event_stream,
    )
    db.add(log)
    await db.flush()
    await db.refresh(log)
    return log
