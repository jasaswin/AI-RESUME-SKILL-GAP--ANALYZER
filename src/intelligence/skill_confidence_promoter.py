class SkillConfidencePromoter:
    @staticmethod
    def promote(resume_skills, inferred_skills, skill_depths):
        promoted = set()

        for skill in inferred_skills:
            depth = skill_depths.get(skill)
            if depth in {"intermediate", "advanced"}:
                promoted.add(skill)

        return promoted
