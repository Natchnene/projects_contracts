from sqlite import db
from datetime import date


class Contract:

    def __init__(self, name: str):
        self.name = name
        self.created_date = date.today()
        self.signing_date = None
        self.status = "Черновик"
        self.project_id = None

    def save(self):
        db.cursor.execute("INSERT INTO contracts (name, created_date, signing_date, status, project_id) VALUES (?, ?, ?, ?, ?)",
                          (self.name, self.created_date, self.signing_date, self.status, self.project_id))
        db.connection.commit()


class Project:

    def __init__(self, name: str):
        self.name = name
        self.created_date = date.today()

    def save(self):
        db.cursor.execute("INSERT INTO projects (name, created_date) VALUES (?, ?)", (self.name, self.created_date))
        db.connection.commit()
