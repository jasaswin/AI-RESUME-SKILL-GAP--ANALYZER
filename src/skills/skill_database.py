

import csv
import json
from pathlib import Path


class SkillDatabase:
    """
    Loads and manages master skill list and skill aliases
    """

    def __init__(self):
        base_path = Path(__file__).resolve().parents[2]

        self.skill_csv_path = base_path / "data" / "skills" / "master_skills.csv"
        self.alias_json_path = base_path / "data" / "skills" / "skill_alias.json"

        self.skills = self._load_skills()
        self.aliases = self._load_aliases()

        
        print("ALIASES LOADED:", self.aliases)

    def _load_skills(self) -> dict:
        """
        Load skills from CSV safely (handles Excel BOM issue)
        """
        skills = {}

        with open(self.skill_csv_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {"skill", "category"}
            if not required_columns.issubset(set(reader.fieldnames)):
                raise ValueError(
                    f"CSV must contain columns: {required_columns}, "
                    f"found: {reader.fieldnames}"
                )

            for row in reader:
                skill = row["skill"].strip().lower()
                category = row["category"].strip().lower()
                skills[skill] = category

        return skills

    def _load_aliases(self) -> dict:
        """
        Load skill aliases (optional)
        """
        if not self.alias_json_path.exists():
            return {}

        with open(self.alias_json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def normalize_skill(self, skill: str) -> str:
        """
        Convert alias to standard skill name
        """
        skill = skill.lower().strip()
        return self.aliases.get(skill, skill)

    def is_valid_skill(self, skill: str) -> bool:
        """
        Check if skill exists in master database
        """
        skill = self.normalize_skill(skill)
        return skill in self.skills

    def get_category(self, skill: str) -> str | None:
        """
        Get category of a skill
        """
        skill = self.normalize_skill(skill)
        return self.skills.get(skill)
