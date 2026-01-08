class ResumeArchetypeDetector:
    """
    Classifies resumes into archetypes to stabilize scoring.
    """

    @staticmethod
    def detect(resume_skills: set) -> str:
        frontend = {"react", "javascript", "html", "css"}
        backend = {"python", "django", "flask", "fastapi", "nodejs"}
        data_ml = {"machine learning", "data analysis", "sql", "nlp"}
        business = {"excel", "power bi", "business analysis"}
        devops = {"docker", "aws", "kubernetes"}

        if resume_skills & frontend and resume_skills & backend:
            return "fullstack_generalist"

        if resume_skills & frontend:
            return "frontend_heavy"

        if resume_skills & data_ml:
            return "data_ml_heavy"

        if resume_skills & business:
            return "business_tech"

        if resume_skills & devops:
            return "backend_heavy"

        return "generalist"
