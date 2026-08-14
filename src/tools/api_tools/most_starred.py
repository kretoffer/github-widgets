import aiohttp

from config import config
from schemas.external.gh import RepoInfo


async def get_gh_most_stared_repos(
    username: str, count: int = 3, show_license: bool = True, show_language: bool = True
) -> list[RepoInfo]:
    """Return top starred repos names desc"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "github-widgets-by-kretoffer",
        }
        async with session.get(f"https://api.github.com/users/{username}/repos?per_page=100", headers=headers) as resp:
            if resp.status >= 400:
                raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
            result = await resp.json()
            if not isinstance(result, list):
                raise Exception(f"Unexpected GitHub API response: {result}")

            repositories = []
            for repo in result:
                license = repo.get("license")
                repositories.append(
                    RepoInfo(
                        full_name=repo["full_name"],
                        description=repo.get("description"),
                        stars=repo.get("stargazers_count", 0),
                        forks=repo.get("forks_count", 0),
                        language=repo.get("language") if show_language else None,
                        license=license.get("spdx_id") if license and show_license else None,
                    )
                )

            repositories.sort(key=lambda r: r.stars, reverse=True)
            return repositories[:count]
