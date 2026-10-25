FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-noto-cjk \
    libpango-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r appuser && useradd -r -g appuser -m appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser . .

USER appuser

EXPOSE 8080

STOPSIGNAL SIGTERM

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
