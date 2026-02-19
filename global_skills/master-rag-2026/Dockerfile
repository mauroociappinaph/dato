FROM python:3.11-slim

WORKDIR /app

COPY master-rag-2026/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY master-rag-2026/scripts/ ./scripts/
COPY shared/ ./shared/

ENTRYPOINT ["python", "scripts/main.py"]
