"""
Pydantic схемы для валидации данных.
- Проверяем что клиент отправил правильные данные
- Преобразуем SQLAlchemy объекты в JSON для ответа
"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class IncidentStatus(str, Enum):
    """Допустимые статусы инцидента"""
    NEW = "новый"
    IN_PROGRESS = "в работе"
    CLOSED = "закрыт"


class IncidentBase(BaseModel):
    """Базовые поля инцидента (общие для создания и ответа)"""
    text: str = Field(..., min_length=1, max_length=1000)
    description: str = Field(..., min_length=1)
    sstatus: IncidentStatus = Field(default=IncidentStatus.NEW)
    source: str = Field(..., min_length=1, max_length=100)


class IncidentCreate(IncidentBase):
    """
    Схема для создания инцидента (POST запрос).
    Клиент отправляет эти данные.
    """
    pass


class IncidentUpdate(BaseModel):
    """
    Схема для обновления инцидента (PATCH запрос).
    """
    text: str | None = Field(None, min_length=1, max_length=1000)
    description: str | None = Field(None, min_length=1)
    status: IncidentStatus | None = None
    source: str | None = Field(None, min_length=1, max_length=100)


class IncidentResponse(IncidentBase):
    """
    Схема для ответа клиенту.
    Включает id и created_at из БД.
    """
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
