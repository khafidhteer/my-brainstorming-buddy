# ============================================================
# Dockerfile for My Thinker Buddy
# ============================================================
# This file packages the app into a container so it runs
# the same way on any server (Ubuntu, Windows, etc.).
# ============================================================

# ---- Stage 1: Install dependencies ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy only the requirements file first (for better caching)
COPY requirements.txt .

# Install all Python packages
RUN pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Runtime image (smaller) ----
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy the application code
COPY . .

# The app uses Streamlit on port 8501
EXPOSE 8501

# Health check — Streamlit provides a health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

# Command to start the Streamlit web UI
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]