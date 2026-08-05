"""
Human Decision Process Model (HDPM)
EVENT → PERCEPTION → INTERPRETATION → PREDICTION →
DECISION → ACTION → OUTCOME → REFLECTION
"""

from typing import Dict, Any, List
import re


class HumanDecisionProcessModel:
    """
    Analyzes a written response against the classic stages of human decision making.
    Returns a structured breakdown that feeds into the AI report.
    """

    STAGES = [
        "event",
        "perception",
        "interpretation",
        "prediction",
        "decision",
        "action",
        "outcome",
        "reflection",
    ]

    STAGE_MARKERS = {
        "event": ["situation", "problem", "challenge", "event", "occurred", "happened"],
        "perception": ["noticed", "observed", "saw", "detected", "aware", "recognized"],
        "interpretation": ["means", "implies", "suggests", "indicates", "because", "reason"],
        "prediction": ["will", "likely", "expect", "forecast", "anticipate", "outcome if"],
        "decision": ["decide", "choose", "select", "opt", "recommend", "should", "will do"],
        "action": ["implement", "execute", "deploy", "start", "take action", "steps"],
        "outcome": ["result", "resulted", "achieved", "impact", "consequence", "effect"],
        "reflection": ["learned", "in retrospect", "next time", "limitation", "bias", "would"],
    }

    def analyze(self, answer_text: str) -> Dict[str, Any]:
        text = answer_text.lower()
        stage_scores: Dict[str, float] = {}
        stage_evidence: Dict[str, List[str]] = {}

        for stage in self.STAGES:
            markers = self.STAGE_MARKERS[stage]
            hits = [m for m in markers if m in text]
            score = min(100.0, len(hits) * 22 + (8 if hits else 0))
            stage_scores[stage] = round(score, 1)
            stage_evidence[stage] = hits[:5]

        # Overall process completeness
        covered = sum(1 for s in stage_scores.values() if s >= 30)
        completeness = round((covered / len(self.STAGES)) * 100, 1)

        # Dominant stages
        sorted_stages = sorted(stage_scores.items(), key=lambda x: x[1], reverse=True)
        dominant = [s[0] for s in sorted_stages[:3]]

        return {
            "stages": stage_scores,
            "evidence": stage_evidence,
            "completeness": completeness,
            "dominant_stages": dominant,
            "missing_stages": [s for s, sc in stage_scores.items() if sc < 25],
            "narrative": self._build_narrative(stage_scores, completeness),
        }

    def _build_narrative(self, scores: Dict[str, float], completeness: float) -> str:
        if completeness >= 75:
            return (
                "The response demonstrates a mature decision process covering most "
                "stages of the Human Decision Process Model."
            )
        if completeness >= 50:
            return (
                "The decision process is partially developed. Some critical stages "
                "(especially prediction or reflection) appear under-represented."
            )
        return (
            "The response shows a limited decision process. Strengthening perception, "
            "prediction and reflection stages would significantly improve decision quality."
        )


hdpm = HumanDecisionProcessModel()
