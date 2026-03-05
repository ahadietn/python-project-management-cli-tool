"""
tests/test_models.py — Run with: python tests/test_models.py
Tests all core model logic without needing pytest.
"""

import sys, os, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.task import Task
from models.project import Project
from models.user import User
import utils.storage as storage

def test_task_defaults():
    t = Task("Write docs")
    assert t.title == "Write docs" and t.status == "pending"
    
def test_task_complete():
    t = Task("Deploy")
    t.complete()
    assert t.status == "complete"

def test_task_invalid_status():
    t = Task("Fix bug")
    try:
        t.status = "done"
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_task_roundtrip():
    t = Task("Refactor", "Alex", "in_progress")
    r = Task.from_dict(t.to_dict())
    assert r.title == t.title and r.status == t.status and r.id == t.id

def test_project_add_task():
    p = Project("Backend")
    p.add_task(Task("Set up DB"))
    assert len(p.tasks) == 1

def test_project_find_task_case_insensitive():
    p = Project("Frontend")
    t = Task("Build Login")
    p.add_task(t)
    assert p.find_task("build login") is t

def test_project_empty_title_raises():
    try:
        Project("  ")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_project_roundtrip():
    p = Project("API", "REST API", "2025-12-31")
    p.add_task(Task("Create endpoints"))
    r = Project.from_dict(p.to_dict())
    assert r.title == p.title and len(r.tasks) == 1

def test_user_inherits_person():
    u = User("Alex", "alex@example.com")
    assert u.name == "Alex" and u.email == "alex@example.com"

def test_user_empty_name_raises():
    try:
        User("")
        assert False, "Should have raised ValueError"
    except ValueError:
        pass

def test_user_add_project():
    u = User("Jordan")
    u.add_project(Project("Dashboard"))
    assert len(u.projects) == 0

def test_user_find_project_case_insensitive():
    u = User("Sam")
    p = Project("Mobile App")
    u.add_project(p)
    assert u.find_project("mobile app") is p

def test_user_roundtrip():
    u = User("Taylor", "t@test.com")
    proj = Project("Website")
    proj.add_task(Task("Design homepage"))
    u.add_project(proj)
    r = User.from_dict(u.to_dict())
    assert r.name == u.name and len(r.projects[0].tasks) == 1

def test_save_and_load():
    with tempfile.TemporaryDirectory() as tmp:
        storage.DATA_FILE = os.path.join(tmp, "data.json")
        u = User("Test User")
        p = Project("Test Project")
        p.add_task(Task("Test Task"))
        u.add_project(p)
        storage.save([u])
        loaded = storage.load()
        assert loaded[0].name == "Test User"
        assert loaded[0].projects[0].tasks[0].title == "Test Task"


if __name__ == "__main__":
    tests = [(k, v) for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    passed = failed = 0
    print(f"\nRunning {len(tests)} tests...\n")
    for name, fn in tests:
        try:
            fn()
            print(f"  ✔  {name}")
            passed += 1
        except Exception as e:
            print(f"  ✘  {name}  →  {e}")
            failed += 1
    print(f"\n{passed} passed | {failed} failed\n")
    sys.exit(0 if failed == 0 else 1)