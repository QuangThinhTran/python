from database import Database
import tkinter as tk

from view import ProjectManagerApp

if __name__ == "__main__":
    Database()
    root = tk.Tk()
    app = ProjectManagerApp(root)
    root.mainloop()
