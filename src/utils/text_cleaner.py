import re
from nltk.corpus import stopwords
import nltk

nltk.download("stopwords")

STOP_WORDS = set(stopwords.words("english"))


def clean_text(text: str) -> str:
    """
    Clean raw resume text
    """
    text = text.lower()
    text = re.sub(r"\S+@\S+", " ", text)
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"[^a-zA-Z ]", " ", text)

    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS]

    return " ".join(tokens)
