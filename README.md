# Incident Management API

Микросервис для учёта инцидентов Telegram-ботов.

## Технологии

- **Python 3.10+**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - валидация данных
- **PostgreSQL** - база данных
- **Docker** - контейнеризация БД

## Установка и запуск

### 1. Клонировать репозиторий
```bash
git clone https://github.com/maksim-bolotin/incident-service.git
cd incident-service
```

### 2. Запустить PostgreSQL через Docker
```bash
docker compose up -d postgres
```

Проверить что контейнер работает:
```bash
docker compose ps
```

### 3. Установить зависимости
```bash
pip install -r requirements.txt
```

### 4. Запустить приложение
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: `http://localhost:8000`

### 5. Открыть документацию API

Swagger UI: `http://localhost:8000/docs`

## Остановка
```bash
# Остановить приложение
Ctrl+C

# Остановить PostgreSQL контейнер
docker compose down

# Остановить и удалить данные БД
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
│   └── main.py           # FastAPI приложение, endpoints
├── docker-compose.yml    # Конфигурация Docker контейнеров
├── requirements.txt      # Зависимости Python
└── README.md             # Документация
```

## Конфигурация БД

База данных настраивается через переменную окружения `DATABASE_URL`.

**По умолчанию (из docker-compose.yml):**
```
postgresql://incidents_user:incidents_password@localhost:5432/incidents_db
```

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
