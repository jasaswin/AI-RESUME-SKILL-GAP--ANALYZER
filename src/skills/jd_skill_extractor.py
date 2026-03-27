# jd skill extractor.py
# import re
# from src.skills.skill_database import SkillDatabase


# class JDSkillExtractor:
#     """
#     Section-aware JD Skill Extractor.
#     Correctly separates required vs optional skills.
#     """

#     def __init__(self):
#         self.skill_db = SkillDatabase()

#         self.required_markers = [
#             "required", "must have", "must", "mandatory"
#         ]

#         self.optional_markers = [
#             "good to have", "preferred", "nice to have"
#         ]

#     # -------------------------------------------------
#     # MAIN METHOD
#     # -------------------------------------------------
#     def extract_skills(self, jd_text: str) -> dict:

#         lines = jd_text.lower().split("\n")

#         core_skills = set()
#         optional_skills = set()

#         current_section = None

#         for line in lines:
#             line = line.strip()

#             if not line:
#                 continue

#             # ---------------------------
#             # Detect section changes
#             # ---------------------------
#             if any(marker in line for marker in self.required_markers):
#                 current_section = "core"
#                 continue

#             if any(marker in line for marker in self.optional_markers):
#                 current_section = "optional"
#                 continue

#             # ---------------------------
#             # Extract skills from line
#             # ---------------------------
#             tokens = re.split(r"[,\s/]+", line)

#             for token in tokens:
#                 token = token.strip()

#                 if not token:
#                     continue

#                 normalized = self.skill_db.normalize_skill(token)

#                 if self.skill_db.is_valid_skill(normalized):
#                     if current_section == "core":
#                         core_skills.add(normalized)
#                     elif current_section == "optional":
#                         optional_skills.add(normalized)

#         return {
#             "core_skills": sorted(list(core_skills)),
#             "optional_skills": sorted(list(optional_skills))
#         }





# import re
# from src.skills.skill_database import SkillDatabase


# class JDSkillExtractor:
#     """
#     Robust JD Skill Extractor.
#     Works for:
#     - Multi-line JD
#     - Single-line JD (like Swagger input)
#     - Paragraph JD
#     """

#     def __init__(self):
#         self.skill_db = SkillDatabase()

#         self.required_markers = [
#             "required", "must have", "mandatory"
#         ]

#         self.optional_markers = [
#             "good to have", "preferred", "nice to have"
#         ]

#     def extract_skills(self, jd_text: str) -> dict:

#         jd_text = jd_text.lower()

#         core_skills = set()
#         optional_skills = set()

#         current_section = None

#         lines = jd_text.split("\n")

#         for line in lines:
#             line = line.strip()

#             if not line:
#                 continue

#             # -------- Detect section --------
#             if any(marker in line for marker in self.required_markers):
#                 current_section = "core"

#             elif any(marker in line for marker in self.optional_markers):
#                 current_section = "optional"

#             # -------- Extract skills from same line --------
#             tokens = re.split(r"[,\s/:\.-]+", line)

#             for token in tokens:
#                 token = token.strip()
#                 if not token:
#                     continue

#                 normalized = self.skill_db.normalize_skill(token)

#                 if self.skill_db.is_valid_skill(normalized):
#                     if current_section == "core":
#                         core_skills.add(normalized)
#                     elif current_section == "optional":
#                         optional_skills.add(normalized)

#         return {
#             "core_skills": sorted(list(core_skills)),
#             "optional_skills": sorted(list(optional_skills))
#         }




import re
from src.skills.skill_database import SkillDatabase


class JDSkillExtractor:
    """
    Robust JD Skill Extractor.

    Guarantees:
    - Handles Node.js
    - Handles punctuation
    - Handles single-line JD
    - Handles paragraph JD
    - Uses alias normalization
    """

    def __init__(self):
        self.skill_db = SkillDatabase()

        self.required_markers = [
            "required", "must have", "mandatory"
        ]

        self.optional_markers = [
            "good to have", "preferred", "nice to have"
        ]

    # -------------------------------------------------
    # MAIN METHOD
    # -------------------------------------------------
    def extract_skills(self, jd_text: str) -> dict:

        if not jd_text:
            return {"core_skills": [], "optional_skills": []}

        jd_text = jd_text.lower()

        core_skills = set()
        optional_skills = set()
        current_section = None

        lines = jd_text.split("\n")

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # ---------------------------
            # Detect Section
            # ---------------------------
            if any(marker in line for marker in self.required_markers):
                current_section = "core"

            elif any(marker in line for marker in self.optional_markers):
                current_section = "optional"

            # ---------------------------
            # Clean punctuation safely
            # ---------------------------
            clean_line = re.sub(r"[^\w\s/]", " ", line)

            tokens = re.split(r"[\s/]+", clean_line)

            for token in tokens:
                token = token.strip()
                if not token:
                    continue

                normalized = self.skill_db.normalize_skill(token)

                if self.skill_db.is_valid_skill(normalized):
                    if current_section == "core":
                        core_skills.add(normalized)
                    elif current_section == "optional":
                        optional_skills.add(normalized)

        return {
            "core_skills": sorted(list(core_skills)),
            "optional_skills": sorted(list(optional_skills))
        }
