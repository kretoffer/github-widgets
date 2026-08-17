import asyncio
from typing import Any

import aiohttp

from config import config
from schemas.external.gh import LanguageShare

_GH_API = "https://api.github.com"
_PAGE_SIZE = 100
_MAX_CONCURRENCY = 10

_HEADERS = {
    "Authorization": f"Bearer {config.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2026-03-10",
    "User-Agent": "github-widgets-by-kretoffer",
}


async def _fetch_json(session: aiohttp.ClientSession, url: str) -> Any:
    async with session.get(url, headers=_HEADERS) as resp:
        if resp.status >= 400:
            raise Exception(f"GitHub API error {resp.status}, {await resp.text()}")
        return await resp.json()


async def _fetch_repo_languages(session: aiohttp.ClientSession, full_name: str) -> dict[str, int] | None:
    try:
        data = await _fetch_json(session, f"{_GH_API}/repos/{full_name}/languages")
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    return {lang: int(bytes_) for lang, bytes_ in data.items() if bytes_ > 0}


async def get_gh_most_used_languages(username: str, count: int = 5, exclude_forks: bool = True) -> list[LanguageShare]:
    """Aggregate per-repository language bytes into a sorted top-N list."""
    async with aiohttp.ClientSession() as session:
        totals: dict[str, int] = {}
        repo_counts: dict[str, int] = {}
        page = 1
        while True:
            result = await _fetch_json(session, f"{_GH_API}/users/{username}/repos?per_page={_PAGE_SIZE}&page={page}")
            if not isinstance(result, list):
                raise Exception(f"Unexpected GitHub API response: {result}")
            full_names = [repo["full_name"] for repo in result if not (exclude_forks and repo.get("fork"))]
            semaphore = asyncio.Semaphore(_MAX_CONCURRENCY)

            async def _limited(name: str) -> dict[str, int] | None:
                async with semaphore:
                    return await _fetch_repo_languages(session, name)

            per_repo = await asyncio.gather(*(_limited(name) for name in full_names))
            for languages in per_repo:
                if not languages:
                    continue
                for language, bytes_ in languages.items():
                    totals[language] = totals.get(language, 0) + bytes_
                    repo_counts[language] = repo_counts.get(language, 0) + 1
            if len(result) < _PAGE_SIZE:
                break
            page += 1

        grand_total = sum(totals.values())
        if grand_total <= 0:
            return []
        ranked = sorted(totals.items(), key=lambda item: item[1], reverse=True)[:count]
        return [
            LanguageShare(name=name, share=round(size / grand_total * 100, 1), count=repo_counts.get(name, 0))
            for name, size in ranked
        ]
