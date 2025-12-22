import pdfplumber


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract raw text from a PDF resume
    """
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.strip()


def extract_text_from_txt(file_path: str) -> str:
    """
    Extract raw text from a TXT resume
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_resume_text(file_path: str) -> str:
    """
    Detect file type and extract resume text
    """
    if file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith(".txt"):
        return extract_text_from_txt(file_path)
    else:
        raise ValueError("Unsupported resume format")
