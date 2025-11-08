"""
Настройка подключения к БД и управление сессиями.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

from app.models import Base

# Настройка подключения к БД
DATABASE_URL = "sqlite:///./incidents.db"

# Создаём подключение к БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Только для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db() -> None:
    """
    Создаёт все таблицы в БД. Вызывается при старте приложения.
    """
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    """
    Генератор сессий БД дляиспользования в эндпоинтах.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
