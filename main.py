from config.database import Database
import tkinter as tk
from view import ProjectManagerApp


def main():
    try:
        Database()
        root = tk.Tk()
        app = ProjectManagerApp(root)
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("Cleaning up resources...")


if __name__ == "__main__":
    main()
