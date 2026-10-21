# State

## Current
focus: contribution-streak widget: полная реализация через GraphQL (по годам), вычисление streak, 3-боксовый UI с анимированным кольцом-прогрессом + пламенем
phase: implementing
task: github-widgets: contribution-streak widget
next: Widget готов: ruff/pyright чистый, live-рендер 200 для всех параметров. Можно использовать
handoff: Widget создан: api/streak.py, tools/api_tools/streak.py, tools/svg_tools/streak.py, templates/svg/streak.svg, README обновлён

## Decisions
- Проект: github-widgets — FastAPI-сервис, который отдаёт динамические SVG-виджеты для встраивания в README GitHub.
- Каждый виджет: получает данные из GitHub API и рендерит SVG-карточку в тёмном GitHub-стиле.
- `src/templates/svg/<widget>.svg` — Jinja2-шаблон. Рендерится через `renderer.render()` который оборачивает в `base.svg`.
- `base.svg`: `<svg viewBox="0 0 {width} {height}">` → `<foreignObject>` → `<div xmlns=xhtml>` → `<style>` (сброс, `.widget` с `background-color`, `border: 2px solid {colors.widget_border}`, `border-radius: 20px`, отступы) → `.widget-header` (заголовок, если `header_text`) → `{{ widget_content | safe }}`.
- Доступные в шаблоне переменные от стиля: `width`, `content_width`, `colors.*` (hex: primary, secondary, background, surface, text, border, success, warning, header, widget_border), `fonts.*` (large/big/medium/small/tiny).
- Фильтры рендерера: `escape`, `color_hex`, `text2color` (sha256 из текста → #RRGGBB для окрашивания меток по названию).
- Тёмная тема GitHub: `background #0d1117`, `surface #161b22`, `text #e6edf3`, `border #30363d`, `primary #4493f8`, `secondary #a1a1a1`, `header #f0f0f0`, `widget_border transparent`.
- Карточки: скруглённые (`border-radius: 12px` у элементов, 20px у виджета), тонкие рамки `2px solid {colors.border}`, маленькие скруглённые квадратные маркеры (не круги — border-radius: 4px у точек, 12px у карточек).
- Анимации: через `@keyframes` + `animation-delay: {index * duration}s`, счётчик через `{% set ns = namespace(index=0) %}` и `{% set ns.index = ns.index + 1 %}` в цикле. Каждый виджет поддерживает `animation-duration` (0 = без анимации). Направления: появиться снизу (translateY), слева (translateX(12px)). Отдельный счётчик для секций, задерживаемых после предыдущих блоков (не продолжать индекс предыдущего цикла).
- Отступы: header 50px, side padding 10px, gap ~6-10px, bottom padding 10px.
- Высота виджета всегда вычисляется заранее в svg_tools по константам и умножается на `_SAFETY_FACTOR ~1.12-1.15` (запас).
- `text_to_color(text)` — ДЕТЕРМИНИРОВАННАЯ палитра для именованных сущностей (языки, навыки). ВРЕМЕННАЯ функция, кастомизируется по мере появления виджетов.
- `src/api/__init__.py`: `api_router = APIRouter(prefix="/api")`, каждый виджет регистрируется отдельным include_router.
- `src/main.py`: FastAPI app, монтирует роутер + static.
- `uv run ruff check src/`
- `uv run pyright src/`
- Live-проверка: `uv run python` + TestClient + mock/patch fetch-функций или реальный GITHUB_TOKEN из `.env`; проверить `status_code=200` и наличие viewBox/ключевых элементов в разметке.

## Log
- [2026-08-19] Сброс фокуса: забыты детали реализации конкретных виджетов; зафиксирована только суть проекта и стиль (см. Decisions).
- [auto] [2026-08-19 21:15] Committed: "add most-used-languages widget"
- [2026-08-19 22:01] Checkpoint: contribution-streak widget: полная реализация через GraphQL (по годам), вычисление streak, 3-боксовый UI с анимированным кольцом-прогрессом + пламенем
