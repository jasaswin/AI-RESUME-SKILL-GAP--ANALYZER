

# src/nlp/jd_text_processor.py

import re
import nltk
from nltk.tokenize import sent_tokenize

# Download tokenizer (only first time)
nltk.download('punkt')


class JobDescriptionProcessor:
    """
    Cleans and filters Job Description text
    """

    def __init__(self, raw_text: str):
        self.raw_text = raw_text

    def clean_text(self) -> str:
        """
        Lowercase, remove punctuation, numbers, and extra spaces
        """
        text = self.raw_text.lower()
        text = re.sub(r'[^a-z\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def filter_relevant_sentences(self) -> str:
        """
        Keep only skill-related sentences
        """
        keywords = [
            "skill", "experience", "proficient",
            "required", "must", "knowledge", "familiar"
        ]

        sentences = sent_tokenize(self.raw_text)
        relevant = []

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(word in sentence_lower for word in keywords):
                relevant.append(sentence_lower)

        return " ".join(relevant)

    def process(self) -> str:
        """
        Full JD preprocessing pipeline
        """
        filtered_text = self.filter_relevant_sentences()
        cleaned_text = self.clean_text()
        return cleaned_text
