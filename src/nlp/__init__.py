from src.nlp.resume_text_extractor import extract_resume_text
from src.utils.text_cleaner import clean_text
from src.nlp.tokenizer import tokenize_text
from src.nlp.lemmatizer import lemmatize_tokens


def process_resume(file_path: str) -> list:
    """
    End-to-end resume NLP pipeline
    """
    raw_text = extract_resume_text(file_path)
    cleaned_text = clean_text(raw_text)
    tokens = tokenize_text(cleaned_text)
    lemmatized_tokens = lemmatize_tokens(tokens)
    return lemmatized_tokens
