from src.llm.llm_formatter import LLMFormatter


class ReasoningEngine:
    """
    Career guidance chatbot that reasons over AI analysis outputs
    """

    def __init__(self, analysis: dict):
        self.analysis = analysis

    def respond(self, intent: str, question: str) -> str:
        if intent == "READINESS":
            return self._readiness_response()

        if intent == "WHY_SCORE_LOW":
            return self._why_score_low()

        if intent == "WHAT_TO_LEARN_FIRST":
            return self._what_to_learn_first()

        if intent == "TIME_ESTIMATE":
            return self._time_estimate()

        if intent == "SKILL_COMPARISON":
            return self._skill_comparison(question)

        return (
            "I can help you understand your job readiness, "
            "skill gaps, learning roadmap, and priorities."
        )

    # ===============================
    # Intent-specific responses
    # ===============================

    def _readiness_response(self) -> str:
        readiness = self.analysis["career_readiness"]

        return (
            f"You are currently {readiness['readiness_level']}. "
            f"Hiring signal: {readiness['hiring_signal']}."
        )

    def _why_score_low(self) -> str:
        missing = self.analysis["gaps"]["missing_optional_skills"]

        if not missing:
            return "Your score is strong. There are no major missing skills."

        return (
            "Your match score is lower mainly because you are missing "
            f"these skills: {', '.join(missing)}. "
            "These affect deployment and real-world readiness."
        )

    def _what_to_learn_first(self) -> str:
        high_priority = self.analysis["priority_map"]["high_priority"]

        if not high_priority:
            return "You should focus on strengthening existing skills."

        return (
            f"You should start by learning {high_priority[0]}. "
            "It has the highest impact on your job readiness."
        )

    def _time_estimate(self) -> str:
        roadmap = self.analysis["roadmap"]

        if not roadmap:
            return "You are already close to being job-ready."

        total_weeks = sum(step["estimated_weeks"] for step in roadmap)

        return (
            f"Based on your learning roadmap, "
            f"you can be ready to apply in approximately {total_weeks} weeks."
        )

    def _skill_comparison(self, question: str) -> str:
        q = question.lower()

        if "docker" in q and "aws" in q:
            return (
                "Docker should be prioritized first because it directly improves "
                "deployment readiness. AWS can be learned after Docker."
            )

        return (
            "Both skills are useful, but priority depends on your current gaps "
            "and job readiness requirements."
        )
    

class ResponseEngine:
    """
    Adapter layer: Rule-based response → Optional LLM phrasing
    """

    def __init__(self):
        self.formatter = LLMFormatter()

    def respond(self, intent: str, analysis: dict, question: str = "") -> str:
        chatbot = ReasoningEngine(analysis)

        # Step 1: Rule-based response (ground truth)
        rule_based_response = chatbot.respond(intent, question)

        # Step 2: LLM phrasing layer (optional, safe)
        final_response = self.formatter.llm.generate(rule_based_response)

        return final_response



