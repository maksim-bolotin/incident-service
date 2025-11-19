"""
FastAPI приложение для управления инцидентами.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db, init_db
from app.models import Incident
from app.schemas import IncidentCreate, IncidentUpdate, IncidentResponse

app = FastAPI(
    title="Incident Management API",
    version="1.0.1"
)

# Создаём таблицы при запуске
init_db()


@app.post("/incidents/", response_model=IncidentResponse, status_code=201)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    """Создать инцидент"""
    db_incident = Incident(**incident.model_dump())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident


@app.get("/incidents/", response_model=list[IncidentResponse])
def get_incidents(
    status: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Получить список инцидентов с фильтром по статусу"""
    query = db.query(Incident)

    if status:
        query = query.filter(Incident.status == status)

    incidents = query.order_by(Incident.created_at.desc()).offset(skip).limit(limit).all()
    return incidents


@app.patch("/incidents/{incident_id}", response_model=IncidentResponse)
def update_incident(
    incident_id: int,
    incident_update: IncidentUpdate,
    db: Session = Depends(get_db)
):
    """Обновить инцидент по ID"""
    db_incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not db_incident:
        raise HTTPException(status_code=404, detail="Инцидент не найден")

    # Обновляем только переданные поля
    for field, value in incident_update.model_dump(exclude_unset=True).items():
        setattr(db_incident, field, value)

    db.commit()
    db.refresh(db_incident)
    return db_incident


@app.get("/")
def root():
    """
    Корневой endpoint - проверка, что API работает.
    """
    return {
        "message": "Incident Management API",
        "docs": "/docs",
        "version": "1.0.0"
    }
