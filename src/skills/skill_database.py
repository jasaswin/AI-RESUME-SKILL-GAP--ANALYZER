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

        self.skill_clusters = self._build_skill_clusters()

        self.skills = self._load_skills()
        self.aliases = self._load_aliases()

    # --------------------------------------------------
    # Cluster logic (used for inference only)
    # --------------------------------------------------
    def _build_skill_clusters(self) -> dict:
        """
        Defines logical skill groupings used for inference
        """
        return {
            "dsa_cluster": {
                "algorithms",
                "data structures",
                "problem solving"
            },
            "backend_cluster": {
                "python",
                "java",
                "nodejs",
                "flask"
            },
            "ml_cluster": {
                "machine learning",
                "data analysis",
                "deep learning",
                "nlp"
            }
        }

    # --------------------------------------------------
    # Skill loading
    # --------------------------------------------------
    def _load_skills(self) -> dict:
        """
        Load skills from CSV safely (handles Excel BOM issue)
        """
        skills = {}

        with open(self.skill_csv_path, mode="r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {"skill", "category", "domain", "base_weight"}
            if not required_columns.issubset(set(reader.fieldnames)):
                raise ValueError(
                    f"CSV must contain columns: {required_columns}, "
                    f"found: {reader.fieldnames}"
                )

            for row in reader:
                skill = row["skill"].strip().lower()

                skills[skill] = {
                    "category": row["category"].strip().lower(),
                    "domain": row["domain"].strip().lower(),
                    "weight": float(row["base_weight"])
                }

        return skills

    def _load_aliases(self) -> dict:
        """
        Load skill aliases (optional)
        """
        if not self.alias_json_path.exists():
            return {}

        with open(self.alias_json_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # --------------------------------------------------
    # Normalization helpers
    # --------------------------------------------------
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
        return self.skills.get(skill, {}).get("category")

    def get_domain(self, skill: str) -> str | None:
        """
        Get domain of a skill
        """
        skill = self.normalize_skill(skill)
        return self.skills.get(skill, {}).get("domain")

    def get_weight(self, skill: str) -> float:
        """
        Get base importance weight of a skill
        """
        skill = self.normalize_skill(skill)
        return self.skills.get(skill, {}).get("weight", 1.0)

    # --------------------------------------------------
    # 🔥 NEW: Domain detection (JD-level)
    # --------------------------------------------------
    def detect_domain(self, skills: set[str]) -> str | None:
        """
        Detect dominant domain from a set of skills.
        Returns: engineering | analytics | design | business | None
        """

        if not skills:
            return None

        domain_votes: dict[str, int] = {}

        for skill in skills:
            domain = self.get_domain(skill)
            if not domain:
                continue

            domain_votes[domain] = domain_votes.get(domain, 0) + 1

        if not domain_votes:
            return None

        # Return dominant domain
        return max(domain_votes, key=domain_votes.get)

    # --------------------------------------------------
    # Inference logic
    # --------------------------------------------------
    def infer_related_skills(self, detected_skills: set[str]) -> set[str]:
        """
        Infer missing skills based on strong cluster presence.
        Uses conservative rule: infer only if >=2 cluster skills exist.
        """
        inferred = set()
        normalized_skills = {self.normalize_skill(s) for s in detected_skills}

        for cluster_skills in self.skill_clusters.values():
            overlap = normalized_skills & cluster_skills
            if len(overlap) >= 2:
                inferred |= cluster_skills - normalized_skills

        return inferred
