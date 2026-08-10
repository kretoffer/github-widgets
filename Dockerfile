# --- Stage 1: Build and sync dependencies 
FROM python:3.14-slim-bookworm AS builder

# Install uv directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and environment variables
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# Install dependencies first to maximize Docker layer caching
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# --- Stage 2: Final minimal runtime image ---
FROM python:3.14-slim-bookworm AS runtime

WORKDIR /app

# Create a non-privileged user for security
RUN useradd -u 1001 -m appuser

# Copy the pre-built virtual environment and source code
COPY --from=builder /app/.venv /app/.venv
COPY ./src /app/src
COPY ./static /app/static

# Update PATH to automatically use the virtual environment's binaries
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH=/app/src

# Switch to the non-root user and expose the port
USER appuser
EXPOSE 8000

# Run FastAPI using its production CLI command
CMD ["fastapi", "run", "src/main.py", "--proxy-headers", "--port", "8000", "--host", "0.0.0.0"]
