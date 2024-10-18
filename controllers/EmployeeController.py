from database import Database

class EmployeeController:
    def __init__(self):
        self.db = Database()

    def add_employee(self, name, email, role):
        self.db.cursor.execute('''
            INSERT INTO employees (name, email, role)
            VALUES (?, ?, ?)
        ''', (name, email, role))
        self.db.connection.commit()

    def get_employees(self):
        self.db.cursor.execute('SELECT * FROM employees')
        return self.db.cursor.fetchall()    

    def get_employee_name(self, employee_id):
        self.db.cursor.execute('SELECT name FROM employees WHERE id = ?', (employee_id,))
        result = self.db.cursor.fetchone()
        return result[0] if result else "Không có"

    def get_employee_details(self, employee_name):
        # Assuming you have a list or database of employees
        for employee in self.employees:  # Replace with your actual data source
            if employee['name'] == employee_name:
                return employee
        return None  # Return None if not found
