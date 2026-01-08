import re

class ResumeSignalAnalyzer:
    """
    Extracts recruiter-style signals from resume (deterministic fallback)
    """

    def analyze(self, resume_text: str) -> dict:
        text = resume_text.lower()

        signals = {
            "project_focus": False,
            "deployment_experience": False,
            "problem_solving_signal": False,
            "metrics_signal": False
        }

        # Project signal
        if re.search(r"\bproject(s)?\b", text):
            signals["project_focus"] = True

        # Deployment signal
        if any(x in text for x in ["docker", "aws", "deploy", "cloud", "hosted"]):
            signals["deployment_experience"] = True

        # Problem solving signal
        if any(x in text for x in ["optimized", "debugged", "improved", "algorithm"]):
            signals["problem_solving_signal"] = True

        # Metrics / impact signal
        if re.search(r"\b\d+%|\b\d+x|\b\d+\+\b", text):
            signals["metrics_signal"] = True

        return signals
