# ─── Stage 1: dependency installation ───────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files first (better layer caching)
# If only source code changes, Docker reuses the cached dependency layer
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev

# ─── Stage 2: final image ───────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Non-root user — never run application containers as root
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy the virtual environment from the builder stage
COPY --from=builder /app/.venv ./.venv

# Copy application source
COPY app/ ./app/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Make sure the venv binaries are on PATH
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

EXPOSE 8001

# Run migrations then start the server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8001"]
