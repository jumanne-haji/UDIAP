"""
AI Report Generation Service
Produces personalized Decision Intelligence reports.
Currently rule-based; architecture ready for LLM integration.
"""

from typing import Dict, Any, List
from ai_engine.scoring.engine import scoring_engine
from ai_engine.hdpm.model import hdpm


class ReportGenerator:
    STRENGTH_THRESHOLDS = {
        "critical_thinking": 70,
        "risk_management": 65,
        "technical_reasoning": 70,
        "communication": 70,
        "adaptability": 65,
        "reflection": 60,
    }

    def generate(
        self,
        answer_text: str,
        behaviour_features: Dict[str, Any],
        expected_skills: str = None,
        user_name: str = "User",
    ) -> Dict[str, Any]:
        # 1. Content scoring
        content = scoring_engine.score_content(answer_text, expected_skills)

        # 2. Process scoring
        process = scoring_engine.score_process(behaviour_features)

        # 3. Final scores
        scores = scoring_engine.compute_final(content, process)

        # 4. HDPM analysis
        hdpm_result = hdpm.analyze(answer_text)

        # 5. Strengths & weaknesses
        strengths, weaknesses = self._extract_strengths_weaknesses(scores)

        # 6. Recommendations
        recommendations = self._generate_recommendations(scores, hdpm_result, weaknesses)

        # 7. Summary
        overall = scores["overall_score"]
        summary = self._build_summary(user_name, overall, strengths, weaknesses)

        return {
            "summary": summary,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "scores": scores,
            "hdpm_analysis": hdpm_result,
            "full_report": {
                "decision_intelligence_score": overall,
                "content_score": scores["content_score"],
                "process_score": scores["process_score"],
                "dimensions": {
                    "critical_thinking": scores["critical_thinking"],
                    "risk_management": scores["risk_management"],
                    "technical_reasoning": scores["technical_reasoning"],
                    "communication": scores["communication"],
                    "adaptability": scores.get("adaptability", scores.get("adaptability_process", 0)),
                    "reflection": scores.get("reflection", scores.get("reflection_score", 0)),
                },
                "hdpm_completeness": hdpm_result["completeness"],
            },
        }

    def _extract_strengths_weaknesses(self, scores: Dict[str, float]):
        strengths = []
        weaknesses = []

        mapping = {
            "critical_thinking": "Analytical & Critical Thinking",
            "risk_management": "Risk Evaluation & Management",
            "technical_reasoning": "Technical Reasoning",
            "communication": "Clear Communication",
            "adaptability": "Adaptability & Flexibility",
            "reflection": "Reflective Thinking",
            "decision_speed_score": "Decision Speed",
            "revision_quality_score": "Revision Quality",
        }

        for key, label in mapping.items():
            val = scores.get(key, 0)
            if val >= 72:
                strengths.append(label)
            elif val < 55:
                weaknesses.append(label)

        if not strengths:
            strengths.append("Foundational Decision Approach")
        if not weaknesses:
            weaknesses.append("Room for deeper risk exploration")

        return strengths[:4], weaknesses[:3]

    def _generate_recommendations(
        self,
        scores: Dict[str, float],
        hdpm_result: Dict[str, Any],
        weaknesses: List[str],
    ) -> List[str]:
        recs = []

        if scores.get("risk_management", 0) < 60:
            recs.append(
                "Practice explicit risk mapping: list 3 potential downsides and "
                "mitigation strategies before finalizing any decision."
            )
        if scores.get("reflection", scores.get("reflection_score", 0)) < 55:
            recs.append(
                "Add a short reflection paragraph at the end of every analysis: "
                "What assumptions did I make? What would change my conclusion?"
            )
        if hdpm_result.get("completeness", 0) < 60:
            missing = hdpm_result.get("missing_stages", [])
            if missing:
                recs.append(
                    f"Strengthen the following decision stages: {', '.join(missing[:3])}. "
                    "Consciously address each stage when structuring your response."
                )
        if scores.get("revision_quality_score", 0) < 60:
            recs.append(
                "Allow time for at least one deliberate revision cycle. "
                "High-quality decision makers usually revise 2–5 times."
            )
        if scores.get("communication", 0) < 65:
            recs.append(
                "Use structured formats (numbered lists, clear sections, summary) "
                "to improve clarity and executive readability."
            )

        if not recs:
            recs.append(
                "Continue refining your decision process. Consider peer review of "
                "complex decisions to surface blind spots."
            )

        return recs[:5]

    def _build_summary(
        self,
        name: str,
        overall: float,
        strengths: List[str],
        weaknesses: List[str],
    ) -> str:
        level = (
            "Exceptional" if overall >= 85
            else "Strong" if overall >= 70
            else "Developing" if overall >= 55
            else "Emerging"
        )
        return (
            f"{name}, your Decision Intelligence Score is {overall:.1f}/100 "
            f"({level}). You demonstrate particular strength in "
            f"{', '.join(strengths[:2])}. "
            f"Focus areas for growth include {', '.join(weaknesses[:2])}."
        )


report_generator = ReportGenerator()
