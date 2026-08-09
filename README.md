# github-widgets

Dynamic SVG widgets for GitHub, ready to embed into your README.

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
| `header-text`.  | `Roadmap` | Card heading text                    |
| `width`         | `700`     | Card width in px, `300` – `1600`     |
| `primary-color` | `#A0A0A0` | Primary color of widget              |
| `bg-color`      | `transparent` | Widget background color          |

![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/kretoffer/github-widgets?count=2&header-text=My%20Roadmap&width=500&primary-color=%23000000&bg-color=%23A0A0A0)

```
![Issues Roadmap](https://github-widgets.kretoffer.com/api/issues-list/kretoffer/github-widgets?count=2&header-text=My%20Roadmap&width=500&primary-color=%23000000&bg-color=%23A0A0A0)
```

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
