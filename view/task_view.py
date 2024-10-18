import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

from controllers.TaskController import TaskController
from controllers.ProjectController import ProjectController
from controllers.EmployeeController import EmployeeController

TASK_STATUSES = ["Chưa bắt đầu", "Đang thực hiện", "Đã hoàn thành"]

class TaskView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.employee_controller = EmployeeController()
        self.setup_task_tab()

    def setup_task_tab(self):
        style = ttk.Style()
        style.configure("TaskFrame.TFrame", background="#e6f7ff")

        self.task_frame = ttk.Frame(self.root, padding=(10, 10), relief=tk.RAISED, style="TaskFrame.TFrame")
        self.task_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.main_frame = ttk.Frame(self.task_frame)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.task_list_frame = ttk.Frame(self.main_frame)
        self.task_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(self.task_list_frame, width=50, height=10, bg="#ffffff", font=("Arial", 12))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox['yscrollcommand'] = self.scrollbar.set

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.add_task_button = ttk.Button(self.button_frame, text="Thêm task", command=self.show_add_task_form)
        self.add_task_button.pack(pady=5, padx=5)

        self.update_task_button = ttk.Button(self.button_frame, text="Sửa task", command=self.show_update_task_form)
        self.update_task_button.pack(pady=5, padx=5)

        self.delete_task_button = ttk.Button(self.button_frame, text="Xóa task", command=self.delete_task)
        self.delete_task_button.pack(pady=5, padx=5)

        self.detail_task_button = ttk.Button(self.button_frame, text="Chi tiết task", command=self.show_task_details)
        self.detail_task_button.pack(pady=5, padx=5)

        self.load_tasks()

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        projects = self.project_controller.get_projects()
        if projects:
            project_id = projects[0][0]
            tasks = self.task_controller.get_tasks_by_project(project_id)
            for task in tasks:
                self.task_listbox.insert(tk.END, task[2])

    def show_add_task_form(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Thêm Task")
        add_task_window.geometry("400x400")
        add_task_window.configure(bg="#f0f0f0")

        label_font = ("Arial", 10)

        ttk.Label(add_task_window, text="Chọn dự án:", font=label_font).grid(row=0, column=0, sticky=tk.W)
        self.project_combobox = ttk.Combobox(add_task_window)
        self.project_combobox.grid(row=0, column=1)
        self.load_projects_combobox()
        self.project_combobox.config(state='readonly')

        ttk.Label(add_task_window, text="Tên task:", font=label_font).grid(row=1, column=0, sticky=tk.W)
        task_name_entry = ttk.Entry(add_task_window)
        task_name_entry.grid(row=1, column=1)

        ttk.Label(add_task_window, text="Mô tả:", font=label_font).grid(row=2, column=0, sticky=tk.W)
        task_desc_entry = ttk.Entry(add_task_window)
        task_desc_entry.grid(row=2, column=1)

        ttk.Label(add_task_window, text="Trạng thái:", font=label_font).grid(row=3, column=0, sticky=tk.W)
        task_status_combobox = ttk.Combobox(add_task_window, values=TASK_STATUSES)
        task_status_combobox.grid(row=3, column=1)

        ttk.Label(add_task_window, text="Ngày bắt đầu:", font=label_font).grid(row=4, column=0, sticky=tk.W)
        task_start_date_entry = DateEntry(add_task_window, width=12, background='darkblue',
                                          foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        task_start_date_entry.grid(row=4, column=1)

        ttk.Label(add_task_window, text="Ngày kết thúc:", font=label_font).grid(row=5, column=0, sticky=tk.W)
        task_end_date_entry = DateEntry(add_task_window, width=12, background='darkblue',
                                        foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        task_end_date_entry.grid(row=5, column=1)

        ttk.Label(add_task_window, text="Chọn nhân viên:", font=label_font).grid(row=6, column=0, sticky=tk.W)
        self.employee_combobox = ttk.Combobox(add_task_window)
        self.employee_combobox.grid(row=6, column=1)
        self.load_employees_combobox()
        self.employee_combobox.config(state='readonly')

        add_button = ttk.Button(add_task_window, text="Thêm",
                                command=lambda: self.add_task(task_name_entry.get(), task_desc_entry.get(),
                                                              task_status_combobox.get(), task_start_date_entry.get(),
                                                              task_end_date_entry.get(),
                                                              self.project_combobox.current(), add_task_window))
        add_button.grid(row=7, columnspan=2, pady=10, padx=5)
        add_button.configure(style='Accent.TButton')
        add_button.bind("<Enter>", lambda e: self.add_tooltip(add_button, "Thêm task vào dự án"))

    def show_task_details(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.task_controller.get_tasks_by_project(self.project_controller.get_projects()[0][0])[
                selected_index[0]]

            detail_window = tk.Toplevel(self.root)
            detail_window.title("Chi tiết Task")
            detail_window.geometry("400x300")

            ttk.Label(detail_window, text="Tên task:").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=task[2]).grid(row=0, column=1)

            ttk.Label(detail_window, text="Mô tả:").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=task[3]).grid(row=1, column=1)

            ttk.Label(detail_window, text="Trạng thái:").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=task[4]).grid(row=2, column=1)

            ttk.Label(detail_window, text="Ngày bắt đầu:").grid(row=3, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=task[5]).grid(row=3, column=1)

            ttk.Label(detail_window, text="Ngày kết thúc:").grid(row=4, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=task[6]).grid(row=4, column=1)

            ttk.Label(detail_window, text="Nhân viên phụ trách:").grid(row=5, column=0, sticky=tk.W)
            employee_id = task[7]
            employee_name = self.employee_controller.get_employee_name(employee_id) if employee_id else "Không có"
            ttk.Label(detail_window, text=employee_name).grid(row=5, column=1)

            ttk.Button(detail_window, text="Đóng", command=detail_window.destroy).grid(row=6, columnspan=2, pady=10)

    def load_projects_combobox(self):
        projects = self.project_controller.get_projects()
        self.project_combobox['values'] = [project[1] for project in projects]

    def load_employees_combobox(self):
        employees = self.employee_controller.get_employees()
        self.employee_combobox['values'] = [f"{employee[1]} - {employee[2]}" for employee in employees]

    def add_task(self, name, description, status, start_date, end_date, project_index, window):
        selected_project_index = self.project_combobox.current()
        if selected_project_index < 0:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một dự án trước!")
            return

        if not name or not start_date or not end_date:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")
            return

        project_id = self.project_controller.get_projects()[selected_project_index][0]

        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
            employee_index = self.employee_combobox.current()
            employee_id = self.employee_controller.get_employees()[employee_index][0] if employee_index >= 0 else None
            self.task_controller.add_task(project_id, name, description, status, start_date, end_date, employee_id)
            self.load_tasks()
            window.destroy()
        except ValueError:
            messagebox.showwarning("Cảnh báo", "Ngày tháng không hợp lệ!")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_id = self.task_controller.get_tasks_by_project(self.project_controller.get_projects()[0][0])[
                selected_index[0]][0]
            self.task_controller.delete_task(task_id)
            self.load_tasks()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn task để xóa!")

    def show_update_task_form(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task = self.task_controller.get_tasks_by_project(self.project_controller.get_projects()[0][0])[
                selected_index[0]]
            update_task_window = tk.Toplevel(self.root)
            update_task_window.title("Sửa Task")
            update_task_window.geometry("400x400")

            ttk.Label(update_task_window, text="Tên task:").grid(row=0, column=0, sticky=tk.W)
            task_name_entry = ttk.Entry(update_task_window)
            task_name_entry.insert(0, task[2])
            task_name_entry.grid(row=0, column=1)

            ttk.Label(update_task_window, text="Mô tả:").grid(row=1, column=0, sticky=tk.W)
            task_desc_entry = ttk.Entry(update_task_window)
            task_desc_entry.insert(0, task[3])
            task_desc_entry.grid(row=1, column=1)

            ttk.Label(update_task_window, text="Trạng thái:").grid(row=2, column=0, sticky=tk.W)
            status_combobox = ttk.Combobox(update_task_window, values=TASK_STATUSES)
            status_combobox.set(task[4])
            status_combobox.grid(row=2, column=1)

            ttk.Label(update_task_window, text="Ngày bắt đầu:").grid(row=3, column=0, sticky=tk.W)
            start_date_entry = DateEntry(update_task_window, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            start_date_entry.set_date(task[5])
            start_date_entry.grid(row=3, column=1)

            ttk.Label(update_task_window, text="Ngày kết thúc:").grid(row=4, column=0, sticky=tk.W)
            end_date_entry = DateEntry(update_task_window, width=12, background='darkblue',
                                       foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            end_date_entry.set_date(task[6])
            end_date_entry.grid(row=4, column=1)

            ttk.Label(update_task_window, text="Chọn nhân viên:").grid(row=5, column=0, sticky=tk.W)
            self.employee_combobox = ttk.Combobox(update_task_window)
            self.employee_combobox.grid(row=5, column=1)
            self.load_employees_combobox()
            self.employee_combobox.set(task[7])
            self.employee_combobox.config(state='readonly')

            update_button = ttk.Button(update_task_window, text="Cập nhật",
                                       command=lambda: self.update_task(task[0], task_name_entry.get(),
                                                                        task_desc_entry.get(), status_combobox.get(),
                                                                        start_date_entry.get(), end_date_entry.get(),
                                                                        self.employee_combobox.current(), update_task_window))
            update_button.grid(row=6, columnspan=2, pady=10)

    def update_task(self, task_id, name, description, status, start_date, end_date, employee_index, window):
        if name and start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
                project_id = self.project_controller.get_projects()[0][0]
                employee_id = self.employee_controller.get_employees()[employee_index][0] if employee_index >= 0 else None
                self.task_controller.update_task(task_id, project_id, name, description, status, start_date, end_date,
                                                 employee_id)
                self.load_tasks()
                window.destroy()
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Ngày tháng không hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")