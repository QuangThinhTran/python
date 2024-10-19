from config.database import Database


class EmployeeController:
    def __init__(self):
        self.employees = None
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
        for employee in self.employees:
            if employee['name'] == employee_name:
                return employee
        return None

    def update_employee(self, employee_id, name, email, role):
        self.db.cursor.execute(''' 
            UPDATE employees SET name = ?, email = ?, role = ? 
            WHERE id = ? 
        ''', (name, email, role, employee_id))
        self.db.connection.commit()

    def delete_employee(self, employee_id):
        self.db.cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))
        self.db.connection.commit()
