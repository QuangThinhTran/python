import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('../project_management.db')
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                role TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT,
                start_date TEXT,
                end_date TEXT,
                employee_id INTEGER,
                FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE,
                FOREIGN KEY (employee_id) REFERENCES employees (id)
            )
        ''')
        self.connection.commit()

    def close(self):
        self.connection.close()
