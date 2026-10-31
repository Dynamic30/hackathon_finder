FROM python:3.12-slim AS api
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY backend backend
COPY frontend frontend
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

FROM api AS scraper
RUN playwright install --with-deps chromium
COPY scrapers scrapers
CMD ["python", "-m", "scrapers.orchestrator"]
