# Multi-stage build optimized for Podman
# Stage 1: Builder
FROM docker.io/python:3.11-slim as builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime
FROM docker.io/python:3.11-slim

# Create non-root user
RUN groupadd -r bookgram && \
    useradd -r -g bookgram -u 1000 bookgram && \
    mkdir -p /app && \
    chown -R bookgram:bookgram /app

# Set working directory
WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=bookgram:bookgram app ./app
COPY --chown=bookgram:bookgram pyproject.toml ./

# Switch to non-root user
USER bookgram

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
