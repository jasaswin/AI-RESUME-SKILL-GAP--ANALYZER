
import pdfplumber


def extract_text_from_pdf(file) -> str:
    """
    Extracts text from uploaded PDF file.
    """

    text = ""

    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text.strip()