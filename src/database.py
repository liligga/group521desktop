import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS todos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    todo TEXT,
                    category TEXT
                )
                """
            )
            conn.commit()

    def add_todo(self, todo: str, category: str):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO todos (todo, category) VALUES (?, ?)
                """,
                (todo, category),
            )
            conn.commit()

    def all_todos(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos")
            return cursor.fetchall()
