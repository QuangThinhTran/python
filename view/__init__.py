import tkinter as tk
from tkinter import ttk
from view.project_view import ProjectView
from view.task_view import TaskView
from view.employee_view import EmployeeView

class ProjectManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý dự án")
        self.root.geometry("600x500")
        self.root.configure(bg="#f5f5f5")

        self.tab_control = ttk.Notebook(self.root)
        self.project_tab = ttk.Frame(self.tab_control)
        self.task_tab = ttk.Frame(self.tab_control)
        self.employee_tab = ttk.Frame(self.tab_control)
        self.tab_control.pack(fill='both', expand=True)

        self.project_view = ProjectView(self.project_tab)
        self.task_view = TaskView(self.task_tab)
        self.employee_view = EmployeeView(self.employee_tab)

        self.tab_control.add(self.project_tab, text="Dự án")
        self.tab_control.add(self.task_tab, text="Công việc")
        self.tab_control.add(self.employee_tab, text="Nhân viên")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManagerApp(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("Application closed by user.")
