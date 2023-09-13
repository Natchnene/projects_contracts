import sqlite3
from datetime import date


class Database:

    def __init__(self):
        self.connection = sqlite3.connect("sqlite3.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS projects "
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "name TEXT NOT NULL, "
                            "created_date TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS contracts "
                            "(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                            "name TEXT NOT NULL, "
                            "created_date TEXT NOT NULL, "
                            "signing_date TEXT,"
                            "status TEXT NOT NULL,"
                            "project_id INTEGER, "
                            "FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE SET NULL)")
        self.connection.commit()

    def all_contracts(self):
        """ Get all contracts """
        self.cursor.execute("SELECT * FROM contracts")
        contracts = self.cursor.fetchall()
        if len(contracts) != 0:
            print("\nСписок договоров:")
            for contract in contracts:
                print(f"ID-{contract[0]} {contract[1]} {contract[4]}")
        else:
            print("У вас нет договоров.")

    def all_draft_contracts(self):
        """ Get all contracts status = 'Черновик' """
        self.cursor.execute("SELECT * FROM contracts WHERE status = 'Черновик'")
        draft_contracts = self.cursor.fetchall()
        return draft_contracts

    def all_active_contracts(self):
        """ Get all contracts status = 'Активен' """
        self.cursor.execute("SELECT * FROM contracts WHERE status = 'Активен'")
        active_contracts = self.cursor.fetchall()
        return active_contracts

    def all_active_free_contracts(self):
        """ Get all contracts status = 'Активен' and project_id = NULL"""
        self.cursor.execute("SELECT * FROM contracts WHERE status = 'Активен' AND project_id IS NULL")
        active_free_contracts = self.cursor.fetchall()
        return active_free_contracts

    def all_projects(self):
        """ Get all projects """
        self.cursor.execute("SELECT * FROM projects")
        projects = self.cursor.fetchall()
        if len(projects) != 0:
            print("\nСписок проектов:")
            for project in self.cursor.fetchall():
                print(f"ID-{project[0]} {project[1]}")
        else:
            print("У вас нет проектов.")

    def all_active_projects(self):
        """ Get all projects, which have active contract """
        self.cursor.execute("SELECT * FROM projects "
                            "INNER JOIN contracts ON projects.id = contracts.project_id "
                            "AND contracts.status = 'Активен'")
        return self.cursor.fetchall()

    def sign(self, contract_id):
        """ Makes the contract active """
        self.cursor.execute("SELECT id FROM contracts WHERE id = ? AND status = ?", (contract_id, 'Черновик'))
        id = self.cursor.fetchone()
        if id is not None:
            self.cursor.execute("UPDATE contracts SET status = 'Активен', signing_date = ?  WHERE id = ?",
                                (date.today(), contract_id))
            self.connection.commit()
            print("\nДоговор подтвержден.")
        else:
            print("\nНеверный ID договора.")

    def finalise(self, contract_id):
        """ Makes the contract complete """
        self.cursor.execute("SELECT id FROM contracts WHERE id = ? AND status = ?", (contract_id, 'Активен'))
        id = self.cursor.fetchone()
        if id is not None:
            self.cursor.execute("UPDATE contracts SET status = ?  WHERE id = ?", ('Завершен', contract_id))
            self.connection.commit()
            print("\nДоговор завершен.")
        else:
            print("\nНеверный ID договора.")

    def add_contract(self, project_id, contract_id):
        """Adds the contract to the project """
        self.cursor.execute("SELECT id FROM contracts WHERE project_id = ? AND status = 'Активен'", project_id)
        contract = self.cursor.fetchone()
        if contract is None:
            self.cursor.execute("UPDATE contracts SET project_id = ?  WHERE id = ?", (project_id, contract_id))
            self.connection.commit()
            print("\nДоговор успешно добавлен.")
        else:
            print(f"\nУ проекта ID-{project_id} уже есть активный договор.")


db = Database()
