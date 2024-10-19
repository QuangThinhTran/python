from config.database import Database


class TaskController:
    def __init__(self):
        self.db = Database()

    def add_task(self, project_id, name, description, status, start_date, end_date, employee_id=None):
        self.db.cursor.execute('''
            INSERT INTO tasks (project_id, name, description, status, start_date, end_date, employee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (project_id, name, description, status, start_date, end_date, employee_id))
        self.db.connection.commit()

    def delete_task(self, task_id):
        self.db.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.db.connection.commit()

    def update_task(self, task_id, project_id, name, description, status, start_date, end_date, employee_id=None):
        self.db.cursor.execute('''
            UPDATE tasks SET project_id = ?, name = ?, description = ?, status = ?, start_date = ?, end_date = ?, employee_id = ?
            WHERE id = ?
        ''', (project_id, name, description, status, start_date, end_date, employee_id, task_id))
        self.db.connection.commit()

    def get_tasks_by_project(self, project_id):
        self.db.cursor.execute('SELECT * FROM tasks WHERE project_id = ?', (project_id,))
        return self.db.cursor.fetchall()
