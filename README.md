<div align="center">
  <a href="https://github.com/kretoffer/github-widgets">
    <img src="./static/github-widgets-by-kretoffer.svg" alt="Logo" width="180" height="180">
  </a>

  <h2 align="center">GitHub widgets by Kretoffer</h2>

  <p align="center">
    Dynamic SVG widgets for GitHub, ready to embed into your README
    <br />
    <a href="https://github.com/kretoffer/github-widgets/tree/main/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/kretoffer/github-widgets/issues/new?labels=bug&template=BUG-REPORT.yml">Report Bug</a>
    &middot;
    <a href="https://github.com/kretoffer/github-widgets/issues/new?labels=enhancement&template=FEATURE-REQUEST.yml">Request Feature</a>
    <br>
    <br>
        <a href="https://github.com/kretoffer/github-widgets/actions"><img src="https://img.shields.io/github/actions/workflow/status/kretoffer/github-widgets/ci.yml?style=for-the-badge&logo=github&label=tests&color=8A2BE2" alt="Tests"></a>
        <a href="https://github.com/kretoffer/github-widgets/actions"><img src="https://img.shields.io/github/actions/workflow/status/kretoffer/github-widgets/cd.yml?style=for-the-badge&logo=github&label=deploy&color=8A2BE2" alt="Deploy"></a>
        <a href="https://github-widgets.kretoffer.com"><img src="https://img.shields.io/badge/github--widgets.kretoffer.com-orange?style=for-the-badge" alt="github-widgets.kretoffer.com"></a>
        <a href="https://github.com/kretoffer/github-widgets/stargazers"><img src="https://img.shields.io/github/stars/kretoffer/github-widgets?style=for-the-badge&logo=githubsponsors&logoColor=FFFFFF&label=stars&color=FFD700" alt="Stars"></a>
        <a href="https://github.com/kretoffer/github-widgets/issues"><img src="https://img.shields.io/github/issues/kretoffer/github-widgets?style=for-the-badge&logo=openbugbounty&logoColor=FFFFFF&label=issues&color=FF6B6B" alt="Issues"></a>
        <a href="LICENSE"><img src="https://img.shields.io/github/license/kretoffer/github-widgets?style=for-the-badge&logo=libreoffice" alt="LICENSE"></a>
  </p>
</div>


## Quick Start

Open the official widget builder at [github-widgets.kretoffer.com](https://github-widgets.kretoffer.com), pick a widget, customize it, and copy the generated snippet into your `README.md`. That's it.

## Widgets

### Issues Roadmap

A roadmap card generated from repository issues, with status badges (open/closed), labels and a custom heading.

![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/kretoffer/github-widgets)

```
![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/{GITHUB_USERNAME}/{GITHUB_REPO})
```

#### Parameters

| Parameter       | Default   | Description                          |
|-----------------|-----------|--------------------------------------|
| `count`         | `20`      | Number of issues to show             |
| `header-text`   | `Roadmap` | Card heading text                    |
| `width`         | `500`     | Card width in px, `300` – `1600`     |
| `theme`         | `default` | Predefined widget theme              |
| `labels`        | `true`    | Show labels on issue card            |
| `closed`        | `false`   | Show closed issues                   |
| `animation-duration` | `0.7` | Time in seconds (s) for **one** issue to appear, not the whole animation. Issues appear one by one; total animation time = `animation-duration × number of issues`. `0` — no animation |

![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/kretoffer/github-widgets?count=2&header-text=My%20Roadmap&width=500&theme=default&closed=true)

```
![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/kretoffer/github-widgets?count=2&header-text=My%20Roadmap&width=500&theme=default&closed=true)
```

### User Stats

A stats card for any GitHub user: stars, commits, PRs, issues, followers and more, split into responsive columns.

![User Stats](https://github-widgets.kretoffer.com/api/user-stats/kretoffer)

```
![User Stats](https://github-widgets.kretoffer.com/api/user-stats/{GITHUB_USERNAME})
```

#### Parameters

| Parameter      | Default | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `columns`      | `1`    | Number of columns, `1` – `4`; auto picks `ceil(sqrt(count))` |
| `width`        | `500`   | Card width in px, `300` – `1600`                 |
| `theme`        | `default` | Predefined widget theme                        |
| `animation-duration` | `0.7` | Time in seconds (s) for one metric to appear. `0` — no animation |

Each metric can be toggled with a `show-{key}` parameter, `true` by default:

| Key           | Query param           | Metric                  |
|---------------|-----------------------|-------------------------|
| `stars`       | `show-stars`          | Total stars             |
| `commits`     | `show-commits`        | Total commits           |
| `commits-year`| `show-commits-year`   | Commits this year       |
| `prs`         | `show-prs`            | Total pull requests     |
| `issues`      | `show-issues`         | Total issues            |
| `repos`       | `show-repos`          | Total repositories      |
| `contributed` | `show-contributed`    | Repositories contributed to |
| `followers`   | `show-followers`      | Followers               |
| `following`   | `show-following`      | Following               |
| `forks`       | `show-forks`          | Total forks             |
| `starred`     | `show-starred`        | Repos starred           |
| `merged-prs`  | `show-merged-prs`     | Merged pull requests    |

Example hiding two metrics:

```
![User Stats](https://github-widgets.kretoffer.com/api/user-stats/kretoffer?columns=3&show-starred=false&show-merged-prs=false)
```

### Tech Stack

A skill table card with Simple Icons logos, grouped into sections, for your tech stack.

![Tech Stack](https://github-widgets.kretoffer.com/api/tech-stack?skills=--Programming%20Languages--%7Cpython%7CFastAPI:fastapi%7C--Databases--%7Cpostgresql&header-text=My%20Stack)

```
![Tech Stack](https://github-widgets.kretoffer.com/api/tech-stack?skills=--Programming%20Languages--%7Cpython%7CFastAPI:fastapi%7C--Databases--%7Cpostgresql&header-text=My%20Stack)
```

The `skills` parameter is a `|`-separated list of items. A token wrapped in `--` on both sides (e.g. `--Programming Languages--`) becomes a section header. A plain slug (e.g. `python`) renders the matching Simple Icons logo with a pretty title. Use `Title:slug` (e.g. `FastAPI:fastapi`) to set a custom title for a slug.

#### Parameters

| Parameter       | Default | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `skills`        | —       | Required. `|`-separated list of slugs and `--Section--` headers |
| `header-text`   | —       | Card heading text                                |
| `columns`       | `4`     | Number of columns, `1` – `10`                    |
| `show-titles`   | `true`  | Show captions under icons                        |
| `icon-size`     | `48`    | Icon size in px, `16` – `128`                    |
| `use-original-colors` | `true` | Use brand colors from Simple Icons; `false` falls back to the theme text color |
| `icon-color`    | —       | Override icon color for all tiles (e.g. `#e6edf3`) |
| `gap`           | `16`    | Gap between tiles in px, `0` – `64`              |
| `width`         | `500`   | Card width in px, `300` – `1600`                 |
| `theme`         | `default` | Predefined widget theme                        |
| `animation-duration` | `0.6` | Time in seconds (s) for one element to appear. `0` — no animation |

## Self-hosting

Run your own instance with Docker:

```bash
docker run -e GITHUB_TOKEN=your_token -p 8000:8000 ghcr.io/kretoffer/github-widgets:latest
```

Required environment variables (see `.env.example`):

- `GITHUB_TOKEN` — GitHub token used to fetch repository data

Then point your embeds to your own host instead of the public instance.

## Development

```bash
uv sync --all-groups
uv run github-widgets
```

Quality checks:

```bash
uv run ruff check
uv run pyright
uv run pytest
```

Project layout:

```
src/
├── api/                 # FastAPI routes
├── schemas/             # Pydantic models
├── templates/           # SVG templates
└── tools/               # GitHub API and render logic
```

## License

[License](LICENSE)
