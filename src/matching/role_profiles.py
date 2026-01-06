ROLE_PROFILES = {
    "ai_ml_developer": {
        # 🔹 Role definition
        "core_skills": {
            "python", "machine learning", "nlp", "data analysis", "sql"
        },
        "optional_skills": {
            "deep learning", "docker", "aws", "flask", "power bi", "tableau"
        },

        # 🔹 Scoring config (already used)
        "weights": {
            "tfidf": 0.4,
            "core_coverage": 0.35,
            "optional_coverage": 0.15,
            "depth_bonus": 0.1
        },

        # 🔹 Intelligence config
        "depth_priority": {
            "machine learning", "nlp", "python"
        },

        "missing_core_penalty": 0.35
    },

    "business_analyst": {
        "core_skills": {
            "data analysis", "sql", "excel", "power bi"
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
    }
}
