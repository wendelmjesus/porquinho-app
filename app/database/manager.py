import os
import sqlite3


class DatabaseManager:
    def __init__(self, database_path, default_categories):
        self.database_path = database_path
        self.default_categories = default_categories
        self.schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")

    def connect(self):
        os.makedirs(os.path.dirname(self.database_path), exist_ok=True)
        return sqlite3.connect(self.database_path)

    def initialize(self):
        with self.connect() as connection:
            with open(self.schema_path, "r", encoding="utf-8") as schema_file:
                connection.executescript(schema_file.read())

            category_count = connection.execute(
                "SELECT COUNT(*) FROM categories"
            ).fetchone()[0]

            if category_count == 0:
                for category_type, categories in self.default_categories.items():
                    for category_name in categories:
                        connection.execute(
                            "INSERT OR IGNORE INTO categories (type, name) VALUES (?, ?)",
                            (category_type, category_name),
                        )

    def load_data(self):
        with self.connect() as connection:
            category_rows = connection.execute(
                "SELECT type, name FROM categories ORDER BY type, LOWER(name)"
            ).fetchall()
            transaction_rows = connection.execute(
                """
                SELECT id, description, category, type, date, amount
                FROM transactions
                ORDER BY id DESC
                """
            ).fetchall()
            goal_rows = connection.execute(
                "SELECT id, name, target, current FROM goals ORDER BY id DESC"
            ).fetchall()

        categories = {
            "Receita": [],
            "Despesa": [],
        }

        for category_type, category_name in category_rows:
            categories.setdefault(category_type, []).append(category_name)

        for category_type in self.default_categories:
            if "Outros" not in categories.get(category_type, []):
                categories.setdefault(category_type, []).append("Outros")
                self.save_category(category_type, "Outros")

        transactions = [
            {
                "id": transaction_id,
                "description": description,
                "category": category,
                "type": transaction_type,
                "date": transaction_date,
                "amount": amount,
            }
            for transaction_id, description, category, transaction_type, transaction_date, amount
            in transaction_rows
        ]

        goals = [
            {
                "id": goal_id,
                "name": name,
                "target": target,
                "current": current,
            }
            for goal_id, name, target, current in goal_rows
        ]

        return categories, transactions, goals

    def save_category(self, category_type, category_name):
        with self.connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO categories (type, name) VALUES (?, ?)",
                (category_type, category_name),
            )

    def delete_category(self, category_type, category_name):
        with self.connect() as connection:
            connection.execute(
                "DELETE FROM categories WHERE type = ? AND name = ?",
                (category_type, category_name),
            )

    def save_transaction(self, transaction):
        with self.connect() as connection:
            connection.execute(
                """
                INSERT INTO transactions (description, category, type, date, amount)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    transaction["description"],
                    transaction["category"],
                    transaction["type"],
                    transaction["date"],
                    transaction["amount"],
                ),
            )
            transaction["id"] = connection.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]

    def update_transaction(self, transaction):
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE transactions
                SET description = ?, category = ?, type = ?, date = ?, amount = ?
                WHERE id = ?
                """,
                (
                    transaction["description"],
                    transaction["category"],
                    transaction["type"],
                    transaction["date"],
                    transaction["amount"],
                    transaction["id"],
                ),
            )

    def delete_transactions(self, transaction_ids):
        with self.connect() as connection:
            connection.executemany(
                "DELETE FROM transactions WHERE id = ?",
                [(transaction_id,) for transaction_id in transaction_ids],
            )

    def save_goal(self, goal):
        with self.connect() as connection:
            connection.execute(
                "INSERT INTO goals (name, target, current) VALUES (?, ?, ?)",
                (goal["name"], goal["target"], goal["current"]),
            )
            goal["id"] = connection.execute(
                "SELECT last_insert_rowid()"
            ).fetchone()[0]

    def update_goal(self, goal):
        with self.connect() as connection:
            connection.execute(
                """
                UPDATE goals
                SET name = ?, target = ?, current = ?
                WHERE id = ?
                """,
                (goal["name"], goal["target"], goal["current"], goal["id"]),
            )

    def delete_goals(self, goal_ids):
        with self.connect() as connection:
            connection.executemany(
                "DELETE FROM goals WHERE id = ?",
                [(goal_id,) for goal_id in goal_ids],
            )
