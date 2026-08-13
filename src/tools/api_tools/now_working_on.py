import aiohttp

from config import config

_NEDED_PUSHS_COUNT = 5


async def get_gh_now_working_on_repo(username: str) -> tuple[str, str]:
    """return username, reponame"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "github-widgets-by-kretoffer",
        }
        async with session.get(
            f"https://api.github.com/users/{username}/events/public?per_page=100", headers=headers
        ) as resp:
            if resp.status >= 400:
                raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
            result = await resp.json()
            if not isinstance(result, list):
                raise Exception(f"Unexpected GitHub API response: {result}")

            pushs: dict[str, int] = {}
            for event in result:
                if event["type"] == "PushEvent":
                    if event["repo"]["name"] not in pushs:
                        pushs[event["repo"]["name"]] = 0
                    pushs[event["repo"]["name"]] += 1
                    if pushs[event["repo"]["name"]] >= _NEDED_PUSHS_COUNT:
                        return tuple(event["repo"]["name"].split("/"))

            if not pushs:
                return tuple(result[0]["repo"]["name"].split("/"))

            return tuple(max(pushs, key=pushs.get).split("/"))  # pyright: ignore[reportArgumentType, reportCallIssue]
