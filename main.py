from configparser import ConfigParser

from src.functions import get_repos_stats
from src.postgres_db import PostgresDB


def load_db_config(filename: str = "database.ini", section: str = "postgresql") -> dict:
    """Читает параметры подключения к базе данных из INI-файла."""
    parser = ConfigParser()
    parser.read(filename)

    if not parser.has_section(section):
        raise ValueError(f"Секция '{section}' не найдена в файле '{filename}'.")

    return dict(parser.items(section))


def main() -> None:
    username = "illarionovamari26"
    db_params = load_db_config()

    repos_stats = get_repos_stats(username)

    db = PostgresDB(db_params)
    db.create_table()
    db.insert_data(repos_stats)
    db.export_to_json("repos_stats.json")

    print(f"Сохранено репозиториев: {len(repos_stats)}. Выгружено в repos_stats.json.")


if __name__ == "__main__":
    main()