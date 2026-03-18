"""
Tests for task_manager.py
Generated with GitHub Copilot Agent Mode — Demo 4
"""

import pytest
from task_manager import (
    add_task,
    get_tasks,
    complete_task,
    delete_task,
    get_tasks_by_priority,
    get_overdue_tasks,
    update_task,
    _tasks,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────
@pytest.fixture(autouse=True)
def clear_tasks():
    """Reset in-memory store before every test."""
    import task_manager
    task_manager._tasks.clear()
    task_manager._next_id = 1
    yield
    task_manager._tasks.clear()
    task_manager._next_id = 1


# ── add_task ─────────────────────────────────────────────────────────────────
class TestAddTask:
    def test_returns_dict_with_expected_keys(self):
        task = add_task("Buy milk")
        assert {"id", "title", "priority", "completed", "created_at"} <= task.keys()

    def test_default_priority_is_medium(self):
        task = add_task("Write docs")
        assert task["priority"] == "medium"

    def test_ids_auto_increment(self):
        t1 = add_task("First")
        t2 = add_task("Second")
        assert t2["id"] == t1["id"] + 1

    def test_task_is_not_completed_on_creation(self):
        task = add_task("New task")
        assert task["completed"] is False

    def test_due_date_stored_correctly(self):
        task = add_task("Deadline task", due_date="2025-12-31")
        assert task["due_date"] == "2025-12-31"


# ── get_tasks ────────────────────────────────────────────────────────────────
class TestGetTasks:
    def test_returns_all_tasks_when_no_filter(self):
        add_task("A")
        add_task("B")
        assert len(get_tasks()) == 2

    def test_filter_completed(self):
        t = add_task("Done")
        complete_task(t["id"])
        add_task("Pending")
        assert len(get_tasks(completed=True)) == 1
        assert len(get_tasks(completed=False)) == 1

    def test_returns_empty_list_when_no_tasks(self):
        assert get_tasks() == []


# ── complete_task ────────────────────────────────────────────────────────────
class TestCompleteTask:
    def test_marks_task_completed(self):
        task = add_task("Finish report")
        result = complete_task(task["id"])
        assert result is True
        assert get_tasks(completed=True)[0]["completed"] is True

    def test_returns_false_for_missing_id(self):
        assert complete_task(999) is False

    def test_completed_at_is_set(self):
        task = add_task("Do something")
        complete_task(task["id"])
        assert "completed_at" in get_tasks()[0]


# ── delete_task ──────────────────────────────────────────────────────────────
class TestDeleteTask:
    def test_deletes_existing_task(self):
        task = add_task("Delete me")
        assert delete_task(task["id"]) is True
        assert get_tasks() == []

    def test_returns_false_for_missing_id(self):
        assert delete_task(42) is False


# ── get_tasks_by_priority ────────────────────────────────────────────────────
class TestGetTasksByPriority:
    def test_filters_by_priority(self):
        add_task("Urgent", priority="high")
        add_task("Chill", priority="low")
        high = get_tasks_by_priority("high")
        assert len(high) == 1
        assert high[0]["title"] == "Urgent"

    def test_invalid_priority_raises(self):
        with pytest.raises(ValueError):
            get_tasks_by_priority("extreme")


# ── get_overdue_tasks ────────────────────────────────────────────────────────
class TestGetOverdueTasks:
    def test_returns_overdue_incomplete_tasks(self):
        add_task("Late task", due_date="2020-01-01")
        add_task("Future task", due_date="2099-12-31")
        overdue = get_overdue_tasks()
        assert len(overdue) == 1
        assert overdue[0]["title"] == "Late task"

    def test_completed_overdue_not_returned(self):
        t = add_task("Done late", due_date="2020-01-01")
        complete_task(t["id"])
        assert get_overdue_tasks() == []


# ── update_task ───────────────────────────────────────────────────────────────
class TestUpdateTask:
    def test_updates_title(self):
        task = add_task("Old title")
        updated = update_task(task["id"], title="New title")
        assert updated["title"] == "New title"

    def test_raises_for_missing_task(self):
        with pytest.raises(ValueError):
            update_task(999, title="Ghost")

    def test_raises_for_invalid_field(self):
        task = add_task("Valid task")
        with pytest.raises(KeyError):
            update_task(task["id"], nonexistent_field="oops")
