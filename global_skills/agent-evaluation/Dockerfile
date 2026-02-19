FROM python:3.11-slim

WORKDIR /app

COPY agent-evaluation/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY agent-evaluation/scripts/ ./scripts/
COPY shared/ ./shared/

ENTRYPOINT ["python", "scripts/main.py"]
