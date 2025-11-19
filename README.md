# Incident Management API

Микросервис для учёта инцидентов Telegram-ботов с асинхронной обработкой задач.

## Технологии

- **Python 3.10+**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **PostgreSQL** - база данных
- **Redis** - message broker для Celery
- **Celery** - очередь фоновых задач
- **Docker** - контейнеризация

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/maksim-bolotin/incident-service.git
cd incident-service
```

### 2. Запустить PostgreSQL и Redis через Docker
```bash
docker compose up -d
```

Проверить что контейнеры работают:
```bash
docker compose ps
```

Должны быть запущены: `incident_postgres` и `incident_redis`.

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Запустить Celery Worker

**Терминал 1:**
```bash
# Windows
celery -A app.celery_app worker --pool=gevent --concurrency=10 --loglevel=info

# Linux/Mac
celery -A app.celery_app worker --loglevel=info
```

### 5. Запустить FastAPI приложение

**Терминал 2:**
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

### 6. Открыть документацию API

Swagger UI: `http://localhost:8000/docs`

## Фоновые задачи

При создании инцидента автоматически запускаются асинхронные задачи:

- **send_email_notification** - отправка email уведомления (симуляция 3 сек)
- **send_telegram_notification** - отправка в Telegram (симуляция 2 сек)
- **update_incident_statistics** - обновление статистики (симуляция 1 сек)

**Преимущества:**
- API отвечает мгновенно (~30ms вместо ~6000ms)
- Задачи выполняются параллельно в фоне
- Не блокируют другие запросы

## Остановка
```bash
# Остановить FastAPI (Терминал 2)
Ctrl+C

# Остановить Celery Worker (Терминал 1)
Ctrl+C

# Остановить Docker контейнеры
docker compose down

# Остановить и удалить данные
docker compose down -v
```

## API Endpoints

### POST /incidents/

Создание нового инцидента.

**Request:**
```json
{
  "text": "Бот не отвечает на команды",
  "description": "После обновления бот перестал реагировать на /start",
  "status": "новый",
  "source": "operator"
}
```

**Response (201):**
```json
{
  "id": 1,
  "text": "Бот не отвечает на команды",
  "description": "После обновления бот перестал реагировать на /start",
  "status": "новый",
  "source": "operator",
  "created_at": "2025-11-08T12:00:00"
}
```

### GET /incidents/

Получение списка инцидентов с фильтрацией и пагинацией.

**Query параметры:**
- `status` (optional) - фильтр по статусу ("новый", "в работе", "закрыт")
- `skip` (default: 0) - пропустить N записей
- `limit` (default: 100) - максимум записей в ответе

**Примеры:**
```bash
# Все инциденты
GET /incidents/

# Только со статусом "новый"
GET /incidents/?status=новый

# Пагинация (пропустить 10, взять 5)
GET /incidents/?skip=10&limit=5
```

**Response (200):**
```json
[
  {
    "id": 1,
    "text": "Бот не отвечает на команды",
    "description": "...",
    "status": "новый",
    "source": "operator",
    "created_at": "2025-11-08T12:00:00"
  }
]
```

### PATCH /incidents/{id}

Обновление инцидента. Можно обновить любое поле или несколько полей.

**Request:**
```json
{
  "status": "в работе"
}
```

**Response (200):**
```json
{
  "id": 1,
  "text": "Бот не отвечает на команды",
  "description": "...",
  "status": "в работе",
  "source": "operator",
  "created_at": "2025-11-08T12:00:00"
}
```

**Errors:**
- `404` - инцидент не найден

## Структура проекта
```
incident-service/
├── app/
│   ├── database.py       # Подключение к БД, сессии
│   ├── models.py         # SQLAlchemy модели
│   ├── schemas.py        # Pydantic схемы валидации
│   ├── main.py           # FastAPI приложение, endpoints
│   ├── celery_app.py     # Конфигурация Celery
│   └── tasks.py          # Фоновые задачи Celery
├── docker-compose.yml    # Конфигурация Docker (PostgreSQL, Redis)
├── requirements.txt      # Зависимости Python
└── README.md             # Документация
```

## Конфигурация

### База данных (DATABASE_URL)
```
postgresql://incidents_user:incidents_password@localhost:5432/incidents_db
```

### Redis (REDIS_URL)
```
redis://localhost:6379/0
```

## Мониторинг Celery (опционально)

Установить Flower для веб-интерфейса мониторинга:
```bash
pip install flower
celery -A app.celery_app flower
```

Откроется: `http://localhost:5555`

## Модель данных

### Incident

| Поле        | Тип                     | Описание                                      |
|-------------|-------------------------|-----------------------------------------------|
| id          | Integer                 | Уникальный идентификатор                      |
| text        | String(1000)            | Краткое описание инцидента                    |
| description | Text                    | Детальное описание                            |
| status      | String(50)              | Статус: "новый", "в работе", "закрыт"         |
| source      | String(100)             | Источник: "operator", "monitoring", "partner" |
| created_at  | DateTime(timezone=True) | Дата и время создания (автоматически)         |
