"""Pretty-print tables using the tabulate package."""

from tabulate import tabulate


def show_users(users):
    if not users:
        return print("No users found.")
    rows = [[u.id, u.name, u.email or "—", len(u.projects)] for u in users]
    print("\n" + tabulate(rows, headers=["ID", "Name", "Email", "Projects"], tablefmt="rounded_outline"))


def show_projects(projects, owner=""):
    if not projects:
        return print("No projects found.")
    rows = [[p.id, p.title, p.description or "—", p.due_date or "—", len(p.tasks)] for p in projects]
    label = f" ({owner})" if owner else ""
    print(f"\nProjects{label}")
    print(tabulate(rows, headers=["ID", "Title", "Description", "Due Date", "Tasks"], tablefmt="rounded_outline"))


def show_tasks(tasks, project=""):
    if not tasks:
        return print("No tasks found.")
    rows = [[t.id, t.title, t.status, t.assigned_to or "—"] for t in tasks]
    label = f" in '{project}'" if project else ""
    print(f"\nTasks{label}")
    print(tabulate(rows, headers=["ID", "Title", "Status", "Assigned To"], tablefmt="rounded_outline"))