import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkFont
from tkcalendar import DateEntry
from datetime import datetime
import pandas as pd

from config.util import STATUSES, Util
from controllers.TaskController import TaskController
from controllers.ProjectController import ProjectController
from controllers.EmployeeController import EmployeeController


class TaskView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.task_controller = TaskController()
        self.project_controller = ProjectController()
        self.employee_controller = EmployeeController()
        self.util = Util(root)

        self.custom_font = tkFont.Font(family="Helvetica", size=10)

        self.setup_task_tab()

    def setup_task_tab(self):
        self.task_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.RAISED)
        self.task_frame.pack(pady=20, fill='both', expand=True)

        title_label = ttk.Label(self.task_frame, text="QUẢN LÝ CÔNG VIỆC", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))

        button_frame = ttk.Frame(self.task_frame)
        button_frame.pack(pady=10)

        self.add_task_button = ttk.Button(button_frame, text="Thêm công việc", command=self.show_add_task_form)
        self.add_task_button.grid(row=0, column=0, padx=5)

        self.update_task_button = ttk.Button(button_frame, text="Sửa công việc", command=self.show_update_task_form)
        self.update_task_button.grid(row=0, column=1, padx=5)

        self.delete_task_button = ttk.Button(button_frame, text="Xóa công việc", command=self.delete_task)
        self.delete_task_button.grid(row=0, column=2, padx=5)

        self.detail_task_button = ttk.Button(button_frame, text="Chi tiết công việc", command=self.show_task_details)
        self.detail_task_button.grid(row=0, column=3, padx=5)

        self.task_list_frame = ttk.Frame(self.task_frame)
        self.task_list_frame.pack(pady=10, fill='both', expand=True)

        self.task_listbox = tk.Listbox(self.task_list_frame, width=60, height=12, font=self.custom_font, bg="#f9f9f9",
                                       selectbackground="#d0e0f0")
        self.task_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox['yscrollcommand'] = self.scrollbar.set

        self.load_tasks()

        bottom_button_frame = ttk.Frame(self.task_frame)
        bottom_button_frame.pack(pady=10)

        self.export_task_button = ttk.Button(bottom_button_frame, text="Xuất Excel", command=self.export_to_excel)
        self.export_task_button.grid(row=0, column=0, padx=5)

        self.import_task_button = ttk.Button(bottom_button_frame, text="Nhập Excel", command=self.import_from_excel)
        self.import_task_button.grid(row=0, column=1, padx=5)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        projects = self.task_controller.get_all_tasks()
        if projects:
            project_id = projects[0][0]
            tasks = self.task_controller.get_tasks_by_project(project_id)
            for task in tasks:
                self.task_listbox.insert(tk.END, task[2])

    def show_add_task_form(self):
        add_task_window = tk.Toplevel(self.root)
        add_task_window.title("Thêm Công Việc")
        self.util.center_window(add_task_window, 400, 300)
        add_task_window.geometry("450x500")
        add_task_window.configure(bg="#f0f0f0")
        add_task_window.resizable(False, False)

        main_frame = ttk.Frame(add_task_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Thêm Công Việc Mới", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Chọn dự án:", ttk.Combobox(main_frame, state='readonly')),
            ("Tên công việc:", ttk.Entry(main_frame)),
            ("Mô tả:", tk.Text(main_frame, height=5, width=40)),
            ("Trạng thái:", ttk.Combobox(main_frame, values=STATUSES, state='readonly')),
            ("Ngày bắt đầu:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                        date_pattern='yyyy-mm-dd', state='readonly')),
            ("Ngày kết thúc:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd', state='readonly')),
            ("Chọn nhân viên:", ttk.Combobox(main_frame, state='readonly'))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)

        self.load_projects_combobox(fields[0][1])
        self.load_employees_combobox(fields[6][1])

        add_button = ttk.Button(main_frame, text="Thêm", command=lambda: self.add_task(
            fields[1][1].get(), fields[2][1].get("1.0", tk.END),
            fields[3][1].get(),
            fields[4][1].get(), fields[5][1].get(), fields[0][1].current(),
            fields[6][1].current(), add_task_window
        ))
        add_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def show_task_details(self):
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Chi tiết Công Việc")
        self.util.center_window(detail_window, 400, 300)
        detail_window.geometry("400x400")
        detail_window.configure(bg="#f0f0f0")
        detail_window.resizable(False, False)
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để xem chi tiết!")
            return

        task = self.task_controller.get_tasks_by_project(self.project_controller.get_projects()[0][0])[
            selected_index[0]]

        main_frame = ttk.Frame(detail_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Chi Tiết Công Việc", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Tên công việc:", task[2]),
            ("Mô tả:", task[3]),
            ("Trạng thái:", task[4]),
            ("Ngày bắt đầu:", task[5]),
            ("Ngày kết thúc:", task[6]),
            ("Nhân viên phụ trách:", self.employee_controller.get_employee_name(task[7]) if task[7] else "Không có")
        ]

        for i, (label, value) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            ttk.Label(main_frame, text=value).grid(row=i + 1, column=1, sticky=tk.W, pady=5)

        ttk.Button(main_frame, text="Đóng", command=detail_window.destroy).grid(row=len(fields) + 1, column=0,
                                                                                columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def load_projects_combobox(self, combobox):
        projects = self.project_controller.get_projects()
        combobox['values'] = [project[1] for project in projects]

    def load_employees_combobox(self, combobox):
        employees = self.employee_controller.get_employees()
        combobox['values'] = [f"{employee[1]} - {employee[2]}" for employee in employees]

    def add_task(self, name, description, status, start_date, end_date, project_index, employee_index, window):
        selected_project_index = project_index
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
            employee_index = self.employee_controller.get_employees()[employee_index][
                0] if employee_index >= 0 else None
            self.task_controller.add_task(project_id, name, description, status, start_date, end_date, employee_index)
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
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để xóa!")

    def show_update_task_form(self):
        update_task_window = tk.Toplevel(self.root)
        update_task_window.title("Sửa Công Việc")
        self.util.center_window(update_task_window, 400, 300)
        update_task_window.geometry("450x500")
        update_task_window.configure(bg="#f0f0f0")
        update_task_window.resizable(False, False)
        selected_index = self.task_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn công việc để cập nhật!")
            return

        task = self.task_controller.get_tasks_by_project(self.project_controller.get_projects()[0][0])[
            selected_index[0]]

        main_frame = ttk.Frame(update_task_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Cập Nhật Công Việc", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Tên công việc:", ttk.Entry(main_frame)),
            ("Mô tả:", tk.Text(main_frame, height=5, width=40)),
            ("Trạng thái:", ttk.Combobox(main_frame, values=STATUSES, state='readonly')),
            ("Ngày bắt đầu:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                        date_pattern='yyyy-mm-dd', state='readonly')),
            ("Ngày kết thc:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd', state='readonly')),
            ("Chọn nhân viên:", ttk.Combobox(main_frame, state='readonly'))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)

        fields[0][1].insert(0, task[2])
        fields[1][1].insert(tk.END, task[3])
        fields[2][1].set(task[4])
        fields[3][1].set_date(task[5])
        fields[4][1].set_date(task[6])
        self.load_employees_combobox(fields[5][1])
        if task[7]:
            employee_name = self.employee_controller.get_employee_name(task[7])
            fields[5][1].set(employee_name)

        update_button = ttk.Button(main_frame, text="Cập nhật", command=lambda: self.update_task(
            task[0], fields[0][1].get(), fields[1][1].get("1.0", tk.END),
            fields[2][1].get(),
            fields[3][1].get(), fields[4][1].get(), fields[5][1].current(), update_task_window
        ))
        update_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def update_task(self, task_id, name, description, status, start_date, end_date, employee_index, window):
        if name and start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
                project_id = self.project_controller.get_projects()[0][0]
                employee_id = self.employee_controller.get_employees()[employee_index][
                    0] if employee_index >= 0 else None
                self.task_controller.update_task(task_id, project_id, name, description, status, start_date, end_date,
                                                 employee_id)
                self.load_tasks()
                window.destroy()
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Ngày tháng không hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def export_to_excel(self):
        tasks = self.task_controller.get_all_tasks()
        if not tasks:
            messagebox.showwarning("Cảnh báo", "Không có công việc để xuất!")
            return

        data = {
            "Tên công việc": [task[2] for task in tasks],
            "Mô tả": [task[3] for task in tasks],
            "Trạng thái": [task[4] for task in tasks],
            "Ngày bắt đầu": [task[5] for task in tasks],
            "Ngày kết thúc": [task[6] for task in tasks],
        }

        df = pd.DataFrame(data)

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                   filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Thông báo", f"Dữ liệu đã được xuất ra {file_path} thành công!")
        else:
            messagebox.showwarning("Cảnh báo", "Không có tệp được chọn để xuất!")

    def import_from_excel(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if not file_path:
            return

        success = True

        try:
            df = pd.read_excel(file_path)
            for index, row in df.iterrows():
                name = row.get("Tên công việc")
                description = row.get("Mô tả")
                status = row.get("Trạng thái")
                start_date = row.get("Ngày bắt đầu")
                end_date = row.get("Ngày kết thúc")

                if not name or not description or not status or not start_date or not end_date:
                    messagebox.showwarning("Cảnh báo", f"Cấu trúc file không hợp lệ! Vui lòng kiểm tra lại.")
                    success = False
                    continue

                self.task_controller.add_task(None, name, description, status, start_date, end_date, None)

            self.load_tasks()
            if success:
                messagebox.showinfo("Thông báo", "Dữ liệu đã được nhập thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi nhập dữ liệu: {str(e)}")