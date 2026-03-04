"""User inherits from Person and owns Projects (one-to-many)."""

from models.person import Person
from models.project import Project


class User(Person):
    _next_id = 1

    def __init__(self, name: str, email: str = "", user_id: int = None):
        super().__init__(name, email)  # call Person.__init__
        self.id = user_id or User._next_id
        User._next_id = max(User._next_id, self.id) + 1
        self._projects: list[Project] = []

    # Project management
    def add_project(self, project: Project):
        self._projects.append(project)

    def find_project(self, title: str) -> Project | None:
        return next((p for p in self._projects if p.title.lower() == title.lower()), None)

    @property
    def projects(self):
        return list(self._projects)

    # Serialization
    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "projects": [p.to_dict() for p in self._projects],
        }

    @classmethod
    def from_dict(cls, d):
        user = cls(d["name"], d.get("email", ""), d.get("id"))
        for p in d.get("projects", []):
            user.add_project(Project.from_dict(p))
        return user

    def __str__(self):
        email = f" <{self.email}>" if self.email else ""
        return f"[{self.id}] {self.name}{email} — {len(self._projects)} project(s)"