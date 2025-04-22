import sqlite3


class Database:
    def __init__(self, path: str):
        self.path = path

    # создание таблиц, если они не существуют
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

    # добавление задачи(todo) в таблицу todos
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

    # получение всех задач из таблицы todos
    def all_todos(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM todos")
            # возвращает список кортежей!
            return cursor.fetchall()
