"""
Task Manager - Demo App for GitHub Copilot Training
====================================================
A simple task management module used to demonstrate
GitHub Copilot features during onboarding sessions.
"""

from datetime import datetime
from typing import Optional


# ── Data store (in-memory for demo) ──────────────────────────────────────────
_tasks: list[dict] = []
_next_id: int = 1


# ── DEMO 1: Auto-complete from comment ───────────────────────────────────────
# (In live demo: type comment below and let Copilot generate the function)

# Function that adds a new task with title, priority (low/medium/high), and due date
def add_task(title: str, priority: str = "medium", due_date: Optional[str] = None) -> dict:
    global _next_id
    task = {
        "id": _next_id,
        "title": title,
        "priority": priority,
        "due_date": due_date,
        "completed": False,
        "created_at": datetime.now().isoformat(),
    }
    _tasks.append(task)
    _next_id += 1
    return task


# Function that returns all tasks, optionally filtered by completion status
def get_tasks(completed: Optional[bool] = None) -> list[dict]:
    if completed is None:
        return list(_tasks)
    return [t for t in _tasks if t["completed"] == completed]


# Function that marks a task as complete by its id, returns False if not found
def complete_task(task_id: int) -> bool:
    for task in _tasks:
        if task["id"] == task_id:
            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat()
            return True
    return False


# Function that deletes a task by id, returns False if not found
def delete_task(task_id: int) -> bool:
    global _tasks
    original_len = len(_tasks)
    _tasks = [t for t in _tasks if t["id"] != task_id]
    return len(_tasks) < original_len


# ── DEMO 3: Agent Mode adds this feature ─────────────────────────────────────
# (Agent will add: get_tasks_by_priority, get_overdue_tasks)

def get_tasks_by_priority(priority: str) -> list[dict]:
    """Return all tasks matching the given priority level."""
    valid = {"low", "medium", "high"}
    if priority not in valid:
        raise ValueError(f"Priority must be one of {valid}, got '{priority}'")
    return [t for t in _tasks if t["priority"] == priority]


def get_overdue_tasks() -> list[dict]:
    """Return all incomplete tasks whose due_date has passed."""
    today = datetime.now().date().isoformat()
    return [
        t for t in _tasks
        if not t["completed"] and t.get("due_date") and t["due_date"] < today
    ]


def search_tasks_by_title(query: str) -> list[dict]:
    """Search tasks by title (case-insensitive partial match)."""
    if not query:
        return []
    query_lower = query.lower()
    return [t for t in _tasks if query_lower in t["title"].lower()]


# ── DEMO 5: Inline Chat adds try/except + docstring here ────────────────────
def update_task(task_id: int, **kwargs) -> dict:
    """
    Update fields of an existing task.

    Args:
        task_id: The ID of the task to update.
        **kwargs: Fields to update (title, priority, due_date).

    Returns:
        The updated task dictionary.

    Raises:
        ValueError: If task_id is not found.
        KeyError: If an invalid field is provided.
    """
    allowed_fields = {"title", "priority", "due_date"}
    invalid = set(kwargs) - allowed_fields
    if invalid:
        raise KeyError(f"Invalid fields: {invalid}. Allowed: {allowed_fields}")

    try:
        for task in _tasks:
            if task["id"] == task_id:
                task.update(kwargs)
                task["updated_at"] = datetime.now().isoformat()
                return task
        raise ValueError(f"Task with id={task_id} not found.")
    except (ValueError, KeyError):
        raise
    except Exception as e:
        raise RuntimeError(f"Unexpected error updating task {task_id}: {e}") from e


# ── Quick smoke-test ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    t1 = add_task("Set up Copilot in VS Code", priority="high", due_date="2025-06-01")
    t2 = add_task("Review PR with Copilot Chat", priority="medium")
    t3 = add_task("Write unit tests using Agent mode", priority="high", due_date="2024-01-01")

    print("All tasks:", get_tasks())
    complete_task(t1["id"])
    print("Pending:", get_tasks(completed=False))
    print("High priority:", get_tasks_by_priority("high"))
    print("Overdue:", get_overdue_tasks())
