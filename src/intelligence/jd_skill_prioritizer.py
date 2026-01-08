# src/intelligence/jd_skill_prioritizer.py

class JDSkillPrioritizer:
    """
    Converts JD core skills into priority tiers:
    - critical     → must-have for role (score + readiness blockers)
    - supporting   → trainable skills (Phase 1–2, bullets, fairness)
    - contextual   → nice-to-have, Phase 3 only
    """

    @staticmethod
    def prioritize(jd_core: set, role_profile: dict) -> dict:
        """
        Returns:
        {
            "critical": set,
            "supporting": set,
            "contextual": set
        }
        """

        jd_core = set(jd_core or [])

        # Role-defined expectations (optional, but powerful)
        critical_defined = set(role_profile.get("critical_core_skills", []))
        trainable_defined = set(role_profile.get("trainable_core_skills", []))

        critical = set()
        supporting = set()
        contextual = set()

        for skill in jd_core:
            if skill in critical_defined:
                critical.add(skill)
            elif skill in trainable_defined:
                supporting.add(skill)
            else:
                # Default behavior: entry-level safe
                supporting.add(skill)

        # Safety rule:
        # Never allow all skills to become critical
        if not critical and supporting:
            # Promote top 50% to critical conservatively
            promote_count = max(1, len(supporting) // 2)
            promoted = set(list(supporting)[:promote_count])
            critical |= promoted
            supporting -= promoted

        return {
            "critical": critical,
            "supporting": supporting,
            "contextual": contextual
        }
