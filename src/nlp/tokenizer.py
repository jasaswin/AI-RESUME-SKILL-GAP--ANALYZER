import re
import nltk
from nltk.tokenize import word_tokenize

nltk.download("punkt")

# skill-level normalization map (keep SMALL and explicit)
TOKEN_ALIAS_MAP = {
    "css3": "css",
    "html5": "html"
}


def tokenize_text(text: str) -> list[str]:
    """
    Tokenize and normalize input text into clean tokens
    """

    raw_tokens = word_tokenize(text)
    normalized_tokens = []

    for token in raw_tokens:
        token = token.lower()

        # remove punctuation but keep letters/numbers
        token = re.sub(r"[^a-z0-9+#]", "", token)

        if not token:
            continue

        # normalize known variants early
        token = TOKEN_ALIAS_MAP.get(token, token)

        normalized_tokens.append(token)

    return normalized_tokens
