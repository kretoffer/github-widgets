from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.api_tools.user_stats import get_gh_user_stats
from tools.svg_tools.user_stats import generate_user_stats_resp

users_router = APIRouter(tags=["Users"])


@users_router.get("/user-stats/{username}")
async def get_user_stats(
    username: str,
    style: WidgetStyle,
    header_text: str = Query(None, alias="header-text"),
    show_stars: bool = Query(True, alias="show-stars"),
    show_commits: bool = Query(True, alias="show-commits"),
    show_commits_year: bool = Query(True, alias="show-commits-year"),
    show_prs: bool = Query(True, alias="show-prs"),
    show_issues: bool = Query(True, alias="show-issues"),
    show_repos: bool = Query(True, alias="show-repos"),
    show_contributed: bool = Query(True, alias="show-contributed"),
    show_followers: bool = Query(True, alias="show-followers"),
    show_following: bool = Query(True, alias="show-following"),
    show_forks: bool = Query(True, alias="show-forks"),
    show_starred: bool = Query(True, alias="show-starred"),
    show_merged_prs: bool = Query(True, alias="show-merged-prs"),
    columns: int | None = Query(1, ge=1, le=4),
    animation_duration: float = Query(0.7, ge=0, alias="animation-duration"),
) -> Response:
    show = {
        key
        for key, enabled in {
            "stars": show_stars,
            "commits": show_commits,
            "commits-year": show_commits_year,
            "prs": show_prs,
            "issues": show_issues,
            "repos": show_repos,
            "contributed": show_contributed,
            "followers": show_followers,
            "following": show_following,
            "forks": show_forks,
            "starred": show_starred,
            "merged-prs": show_merged_prs,
        }.items()
        if enabled
    }
    stats = await get_gh_user_stats(username, show)
    return generate_user_stats_resp(
        stats,
        style=style,
        columns=columns,
        header_text=header_text,
        animation_duration=animation_duration,
    )
