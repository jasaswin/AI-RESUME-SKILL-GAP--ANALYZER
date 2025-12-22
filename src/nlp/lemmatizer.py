import nltk
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()


def lemmatize_tokens(tokens: list) -> list:
    """
    Lemmatize list of tokens
    """
    return [lemmatizer.lemmatize(token) for token in tokens]
