import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
from tkcalendar import DateEntry
from datetime import datetime

from controllers.ProjectController import ProjectController


class ProjectView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.project_controller = ProjectController()


        self.custom_font = tkFont.Font(family="Helvetica", size=10)

        self.setup_project_tab()

    def setup_project_tab(self):
        self.project_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.RAISED)  # Increased padding
        self.project_frame.pack(pady=20, fill='both', expand=True)  # Allow frame to expand

        # Title Label
        title_label = ttk.Label(self.project_frame, text="Quản lý Dự Án", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))  # Add some space below the title

        # Button Frame
        button_frame = ttk.Frame(self.project_frame)
        button_frame.pack(pady=10)

        # Add buttons to the button frame
        self.add_project_button = ttk.Button(button_frame, text="Thêm dự án", command=self.show_add_project_form)
        self.add_project_button.grid(row=0, column=0, padx=5)

        self.update_project_button = ttk.Button(button_frame, text="Sửa dự án", command=self.show_update_project_form)
        self.update_project_button.grid(row=0, column=1, padx=5)

        self.delete_project_button = ttk.Button(button_frame, text="Xóa dự án", command=self.delete_project)
        self.delete_project_button.grid(row=0, column=2, padx=5)

        self.detail_project_button = ttk.Button(button_frame, text="Chi tiết dự án", command=self.show_project_details)
        self.detail_project_button.grid(row=0, column=3, padx=5)

        # Project List Frame
        self.project_list_frame = ttk.Frame(self.project_frame)
        self.project_list_frame.pack(pady=10, fill='both', expand=True)

        self.project_listbox = tk.Listbox(self.project_list_frame, width=60, height=12, font=self.custom_font, bg="#f9f9f9", selectbackground="#d0e0f0")
        self.project_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.project_list_frame, orient=tk.VERTICAL, command=self.project_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.project_listbox['yscrollcommand'] = self.scrollbar.set

        self.load_projects()

    def show_project_details(self):
        selected_index = self.project_listbox.curselection()
        if selected_index:
            project_id = self.project_controller.get_projects()[selected_index[0]][0]
            project = self.project_controller.get_projects()[selected_index[0]]

            detail_window = tk.Toplevel(self.root)
            detail_window.title("Chi tiết Dự Án")
            detail_window.geometry("400x300")

            ttk.Label(detail_window, text="Tên dự án:").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=project[1]).grid(row=0, column=1)

            ttk.Label(detail_window, text="Mô tả:").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=project[2]).grid(row=1, column=1)

            ttk.Label(detail_window, text="Ngày bắt đầu:").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=project[3]).grid(row=2, column=1)

            ttk.Label(detail_window, text="Ngày kết thúc:").grid(row=3, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=project[4]).grid(row=3, column=1)

            ttk.Button(detail_window, text="Đóng", command=detail_window.destroy).grid(row=4, columnspan=2, pady=10)

    def load_projects(self):
        projects = self.project_controller.get_projects()
        self.project_listbox.delete(0, tk.END)
        for project in projects:
            self.project_listbox.insert(tk.END, project[1])

    def show_add_project_form(self):
        add_project_window = tk.Toplevel(self.root)
        add_project_window.title("Thêm Dự Án")
        add_project_window.geometry("450x400")
        add_project_window.configure(bg="#f0f0f0")

        # Use grid layout for better organization
        ttk.Label(add_project_window, text="Tên dự án:", background="#f0f0f0").grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        project_name_entry = ttk.Entry(add_project_window)
        project_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(add_project_window, text="Mô tả:", background="#f0f0f0").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        project_desc_entry = ttk.Entry(add_project_window)
        project_desc_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(add_project_window, text="Ngày bắt đầu:", background="#f0f0f0").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        start_date_entry = DateEntry(add_project_window, width=12, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        start_date_entry.grid(row=2, column=1, padx=10, pady=5)
        start_date_entry.config(state='readonly')

        ttk.Label(add_project_window, text="Ngày kết thúc:", background="#f0f0f0").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        end_date_entry = DateEntry(add_project_window, width=12, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        end_date_entry.grid(row=3, column=1, padx=10, pady=5)
        end_date_entry.config(state='readonly')

        add_button = ttk.Button(add_project_window, text="Thêm",
                                command=lambda: self.add_project(project_name_entry.get(), project_desc_entry.get(),
                                                                 start_date_entry.get(), end_date_entry.get(),
                                                                 add_project_window))
        add_button.grid(row=4, columnspan=2, pady=10, padx=5)  # Added padding
        add_button.configure(style='Accent.TButton')  # Change button style
        add_button.bind("<Enter>", lambda e: self.add_tooltip(add_button, "Thêm dự án mới"))  # Tooltip

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
            self.project_controller.delete_project(project_id)
            self.load_projects()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn dự án để xóa!")

    def show_update_project_form(self):
        selected_index = self.project_listbox.curselection()
        if selected_index:
            project_id = self.project_controller.get_projects()[selected_index[0]][0]
            project = self.project_controller.get_projects()[selected_index[0]]

            update_project_window = tk.Toplevel(self.root)
            update_project_window.title("Sửa Dự Án")
            update_project_window.geometry("400x300")

            ttk.Label(update_project_window, text="Tên dự án:").grid(row=0, column=0, sticky=tk.W)
            project_name_entry = ttk.Entry(update_project_window)
            project_name_entry.insert(0, project[1])
            project_name_entry.grid(row=0, column=1)

            ttk.Label(update_project_window, text="Mô tả:").grid(row=1, column=0, sticky=tk.W)
            project_desc_entry = ttk.Entry(update_project_window)
            project_desc_entry.insert(0, project[2])
            project_desc_entry.grid(row=1, column=1)

            ttk.Label(update_project_window, text="Ngày bắt đầu:").grid(row=2, column=0, sticky=tk.W)
            start_date_entry = DateEntry(update_project_window, width=12, background='darkblue',
                                         foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            start_date_entry.set_date(project[3])
            start_date_entry.grid(row=2, column=1)

            ttk.Label(update_project_window, text="Ngày kết thúc:").grid(row=3, column=0, sticky=tk.W)
            end_date_entry = DateEntry(update_project_window, width=12, background='darkblue',
                                       foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
            end_date_entry.set_date(project[4])
            end_date_entry.grid(row=3, column=1)

            update_button = ttk.Button(update_project_window, text="Cập nhật",
                                       command=lambda: self.update_project(project_id, project_name_entry.get(),
                                                                           project_desc_entry.get(),
                                                                           start_date_entry.get(), end_date_entry.get(),
                                                                           update_project_window))
            update_button.grid(row=4, columnspan=2, pady=10)

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
