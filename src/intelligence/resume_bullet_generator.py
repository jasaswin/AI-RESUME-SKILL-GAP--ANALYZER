class RuleBasedBulletGenerator:
    """
    Rule-based fallback bullet generator (phase-aware)
    """

    @staticmethod
    def generate(gap: dict, section: str | None = None) -> dict:
        skill = gap["skill"]
        severity = gap.get("severity", "Medium")

        # 🔥 PROJECT BULLET
        if section == "Projects Section":
            bullet_text = (
                f"• Built an end-to-end project using {skill}, "
                f"including implementation, integration, and documentation."
            )

        # 🔹 SKILL BULLET
        elif severity == "High":
            bullet_text = (
                f"• Developed strong proficiency in {skill} through "
                f"focused practice and applied learning."
            )
        else:
            bullet_text = (
                f"• Gained foundational knowledge of {skill} and applied it "
                f"in guided or academic scenarios."
            )

        return {
            "skill": skill,
            "resume_bullet": bullet_text
        }
