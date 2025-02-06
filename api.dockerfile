FROM python:3.10-slim

COPY api/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

#RUN alembic upgrade head

ENTRYPOINT [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "80", "--workers", "4" ]
