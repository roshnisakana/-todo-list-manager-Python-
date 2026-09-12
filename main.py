"""
main.py
-------
Entry point of the application. Kept intentionally tiny: its only
responsibility is to start the CLI and handle a clean Ctrl+C exit.
"""

from cli import run

if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        # Catch Ctrl+C so the user gets a clean exit message instead
        # of a scary traceback.
        print("\n\nInterrupted. Exiting without losing saved tasks.")
