import asyncio
from datetime import date, datetime, timedelta
from typing import Any

import aiohttp

from config import config
from schemas.external.gh import StreakStats

_GH_API = "https://api.github.com"
_GH_GRAPHQL = "https://api.github.com/graphql"
_MAX_CONCURRENCY = 5

_HEADERS = {
    "Authorization": f"Bearer {config.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "github-widgets-by-kretoffer",
}

_CALENDAR_QUERY = """
query($login: String!, $from: DateTime!, $to: DateTime!) {
  user(login: $login) {
    createdAt
    contributionsCollection(from: $from, to: $to) {
      contributionCalendar {
        weeks {
          contributionDays {
            date
            contributionCount
          }
        }
      }
    }
  }
}
"""


async def _fetch_rest(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url, headers=_HEADERS) as resp:
        if resp.status >= 400:
            raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
        return await resp.json()


async def _fetch_year(session: aiohttp.ClientSession, username: str, year: int) -> dict[date, int]:
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1) - timedelta(days=1)
    payload = {
        "query": _CALENDAR_QUERY,
        "variables": {
            "login": username,
            "from": f"{start:%Y-%m-%d}T00:00:00Z",
            "to": f"{end:%Y-%m-%d}T23:59:59Z",
        },
    }
    async with session.post(_GH_GRAPHQL, json=payload, headers=_HEADERS) as resp:
        if resp.status >= 400:
            raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
        data = await resp.json()

    user = (data or {}).get("data", {}).get("user")
    if user is None:
        errors = (data or {}).get("errors") or [{"message": "No such user"}]
        raise Exception(f"GitHub API error: {errors[0].get('message')}")

    contributions: dict[date, int] = {}
    for week in user.get("contributionsCollection", {}).get("contributionCalendar", {}).get("weeks", []):
        for day in week.get("contributionDays", []):
            contributions[date.fromisoformat(day["date"])] = int(day.get("contributionCount", 0))
    return contributions


def _short_date(day: date) -> str:
    return f"{day:%b} {day.day}"


def _long_date(day: date) -> str:
    return f"{day:%b} {day.day}, {day.year}"


def _range_text(start: date, end: date) -> str:
    if start.year == end.year:
        return f"{_short_date(start)} - {_short_date(end)}"
    return f"{_long_date(start)} - {_long_date(end)}"


def _compute(contributions: dict[date, int]) -> StreakStats:
    today = date.today()
    effective = {day: count for day, count in contributions.items() if day <= today}
    if not effective:
        return StreakStats(
            total_contributions=0,
            total_range="-",
            current_streak=0,
            current_streak_range="-",
            longest_streak=0,
            longest_streak_range="-",
            current_progress=0.0,
        )

    days = sorted(effective)

    first_contrib = next((day for day in days if effective[day] > 0), None)
    total = sum(effective.values())
    if first_contrib:
        total_range = f"{_long_date(first_contrib)} - Present"
    else:
        total_range = "-"

    longest_streak = 0
    longest_start = longest_end = days[0]
    run_start = run_end = days[0]
    run_length = 0
    for day in days:
        if effective[day] > 0:
            if run_length == 0:
                run_start = day
            run_length += 1
            run_end = day
            if run_length > longest_streak:
                longest_streak = run_length
                longest_start, longest_end = run_start, run_end
        else:
            run_length = 0

    current_streak = 0
    current_start = current_end = today
    cursor = today if effective.get(today, 0) > 0 else today - timedelta(days=1)
    while effective.get(cursor, 0) > 0:
        current_streak += 1
        current_end = cursor
        current_start = cursor
        cursor -= timedelta(days=1)

    progress = (current_streak / longest_streak) if longest_streak else 0.0

    return StreakStats(
        total_contributions=total,
        total_range=total_range,
        current_streak=current_streak,
        current_streak_range=_range_text(current_start, current_end) if current_streak else "-",
        longest_streak=longest_streak,
        longest_streak_range=_range_text(longest_start, longest_end) if longest_streak else "-",
        current_progress=round(progress, 4),
    )


async def get_gh_contribution_streak(username: str) -> StreakStats:
    """Fetch the user's contribution calendar year by year and compute streak stats."""
    async with aiohttp.ClientSession() as session:
        user = await _fetch_rest(session, f"{_GH_API}/users/{username}")
        if not isinstance(user, dict):
            raise Exception(f"Unexpected GitHub API response: {user}")
        created_at = user.get("created_at")
        first_year = int(created_at[:4]) if isinstance(created_at, str) and len(created_at) >= 4 else 2008
        current_year = datetime.now().year

        semaphore = asyncio.Semaphore(_MAX_CONCURRENCY)

        async def _limited(year: int) -> dict[date, int]:
            async with semaphore:
                return await _fetch_year(session, username, year)

        contributions: dict[date, int] = {}
        for year in range(first_year, current_year + 1):
            contributions.update(await _limited(year))

    return _compute(contributions)
