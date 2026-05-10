# =============================================================================
# SQL Injection Detection System - Dockerfile
# =============================================================================
# Multi-stage build for Flask backend + React frontend
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: Python dependencies (backend)
# -----------------------------------------------------------------------------
FROM python:3.11-slim as backend-deps

WORKDIR /app/backend

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# Stage 2: Node.js dependencies (frontend)
# -----------------------------------------------------------------------------
FROM node:20-alpine as frontend-deps

WORKDIR /app/frontend

# Copy package files and install dependencies
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci --legacy-peer-deps || npm install --legacy-peer-deps

# -----------------------------------------------------------------------------
# Stage 3: Build production React app
# -----------------------------------------------------------------------------
FROM frontend-deps as frontend-build

COPY frontend/src ./src
COPY frontend/public ./public
COPY frontend/tailwind.config.js frontend/postcss.config.js ./

RUN npm run build

# -----------------------------------------------------------------------------
# Stage 4: Final runtime image
# -----------------------------------------------------------------------------
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=backend/app.py \
    FLASK_ENV=production

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend files
COPY --from=backend-deps /app/backend /app/backend

# Copy built frontend
COPY --from=frontend-build /app/build /app/frontend/build

# Copy dataset and training script
COPY dataset /app/dataset
COPY train_model.py /app/

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose Flask port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Default command runs Flask backend
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"] python:3.9-slim