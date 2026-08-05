"""
UDIAP Scoring Engine
FINAL SCORE = (Content Score × 0.60) + (Process Score × 0.40)
"""

from typing import Dict, Any, Optional
import re
import math


class ScoringEngine:
    """
    Rule-based scoring engine ready for future ML models.
    Content Score focuses on quality of reasoning.
    Process Score focuses on cognitive behaviour captured by COE.
    """

    CONTENT_WEIGHT = 0.60
    PROCESS_WEIGHT = 0.40

    # Keyword indicators for content analysis (simplified rule-based)
    CRITICAL_THINKING_MARKERS = [
        "because", "therefore", "however", "although", "consequently",
        "evidence", "analysis", "evaluate", "compare", "contrast",
        "assumption", "implication", "trade-off", "tradeoff"
    ]
    RISK_MARKERS = [
        "risk", "probability", "uncertainty", "mitigation", "contingency",
        "downside", "upside", "scenario", "worst case", "best case",
        "likelihood", "impact", "exposure"
    ]
    TECHNICAL_MARKERS = [
        "algorithm", "architecture", "performance", "scalability",
        "constraint", "optimization", "complexity", "tradeoff",
        "implementation", "prototype", "metric", "benchmark"
    ]
    COMMUNICATION_MARKERS = [
        "first", "second", "finally", "in summary", "to conclude",
        "for example", "specifically", "clearly", "importantly"
    ]
    ADAPTABILITY_MARKERS = [
        "alternative", "option", "pivot", "adapt", "flexible",
        "if", "else", "depending", "context", "situation"
    ]
    REFLECTION_MARKERS = [
        "i learned", "in retrospect", "looking back", "next time",
        "limitation", "bias", "assumption", "uncertainty"
    ]

    def score_content(self, answer_text: str, expected_skills: Optional[str] = None) -> Dict[str, float]:
        """
        Analyze the textual content of the answer.
        Returns dimension scores 0-100.
        """
        text = answer_text.lower()
        words = re.findall(r'\b\w+\b', text)
        word_count = len(words)

        if word_count < 20:
            # Too short – penalize heavily
            base = max(10.0, word_count * 1.5)
            return {
                "critical_thinking": base * 0.7,
                "risk_management": base * 0.6,
                "technical_reasoning": base * 0.7,
                "communication": base * 0.8,
                "adaptability": base * 0.5,
                "reflection": base * 0.4,
                "content_score": base,
            }

        def density(markers: list) -> float:
            count = sum(1 for m in markers if m in text)
            # Normalize by log of word count to avoid long-text bias
            return min(100.0, (count / max(1, math.log(word_count + 1))) * 35)

        critical = density(self.CRITICAL_THINKING_MARKERS)
        risk = density(self.RISK_MARKERS)
        technical = density(self.TECHNICAL_MARKERS)
        communication = density(self.COMMUNICATION_MARKERS)
        adaptability = density(self.ADAPTABILITY_MARKERS)
        reflection = density(self.REFLECTION_MARKERS)

        # Structure bonus (lists, numbered points, paragraphs)
        structure_bonus = 0.0
        if re.search(r'\n\s*[-•*]\s', answer_text) or re.search(r'\n\s*\d+\.', answer_text):
            structure_bonus += 8.0
        if answer_text.count("\n\n") >= 2:
            structure_bonus += 5.0

        # Length quality (sweet spot ~150-400 words)
        length_score = 100.0
        if word_count < 80:
            length_score = 60 + (word_count / 80) * 30
        elif word_count > 600:
            length_score = max(70.0, 100 - (word_count - 600) * 0.05)

        content_score = (
            critical * 0.22 +
            risk * 0.18 +
            technical * 0.20 +
            communication * 0.15 +
            adaptability * 0.13 +
            reflection * 0.12 +
            structure_bonus
        )
        content_score = min(100.0, content_score * (length_score / 100))

        return {
            "critical_thinking": round(min(100, critical + structure_bonus * 0.3), 2),
            "risk_management": round(min(100, risk), 2),
            "technical_reasoning": round(min(100, technical + structure_bonus * 0.2), 2),
            "communication": round(min(100, communication + structure_bonus), 2),
            "adaptability": round(min(100, adaptability), 2),
            "reflection": round(min(100, reflection), 2),
            "content_score": round(content_score, 2),
        }

    def score_process(self, behaviour: Dict[str, Any]) -> Dict[str, float]:
        """
        Score cognitive process features from BehaviourLog.
        """
        typing_speed = behaviour.get("typing_speed_wpm", 40.0)
        pause_ms = behaviour.get("pause_time_ms", 0)
        total_ms = behaviour.get("total_time_ms", 1)
        revision_count = behaviour.get("revision_count", 0)
        deleted_chars = behaviour.get("deleted_chars", 0)
        thinking_pauses = behaviour.get("thinking_pause_count", 0)
        sentence_restructures = behaviour.get("sentence_restructures", 0)

        # Decision Speed (optimal 30-70 WPM, reasonable total time)
        if 30 <= typing_speed <= 75:
            speed_score = 85 + (5 if 40 <= typing_speed <= 60 else 0)
        elif typing_speed < 20:
            speed_score = 40
        elif typing_speed > 100:
            speed_score = 55  # possible copy-paste or rushed
        else:
            speed_score = 70

        # Thinking pauses are positive (reflection)
        pause_ratio = pause_ms / max(total_ms, 1)
        if 0.15 <= pause_ratio <= 0.45:
            pause_score = 90
        elif pause_ratio < 0.05:
            pause_score = 45  # almost no thinking
        else:
            pause_score = 70

        # Revision quality
        if 2 <= revision_count <= 8:
            revision_score = 88
        elif revision_count == 0:
            revision_score = 50  # no revision
        elif revision_count > 15:
            revision_score = 55  # over-editing / indecision
        else:
            revision_score = 75

        # Adaptability via restructuring
        adapt_score = min(95, 50 + sentence_restructures * 12 + thinking_pauses * 5)

        process_score = (
            speed_score * 0.30 +
            pause_score * 0.25 +
            revision_score * 0.25 +
            adapt_score * 0.20
        )

        return {
            "decision_speed_score": round(speed_score, 2),
            "reflection_score": round(pause_score, 2),
            "revision_quality_score": round(revision_score, 2),
            "adaptability_process": round(adapt_score, 2),
            "process_score": round(process_score, 2),
        }

    def compute_final(
        self,
        content: Dict[str, float],
        process: Dict[str, float],
    ) -> Dict[str, float]:
        content_score = content.get("content_score", 50.0)
        process_score = process.get("process_score", 50.0)

        final = (content_score * self.CONTENT_WEIGHT) + (process_score * self.PROCESS_WEIGHT)

        return {
            **content,
            **process,
            "overall_score": round(final, 2),
            "content_score": content_score,
            "process_score": process_score,
        }


# Singleton instance
scoring_engine = ScoringEngine()
