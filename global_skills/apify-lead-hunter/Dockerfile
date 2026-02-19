FROM python:3.11-slim

WORKDIR /app

COPY apify-lead-hunter/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apify-lead-hunter/scripts/ ./scripts/
COPY shared/ ./shared/

ENTRYPOINT ["python", "scripts/main.py"]
