import aiohttp

from typing import List

from schemas.external.gh import Issue, IssueLabel


async def get_gh_issues_list(username: str, repo: str, count: int = 20) -> List[Issue]:
    issues = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.github.com/repos/{username}/{repo}/issues?state=all&per_page={count}") as resp:
            for issue in await resp.json():
                issues.append(Issue(
                    number=issue["number"],
                    state=issue["state"],
                    title=issue["title"],
                    labels=[IssueLabel(
                        name=label["name"],
                        color=label["color"]
                    ) for label in issue["labels"]]
                ))

    return issues
