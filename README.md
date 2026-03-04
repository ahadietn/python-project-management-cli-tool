# Python Project Management CLI Tool

A command-line tool to manage users, projects, and tasks. Everything is saved automatically to a local JSON file so your data persists between sessions.


## How to Set Up

1. Create a virtual environment:
   python3 -m venv venv

2. Activate it:
   source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the program:
   python main.py --help


## CLI Commands

Add a user:
   python main.py add-user --name "Alex" --email alex@example.com

List all users:
   python main.py list-users

Add a project to a user:
   python main.py add-project --user "Alex" --title "My App" --due-date 2025-12-31

List a user's projects:
   python main.py list-projects --user "Alex"

Add a task to a project:
   python main.py add-task --project "My App" --title "Write tests" --assign "Alex"

List tasks in a project:
   python main.py list-tasks --project "My App"

Mark a task complete:
   python main.py complete-task --project "My App" --task "Write tests"

Update a task status:
   python main.py update-task --project "My App" --task "Write tests" --status in_progress

Search projects by keyword:
   python main.py search-projects --keyword "App"


## How Data is Saved

All data is stored in data/data.json. This file is created automatically the first time you add anything. Every time you run a command that changes data the file is saved automatically. Users contain projects, and projects contain tasks, all nested inside one file.

## How to Run the Tests

   python tests/test_models.py

You should see all 14 tests pass like this:

   Running 14 tests...
       test_project_add_task
       test_task_complete
       test_user_inherits_person
     
   14 passed | 0 failed

## Quick Start Example

   python main.py add-user --name "Alex" --email alex@example.com
   python main.py add-project --user "Alex" --title "My App" --due-date 2025-12-31
   python main.py add-task --project "My App" --title "Design database" --assign "Alex"
   python main.py add-task --project "My App" --title "Build API"
   python main.py list-tasks --project "My App"
   python main.py complete-task --project "My App" --task "Design database"
   python main.py list-tasks --project "My App"