import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from tkcalendar import DateEntry
from datetime import datetime
import pandas as pd
import tkinter.filedialog as filedialog

from config.util import Util
from controllers.ProjectController import ProjectController


class ProjectView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.project_controller = ProjectController()
        self.util = Util(root)

        self.custom_font = tkFont.Font(family="Helvetica", size=10)

        self.setup_project_tab()

    def setup_project_tab(self):
        self.project_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.RAISED)
        self.project_frame.pack(pady=20, fill='both', expand=True)

        title_label = ttk.Label(self.project_frame, text="QUẢN LÝ DỰ ÁN", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))

        button_frame = ttk.Frame(self.project_frame)
        button_frame.pack(pady=10)

        self.add_project_button = ttk.Button(button_frame, text="Thêm dự án", command=self.show_add_project_form)
        self.add_project_button.grid(row=0, column=0, padx=5)

        self.update_project_button = ttk.Button(button_frame, text="Sửa dự án", command=self.show_update_project_form)
        self.update_project_button.grid(row=0, column=1, padx=5)

        self.delete_project_button = ttk.Button(button_frame, text="Xóa dự án", command=self.delete_project)
        self.delete_project_button.grid(row=0, column=2, padx=5)

        self.detail_project_button = ttk.Button(button_frame, text="Chi tiết dự án", command=self.show_project_details)
        self.detail_project_button.grid(row=0, column=3, padx=5)

        self.project_list_frame = ttk.Frame(self.project_frame)
        self.project_list_frame.pack(pady=10, fill='both', expand=True)

        self.project_listbox = tk.Listbox(self.project_list_frame, width=60, height=12, font=self.custom_font,
                                          bg="#f9f9f9", selectbackground="#d0e0f0")
        self.project_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.project_list_frame, orient=tk.VERTICAL, command=self.project_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_listbox['yscrollcommand'] = self.scrollbar.set

        button_frame = ttk.Frame(self.project_frame)
        button_frame.pack(pady=10)

        self.export_project_button = ttk.Button(button_frame, text="Xuất Excel", command=self.export_to_excel)
        self.export_project_button.grid(row=0, column=0, padx=5)

        self.import_project_button = ttk.Button(button_frame, text="Nhập Excel",
                                                command=self.import_from_excel)
        self.import_project_button.grid(row=0, column=1, padx=5)

        self.load_projects()

    def show_project_details(self):
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Chi tiết Dự Án")
        self.util.center_window(detail_window, 400, 300)
        detail_window.geometry("400x300")
        detail_window.configure(bg="#f0f0f0")
        detail_window.resizable(False, False)
        selected_index = self.project_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dự án để xem chi tiết!")
            return

        project = self.project_controller.get_projects()[selected_index[0]]

        main_frame = ttk.Frame(detail_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Chi Tiết Dự Án", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                          pady=(0, 20))

        fields = [
            ("Tên dự án:", project[1]),
            ("Mô tả:", project[2]),
            ("Ngày bắt đầu:", project[3]),
            ("Ngày kết thúc:", project[4])
        ]

        for i, (label, value) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            ttk.Label(main_frame, text=value).grid(row=i + 1, column=1, sticky=tk.W, pady=5)

        ttk.Button(main_frame, text="Đóng", command=detail_window.destroy).grid(row=len(fields) + 1, column=0,
                                                                                columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def load_projects(self):
        projects = self.project_controller.get_projects()
        self.project_listbox.delete(0, tk.END)
        for project in projects:
            self.project_listbox.insert(tk.END, project[1])

    def show_add_project_form(self):
        add_project_window = tk.Toplevel(self.root)
        add_project_window.title("Thêm Dự Án")
        self.util.center_window(add_project_window, 400, 350)
        add_project_window.geometry("400x350")
        add_project_window.configure(bg="#f0f0f0")
        add_project_window.resizable(False, False)

        main_frame = ttk.Frame(add_project_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Thêm Dự Án Mới", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                          pady=(0, 20))

        fields = [
            ("Tên dự án:", ttk.Entry(main_frame)),
            ("Mô tả:", tk.Text(main_frame, height=5, width=40)),
            ("Ngày bắt đầu:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                        date_pattern='yyyy-mm-dd', state='readonly')),
            ("Ngày kết thúc:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd', state='readonly'))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)

        add_button = ttk.Button(main_frame, text="Thêm", command=lambda: self.add_project(
            fields[0][1].get(), fields[1][1].get("1.0", tk.END),
            fields[2][1].get(), fields[3][1].get(), add_project_window
        ))
        add_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def add_project(self, name, description, start_date, end_date, window):
        if name and start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
                self.project_controller.add_project(name, description, start_date, end_date)
                self.load_projects()
                window.destroy()
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Ngày tháng không hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def delete_project(self):
        selected_index = self.project_listbox.curselection()
        if selected_index:
            project_id = self.project_controller.get_projects()[selected_index[0]][0]
            self.project_controller.delete_tasks_by_project_id(project_id)
            self.project_controller.delete_project(project_id)
            self.load_projects()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dự án để xóa!")

    def show_update_project_form(self):
        update_project_window = tk.Toplevel(self.root)
        update_project_window.title("Sửa Dự Án")
        self.util.center_window(update_project_window, 400, 300)
        update_project_window.geometry("400x350")
        update_project_window.configure(bg="#f0f0f0")
        update_project_window.resizable(False, False)
        selected_index = self.project_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dự án để cập nhật!")
            return

        project = self.project_controller.get_projects()[selected_index[0]]

        main_frame = ttk.Frame(update_project_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Cập Nhật Dự Án", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2,
                                                                                          pady=(0, 20))

        fields = [
            ("Tên dự án:", ttk.Entry(main_frame)),
            ("Mô tả:", tk.Text(main_frame, height=5, width=40)),
            ("Ngày bắt đầu:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                        date_pattern='yyyy-mm-dd', state='readonly')),
            ("Ngày kết thúc:", DateEntry(main_frame, width=12, background='darkblue', foreground='white', borderwidth=2,
                                         date_pattern='yyyy-mm-dd', state='readonly'))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)

            if i == 0:
                widget.insert(0, project[1])
            elif i == 1:
                widget.insert("1.0", project[2])
            else:
                widget.set_date(project[i + 1])

        update_button = ttk.Button(main_frame, text="Cập nhật", command=lambda: self.update_project(
            project[0], fields[0][1].get(), fields[1][1].get("1.0", tk.END).strip(),
            fields[2][1].get(), fields[3][1].get(), update_project_window
        ))
        update_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def update_project(self, project_id, name, description, start_date, end_date, window):
        if name and start_date and end_date:
            try:
                datetime.strptime(start_date, '%Y-%m-%d')
                datetime.strptime(end_date, '%Y-%m-%d')
                self.project_controller.update_project(project_id, name, description, start_date, end_date)
                self.load_projects()
                window.destroy()
            except ValueError:
                messagebox.showwarning("Cảnh báo", "Ngày tháng không hợp lệ!")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def export_to_excel(self):
        projects = self.project_controller.get_projects()
        if not projects:
            messagebox.showwarning("Cảnh báo", "Không có dự án để xuất!")
            return

        data = {
            "Tên dự án": [project[1] for project in projects],
            "Mô tả": [project[2] for project in projects],
            "Ngày bắt đầu": [project[3] for project in projects],
            "Ngày kết thúc": [project[4] for project in projects],
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
                name = row.get("Tên dự án")
                description = row.get("Mô tả")
                start_date = row.get("Ngày bắt đầu")
                end_date = row.get("Ngày kết thúc")

                if not name or not description or not start_date or not end_date:
                    messagebox.showwarning("Cảnh báo", f"Cấu trúc file không hợp lệ! Vui lòng kiểm tra lại.")
                    success = False
                    continue

                self.project_controller.add_project(name, description, start_date, end_date)

            self.load_projects()
            if success:
                messagebox.showinfo("Thông báo", "Dữ liệu đã được nhập thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi nhập dữ liệu: {str(e)}")