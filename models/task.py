class Task:
    def __init__(self, project_id, name, description, status, start_date, end_date, employee_id=None):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.employee_id = employee_id