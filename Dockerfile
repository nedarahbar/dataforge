FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY pyproject.toml README.md LICENSE ./
COPY app ./app
COPY sample_data ./sample_data

RUN pip install --upgrade pip && pip install . \
    && mkdir -p storage/raw storage/cleaned /app/data

EXPOSE 8000

CMD ["sh", "-c", "mkdir -p /app/data /app/storage/raw /app/storage/cleaned && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
