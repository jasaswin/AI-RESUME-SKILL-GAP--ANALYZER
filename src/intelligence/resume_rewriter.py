class ResumeRewriter:
    """
    Assembles an improved resume structure using generated bullets.
    """

    @staticmethod
    def rewrite(original_text: str, bullet_suggestions: list) -> dict:
        skills_section = []
        project_section = []

        for b in bullet_suggestions:
            bullet = b["resume_bullet"]
            priority = b.get("priority", "Low")

            if priority == "High":
                project_section.append(bullet)
            else:
                skills_section.append(bullet)

        return {
            "skills_section_additions": skills_section,
            "project_section_additions": project_section
        }
