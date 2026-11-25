import json
from typing import Optional
import psycopg2


class PostgresDB:
    """Класс для работы с таблицей статистики репозиториев в PostgreSQL."""

    def __init__(self, params: dict) -> None:
        self.params = params

    def create_table(self) -> None:
        """Создаёт таблицу для хранения статистики репозиториев."""
        conn = psycopg2.connect(**self.params)
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS repositories (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        html_url TEXT,
                        description TEXT,
                        language VARCHAR(100),
                        stars INTEGER DEFAULT 0,
                        forks INTEGER DEFAULT 0
                    )
                    """
                )
            conn.commit()
        finally:
            conn.close()

    def insert_data(self, repos_data: list[dict]) -> None:
        """Добавляет список словарей с данными о репозиториях в таблицу."""
        conn = psycopg2.connect(**self.params)
        try:
            with conn.cursor() as cur:
                for repo in repos_data:
                    cur.execute(
                        """
                        INSERT INTO repositories (name, html_url, description, language, stars, forks)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            repo.get("name"),
                            repo.get("html_url"),
                            repo.get("description"),
                            repo.get("language"),
                            repo.get("stars", 0),
                            repo.get("forks", 0),
                        ),
                    )
            conn.commit()
        finally:
            conn.close()

    def get_data(self, limit: Optional[int] = None) -> list[tuple]:
        """Возвращает строки из таблицы repositories."""
        conn = psycopg2.connect(**self.params)
        try:
            with conn.cursor() as cur:
                query = "SELECT id, name, html_url, description, language, stars, forks FROM repositories"
                if limit is not None:
                    cur.execute(f"{query} LIMIT %s", (limit,))
                else:
                    cur.execute(query)
                return cur.fetchall()
        finally:
            conn.close()

    def export_to_json(self, filename: str = "repos_stats.json") -> None:
        """Экспортирует данные из таблицы в JSON-файл."""
        rows = self.get_data()
        columns = ["id", "name", "html_url", "description", "language", "stars", "forks"]
        data_to_export = [dict(zip(columns, row)) for row in rows]

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data_to_export, file, ensure_ascii=False, indent=2)