
from src.nlp.jd_text_processor import JobDescriptionProcessor

jd_text = """
We are looking for a Data Analyst.
Required skills: Python, SQL, Power BI.
Good communication skills required.
"""

processor = JobDescriptionProcessor(
    "data/job_descriptions/ai_ml_developer.txt"
)
cleaned = processor.process()

print(cleaned)
