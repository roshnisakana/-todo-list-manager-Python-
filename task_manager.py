"""
task_manager.py
----------------
Defines TaskManager: the "business logic" layer of the app.

DESIGN CHOICE:
This class owns the list of Task objects and all the operations on it
(add, remove, complete, view, save, load). It does NOT print anything
to the screen and does NOT ask the user for input directly — that's
the CLI layer's job. This separation means:
  - TaskManager could be reused by a future GUI or web version untouched.
  - It's easy to unit-test TaskManager without simulating user typing.

Persistence uses a simple JSON file (tasks.json) so tasks survive
between runs. JSON was chosen over a database because it requires
no extra dependencies and is easy to inspect/edit by hand.
"""

import json
import os


class TaskManager:
    def __init__(self, storage_file="tasks.json"):
        self.storage_file = storage_file
        self.tasks = []          # List of Task objects, kept in memory
        self._next_id = 1        # Simple auto-incrementing ID counter
        self.load_tasks()

    # ------------------------------------------------------------------
    # Core features
    # ------------------------------------------------------------------

    def add_task(self, description):
        """
        Add a new task. Raises ValueError on invalid input so the CLI
        layer can catch it and show a friendly message (input validation
        lives partly here because TaskManager should never allow itself
        to end up in an invalid state, regardless of which caller uses it).
        """
        from task import Task  # Local import avoids a circular import at module load time

        description = description.strip() if description else ""
        if not description:
            raise ValueError("Task description cannot be empty.")

        new_task = Task(description=description, task_id=self._next_id)
        self.tasks.append(new_task)
        self._next_id += 1
        self.save_tasks()
        return new_task

    def remove_task(self, task_id):
        """Remove a task by ID. Raises KeyError if not found."""
        task = self._find_task(task_id)
        self.tasks.remove(task)
        self.save_tasks()
        return task

    def complete_task(self, task_id):
        """Mark a task as completed by ID. Raises KeyError if not found."""
        task = self._find_task(task_id)
        task.mark_complete()
        self.save_tasks()
        return task

    def list_tasks(self, filter_by="all"):
        """
        Return tasks filtered by status.
        filter_by: "all" | "pending" | "completed"
        """
        if filter_by == "pending":
            return [t for t in self.tasks if not t.completed]
        if filter_by == "completed":
            return [t for t in self.tasks if t.completed]
        return list(self.tasks)  # "all" (default) — return a copy

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _find_task(self, task_id):
        """Locate a task by its ID or raise KeyError with a clear message."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task found with ID {task_id}.")

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save_tasks(self):
        """Write current tasks to the JSON storage file."""
        from task import Task  # local import, same reasoning as above

        data = [task.to_dict() for task in self.tasks]
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            # We don't crash the app if saving fails (e.g. disk full,
            # permissions) — we surface it so the user is aware.
            print(f"Warning: could not save tasks ({e}).")

    def load_tasks(self):
        """Load tasks from the JSON storage file, if it exists."""
        from task import Task

        if not os.path.exists(self.storage_file):
            return  # First run — nothing to load yet, that's fine.

        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            # Corrupted or unreadable file: start fresh rather than crashing.
            print(f"Warning: could not read '{self.storage_file}' ({e}). "
                  f"Starting with an empty task list.")
            return

        self.tasks = [Task.from_dict(item) for item in raw_data]
        # Recompute next_id so new tasks never collide with loaded ones.
        if self.tasks:
            self._next_id = max(t.id for t in self.tasks) + 1
