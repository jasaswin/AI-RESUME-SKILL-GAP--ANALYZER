class MatchResult:
    def __init__(self, similarity_score: float):
        self.similarity_score = similarity_score
        self.match_percentage = round(similarity_score * 100, 2)

    def to_dict(self):
        return {
            "similarity_score": self.similarity_score,
            "match_percentage": self.match_percentage
        }
