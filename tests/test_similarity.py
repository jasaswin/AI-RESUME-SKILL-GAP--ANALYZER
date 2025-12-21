
import numpy as np
from src.matching.similarity_calculator import SimilarityCalculator

resume_vec = np.array([[0.0, 0.6, 0.0, 0.6, 0.6]])
jd_vec = np.array([[0.5, 0.4, 0.5, 0.4, 0.4]])

score = SimilarityCalculator.cosine_similarity_score(resume_vec, jd_vec)

print("SIMILARITY SCORE:", score)
print("MATCH %:", round(score * 100, 2))
