from src.intelligence.career_readiness import CareerReadinessAnalyzer

analyzer = CareerReadinessAnalyzer()

result = analyzer.analyze(
    final_match_percentage=62.15,
    confidence=57.69,
    missing_core_skills=[],
    missing_optional_skills=["aws", "docker"]
)

print("CAREER READINESS RESULT:")
print(result)
