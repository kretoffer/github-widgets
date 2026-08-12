import aiohttp

from config import config
from schemas.external.gh import RepoInfo


async def get_gh_repo_info(username: str, repo: str, show_license: bool = True, show_language: bool = True) -> RepoInfo:
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "github-widgets-by-kretoffer",
        }
        async with session.get(f"https://api.github.com/repos/{username}/{repo}", headers=headers) as resp:
            if resp.status >= 400:
                raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
            result = await resp.json()
            if not isinstance(result, dict):
                raise Exception(f"Unexpected GitHub API response: {result}")

    license = result.get("license")
    return RepoInfo(
        full_name=result["full_name"],
        description=result.get("description"),
        stars=result.get("stargazers_count", 0),
        forks=result.get("forks_count", 0),
        language=result.get("language") if show_language else None,
        license=license.get("spdx_id") if license and show_license else None,
    )
