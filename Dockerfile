FROM python:3.12-slim

# Prevent .pyc files and enable stdout/stderr unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

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
