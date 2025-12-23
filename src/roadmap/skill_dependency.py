class SkillDependencyResolver:
    """
    Handles dependency-aware ordering of skills
    """

    def __init__(self):
        # Skill → prerequisites
        self.dependencies = {
            "aws": ["docker"],
            "kubernetes": ["docker", "aws"],
            "ci/cd": ["docker"],
            "react": ["javascript"],
            "nodejs": ["javascript"]
        }

    def resolve(self, skills: list) -> list:
        """
        Orders skills so prerequisites come first
        """
        resolved = []
        visited = set()

        def dfs(skill):
            if skill in visited:
                return
            visited.add(skill)

            for dep in self.dependencies.get(skill, []):
                if dep in skills:
                    dfs(dep)

            if skill not in resolved:
                resolved.append(skill)

        for skill in skills:
            dfs(skill)

        return resolved
