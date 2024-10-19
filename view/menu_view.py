import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from datetime import datetime

from config.util import STATUSES, NOT_STARTED, IN_PROGRESS, COMPLETED, Util
from controllers.EmployeeController import EmployeeController
from controllers.ProjectController import ProjectController


class MenuView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.employee_controller = EmployeeController()
        self.project_controller = ProjectController()
        self.util = Util(root)

        self.custom_font = tkFont.Font(family="Helvetica", size=10)

        self.set_up_menu_tab()

    def set_up_menu_tab(self):
        self.menu_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.RAISED)
        self.menu_frame.pack(pady=20, fill='both', expand=True)

        title_label = ttk.Label(self.menu_frame, text="TRANG CHỦ", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))

        self.tab_control = ttk.Notebook(self.menu_frame)
        self.tab_control.pack(expand=1, fill="both")

        self.create_project_tabs()

    def create_project_tabs(self):
        for status in STATUSES:
            tab = ttk.Frame(self.tab_control)
            self.tab_control.add(tab, text=status)

            tree = ttk.Treeview(tab, columns=("name", "start_date", "end_date"), show="headings")
            tree.heading("name", text="Tên dự án")
            tree.heading("start_date", text="Ngày bắt đầu")
            tree.heading("end_date", text="Ngày kết thúc")

            tree.column("name", anchor="center")
            tree.column("start_date", anchor="center")
            tree.column("end_date", anchor="center")

            tree.pack(expand=1, fill="both")

            tree.bind("<<TreeviewSelect>>", lambda event, status=STATUSES: self.open_job_info(event, status))

            projects = self.project_controller.get_projects()

            current_time = datetime.now()

            for project in projects:
                name = project[1]
                start_date_str = project[3]
                end_date_str = project[4]

                if not (isinstance(start_date_str, str) and isinstance(end_date_str, str)):
                    continue

                start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
                end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

                if status == NOT_STARTED and current_time < start_date:
                    tree.insert("", "end", values=(name, start_date_str, end_date_str))
                elif status == IN_PROGRESS and start_date <= current_time <= end_date:
                    tree.insert("", "end", values=(name, start_date_str, end_date_str))
                elif status == COMPLETED and current_time > end_date:
                    tree.insert("", "end", values=(name, start_date_str, end_date_str))

    def open_job_info(self, event, status):
        selected_item = event.widget.selection()
        if selected_item:
            item_values = event.widget.item(selected_item, 'values')
            project_name = item_values[0]

            job_info_window = tk.Toplevel(self.root)
            job_info_window.geometry("900x750")

            self.util.center_window(job_info_window, 900, 550)

            job_info_frame = ttk.Frame(job_info_window, padding=(10, 10))
            job_info_frame.pack(fill='both', expand=True)

            job_info_label = ttk.Label(job_info_frame, text="CÔNG VIỆC", font=("Helvetica", 16, "bold"))
            job_info_label.pack(pady=(0, 20))

            tree_frame = ttk.Frame(job_info_frame)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            job_tree_scrollbar = ttk.Scrollbar(tree_frame)
            job_tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            job_tree = ttk.Treeview(tree_frame, columns=("job_name", "employee_name", "status", "description"),
                                    show="headings", yscrollcommand=job_tree_scrollbar.set)
            job_tree.heading("job_name", text="Tiêu đề", anchor=tk.CENTER)
            job_tree.heading("employee_name", text="Nhân viên", anchor=tk.CENTER)
            job_tree.heading("status", text="Trạng thái", anchor=tk.CENTER)
            job_tree.heading("description", text="Mô tả", anchor=tk.CENTER)

            job_tree.column("job_name", anchor="center", width=150)
            job_tree.column("employee_name", anchor="center", width=150)
            job_tree.column("status", anchor="center", width=100)
            job_tree.column("description", anchor="w", width=250)

            job_tree_scrollbar.config(command=job_tree.yview)
            job_tree.pack(fill=tk.BOTH, expand=True)

            jobs = self.project_controller.get_tasks_for_project(project_name)
            if jobs:
                for job in jobs:
                    job_tree.insert("", "end", values=(job[0], job[1], job[2], job[3]))
            else:
                no_jobs_label = ttk.Label(job_info_frame, text="Không có công việc nào cho dự án này.",
                                          foreground="red")
                no_jobs_label.pack(pady=10)
