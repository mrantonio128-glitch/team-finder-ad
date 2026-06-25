FROM python:3.14-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN addgroup --system app && \
    adduser --system --ingroup app app

WORKDIR /app

# Кэшируем установку зависимостей
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем приложение и точку входа
COPY . ./
RUN chmod +x docker-entrypoint.sh && \
    mkdir -p /app/staticfiles && \
    chown -R app:app /app

USER app

EXPOSE 8000

ENTRYPOINT ["/app/docker-entrypoint.sh"]
STOPSIGNAL SIGINT
