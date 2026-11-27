# ---------- Stage 1: build the Python packages ----------
FROM python:3.11-slim-bookworm AS builder

WORKDIR /build

COPY requirements-dev.txt .
RUN pip install --upgrade pip && \
    pip wheel --no-cache-dir --wheel-dir /build/wheels -r requirements-dev.txt


# ---------- Stage 2: final runtime image ----------
FROM python:3.11-slim-bookworm AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app \
    MODEL_DIR=/app/models

WORKDIR /app

# Small system library that OpenCV may need
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install the packages built in stage 1
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

# Copy project code (models are NOT copied; they are mounted)
COPY src/ ./src/
COPY configs/ ./configs/
COPY scripts/ ./scripts/

# Run as a non-root user
RUN useradd -m -u 1001 aiuser && chown -R aiuser:aiuser /app
USER aiuser

# For now this only checks the environment; replace with the real service later
CMD ["python", "scripts/verify_env.py"]