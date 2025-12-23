class ResumeSignalAnalyzer:
    """
    Extracts recruiter-style signals from resume
    """

    def analyze(self, resume_text: str) -> dict:

        signals = {
            "project_focus": False,
            "deployment_experience": False,
            "problem_solving_signal": False
        }

        text = resume_text.lower()

        if "project" in text:
            signals["project_focus"] = True

        if any(x in text for x in ["docker", "aws", "deploy", "cloud"]):
            signals["deployment_experience"] = True

        if any(x in text for x in ["problem", "optimized", "algorithm", "dsa"]):
            signals["problem_solving_signal"] = True

        return signals
