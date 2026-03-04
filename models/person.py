"""Base class — User inherits from this (demonstrates inheritance)."""


class Person:
    def __init__(self, name: str, email: str = ""):
        if not name.strip():
            raise ValueError("Name cannot be empty.")
        self.name = name.strip()
        self.email = email.strip()

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"