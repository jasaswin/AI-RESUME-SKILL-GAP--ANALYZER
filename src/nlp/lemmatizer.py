from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

# tech terms that should NEVER be lemmatized
PROTECTED_TOKENS = {
    "css", "html", "javascript", "nodejs", "react",
    "git", "github", "aws", "docker", "sql"
}


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    lemmatized = []

    for token in tokens:
        if token in PROTECTED_TOKENS:
            lemmatized.append(token)
        else:
            lemmatized.append(lemmatizer.lemmatize(token))

    return lemmatized
