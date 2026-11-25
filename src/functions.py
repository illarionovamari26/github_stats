import requests


def get_repos_stats(username: str) -> list[dict]:
    """Получает статистику по репозиториям пользователя GitHub."""
    url = f"https://api.github.com/users/{username}/repos"
    params = {
        "per_page": 100,
        "sort": "updated",
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    repos = response.json()
    stats = []

    for repo in repos:
        stats.append(
            {
                "name": repo.get("name"),
                "html_url": repo.get("html_url"),
                "description": repo.get("description"),
                "language": repo.get("language"),
                "stars": repo.get("stargazers_count", 0),
                "forks": repo.get("forks_count", 0),
            }
        )

    return stats