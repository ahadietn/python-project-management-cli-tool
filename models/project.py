"""A project owned by a User, containing Tasks (one-to-many)."""

from models.task import Task


class Project:
    _next_id = 1

    def __init__(self, title: str, description: str = "", due_date: str = "", project_id: int = None):
        if not title.strip():
            raise ValueError("Project title cannot be empty.")
        self.id = project_id or Project._next_id
        Project._next_id = max(Project._next_id, self.id) + 1

        self.title = title.strip()
        self.description = description
        self.due_date = due_date
        self._tasks: list[Task] = []

    # Task management
    def add_task(self, task: Task):
        self._tasks.append(task)

    def find_task(self, title: str) -> Task | None:
        return next((t for t in self._tasks if t.title.lower() == title.lower()), None)

    @property
    def tasks(self):
        return list(self._tasks)

    # Serialization
    def to_dict(self):
        return {
            "id": self.id, "title": self.title,
            "description": self.description, "due_date": self.due_date,
            "tasks": [t.to_dict() for t in self._tasks],
        }

    @classmethod
    def from_dict(cls, d):
        proj = cls(d["title"], d.get("description", ""), d.get("due_date", ""), d.get("id"))
        for t in d.get("tasks", []):
            proj.add_task(Task.from_dict(t))
        return proj

    def __str__(self):
        due = f" (due: {self.due_date})" if self.due_date else ""
        return f"[{self.id}] {self.title}{due} — {len(self._tasks)} task(s)"