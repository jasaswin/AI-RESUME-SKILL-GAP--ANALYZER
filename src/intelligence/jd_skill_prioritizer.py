# src/intelligence/jd_skill_prioritizer.py

class JDSkillPrioritizer:
    """
    Converts JD skills into priority tiers:

    - critical     → must-have (score + readiness blockers)
    - supporting   → trainable (Phase 1–2)
    - contextual   → nice-to-have (Phase 3 only)
    """

    @staticmethod
    def prioritize(
        jd_core: set,
        jd_optional: set,
        role_profile: dict
    ) -> dict:

        jd_core = set(jd_core or [])
        jd_optional = set(jd_optional or [])

        # Role-defined expectations
        critical_defined = set(role_profile.get("critical_core_skills", []))
        trainable_defined = set(role_profile.get("trainable_core_skills", []))

        critical = set()
        supporting = set()
        contextual = set()

        # ---------------- Core skills ----------------
        for skill in jd_core:
            if skill in critical_defined:
                critical.add(skill)
            elif skill in trainable_defined:
                supporting.add(skill)
            else:
                supporting.add(skill)

        # ---------------- Optional skills ----------------
        contextual |= jd_optional

        # ---------------- Safety: remove overlaps ----------------
        contextual -= (critical | supporting)

        # ---------------- Safety: empty core guard ----------------
        if not jd_core and contextual:
            promoted = next(iter(contextual))
            critical.add(promoted)
            contextual.remove(promoted)

        # ---------------- Safety: bounded promotion ----------------
        if not critical and supporting:
            promote_count = min(2, max(1, len(supporting) // 3))
            promoted = set(sorted(supporting)[:promote_count])
            critical |= promoted
            supporting -= promoted

        return {
            "critical": critical,
            "supporting": supporting,
            "contextual": contextual
        }
