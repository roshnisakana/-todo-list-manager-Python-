"""
task.py
-------
Defines the Task class: a simple data model representing one to-do item.

DESIGN CHOICE:
We keep this class "dumb" on purpose — it only knows how to hold and
serialize its own data. It has NO knowledge of files, menus, or the
TaskManager. This keeps responsibilities separated: if tomorrow we
wanted to add a "priority" field, we'd only touch this file.
"""

from datetime import datetime


class Task:
    """Represents a single to-do item."""

    def __init__(self, description, completed=False, created_at=None, task_id=None):
        self.id = task_id  # Assigned by TaskManager; None until added to a list
        self.description = description
        self.completed = completed
        # Store creation timestamp as a string so it's easy to save/load as JSON
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def mark_complete(self):
        """Flip this task's status to completed."""
        self.completed = True

    def mark_incomplete(self):
        """Allow un-completing a task (useful if marked by mistake)."""
        self.completed = False

    def to_dict(self):
        """
        Convert this Task object into a plain dictionary.
        Needed because JSON (used for saving to disk) only understands
        basic Python types (dict, list, str, int, bool), not custom objects.
        """
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Rebuild a Task object from a dictionary (the reverse of to_dict).
        A classmethod is used here (instead of __init__ directly) because
        this is an *alternative constructor* — it builds a Task from saved
        data rather than from fresh user input.
        """
        return cls(
            description=data["description"],
            completed=data.get("completed", False),
            created_at=data.get("created_at"),
            task_id=data.get("id"),
        )

    def __str__(self):
        """Human-friendly display, used when printing the task list."""
        status = "✔" if self.completed else "✘"
        return f"[{status}] ({self.id}) {self.description}  -- added {self.created_at}"
