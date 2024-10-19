from config.database import Database
import tkinter as tk
from view import ProjectManagerApp


def main():
    Database()
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
