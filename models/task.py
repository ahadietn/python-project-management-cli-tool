"""A single task inside a project."""


class Task:
    _next_id = 1  # class-level ID counter

    VALID_STATUSES = ("pending", "in_progress", "complete")

    def __init__(self, title: str, assigned_to: str = "", status: str = "pending", task_id: int = None):
        self.id = task_id or Task._next_id
        Task._next_id = max(Task._next_id, self.id) + 1

        self.title = title
        self.assigned_to = assigned_to
        self._status = "pending"
        self.status = status  # uses setter

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {self.VALID_STATUSES}")
        self._status = value

    def complete(self):
        self.status = "complete"

    def to_dict(self):
        return {"id": self.id, "title": self.title, "assigned_to": self.assigned_to, "status": self._status}

    @classmethod
    def from_dict(cls, d):
        return cls(d["title"], d.get("assigned_to", ""), d.get("status", "pending"), d.get("id"))

    def __str__(self):
        assignee = f" → {self.assigned_to}" if self.assigned_to else ""
        return f"  [{self.id}] {self.title} ({self._status}){assignee}"