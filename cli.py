"""
cli.py
------
The interactive command-line interface. This module's ONLY job is:
  1. Show menus / prompts
  2. Read and validate raw user input
  3. Call TaskManager methods
  4. Print results

It deliberately contains no business logic (no direct list manipulation)
so the "rules" of the to-do list live in exactly one place (task_manager.py).
"""

from task_manager import TaskManager

MENU = """
==============================
   TO-DO LIST MANAGER
==============================
1. View all tasks
2. View pending tasks
3. View completed tasks
4. Add a task
5. Mark a task as completed
6. Remove a task
7. Exit
==============================
"""


def print_tasks(tasks):
    """Shared helper to display a list of tasks, or a friendly empty message."""
    if not tasks:
        print("  (no tasks to show)")
        return
    for task in tasks:
        print(" ", task)


def prompt_for_task_id():
    """
    Ask the user for a task ID and validate it's a positive integer.
    Returns the integer, or None if the user typed something invalid
    (in which case a message has already been printed).
    """
    raw = input("Enter task ID: ").strip()
    if not raw.isdigit():
        print("Invalid input: please enter a numeric task ID.")
        return None
    return int(raw)


def run():
    """Main application loop."""
    manager = TaskManager()

    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()

        # --- View all ---
        if choice == "1":
            print_tasks(manager.list_tasks("all"))

        # --- View pending ---
        elif choice == "2":
            print_tasks(manager.list_tasks("pending"))

        # --- View completed ---
        elif choice == "3":
            print_tasks(manager.list_tasks("completed"))

        # --- Add task ---
        elif choice == "4":
            description = input("Enter task description: ")
            try:
                task = manager.add_task(description)
                print(f"Added task #{task.id}: {task.description}")
            except ValueError as e:
                print(f"Error: {e}")

        # --- Complete task ---
        elif choice == "5":
            if not manager.tasks:
                print("There are no tasks yet.")
                continue
            task_id = prompt_for_task_id()
            if task_id is None:
                continue
            try:
                task = manager.complete_task(task_id)
                print(f"Marked task #{task.id} as completed.")
            except KeyError as e:
                print(f"Error: {e}")

        # --- Remove task ---
        elif choice == "6":
            if not manager.tasks:
                print("There are no tasks yet.")
                continue
            task_id = prompt_for_task_id()
            if task_id is None:
                continue
            try:
                task = manager.remove_task(task_id)
                print(f"Removed task #{task.id}: {task.description}")
            except KeyError as e:
                print(f"Error: {e}")

        # --- Exit ---
        elif choice == "7":
            print("Goodbye! Your tasks have been saved.")
            break

        else:
            print("Invalid option. Please choose a number from 1 to 7.")
