# TeleFinder - Telegram Content Aggregator

**Version**: 1.0.0  
**Status**: In Development  
**Branch**: `001-telegram-aggregator`

## Overview

TeleFinder is a personal Telegram content aggregator that automatically collects messages from user-specified Telegram groups, applies smart filtering (keyword + semantic), and displays results in a unified feed with real-time notifications for high-priority matches.

### Key Features

- 📱 **Multi-Group Monitoring**: Track multiple Telegram groups simultaneously
- 🔍 **Smart Filtering**: Keyword-based + semantic (AI-powered) message filtering
- ⚡ **Real-Time Updates**: WebSocket-powered live feed updates
- 🔥 **Hot Matches**: Instant notifications for high-priority content
- 📊 **Filter Analytics**: Performance metrics for each filter
- 🎯 **Mobile-First**: Responsive UI optimized for mobile devices

## Technology Stack

### Backend
- **Framework**: Python 3.10+ with FastAPI
- **Database**: SQLite (file-based, lightweight)
- **Telegram**: Pyrogram (MTProto) + python-telegram-bot (Bot API)
- **ML**: Sentence Transformers for semantic filtering
- **Auth**: JWT tokens with encrypted Telegram sessions

### Frontend
- **Framework**: Vue.js 3 + TypeScript
- **Styling**: Tailwind CSS
- **State**: Pinia
- **Build**: Vite
- **Real-Time**: WebSocket composables

## Project Structure

```
TeleFinder/
├── backend/                 # Python FastAPI backend
│   ├── src/
│   │   ├── api/            # API routes and middleware
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── services/       # Business logic
│   │   ├── telegram/       # Telegram integration
│   │   ├── config/         # Configuration management
│   │   └── schemas/        # Pydantic schemas
│   ├── tests/              # Backend tests
│   ├── alembic/            # Database migrations
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── pages/         # Page views
│   │   ├── services/      # API clients
│   │   ├── stores/        # Pinia stores
│   │   ├── types/         # TypeScript types
│   │   └── router/        # Vue Router
│   ├── tests/             # Frontend tests
│   └── package.json       # Node.js dependencies
│
├── specs/                  # Design documents
│   └── 001-telegram-aggregator/
│       ├── spec.md        # Feature specification
│       ├── plan.md        # Implementation plan
│       ├── data-model.md  # Database schema
│       ├── research.md    # Technical decisions
│       ├── quickstart.md  # Developer setup guide
│       ├── tasks.md       # Task breakdown
│       └── contracts/     # API contracts
│
├── .env.example           # Environment variables template
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Telegram account

### 1. Clone Repository

```bash
git clone <repository-url>
cd TeleFinder
git checkout 001-telegram-aggregator
```

### 2. Setup Environment

```bash
cp .env.example .env
# Edit .env with your Telegram API credentials
```

Get Telegram API credentials from [https://my.telegram.org/apps](https://my.telegram.org/apps)

### 3. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
```

### 4. Frontend Setup

```bash
cd frontend
npm install
```

### 5. Run Development Servers

**Backend** (Terminal 1):
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (Terminal 2):
```bash
cd frontend
npm run dev
```

Access the application:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Documentation

- **Feature Specification**: [specs/001-telegram-aggregator/spec.md](specs/001-telegram-aggregator/spec.md)
- **Implementation Plan**: [specs/001-telegram-aggregator/plan.md](specs/001-telegram-aggregator/plan.md)
- **Developer Guide**: [specs/001-telegram-aggregator/quickstart.md](specs/001-telegram-aggregator/quickstart.md)
- **API Contracts**: [specs/001-telegram-aggregator/contracts/](specs/001-telegram-aggregator/contracts/)
- **Task List**: [specs/001-telegram-aggregator/tasks.md](specs/001-telegram-aggregator/tasks.md)

## Development Workflow

### Constitution Principles

This project follows strict development principles defined in [.specify/memory/constitution.md](.specify/memory/constitution.md):

1. **Technology Stack**: Python FastAPI + Vue.js + TypeScript + Tailwind (non-negotiable)
2. **Telegram Bot API Integration**: Modular, testable, with proper error handling
3. **Markdown Processing**: Validation before rendering
4. **Environment Variables**: All secrets in .env (never committed)
5. **Atomic Commits**: One task = one commit with format `T###: [description]`

### Task-Driven Development

Tasks are defined in [specs/001-telegram-aggregator/tasks.md](specs/001-telegram-aggregator/tasks.md). Follow this workflow:

1. Pick a task from tasks.md (in order, respecting dependencies)
2. Implement the task completely
3. Test the implementation
4. Commit with format: `T###: [task description]`
5. Mark task as complete in tasks.md
6. Move to next task

**Example commit**:
```bash
git add .
git commit -m "T015: Create models/user.py with User model"
```

## User Stories & MVP

### MVP (Phase 3): User Story 1 - Job Search Monitoring

Core functionality for a working product:
- User registration and authentication
- Add Telegram groups to monitor
- Create keyword filters
- View filtered messages in unified feed
- Real-time updates via WebSocket

**MVP Completion**: ~100 tasks (Phases 1-3)

### Additional Features

- **US2 (P2)**: Semantic filtering, filter analytics, notification settings
- **US3 (P3)**: Multi-group management, group statistics, preview mode
- **US4 (P3)**: Mobile-responsive UI, touch gestures, infinite scroll
- **Enhancements**: Hot matches, Markdown rendering, advanced notifications

## Testing

### Backend Tests

```bash
cd backend
pytest
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Contributing

1. Check [tasks.md](specs/001-telegram-aggregator/tasks.md) for available tasks
2. Follow the constitution principles
3. One task = one commit
4. Run tests before committing
5. Update tasks.md to mark completed tasks

## License

[Add License Information]

## Support

For issues and questions:
- Review documentation in [specs/](specs/001-telegram-aggregator/)
- Check API documentation at http://localhost:8000/docs
- See quickstart guide for troubleshooting

---

**Current Status**: Phase 1 (Setup) in progress
**Next Milestone**: Complete foundational infrastructure (Phase 2)
**Target MVP**: User Story 1 completion (Phase 3)

