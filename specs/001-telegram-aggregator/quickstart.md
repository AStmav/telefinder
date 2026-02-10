# Developer Quickstart: TeleFinder

**Feature**: 001-telegram-aggregator  
**Date**: 2026-02-09  
**Estimated Setup Time**: 15-20 minutes

## Overview

This guide walks you through setting up the TeleFinder development environment from scratch. By the end, you'll have a fully functional local instance with backend, frontend, and database running.

---

## Prerequisites

Before starting, ensure you have these tools installed:

| Tool | Version | Check Command | Installation |
|------|---------|---------------|--------------|
| Python | 3.10+ | `python --version` | [python.org](https://www.python.org/) |
| Node.js | 18+ | `node --version` | [nodejs.org](https://nodejs.org/) |
| PostgreSQL | 14+ | `psql --version` | [postgresql.org](https://www.postgresql.org/) |
| Git | 2.0+ | `git --version` | [git-scm.com](https://git-scm.com/) |
| Docker | 20+ (optional) | `docker --version` | [docker.com](https://www.docker.com/) |

**Note**: Docker Compose is recommended for easiest setup but not required.

---

## Step 1: Clone Repository

```bash
git clone <repository-url>
cd TeleFinder
git checkout 001-telegram-aggregator
```

---

## Step 2: Telegram API Credentials

TeleFinder requires Telegram API credentials to monitor groups.

### 2.1 Get API ID and Hash

1. Visit [my.telegram.org](https://my.telegram.org/)
2. Log in with your phone number
3. Go to **API Development Tools**
4. Create a new application:
   - **App title**: TeleFinder Dev
   - **Short name**: telefinder-dev
   - **Platform**: Other
5. Copy your `api_id` and `api_hash`

### 2.2 Create Telegram Bot (for notifications)

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create bot:
   - **Name**: TeleFinder Dev Bot
   - **Username**: telefinder_dev_bot (or similar unique name)
4. Copy the **bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

---

## Step 3: Environment Configuration

### 3.1 Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 3.2 Fill in Required Variables

Edit `.env` and add your credentials:

```env
# Database
DATABASE_URL=postgresql://telefinder:dev_password@localhost:5432/telefinder_dev

# Telegram API (from Step 2.1)
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef1234567890abcdef1234567890

# Telegram Bot (from Step 2.2)
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# JWT Secret (generate random string)
SECRET_KEY=generate-a-random-secret-key-here-min-32-chars

# Session Encryption (generate random key)
SESSION_ENCRYPTION_KEY=generate-another-random-key-32-chars-min

# Optional: Sentence Transformer Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Development Settings
DEBUG=true
LOG_LEVEL=DEBUG
```

**Generate secure random keys**:

```bash
# On Linux/macOS
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Or use OpenSSL
openssl rand -base64 32
```

---

## Step 4: Setup Method (Choose One)

### Option A: Docker Compose (Recommended)

Easiest setup - runs everything in containers.

```bash
# Start all services (backend, frontend, database)
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access**:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Skip to Step 6** if using Docker Compose.

---

### Option B: Manual Setup

Run each component manually for more control.

#### 4.1 Setup Database

**Option B1: Use Local PostgreSQL**

```bash
# Create database and user
psql postgres << EOF
CREATE USER telefinder WITH PASSWORD 'dev_password';
CREATE DATABASE telefinder_dev OWNER telefinder;
GRANT ALL PRIVILEGES ON DATABASE telefinder_dev TO telefinder;
EOF
```

**Option B2: Use Docker for Database Only**

```bash
docker run -d \
  --name telefinder-db \
  -e POSTGRES_USER=telefinder \
  -e POSTGRES_PASSWORD=dev_password \
  -e POSTGRES_DB=telefinder_dev \
  -p 5432:5432 \
  postgres:14
```

#### 4.2 Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Download sentence transformer model (first time only, ~80MB)
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Start backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Backend should start at http://localhost:8000

**Leave this terminal running.**

#### 4.3 Setup Frontend

Open a **new terminal**:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend should start at http://localhost:5173

**Leave this terminal running.**

---

## Step 5: Verify Installation

### 5.1 Check Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 5.2 Check API Documentation

Open browser: http://localhost:8000/docs

You should see interactive Swagger UI with all API endpoints.

### 5.3 Check Frontend

Open browser: http://localhost:5173

You should see the TeleFinder login page.

---

## Step 6: Create Test User

### Option A: Via API (curl)

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "dev@test.com",
    "password": "TestPass123!"
  }'
```

### Option B: Via Frontend

1. Open http://localhost:5173
2. Click "Sign Up"
3. Enter:
   - **Email**: dev@test.com
   - **Password**: TestPass123!
4. Click "Create Account"

### Option C: Via API Docs

1. Open http://localhost:8000/docs
2. Find `POST /auth/register`
3. Click "Try it out"
4. Fill in request body
5. Click "Execute"

---

## Step 7: Authenticate with Telegram

This links your Telegram account for group monitoring.

### 7.1 Log In

Use the test user credentials from Step 6:
- Email: dev@test.com
- Password: TestPass123!

### 7.2 Link Telegram Account

1. After login, go to **Settings** → **Link Telegram**
2. Enter your Telegram phone number (with country code, e.g., +1234567890)
3. Click **Send Code**
4. Check your Telegram app for verification code
5. Enter the code and click **Verify**
6. If you have 2FA enabled on Telegram, enter your password

**Success**: You should see "Telegram account linked successfully"

---

## Step 8: Add a Test Group

### 8.1 Join a Test Group

Join a public Telegram group for testing. Suggestions:
- @python_jobs
- @pythondev
- @remotepython

### 8.2 Add Group to TeleFinder

1. In TeleFinder, go to **Groups** → **Add Group**
2. Enter group username (e.g., `@python_jobs`)
3. Click **Add**

**Expected**: Group should appear in your list with status "Active"

---

## Step 9: Create a Test Filter

1. Go to **Filters** → **Create Filter**
2. Fill in:
   - **Name**: Python Jobs Test
   - **Keywords**: python, developer, remote
   - **Semantic Filtering**: Enable (optional)
   - **Priority**: 5 (normal)
   - **Notifications**: Enable
3. Click **Save**

---

## Step 10: Test End-to-End

### 10.1 Trigger a Match

**Option A**: Wait for new message in monitored group (may take time)

**Option B**: Send test message to yourself:
1. Create a Telegram group with just yourself
2. Add it to TeleFinder
3. Send a message in that group containing your filter keywords

### 10.2 Verify Feed

1. Go to **Feed** page
2. You should see matched messages appear within 1 minute
3. Check **Hot Matches** if priority is high enough (≥7)

### 10.3 Check WebSocket Connection

Open browser DevTools (F12) → Console:

```javascript
// Should see WebSocket connection established
// Look for: "WebSocket connection to 'ws://localhost:8000/ws/feed?token=...'"
```

---

## Common Issues & Solutions

### Issue: Database connection fails

**Error**: `psql: error: connection to server at "localhost", port 5432 failed`

**Solution**:
```bash
# Check if PostgreSQL is running
systemctl status postgresql  # Linux
brew services list  # macOS

# Start PostgreSQL if stopped
systemctl start postgresql  # Linux
brew services start postgresql  # macOS
```

---

### Issue: Backend fails to start - "Module not found"

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: Frontend shows "Network Error"

**Solution**:
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in `backend/src/main.py`
3. Clear browser cache and reload

---

### Issue: Telegram authentication fails

**Error**: `Invalid phone number` or `API ID/Hash invalid`

**Solution**:
1. Verify `TELEGRAM_API_ID` and `TELEGRAM_API_HASH` in `.env`
2. Ensure phone number includes country code (+1234567890)
3. Check [my.telegram.org](https://my.telegram.org/) credentials are correct

---

### Issue: No messages appearing in feed

**Checklist**:
- [ ] Telegram account linked successfully
- [ ] Group added and status is "Active"
- [ ] Filter created and enabled
- [ ] Group has recent messages
- [ ] Backend logs show message processing (check terminal or `docker-compose logs`)

**Debug**:
```bash
# Check backend logs
docker-compose logs -f backend

# Or if running manually:
# Check terminal where uvicorn is running
```

---

### Issue: Sentence transformer download fails

**Error**: `ConnectionError` when downloading model

**Solution**:
```bash
# Manually download model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Or use different model in .env:
EMBEDDING_MODEL=paraphrase-MiniLM-L3-v2
```

---

## Development Workflow

### Running Tests

**Backend**:
```bash
cd backend
pytest
```

**Frontend**:
```bash
cd frontend
npm run test
```

### Database Migrations

**Create new migration**:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

**Apply migrations**:
```bash
alembic upgrade head
```

**Rollback migration**:
```bash
alembic downgrade -1
```

### Code Formatting

**Backend (Python)**:
```bash
cd backend
black src/
isort src/
```

**Frontend (TypeScript)**:
```bash
cd frontend
npm run lint
npm run format
```

---

## Useful Commands

| Action | Command |
|--------|---------|
| View API docs | Open http://localhost:8000/docs |
| Check backend logs | `docker-compose logs -f backend` |
| Check frontend logs | `docker-compose logs -f frontend` |
| Reset database | `docker-compose down -v && docker-compose up -d` |
| Rebuild containers | `docker-compose up -d --build` |
| Access database | `psql postgresql://telefinder:dev_password@localhost/telefinder_dev` |
| Stop all services | `docker-compose down` |

---

## Next Steps

Once your local environment is running:

1. **Read the specs**: Review `spec.md`, `research.md`, `data-model.md`
2. **Explore API contracts**: Check `contracts/api-spec.yaml` and `contracts/websocket.md`
3. **Review tasks**: See `tasks.md` (once generated via `/speckit.tasks`)
4. **Start development**: Pick a task and create a branch

---

## Getting Help

- **Documentation**: `/specs/001-telegram-aggregator/`
- **API Reference**: http://localhost:8000/docs
- **Constitution**: `.specify/memory/constitution.md`
- **Logs**: `docker-compose logs` or check terminal output

---

## Production Deployment Notes

**Not for local development** - reference only:

1. Use production-grade WSGI server (Gunicorn + Uvicorn workers)
2. Enable HTTPS (TLS certificates via Let's Encrypt)
3. Use managed PostgreSQL (AWS RDS, DigitalOcean Managed DB)
4. Set up reverse proxy (Nginx)
5. Configure environment variables via secrets management
6. Enable monitoring (Prometheus, Grafana)
7. Set up automated backups for database

See deployment guide (to be created) for full production setup.

---

**Setup Complete!** 🎉

You now have a fully functional TeleFinder development environment.

