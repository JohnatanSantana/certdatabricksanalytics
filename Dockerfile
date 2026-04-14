FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    UV_SYSTEM_PYTHON=1 \
    UV_NO_CACHE=1

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Install dependencies (layer cached separately from source)
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy application source and quiz data files
COPY src/ ./src/
COPY data/ ./data/

# Streamlit config: disable telemetry, set server options
RUN mkdir -p /root/.streamlit && \
    printf '[server]\nheadless = true\naddress = "0.0.0.0"\nport = 8501\n\n[browser]\ngatherUsageStats = false\n' \
    > /root/.streamlit/config.toml

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

# entrypoint.sh runs init_db() AFTER the volume is mounted, then starts Streamlit
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
