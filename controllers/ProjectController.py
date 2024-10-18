from database import Database


class ProjectController:
    def __init__(self):
        self.db = Database()

    def add_project(self, name, description, start_date, end_date):
        self.db.cursor.execute('''
            INSERT INTO projects (name, description, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (name, description, start_date, end_date))
        self.db.connection.commit()

    def delete_project(self, project_id):
        self.db.cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.db.connection.commit()

    def update_project(self, project_id, name, description, start_date, end_date):
        self.db.cursor.execute('''
            UPDATE projects SET name = ?, description = ?, start_date = ?, end_date = ?
            WHERE id = ?
        ''', (name, description, start_date, end_date, project_id))
        self.db.connection.commit()

    def get_projects(self):
        self.db.cursor.execute('SELECT * FROM projects')
        return self.db.cursor.fetchall()