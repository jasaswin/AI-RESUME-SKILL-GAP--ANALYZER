

class SkillGapIdentifier:
    """
    Identifies missing skills and categorizes gaps
    """

    @staticmethod
    def identify_gaps(resume_skills: set, jd_core: set, jd_optional: set):
        """
        Returns missing core and optional skills
        """
        missing_core = sorted(jd_core - resume_skills)
        missing_optional = sorted(jd_optional - resume_skills)

        return {
            "missing_core_skills": missing_core,
            "missing_optional_skills": missing_optional
        }
