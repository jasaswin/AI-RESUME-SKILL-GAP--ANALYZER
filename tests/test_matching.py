from src.vectorizer.tfidf_vectorizer import SkillVectorizer
from src.matching.similarity_calculator import SimilarityCalculator

def test_phase_5_similarity():
    resume_skills = ['python', 'sql', 'machine learning', 'nlp']
    jd_skills = ['python', 'sql', 'aws', 'docker']

    resume_text = " ".join(resume_skills)
    jd_text = " ".join(jd_skills)

    vectorizer = SkillVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])

    resume_vector = vectors[0]
    jd_vector = vectors[1]

    score = SimilarityCalculator.cosine_similarity_score(
        resume_vector,
        jd_vector
    )

    print("PHASE 5 SIMILARITY SCORE:", score)
    print("PHASE 5 MATCH %:", round(score * 100, 2))


if __name__ == "__main__":
    test_phase_5_similarity()
