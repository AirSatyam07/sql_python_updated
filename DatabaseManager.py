import sqlite3
import os

class Database_manager:
    def __init__(self, db_name="database/bank4.db"):
        self.db_name = db_name
        # Ensure the directory exists
        os.makedirs(os.path.dirname(db_name), exist_ok=True)
        self.conn = sqlite3.connect(db_name)
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                userid VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL
            )
        ''')

        self.curr.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                ssn_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone INTEGER,
                usrname VARCHAR(255) NOT NULL,
                pwd VARCHAR(255) NOT NULL,
                ACCOUNT_NO VARCHAR(255) UNIQUE NOT NULL,
                AMOUNT FLOAT DEFAULT 0
            )
        ''')

    def execute(self, query, params=()):
        self.curr.execute(query, params)
        self.conn.commit()

    def fetchone(self, query, params=()):
        self.curr.execute(query, params)
        return self.curr.fetchone()

    def fetchall(self, query, params=()):
        self.curr.execute(query, params)
        return self.curr.fetchall()

    def close(self):
        self.conn.close()

    def fetch_all_customers(self):
        q = "SELECT * FROM customers"
        self.curr.execute(q)
        rows = self.curr.fetchall()
        for row in rows:
            print(row)


# Example usage
if __name__ == "__main__":
    db = Database_manager()
    db.create_table()
    db.fetch_all_customers()
