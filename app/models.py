"""
Модель для инцидентов.
Описываем структуру таблицы incidents в БД.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Базовый класс для всех моделей
Base = declarative_base()


class Incident(Base):
    """Модель инцидента - описание таблицы в БД"""

    # Название таблицы в БД
    __tablename__ = "incidents"

    # Поля таблицы
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="новый")
    source = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
