import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")


def tokenize_text(text: str) -> list:
    """
    Tokenize input text into words
    """
    return word_tokenize(text)
