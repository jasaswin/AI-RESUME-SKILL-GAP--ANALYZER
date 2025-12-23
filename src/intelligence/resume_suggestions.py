class ResumeSuggestionEngine:
    """
    Generates actionable resume improvement suggestions
    """

    def generate(
        self,
        resume_text: str,
        resume_skills: set,
        missing_skills: list
    ) -> list:

        suggestions = []

        # 1️⃣ Missing critical skills
        if missing_skills:
            suggestions.append(
                f"Add projects demonstrating {', '.join(missing_skills)} usage."
            )

        # 2️⃣ Project mentions
        if "project" not in resume_text.lower():
            suggestions.append(
                "Include a dedicated Projects section with outcomes and tools used."
            )

        # 3️⃣ Metrics & impact
        if "%" not in resume_text and "improved" not in resume_text.lower():
            suggestions.append(
                "Add measurable impact (e.g., performance improvement, accuracy, users)."
            )

        # 4️⃣ Deployment signal
        if not any(x in resume_text.lower() for x in ["docker", "aws", "deploy"]):
            suggestions.append(
                "Mention deployment experience (Docker, cloud, or hosting)."
            )

        return suggestions
