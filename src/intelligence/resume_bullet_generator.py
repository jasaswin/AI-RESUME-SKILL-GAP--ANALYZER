# src/intelligence/resume_bullet_generator.py

class RuleBasedBulletGenerator:
    """
    Rule-based fallback bullet generator
    """

    @staticmethod
    def generate(gap: dict) -> dict:
        skill = gap["skill"]
        severity = gap["severity"]

        if severity == "High":
            bullet_text = (
                f"• Developed hands-on experience with {skill} through "
                f"real-world projects, focusing on practical applications."
            )
        else:
            bullet_text = (
                f"• Gained foundational knowledge of {skill} and applied it "
                f"in academic or practice-based scenarios."
            )

        return {
            "skill": skill,
            "resume_bullet": bullet_text
        }
