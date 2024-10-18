import tkinter as tk
from tkinter import ttk, messagebox

from controllers.EmployeeController import EmployeeController


class EmployeeView(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.employee_controller = EmployeeController()
        self.setup_employee_tab()

    def setup_employee_tab(self):
        # Adjusting padding and layout for a more modern UI
        self.employee_frame = ttk.Frame(self.root, padding=(20, 20), relief=tk.FLAT)  # Changed relief to FLAT
        self.employee_frame.pack(pady=30)  # Increased padding

        # Adding a title label
        ttk.Label(self.employee_frame, text="Quản lý nhân viên", font=("Arial", 16)).grid(row=0, columnspan=2, pady=(0, 10))

        # Employee Name
        ttk.Label(self.employee_frame, text="Tên nhân viên:").grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.employee_name_entry = ttk.Entry(self.employee_frame)
        self.employee_name_entry.grid(row=1, column=1, pady=(5, 0))

        # Email
        ttk.Label(self.employee_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=(5, 0))
        self.employee_email_entry = ttk.Entry(self.employee_frame)
        self.employee_email_entry.grid(row=2, column=1, pady=(5, 0))

        # Role
        ttk.Label(self.employee_frame, text="Vai trò:").grid(row=3, column=0, sticky=tk.W, pady=(5, 0))
        self.employee_role_entry = ttk.Entry(self.employee_frame)
        self.employee_role_entry.grid(row=3, column=1, pady=(5, 0))

        # Adding a more modern button style
        self.add_employee_button = ttk.Button(self.employee_frame, text="Thêm nhân viên", command=self.add_employee, style="Accent.TButton")  # Changed style
        self.add_employee_button.grid(row=4, columnspan=2, pady=(15, 10))  # Adjusted padding

        self.employee_listbox = tk.Listbox(self.employee_frame, width=50, height=10)
        self.employee_listbox.grid(row=5, columnspan=2, pady=(5, 0))

        self.scrollbar = ttk.Scrollbar(self.employee_frame, orient=tk.VERTICAL, command=self.employee_listbox.yview)
        self.scrollbar.grid(row=5, column=2, sticky='ns')
        self.employee_listbox['yscrollcommand'] = self.scrollbar.set

        # Adding a more modern button style
        self.detail_employee_button = ttk.Button(self.employee_frame, text="Chi tiết nhân viên", command=self.show_employee_details, style="Accent.TButton")  # Changed style
        self.detail_employee_button.grid(row=6, columnspan=2, pady=10)  # Adjusted padding

        self.load_employees()

    def load_employees(self):
        employees = self.employee_controller.get_employees()
        self.employee_listbox.delete(0, tk.END)
        for employee in employees:
            self.employee_listbox.insert(tk.END, employee[1])  # Use the key 'name' to access the employee's name

    def add_employee(self):
        name = self.employee_name_entry.get()
        email = self.employee_email_entry.get()
        role = self.employee_role_entry.get()

        if name and email and role:
            self.employee_controller.add_employee(name, email, role)
            self.load_employees()
            self.clear_employee_fields()
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ thông tin!")

    def clear_employee_fields(self):
        self.employee_name_entry.delete(0, tk.END)
        self.employee_email_entry.delete(0, tk.END)
        self.employee_role_entry.delete(0, tk.END)

    def show_employee_details(self):
        selected_index = self.employee_listbox.curselection()
        if selected_index:
            mployee_id = self.employee_controller.get_employees()[selected_index[0]][0]
            mployee = self.employee_controller.get_employees()[selected_index[0]]

            detail_window = tk.Toplevel(self.root)
            detail_window.title("Chi tiết Nhân Viên")
            detail_window.geometry("450x350")  # Adjusted size for better visibility

            ttk.Label(detail_window, text="Tên nhân viên:").grid(row=0, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=mployee[1]).grid(row=0, column=1)

            ttk.Label(detail_window, text="Email:").grid(row=1, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=mployee[2]).grid(row=1, column=1)

            ttk.Label(detail_window, text="Vai trò:").grid(row=2, column=0, sticky=tk.W)
            ttk.Label(detail_window, text=mployee[3]).grid(row=2, column=1)

            ttk.Button(detail_window, text="Đóng", command=detail_window.destroy).grid(row=3, columnspan=2, pady=10)
