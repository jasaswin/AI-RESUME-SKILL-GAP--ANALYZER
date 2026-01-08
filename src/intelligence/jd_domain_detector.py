class JDDomainDetector:
    """
    Detects the primary domain of a Job Description
    using conservative keyword overlap.
    """

    DOMAIN_KEYWORDS = {
        "engineering": {
            "python", "java", "javascript", "api", "backend",
            "frontend", "react", "nodejs", "ml", "machine learning",
            "nlp", "sql", "docker", "aws"
        },
        "analytics": {
            "data analysis", "analysis", "dashboard", "reporting",
            "visualization", "sql", "excel", "power bi", "tableau",
            "metrics", "kpi"
        },
        "design": {
            "ux", "user experience", "wireframe", "wireframing",
            "prototype", "prototyping", "figma", "adobe xd",
            "usability", "accessibility", "user research"
        },
        "business": {
            "business analysis", "stakeholder", "requirements",
            "process", "workflow", "documentation", "client"
        }
    }

    @classmethod
    def detect(cls, jd_text: str) -> str:
        text = jd_text.lower()
        scores = {}

        for domain, keywords in cls.DOMAIN_KEYWORDS.items():
            scores[domain] = sum(1 for k in keywords if k in text)

        # pick domain with max overlap
        best_domain = max(scores, key=scores.get)

        # safety fallback
        if scores[best_domain] == 0:
            return "engineering"

        return best_domain
