

from sklearn.feature_extraction.text import TfidfVectorizer


class SkillVectorizer:
    """
    Converts skill text into TF-IDF vectors
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform(self, texts: list[str]):
        """
        Fit TF-IDF on given texts and return vectors
        """
        return self.vectorizer.fit_transform(texts)

    def transform(self, texts: list[str]):
        """
        Transform new texts using existing TF-IDF model
        """
        return self.vectorizer.transform(texts)

    def get_feature_names(self):
        """
        Get feature (skill) names
        """
        return self.vectorizer.get_feature_names_out()
