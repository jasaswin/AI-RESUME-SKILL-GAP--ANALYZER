

# src/explainability/explanation_generator.py

class ExplanationGenerator:
    """
    Generates ML-style explanations for skill matching
    """

    def __init__(self):
        pass

    def generate_explanation(
        self,
        matched_skills: list,
        missing_skills: list,
        core_missing_skills: list,
        similarity_score: float
    ) -> dict:
        """
        Explain model decision using features
        """

        explanation = {
            "summary": "",
            "positive_factors": [],
            "negative_factors": [],
            "model_insight": ""
        }

        # Positive explanations
        if matched_skills:
            explanation["positive_factors"].append(
                f"Resume matches {len(matched_skills)} required skills"
            )

        # Negative explanations
        if missing_skills:
            explanation["negative_factors"].append(
                f"{len(missing_skills)} skills are missing from the resume"
            )

        if core_missing_skills:
            explanation["negative_factors"].append(
                f"Critical skills missing: {', '.join(core_missing_skills)}"
            )

        # Model reasoning
        if similarity_score >= 0.7:
            explanation["summary"] = "Strong match between resume and job role"
            explanation["model_insight"] = (
                "High cosine similarity indicates strong alignment "
                "between skill vectors"
            )
        elif similarity_score >= 0.4:
            explanation["summary"] = "Partial match with noticeable skill gaps"
            explanation["model_insight"] = (
                "Moderate similarity suggests partial overlap in skill space"
            )
        else:
            explanation["summary"] = "Weak match for the given role"
            explanation["model_insight"] = (
                "Low similarity indicates limited overlap in core skills"
            )

        return explanation
