import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""CREATE TABLE IF NOT EXISTS complaints(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone_number TEXT,
            complaint TEXT
            )
            """)
            conn.commit()

    def save_survey(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute(
                """
                INSERT INTO complaints (name, phone_number, complaint)
                VALUES (?, ?, ?)
    
                """,
                (data["name"], data["phone_number"], data["complaint"])
            )

    """со словарем"""
    def get_all_complaints(self):
        with sqlite3.connect(self.path) as conn:
            result = conn.execute("SELECT * FROM complaints")
            result.row_factory = sqlite3.Row
            data = result.fetchall()
            return [dict(row) for row in data]
