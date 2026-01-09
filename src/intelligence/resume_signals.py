import re


class ResumeSignalAnalyzer:
    """
    Recruiter-style signal extractor (deterministic, high-recall, safe).

    This module is intentionally rule-based and conservative.
    Once stabilized, it SHOULD NOT be frequently modified.
    """

    def analyze(self, resume_text: str) -> dict:
        text = resume_text.lower() if resume_text else ""

        signals = {
            "project_focus": False,
            "deployment_experience": False,
            "problem_solving_signal": False,
            "metrics_signal": False
        }

        # ==================================================
        # 1️⃣ PROJECT FOCUS SIGNAL
        # ==================================================
        # Real-world heuristic:
        # - Multiple projects OR
        # - Stack-heavy descriptions OR
        # - End-to-end system wording
        if (
            re.search(r"\bproject(s)?\b", text)
            or re.search(r"\b(full[- ]?stack|backend|frontend|end[- ]?to[- ]?end)\b", text)
            or text.count("project") >= 2
        ):
            signals["project_focus"] = True

        # ==================================================
        # 2️⃣ DEPLOYMENT EXPERIENCE SIGNAL (CRITICAL FIX)
        # ==================================================
        # Trigger if ANY hosting / production / cloud indicator exists
        deployment_keywords = [
            "deploy", "deployed", "deployment",
            "render", "vercel", "netlify",
            "aws", "ec2", "s3",
            "docker", "container",
            "cloud", "hosted",
            "production", "live api", "live server"
        ]

        if any(k in text for k in deployment_keywords):
            signals["deployment_experience"] = True

        # ==================================================
        # 3️⃣ PROBLEM SOLVING SIGNAL (CRITICAL FIX)
        # ==================================================
        # Recruiter heuristic:
        # - DSA / algorithms
        # - Hackathons
        # - Backend logic
        # - Workflows / alerts / optimization
        problem_solving_keywords = [
            "dsa", "data structures", "algorithm",
            "problem solving", "logic",
            "hackathon", "competitive",
            "optimized", "debugged", "improved",
            "workflow", "alert", "scheduler",
            "backend", "api", "authentication"
        ]

        if any(k in text for k in problem_solving_keywords):
            signals["problem_solving_signal"] = True

        # ==================================================
        # 4️⃣ METRICS / IMPACT SIGNAL
        # ==================================================
        # Numbers, scale, impact indicators
        if re.search(r"\b\d+%|\b\d+x|\b\d+\+\b|\busers\b|\brequests\b", text):
            signals["metrics_signal"] = True

        return signals
