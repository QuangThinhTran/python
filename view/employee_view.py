import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font as tkFont
import pandas as pd
from tkinter import filedialog

from config.util import Util
from controllers.EmployeeController import EmployeeController


class EmployeeView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.employee_controller = EmployeeController()
        self.util = Util(root)

        self.custom_font = tkFont.Font(family="Helvetica", size=10)

        self.setup_employee_tab()

    def setup_employee_tab(self):
        self.employee_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.RAISED)
        self.employee_frame.pack(pady=20, fill='both', expand=True)

        title_label = ttk.Label(self.employee_frame, text="QUẢN LÝ NHÂN VIÊN", font=("Helvetica", 16))
        title_label.pack(pady=(0, 20))

        button_frame = ttk.Frame(self.employee_frame)
        button_frame.pack(pady=10)

        self.add_employee_button = ttk.Button(button_frame, text="Thêm nhân viên", command=self.show_add_employee_form)
        self.add_employee_button.grid(row=0, column=0, padx=5)

        self.update_employee_button = ttk.Button(button_frame, text="Sửa nhân viên",
                                                 command=self.show_update_employee_form)
        self.update_employee_button.grid(row=0, column=1, padx=5)

        self.delete_employee_button = ttk.Button(button_frame, text="Xóa nhân viên", command=self.delete_employee)
        self.delete_employee_button.grid(row=0, column=2, padx=5)

        self.detail_employee_button = ttk.Button(button_frame, text="Chi tiết nhân viên",
                                                 command=self.show_employee_details)
        self.detail_employee_button.grid(row=0, column=3, padx=5)

        self.employee_list_frame = ttk.Frame(self.employee_frame)
        self.employee_list_frame.pack(pady=10, fill='both', expand=True)

        self.employee_listbox = tk.Listbox(self.employee_list_frame, width=60, height=12, font=self.custom_font,
                                           bg="#f9f9f9", selectbackground="#d0e0f0")
        self.employee_listbox.pack(side=tk.LEFT, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(self.employee_list_frame, orient=tk.VERTICAL,
                                       command=self.employee_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.employee_listbox['yscrollcommand'] = self.scrollbar.set

        self.load_employees()

        bottom_button_frame = ttk.Frame(self.employee_frame)
        bottom_button_frame.pack(pady=10)

        self.export_employee_button = ttk.Button(bottom_button_frame, text="Xuất Excel", command=self.export_to_excel)
        self.export_employee_button.grid(row=0, column=0, padx=5)

        self.import_employee_button = ttk.Button(bottom_button_frame, text="Nhập Excel", command=self.import_from_excel)
        self.import_employee_button.grid(row=0, column=1, padx=5)

    def load_employees(self):
        employees = self.employee_controller.get_employees()
        self.employee_listbox.delete(0, tk.END)
        for employee in employees:
            self.employee_listbox.insert(tk.END, employee[1])

    def show_add_employee_form(self):
        add_employee_window = tk.Toplevel(self.root)
        add_employee_window.title("Thêm Nhân viên")
        self.util.center_window(add_employee_window, 400, 300)
        add_employee_window.geometry("400x300")
        add_employee_window.configure(bg="#f0f0f0")
        add_employee_window.resizable(False, False)

        main_frame = ttk.Frame(add_employee_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Thêm Nhân viên Mới", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Tên nhân viên:", ttk.Entry(main_frame)),
            ("Email:", ttk.Entry(main_frame)),
            ("Chức vụ:", self.create_role_listbox(main_frame))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)

        add_button = ttk.Button(main_frame, text="Thêm", command=lambda: self.add_employee(
            fields[0][1].get(), fields[1][1].get(), fields[2][1].get(), add_employee_window
        ))
        add_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def add_employee(self, name, email, role, window):
        if name and email and role:
            if not self.validate_email(email):
                messagebox.showwarning("Cảnh báo", "Email không hợp lệ!")
                return
            self.employee_controller.add_employee(name, email, role)
            self.load_employees()
            window.destroy()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def show_update_employee_form(self):
        update_employee_window = tk.Toplevel(self.root)
        update_employee_window.title("Sửa Nhân viên")
        self.util.center_window(update_employee_window, 400, 300)
        update_employee_window.geometry("400x300")
        update_employee_window.configure(bg="#f0f0f0")
        update_employee_window.resizable(False, False)
        selected_index = self.employee_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để cập nhật!")
            return

        employee = self.employee_controller.get_employees()[selected_index[0]]

        main_frame = ttk.Frame(update_employee_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Cập Nhật Nhân viên", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Tên nhân viên:", ttk.Entry(main_frame)),
            ("Email:", ttk.Entry(main_frame)),
            ("Chức vụ:", self.create_role_listbox(main_frame))
        ]

        for i, (label, widget) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            widget.grid(row=i + 1, column=1, sticky=tk.EW, pady=5)
            if i < 2:
                widget.insert(0, employee[i + 1])
            else:
                widget.set(employee[i + 1])

        update_button = ttk.Button(main_frame, text="Cập nhật", command=lambda: self.update_employee(
            employee[0], fields[0][1].get(), fields[1][1].get(), fields[2][1].get(), update_employee_window
        ))
        update_button.grid(row=len(fields) + 1, column=0, columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def update_employee(self, employee_id, name, email, role, window):
        if name and email and role:
            if not self.validate_email(email):
                messagebox.showwarning("Cảnh báo", "Email không hợp lệ!")
                return
            self.employee_controller.update_employee(employee_id, name, email, role)
            self.load_employees()
            window.destroy()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def delete_employee(self):
        selected_index = self.employee_listbox.curselection()
        if selected_index:
            employee_id = self.employee_controller.get_employees()[selected_index[0]][0]
            self.employee_controller.delete_employee(employee_id)
            self.load_employees()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để xóa!")

    def show_employee_details(self):
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Chi tiết Nhân viên")
        self.util.center_window(detail_window, 400, 300)
        detail_window.geometry("400x250")
        detail_window.configure(bg="#f0f0f0")
        detail_window.resizable(False, False)
        selected_index = self.employee_listbox.curselection()

        if not selected_index:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn nhân viên để xem chi tiết!")
            return

        employee = self.employee_controller.get_employees()[selected_index[0]]

        main_frame = ttk.Frame(detail_window, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Chi Tiết Nhân viên", font=("Helvetica", 16, "bold")).grid(row=0, column=0,
                                                                                              columnspan=2,
                                                                                              pady=(0, 20))

        fields = [
            ("Tên nhân viên:", employee[1]),
            ("Email:", employee[2]),
            ("Vai trò:", employee[3])
        ]

        for i, (label, value) in enumerate(fields):
            ttk.Label(main_frame, text=label).grid(row=i + 1, column=0, sticky=tk.W, pady=5)
            ttk.Label(main_frame, text=value).grid(row=i + 1, column=1, sticky=tk.W, pady=5)

        ttk.Button(main_frame, text="Đóng", command=detail_window.destroy).grid(row=len(fields) + 1, column=0,
                                                                                columnspan=2, pady=(20, 0))

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)

        main_frame.grid_columnconfigure(1, weight=1)

    def create_role_listbox(self, parent):
        role_listbox = ttk.Combobox(parent, values=["Quản lý", "Nhân viên"], state="readonly")
        role_listbox.set("Nhân viên")
        return role_listbox

    def validate_email(self, email):
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def export_to_excel(self):
        employees = self.employee_controller.get_employees()
        if not employees:
            messagebox.showwarning("Cảnh báo", "Không có nhân viên để xuất!")
            return

        data = {
            "Tên nhân viên": [employee[1] for employee in employees],
            "Email": [employee[2] for employee in employees],
            "Vai trò": [employee[3] for employee in employees],
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
                name = row.get("Tên nhân viên")
                email = row.get("Email")
                role = row.get("Vai trò")

                if not name or not email or not role:
                    messagebox.showwarning("Cảnh báo", f"Cấu trúc file không hợp lệ! Vui lòng kiểm tra lại.")
                    success = False
                    continue

                self.employee_controller.add_employee(name, email, role)

            self.load_employees()
            if success:
                messagebox.showinfo("Thông báo", "Dữ liệu đã được nhập thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra khi nhập dữ liệu: {str(e)}")
