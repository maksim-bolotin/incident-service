"""
Celery задачи для фоновой обработки.
"""

import time
from datetime import datetime, timezone
from app.celery_app import celery_app


@celery_app.task(name="send_email_notification")
def send_email_notification(incident_id: int, incident_text: str):
    """
    Отправка email уведомления о новом инциденте.
    (Симуляция)
    """
    print(f"[EMAIL] Отправка email для инцидента #{incident_id}")
    print(f"[EMAIL] Текст: {incident_text}")

    # Симулируем медленную операцию
    time.sleep(3)

    print(f"[EMAIL] Email отправлен успешно для инцидента #{incident_id}")
    return {
        "status": "sent",
        "incident_id": incident_id,
        "sent_at": datetime.now(timezone.utc).isoformat()
    }


@celery_app.task(name="send_telegram_notification")
def send_telegram_notification(incident_id: int, incident_text: str):
    """
    Отправка Telegram уведомления о новом инциденте.
    (Симуляция)
    """
    print(f"[TELEGRAM] Отправка в Telegram для инцидента #{incident_id}")
    print(f"[TELEGRAM] Текст: {incident_text}")

    # Симулируем медленную операцию
    time.sleep(2)

    print(f"[TELEGRAM] Сообщение отправлено для инцидента #{incident_id}")
    return {
        "status": "sent",
        "incident_id": incident_id,
        "sent_at": datetime.now(timezone.utc).isoformat()
    }


@celery_app.task(name="update_incident_statistics")
def update_incident_statistics():
    """
    Обновление статистики по инцидентам.
    (Симуляция)
    """
    print("[STATS] Обновление статистики...")

    # Симулируем вычисления
    time.sleep(1)

    print("[STATS] Статистика обновлена")
    return {
        "status": "updated",
        "sent_at": datetime.now(timezone.utc).isoformat()
    }
