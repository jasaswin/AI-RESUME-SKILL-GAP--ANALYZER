class ResumeSuggestionEngine:
    """
    Generates deterministic, prioritized resume improvement suggestions
    """

    def generate(
        self,
        resume_text: str,
        missing_skills: list,
        resume_signals: dict
    ) -> list:

        suggestions = []
        text = resume_text.lower()

        # 1️⃣ Critical skill gaps
        if missing_skills:
            suggestions.append(
                f"Add 1–2 projects demonstrating hands-on usage of {', '.join(missing_skills[:3])}."
            )

        # 2️⃣ Missing project focus
        if not resume_signals.get("project_focus"):
            suggestions.append(
                "Add a Projects section highlighting tools used, problems solved, and outcomes."
            )

        # 3️⃣ Missing metrics
        if not resume_signals.get("metrics_signal"):
            suggestions.append(
                "Include measurable impact (e.g., performance %, users impacted, latency reduced)."
            )

        # 4️⃣ Missing deployment exposure
        if not resume_signals.get("deployment_experience"):
            suggestions.append(
                "Mention deployment or hosting experience (Docker, cloud, or CI/CD pipelines)."
            )

        return suggestions
