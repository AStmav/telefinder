# TeleFinder Backend

Python FastAPI backend for TeleFinder Telegram content aggregator.

## Tech Stack

- **Framework**: FastAPI (async)
- **Database**: SQLite with SQLAlchemy ORM
- **Telegram**: Pyrogram (MTProto) + python-telegram-bot (Bot API)
- **ML**: Sentence Transformers (semantic filtering)
- **Auth**: JWT + encrypted session storage

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `../.env.example` to `../.env` and fill in Telegram API credentials from https://my.telegram.org/apps

### 4. Initialize Database

```bash
alembic upgrade head
```

### 5. Download ML Model (first time only)

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## Running

### Development Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Testing

```bash
pytest
pytest --cov=src tests/  # With coverage
```

## Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## Project Structure

```
backend/
├── src/
│   ├── api/              # API routes and middleware
│   │   ├── routes/       # Endpoint handlers
│   │   ├── middleware/   # Custom middleware
│   │   └── dependencies.py
│   ├── models/           # SQLAlchemy ORM models
│   ├── services/         # Business logic
│   ├── telegram/         # Telegram integration
│   ├── config/           # Configuration
│   ├── schemas/          # Pydantic schemas
│   └── main.py           # FastAPI app
├── tests/
│   ├── contract/         # API contract tests
│   ├── integration/      # Integration tests
│   └── unit/             # Unit tests
├── alembic/              # Database migrations
└── requirements.txt
```

## Key Components

### Models (SQLAlchemy ORM)
- `User`: User accounts with Telegram authentication
- `TelegramGroup`: Monitored Telegram groups
- `Message`: Collected messages with embeddings
- `Filter`: User-defined filtering criteria
- `Notification`: Notification delivery tracking

### Services (Business Logic)
- `TelegramService`: Group monitoring via Pyrogram
- `FilterService`: Keyword + semantic filtering
- `FeedService`: Feed aggregation and sorting
- `NotificationService`: Notification delivery
- `MarkdownService`: Markdown rendering

### API Routes
- `/auth`: Authentication (register, login, Telegram link)
- `/groups`: Group management (CRUD operations)
- `/filters`: Filter management (CRUD operations)
- `/feed`: Message feed (with sorting, filtering)
- `/notifications`: Notification history
- `/ws/feed`: WebSocket real-time updates

## Environment Variables

See `../.env.example` for all available configuration options.

**Required**:
- `SQLITE_DB_PATH`: Database file path
- `TELEGRAM_API_ID`: From my.telegram.org
- `TELEGRAM_API_HASH`: From my.telegram.org
- `TELEGRAM_BOT_TOKEN`: From @BotFather
- `SECRET_KEY`: JWT signing key
- `SESSION_ENCRYPTION_KEY`: Telegram session encryption

## Troubleshooting

### Database Locked
SQLite issue with concurrent writes. Ensure only one process accesses DB at a time in development.

### Telegram Authentication Fails
- Verify API_ID and API_HASH are correct
- Check phone number format includes country code (+1234567890)
- Ensure Telegram app is accessible to receive verification code

### Sentence Transformer Download Fails
```bash
# Manual download
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

## Development Tips

- Use `/docs` for interactive API testing
- Check `backend/telefinder.db` with SQLite browser
- Enable DEBUG mode in .env for detailed logs
- Use `pytest -v` for verbose test output

---

For full documentation, see `/specs/001-telegram-aggregator/`

