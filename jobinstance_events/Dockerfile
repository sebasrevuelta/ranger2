FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    SERVICE_NAME=jobinstance_events \
    PORT=8080

WORKDIR /app

COPY jobinstance_events/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY jobinstance_events/ ./jobinstance_events/

EXPOSE 8080

CMD ["gunicorn", "-c", "jobinstance_events/gunicorn.py", "jobinstance_events.wsgi:app"]
