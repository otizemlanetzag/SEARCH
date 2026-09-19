FROM python:3.12-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD ["sh", "-c", "if [ ! -f search_engine/search_index.json ]; then python -m search_engine.build_index; fi; uvicorn search_engine.api:app --host 0.0.0.0 --port ${PORT}"]
