import asyncio
import re
from datetime import date
from typing import Any

import aiohttp

from config import config
from schemas.external.gh import Metric, UserStats

_GH_API = "https://api.github.com"
_PAGE_SIZE = 100
_MAIN = "repository"

_HEADERS = {
    "Authorization": f"Bearer {config.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "github-widgets-by-kretoffer",
}

_ICONS = {
    "stars": (
        "M8 .25a.75.75 0 0 1 .673.418l1.882 3.815 4.21.612a.75.75 0 0 1 .416 1.279l-3.046 2.97.719 4.192a.751.751"
        + " 0 0 1-1.088.791L8 12.347l-3.766 1.98a.75.75 0 0 1-1.088-.79l.72-4.194L.818 6.374a.75.75 0 0 1"
        + " .416-1.28l4.21-.611L7.327.668A.75.75 0 0 1 8 .25Zm0 2.445L6.615 5.5a.75.75 0 0 1-.564.41l-3.097.45 2.24"
        + " 2.184a.75.75 0 0 1 .216.664l-.528 3.084 2.769-1.456a.75.75 0 0 1 .698 0l2.77 1.456-.53-3.084a.75.75 0 0"
        + " 1 .216-.664l2.24-2.183-3.096-.45a.75.75 0 0 1-.564-.41L8 2.694Z"
    ),
    "commits": ("M8 2a6 6 0 100 12A6 6 0 008 2zm0 1.5a4.5 4.5 0 110 9 4.5 4.5 0 010-9zM8 5a3 3 0 100 6 3 3 0 000-6z"),
    "commits-year": (
        "M4.75 0a.75.75 0 0 1 .75.75V2h5V.75a.75.75 0 0 1 1.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0"
        + " 0 1 13.25 16H2.75A1.75 1.75 0 0 1 1 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 0 1 4.75 0ZM2.5"
        + " 7.5v6.75c0 .138.112.25.25.25h10.5a.25.25 0 0 0 .25-.25V7.5Zm10.75-4H2.75a.25.25 0 0"
        + " 0-.25.25V6h11V3.75a.25.25 0 0 0-.25-.25Z"
    ),
    "prs": (
        "M1.5 3.25a2.25 2.25 0 1 1 3 2.122v5.256a2.251 2.251 0 1 1-1.5 0V5.372A2.25 2.25 0 0 1 1.5"
        + " 3.25Zm5.677-.177L9.573.677A.25.25 0 0 1 10 .854V2.5h1A2.5 2.5 0 0 1 13.5 5v5.628a2.251 2.251 0 1 1-1.5"
        + " 0V5a1 1 0 0 0-1-1h-1v1.646a.25.25 0 0 1-.427.177L7.177 3.427a.25.25 0 0 1 0-.354ZM3.75 2.5a.75.75 0 1 0"
        + " 0 1.5.75.75 0 0 0 0-1.5Zm0 9.5a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Zm8.25.75a.75.75 0 1 0 1.5 0 .75.75 0"
        + " 0 0-1.5 0Z"
    ),
    "issues": (
        "M8 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z M8 0a8 8 0 1 1 0 16A8 8 0 0 1 8 0ZM1.5 8a6.5 6.5 0 1 0 13 0"
        + " 6.5 6.5 0 0 0-13 0Z"
    ),
    "repos": (
        "M2 2.5A2.5 2.5 0 0 1 4.5 0h8.75a.75.75 0 0 1 .75.75v12.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1"
        + " 0-1.5h1.75v-2h-8a1 1 0 0 0-.714 1.7.75.75 0 1 1-1.072 1.05A2.495 2.495 0 0 1 2 11.5Zm10.5-1h-8a1 1 0 0"
        + " 0-1 1v6.708A2.486 2.486 0 0 1 4.5 9h8ZM5 12.25a.25.25 0 0 1 .25-.25h3.5a.25.25 0 0 1 .25.25v3.25a.25.25"
        + " 0 0 1-.4.2l-1.45-1.087a.249.249 0 0 0-.3 0L5.4 15.7a.25.25 0 0 1-.4-.2Z"
    ),
    "contributed": (
        "M2 5.5a3.5 3.5 0 1 1 5.898 2.549 5.508 5.508 0 0 1 3.034 4.084.75.75 0 1 1-1.482.235 4 4 0 0 0-7.9 0"
        + " .75.75 0 0 1-1.482-.236A5.507 5.507 0 0 1 3.102 8.05 3.493 3.493 0 0 1 2 5.5ZM11 4a3.001 3.001 0 0 1"
        + " 2.22 5.018 5.01 5.01 0 0 1 2.56 3.012.749.749 0 0 1-.885.954.752.752 0 0 1-.549-.514 3.507 3.507 0 0"
        + " 0-2.522-2.372.75.75 0 0 1-.574-.73v-.352a.75.75 0 0 1 .416-.672A1.5 1.5 0 0 0 11 5.5.75.75 0 0 1 11"
        + " 4Zm-5.5-.5a2 2 0 1 0-.001 3.999A2 2 0 0 0 5.5 3.5Z"
    ),
    "followers": (
        "M10.561 8.073a6.005 6.005 0 0 1 3.432 5.142.75.75 0 1 1-1.498.07 4.5 4.5 0 0 0-8.99 0 .75.75 0 0"
        + " 1-1.498-.07 6.004 6.004 0 0 1 3.431-5.142 3.999 3.999 0 1 1 5.123 0ZM10.5 5a2.5 2.5 0 1 0-5 0 2.5 2.5 0"
        + " 0 0 5 0Z"
    ),
    "following": (
        "M7.9 8.548h-.001a5.528 5.528 0 0 1 3.1 4.659.75.75 0 1 1-1.498.086A4.01 4.01 0 0 0 5.5 9.5a4.01 4.01 0 0"
        + " 0-4.001 3.793.75.75 0 1 1-1.498-.085 5.527 5.527 0 0 1 3.1-4.66 3.5 3.5 0 1 1 4.799 0ZM13.25 0a.75.75 0"
        + " 0 1 .75.75V2h1.25a.75.75 0 0 1 0 1.5H14v1.25a.75.75 0 0 1-1.5 0V3.5h-1.25a.75.75 0 0 1"
        + " 0-1.5h1.25V.75a.75.75 0 0 1 .75-.75ZM5.5 4a2 2 0 1 0-.001 3.999A2 2 0 0 0 5.5 4Z"
    ),
    "forks": (
        "M9.5 3.25a2.25 2.25 0 1 1 3 2.122V6A2.5 2.5 0 0 1 10 8.5H6a1 1 0 0 0-1 1v1.128a2.251 2.251 0 1 1-1.5"
        + " 0V5.372a2.25 2.25 0 1 1 1.5 0v1.836A2.493 2.493 0 0 1 6 7h4a1 1 0 0 0 1-1v-.628A2.25 2.25 0 0 1 9.5"
        + " 3.25Zm-6 0a.75.75 0 1 0 1.5 0 .75.75 0 0 0-1.5 0Zm8.25-.75a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5ZM4.25"
        + " 12a.75.75 0 1 0 0 1.5.75.75 0 0 0 0-1.5Z"
    ),
    "starred": (
        "M3 2.75C3 1.784 3.784 1 4.75 1h6.5c.966 0 1.75.784 1.75 1.75v11.5a.75.75 0 0 1-1.227.579L8 11.722l-3.773"
        + " 3.107A.751.751 0 0 1 3 14.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.91l3.023-2.489a.75.75 0 0 1 .954 0l3.023"
        + " 2.49V2.75a.25.25 0 0 0-.25-.25Z"
    ),
    "merged-prs": (
        "M5.45 5.154A4.25 4.25 0 0 0 9.25 7.5h1.378a2.251 2.251 0 1 1 0 1.5H9.25A5.734 5.734 0 0 1 5"
        + " 7.123v3.505a2.25 2.25 0 1 1-1.5 0V5.372a2.25 2.25 0 1 1 1.95-.218ZM4.25 13.5a.75.75 0 1 0 0-1.5.75.75 0"
        + " 0 0 0 1.5Zm8.5-4.5a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5ZM5 3.25a.75.75 0 1 0 0 .005V3.25Z"
    ),
}

CATALOG: list[tuple[str, str]] = [
    ("stars", "Total Stars"),
    ("commits", "Total Commits"),
    ("commits-year", "Commits This Year"),
    ("prs", "Total PRs"),
    ("issues", "Total Issues"),
    ("repos", "Total Repositories"),
    ("contributed", "Contributed To"),
    ("followers", "Followers"),
    ("following", "Following"),
    ("forks", "Total Forks"),
    ("starred", "Repos Starred"),
    ("merged-prs", "Merged PRs"),
]


async def _fetch_json(session: aiohttp.ClientSession, url: str, accept: str | None = None) -> Any:
    headers = dict(_HEADERS)
    if accept is not None:
        headers["Accept"] = accept
    async with session.get(url, headers=headers) as resp:
        if resp.status >= 400:
            raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
        return await resp.json()


async def _fetch_user(session: aiohttp.ClientSession, username: str) -> dict[str, Any]:
    data = await _fetch_json(session, f"{_GH_API}/users/{username}")
    if not isinstance(data, dict):
        raise Exception(f"Unexpected GitHub API response: {data}")
    return data


async def _fetch_repos(session: aiohttp.ClientSession, username: str) -> list[dict[str, Any]]:
    repos: list[dict[str, Any]] = []
    page = 1
    while True:
        data = await _fetch_json(session, f"{_GH_API}/users/{username}/repos?per_page={_PAGE_SIZE}&page={page}")
        if not isinstance(data, list):
            raise Exception(f"Unexpected GitHub API response: {data}")
        repos.extend(data)
        if len(data) < _PAGE_SIZE:
            break
        page += 1
    return repos


async def _fetch_starred_count(session: aiohttp.ClientSession, username: str) -> int:
    async with session.get(f"{_GH_API}/users/{username}/starred?per_page=1", headers=_HEADERS) as resp:
        if resp.status >= 400:
            raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
        body = await resp.json()
        if not isinstance(body, list):
            raise Exception(f"Unexpected GitHub API response: {body}")
        if not body:
            return 0
        link = resp.headers.get("Link", "")
        for part in link.split(","):
            segment = part.strip()
            if 'rel="last"' in segment:
                match = re.search(r"[?&]page=(\d+)", segment)
                if match:
                    return max(1, int(match.group(1)))
        return 1


async def _search_issues(session: aiohttp.ClientSession, query: str) -> int:
    data = await _fetch_json(session, f"{_GH_API}/search/issues?q={query}")
    if not isinstance(data, dict) or "total_count" not in data:
        raise Exception(f"Unexpected GitHub API response: {data}")
    return int(data["total_count"])


async def _search_commits(session: aiohttp.ClientSession, query: str) -> dict[str, Any]:
    accept = "application/vnd.github.cloak-preview+json"
    data = await _fetch_json(session, f"{_GH_API}/search/commits?q={query}&per_page={_PAGE_SIZE}", accept=accept)
    if not isinstance(data, dict) or "total_count" not in data:
        raise Exception(f"Unexpected GitHub API response: {data}")
    return data


def _contrib_repos(commits: dict[str, Any]) -> int:
    repos: set[str] = set()
    for item in commits.get("items", []):
        if not isinstance(item, dict):
            continue
        repo = item.get(_MAIN) if isinstance(item.get(_MAIN), dict) else None
        if repo and isinstance(repo.get("full_name"), str):
            repos.add(repo["full_name"])
    return len(repos)


def _format(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return str(value)


async def get_gh_user_stats(username: str, show: set[str]) -> UserStats:
    """Fetch user metrics for the caller-specified keys and return a UserStats."""
    tasks: dict[str, asyncio.Task] = {}
    session = aiohttp.ClientSession()

    def _spawn(name: str, coro) -> None:
        tasks[name] = asyncio.create_task(coro)

    user_task = asyncio.create_task(_fetch_user(session, username))

    if {"stars", "forks"} & show:
        _spawn("repos", _fetch_repos(session, username))
    if "starred" in show:
        _spawn("starred", _fetch_starred_count(session, username))

    commit_keys = {"commits", "commits-year", "contributed"} & show
    if commit_keys:
        _spawn("commits", _search_commits(session, f"author:{username}"))
        if "commits-year" in commit_keys:
            year = date.today().year
            _spawn("commits-year", _search_commits(session, f"author:{username} author-date:>={year}-01-01"))

    issue_queries = {
        "prs": f"is:pr author:{username}",
        "issues": f"is:issue author:{username}",
        "merged-prs": f"is:pr author:{username} is:merged",
    }
    for key in issue_queries:
        if key in show:
            _spawn(key, _search_issues(session, issue_queries[key]))

    try:
        results = await asyncio.gather(user_task, *tasks.values())
    finally:
        await session.close()

    user = results[0]
    data: dict[str, Any] = {"user": user, **dict(zip(tasks.keys(), results[1:]))}

    return UserStats(
        name=str(user.get("name") or username),
        handle=f"@{user.get('login', username)}",
        metrics=_build_metrics(data, show),
    )


def _build_metrics(data: dict[str, Any], show: set[str]) -> list[Metric]:
    metrics: list[Metric] = []
    stars = forks = 0
    repos = data.get("repos") or []
    for repo in repos:
        stars += int(repo.get("stargazers_count") or 0)
        forks += int(repo.get("forks_count") or 0)

    user = data.get("user") or {}
    values: dict[str, Any] = {
        "stars": stars,
        "commits": data.get("commits", {}).get("total_count", 0),
        "commits-year": data.get("commits-year", {}).get("total_count", 0),
        "prs": data.get("prs", 0),
        "issues": data.get("issues", 0),
        "repos": user.get("public_repos", 0),
        "contributed": _contrib_repos(data.get("commits") or {}),
        "followers": user.get("followers", 0),
        "following": user.get("following", 0),
        "forks": forks,
        "starred": data.get("starred", 0),
        "merged-prs": data.get("merged-prs", 0),
    }

    for key, label in CATALOG:
        if key not in show:
            continue
        metrics.append(Metric(key=key, label=label, value=_format(values.get(key, 0)), icon=_ICONS.get(key, "")))
    return metrics
