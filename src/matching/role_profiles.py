ROLE_PROFILES = {
    "ai_ml_developer": {
        # ---------------- Role Definition ----------------
        "core_skills": {
            "python", "machine learning", "nlp", "data analysis", "sql"
        },

        # 🔴 Severity tiers (CRITICAL FIX)
        "critical_core_skills": {
            "python", "machine learning", "sql"
        },
        "important_core_skills": {
            "data analysis"
        },
        "trainable_core_skills": {
            "nlp"
        },

        "optional_skills": {
            "deep learning", "docker", "aws", "flask", "power bi", "tableau"
        },

        # ---------------- Scoring ----------------
        "weights": {
            "tfidf": 0.4,
            "core_coverage": 0.35,
            "optional_coverage": 0.15,
            "depth_bonus": 0.1
        },

        "depth_priority": {
            "machine learning", "python"
        },

        "missing_core_penalty": 0.35
    },

    "business_analyst": {
        "core_skills": {
            "data analysis", "sql", "excel", "power bi"
        },

        "critical_core_skills": {
            "data analysis", "sql"
        },
        "important_core_skills": {
            "excel"
        },
        "trainable_core_skills": {
            "power bi"
        },

        "optional_skills": {
            "python", "tableau"
        },

        "weights": {
            "tfidf": 0.35,
            "core_coverage": 0.4,
            "optional_coverage": 0.15,
            "depth_bonus": 0.1
        },

        "depth_priority": {
            "data analysis", "sql"
        },

        "missing_core_penalty": 0.25
    },

    "full_stack_developer": {
        "core_skills": {
            "javascript", "html", "css", "react", "nodejs", "sql"
        },

        "critical_core_skills": {
            "javascript", "react", "nodejs"
        },
        "important_core_skills": {
            "html", "css"
        },
        "trainable_core_skills": {
            "sql"
        },

        "optional_skills": {
            "django", "python", "docker", "aws", "git"
        },

        "weights": {
            "tfidf": 0.35,
            "core_coverage": 0.4,
            "optional_coverage": 0.15,
            "depth_bonus": 0.1
        },

        "depth_priority": {
            "javascript", "react", "nodejs"
        },

        "missing_core_penalty": 0.3
    },

    "ux_designer": {
        "core_skills": {
            "ux design", "wireframing", "prototyping",
            "user research", "usability"
        },

        "critical_core_skills": {
            "ux design", "wireframing"
        },
        "important_core_skills": {
            "prototyping", "usability"
        },
        "trainable_core_skills": {
            "user research"
        },

        "optional_skills": {
            "figma", "adobe xd", "user testing"
        },

        "weights": {
            "tfidf": 0.35,
            "core_coverage": 0.4,
            "optional_coverage": 0.15,
            "depth_bonus": 0.1
        },

        "depth_priority": {
            "ux design", "wireframing", "prototyping"
        },

        "missing_core_penalty": 0.25
    }
}
