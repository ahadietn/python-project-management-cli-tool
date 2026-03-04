"""
main.py — Project Tracker CLI
Usage: python main.py <command> [options]

Commands:
  add-user        --name "Alex" [--email alex@example.com]
  list-users
  add-project     --user "Alex" --title "My Project" [--description "..." --due-date 2025-12-31]
  list-projects   --user "Alex"
  add-task        --project "My Project" --title "Do something" [--assign "Alex"]
  list-tasks      --project "My Project"
  complete-task   --project "My Project" --task "Do something"
  update-task     --project "My Project" --task "Do something" [--status in_progress] [--assign "Alex"]
  search-projects --keyword "my"
"""

import argparse
import sys

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage import save, load
from utils.display import show_users, show_projects, show_tasks


def find_user(users, name) -> User | None:
    return next((u for u in users if u.name.lower() == name.lower()), None)


def find_project_globally(users, title) -> tuple[User, Project] | tuple[None, None]:
    """Search all users for a project by title."""
    for u in users:
        p = u.find_project(title)
        if p:
            return u, p
    return None, None


# Command handler

def cmd_add_user(args, users):
    if find_user(users, args.name):
        return print(f"User '{args.name}' already exists.")
    users.append(User(name=args.name, email=args.email or ""))
    save(users)
    print(f" User '{args.name}' created.")


def cmd_list_users(args, users):
    show_users(users)


def cmd_add_project(args, users):
    user = find_user(users, args.user)
    if not user:
        return print(f" User '{args.user}' not found.")
    if user.find_project(args.title):
        return print(f" Project '{args.title}' already exists for this user.")
    user.add_project(Project(args.title, args.description or "", args.due_date or ""))
    save(users)
    print(f" Project '{args.title}' added to '{args.user}'.")


def cmd_list_projects(args, users):
    user = find_user(users, args.user)
    if not user:
        return print(f" User '{args.user}' not found.")
    show_projects(user.projects, owner=user.name)


def cmd_add_task(args, users):
    _, project = find_project_globally(users, args.project)
    if not project:
        return print(f"✘ Project '{args.project}' not found.")
    project.add_task(Task(args.title, assigned_to=args.assign or ""))
    save(users)
    print(f" Task '{args.title}' added to '{args.project}'.")


def cmd_list_tasks(args, users):
    _, project = find_project_globally(users, args.project)
    if not project:
        return print(f" Project '{args.project}' not found.")
    show_tasks(project.tasks, project=project.title)


def cmd_complete_task(args, users):
    _, project = find_project_globally(users, args.project)
    if not project:
        return print(f" Project '{args.project}' not found.")
    task = project.find_task(args.task)
    if not task:
        return print(f" Task '{args.task}' not found.")
    task.complete()
    save(users)
    print(f" Task '{args.task}' marked complete.")


def cmd_update_task(args, users):
    _, project = find_project_globally(users, args.project)
    if not project:
        return print(f" Project '{args.project}' not found.")
    task = project.find_task(args.task)
    if not task:
        return print(f" Task '{args.task}' not found.")
    if args.status:
        try:
            task.status = args.status
        except ValueError as e:
            return print(f" {e}")
    if args.assign is not None:
        task.assigned_to = args.assign
    save(users)
    print(f" Task '{args.task}' updated.")


def cmd_search_projects(args, users):
    keyword = args.keyword.lower()
    results = [(u.name, p) for u in users for p in u.projects
               if keyword in p.title.lower() or keyword in p.description.lower()]
    if not results:
        return print(f"No projects matching '{args.keyword}'.")
    for owner, proj in results:
        print(f"  {owner} / {proj}")


# This is the argument parser

def build_parser():
    parser = argparse.ArgumentParser(prog="tracker", description="Project Tracker CLI")
    sub = parser.add_subparsers(dest="command", metavar="<command>")
    sub.required = True

    # add-user
    p = sub.add_parser("add-user", help="Create a new user")
    p.add_argument("--name", required=True)
    p.add_argument("--email", default="")

    # list-users
    sub.add_parser("list-users", help="List all users")

    # add-project
    p = sub.add_parser("add-project", help="Add a project to a user")
    p.add_argument("--user", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--description", default="")
    p.add_argument("--due-date", dest="due_date", default="")

    # list-projects
    p = sub.add_parser("list-projects", help="List a user's projects")
    p.add_argument("--user", required=True)

    # add-task
    p = sub.add_parser("add-task", help="Add a task to a project")
    p.add_argument("--project", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--assign", default="")

    # list-tasks
    p = sub.add_parser("list-tasks", help="List tasks in a project")
    p.add_argument("--project", required=True)

    # complete-task
    p = sub.add_parser("complete-task", help="Mark a task complete")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)

    # update-task
    p = sub.add_parser("update-task", help="Update task status or assignee")
    p.add_argument("--project", required=True)
    p.add_argument("--task", required=True)
    p.add_argument("--status", choices=Task.VALID_STATUSES)
    p.add_argument("--assign", default=None)

    # search-projects
    p = sub.add_parser("search-projects", help="Search projects by keyword")
    p.add_argument("--keyword", required=True)

    return parser


# This is the entry point
COMMANDS = {
    "add-user":       cmd_add_user,
    "list-users":     cmd_list_users,
    "add-project":    cmd_add_project,
    "list-projects":  cmd_list_projects,
    "add-task":       cmd_add_task,
    "list-tasks":     cmd_list_tasks,
    "complete-task":  cmd_complete_task,
    "update-task":    cmd_update_task,
    "search-projects": cmd_search_projects,
}

if __name__ == "__main__":
    args = build_parser().parse_args()
    users = load()
    COMMANDS[args.command](args, users)