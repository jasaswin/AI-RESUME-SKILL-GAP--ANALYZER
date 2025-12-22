
# tests/test_explainability.py

from src.explainability.confidence_score import ConfidenceScorer
from src.explainability.explanation_generator import ExplanationGenerator

# Mock inputs (from earlier phases)
similarity_score = 0.65
matched_skills = ["python", "sql", "docker"]
missing_skills = ["aws", "kubernetes"]
core_missing_skills = ["aws"]

# Confidence scoring
confidence_scorer = ConfidenceScorer()
confidence = confidence_scorer.compute_confidence(
    similarity_score,
    matched_skills,
    total_job_skills=5
)

print("CONFIDENCE SCORE:", confidence, "%")

# Explanation
explainer = ExplanationGenerator()
explanation = explainer.generate_explanation(
    matched_skills,
    missing_skills,
    core_missing_skills,
    similarity_score
)

print("\nEXPLANATION:")
for key, value in explanation.items():
    print(f"{key.upper()}: {value}")
