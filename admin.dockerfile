FROM python:3.11-alpine

COPY admin/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT python admin.py
