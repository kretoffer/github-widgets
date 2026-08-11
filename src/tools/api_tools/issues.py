import aiohttp

from config import config
from schemas.external.gh import Issue, IssueLabel


async def get_gh_issues_list(username: str, repo: str, count: int = 20, show_labels: bool = True) -> list[Issue]:
    issues = []
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2026-03-10",
            "User-Agent": "github-widgets-by-kretoffer",
        }
        async with session.get(
            f"https://api.github.com/repos/{username}/{repo}/issues?state=all&per_page={count}", headers=headers
        ) as resp:
            if resp.status >= 400:
                raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
            result = await resp.json()
            if not isinstance(result, list):
                raise Exception(f"Unexpected GitHub API response: {result}")
            for issue in result:
                issues.append(
                    Issue(
                        number=issue["number"],
                        state=issue["state"],
                        title=issue["title"],
                        labels=[
                            IssueLabel(
                                name=label["name"],
                                color=label["color"],
                            )
                            for label in issue["labels"]
                        ]
                        if show_labels
                        else [],
                    )
                )

    return issues
