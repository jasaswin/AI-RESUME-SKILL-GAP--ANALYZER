# src/intelligence/resume_rewriter.py

class ResumeRewriter:
    """
    Deterministic resume assembly engine.

    Responsibilities:
    - Place bullets into correct resume sections
    - Enforce upstream routing decisions
    - Enforce resume safety limits
    - NEVER depend on LLMs
    """

    @staticmethod
    def rewrite(
        original_text: str,
        bullet_suggestions: list,
        archetype: str = "general",
        max_skill_bullets: int = 5,
        max_project_bullets: int = 4
    ) -> dict:

        skills_section = []
        project_section = []

        seen_bullets = set()

        for b in bullet_suggestions:
            # ---------------- Defensive extraction ----------------
            bullet = b.get("resume_bullet", "")
            section = b.get("section", "Skills Section")

            if not isinstance(bullet, str):
                continue

            bullet = bullet.strip()
            section = section.strip()

            if not bullet or bullet in seen_bullets:
                continue

            seen_bullets.add(bullet)

            # ---------------- Authoritative routing ----------------
            if section == "Skills Section":
                skills_section.append(bullet)
            elif section == "Projects Section":
                project_section.append(bullet)
            else:
                # 🔒 Hard safety fallback
                skills_section.append(bullet)

        # ---------------- Safety limits ----------------
        skills_section = skills_section[:max_skill_bullets]
        project_section = project_section[:max_project_bullets]

        return {
            "skills_section_additions": skills_section,
            "project_section_additions": project_section
        }
