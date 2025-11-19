"""
Конфигурация Celery для асинхронных задач.
"""

import os
from celery import Celery

# Redis URL для брокера и backend
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Создаем Celery приложение
celery_app = Celery(
    "incident_service",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"]
)

# Конфигурация Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 минут максимум на задачу
    result_expires=3600,  # Результаты хранятся 1 час
)
