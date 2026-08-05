"""
Cognitive Observer Engine (COE)
Pipeline:
User Interaction → Behaviour Collection → Feature Extraction →
Decision Analysis → Cognitive Scoring → AI Report Generation
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
import uuid


class CognitiveObserverEngine:
    """
    Captures and analyzes the cognitive process behind decisions.
    Designed to run silently in the background without interrupting the user.
    """

    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}

    def start_session(self, user_id: int, assessment_id: int) -> str:
        """Initialize a new cognitive observation session."""
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            "user_id": user_id,
            "assessment_id": assessment_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "events": [],
            "aggregates": {
                "keystrokes": 0,
                "pause_time_ms": 0,
                "total_time_ms": 0,
                "revision_count": 0,
                "deleted_chars": 0,
                "thinking_pause_count": 0,
                "sentence_restructures": 0,
                "alternative_explorations": 0,
            },
        }
        return session_id

    def log_event(self, session_id: str, event: Dict[str, Any]) -> None:
        """
        Ingest a raw behavioural event from the frontend.
        Expected event types: keydown, keyup, pause, delete, paste, restructure, etc.
        """
        if session_id not in self.active_sessions:
            return

        session = self.active_sessions[session_id]
        session["events"].append({
            **event,
            "ts": datetime.now(timezone.utc).isoformat(),
        })

        # Update aggregates on the fly
        agg = session["aggregates"]
        etype = event.get("type")

        if etype == "keystroke":
            agg["keystrokes"] += 1
        elif etype == "pause":
            duration = event.get("duration_ms", 0)
            agg["pause_time_ms"] += duration
            if duration >= 2000:  # thinking pause threshold
                agg["thinking_pause_count"] += 1
        elif etype == "delete":
            agg["deleted_chars"] += event.get("chars", 1)
            agg["revision_count"] += 1
        elif etype == "restructure":
            agg["sentence_restructures"] += 1
            agg["revision_count"] += 1
        elif etype == "alternative":
            agg["alternative_explorations"] += 1

    def extract_features(self, session_id: str, total_time_ms: int = 0) -> Dict[str, Any]:
        """
        Extract temporal + behavioural features for scoring.
        """
        if session_id not in self.active_sessions:
            return self._empty_features()

        session = self.active_sessions[session_id]
        agg = session["aggregates"]

        keystrokes = agg["keystrokes"]
        total_ms = total_time_ms or agg["total_time_ms"] or 1

        # Approximate WPM (5 chars per word average)
        minutes = total_ms / 60000
        typing_speed_wpm = (keystrokes / 5) / minutes if minutes > 0 else 0.0

        return {
            "session_id": session_id,
            "keystrokes": keystrokes,
            "typing_speed_wpm": round(typing_speed_wpm, 2),
            "pause_time_ms": agg["pause_time_ms"],
            "total_time_ms": total_ms,
            "thinking_pause_count": agg["thinking_pause_count"],
            "revision_count": agg["revision_count"],
            "deleted_chars": agg["deleted_chars"],
            "sentence_restructures": agg["sentence_restructures"],
            "alternative_explorations": agg["alternative_explorations"],
            "event_count": len(session["events"]),
        }

    def end_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Finalize and return extracted features."""
        features = self.extract_features(session_id)
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
        return features

    def _empty_features(self) -> Dict[str, Any]:
        return {
            "session_id": None,
            "keystrokes": 0,
            "typing_speed_wpm": 0.0,
            "pause_time_ms": 0,
            "total_time_ms": 0,
            "thinking_pause_count": 0,
            "revision_count": 0,
            "deleted_chars": 0,
            "sentence_restructures": 0,
            "alternative_explorations": 0,
            "event_count": 0,
        }


# Global instance (in production use Redis / DB-backed store)
coe = CognitiveObserverEngine()
