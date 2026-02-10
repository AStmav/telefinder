# Implementation Plan: Telegram Content Aggregator (TeleFinder)

**Branch**: `001-telegram-aggregator` | **Date**: 2026-02-09 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-telegram-aggregator/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.cursor/commands/speckit.plan.md` for the execution workflow.

## Summary

TeleFinder is a personal Telegram content aggregator that automatically collects messages from user-specified Telegram groups, applies smart filtering (keyword + semantic), displays results in a unified feed, and sends notifications for high-priority matches. The system saves users 70%+ of manual monitoring time while ensuring critical opportunities (jobs, announcements) are never missed.

**Technical Approach**: Full-stack web application using Python FastAPI backend for Telegram integration and message processing, Vue.js + TypeScript frontend for user interface, with real-time updates and intelligent filtering algorithms.

## Technical Context

**Language/Version**: Python 3.10+ (backend), TypeScript with Vue.js 3 (frontend)
**Primary Dependencies**: FastAPI, python-telegram-bot (or aiogram), Vue.js 3, TypeScript, Tailwind CSS, Vite
**Storage**: SQLite for persistent storage (users, groups, messages, filters)
**Testing**: pytest (backend), Vitest (frontend)
**Target Platform**: Linux server (backend), Modern web browsers (frontend - mobile-first)
**Project Type**: Web application (separate backend/frontend)
**Performance Goals**: Process messages within 1 minute of Telegram posting, handle 10,000 messages/day, support 50+ groups per user
**Constraints**: 1-minute notification delivery SLA, 80%+ signal-to-noise ratio, Telegram API rate limits (20 calls/sec typical)
**Scale/Scope**: Initial target: 100 users, 5,000 groups total, 50,000 messages/day; Design for 10x growth

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ I. Technology Stack (NON-NEGOTIABLE)
- **Backend**: ✅ Python FastAPI
- **Frontend**: ✅ Vue.js with TypeScript
- **Styling**: ✅ Tailwind CSS
- **Integration**: ✅ Telegram Bot API

**Status**: PASS - All technology choices comply with constitution

### ✅ II. Telegram Bot API Integration
- Bot functionality will be modular (separate service layer)
- API interactions abstracted behind TelegramService class
- Error handling for rate limits, access errors, API failures mandatory

**Status**: PASS - Architecture includes proper Telegram abstraction

### ✅ III. Markdown Processing & Validation (NON-NEGOTIABLE)
- Markdown converter service for message display
- Validation before rendering in feed
- Support for Telegram's Markdown format

**Status**: PASS - Markdown processing included in requirements

### ✅ IV. Environment-Based Configuration (NON-NEGOTIABLE)
- All tokens (Telegram Bot token, DB credentials) in environment variables
- `.env.example` will be created documenting all required variables
- Application startup validates required environment variables

**Status**: PASS - Configuration management follows constitution

### ✅ V. Atomic Git Commits (NON-NEGOTIABLE)
- Each task in tasks.md = one commit
- Commit format: `T###: [task description]`
- No multi-task commits

**Status**: PASS - Development workflow will follow task-driven commits

**Overall Constitution Check**: ✅ PASS - No violations, ready for Phase 0 research

## Data Storage & Persistence (SQLite)

**WHAT**  
- Introduce SQLite database for persistent storage.  
- Store user-specific settings, filter configurations, Telegram group subscriptions, and message metadata.  
- Ensure isolation of user data to support multiple simultaneous users.  
- Maintain minimal message and notification history for analytics and offline access.  

**WHY**  
- SQLite is lightweight, file-based, and suitable for small-to-medium multi-user scenarios.  
- Retains user preferences and filter states between sessions.  
- Enables offline or local testing without requiring a separate DB server.  
- Future-proof for migration to PostgreSQL/MySQL without affecting business logic.  

**Linked Entities**: `User`, `TelegramGroup`, `Message`, `Filter`, `Notification`  

---

## Project Structure

### Documentation (this feature)

```text
specs/001-telegram-aggregator/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (entity schemas)
├── quickstart.md        # Phase 1 output (developer setup guide)
├── contracts/           # Phase 1 output (API contracts)
│   ├── api-spec.yaml    # OpenAPI specification
│   └── websocket.md     # WebSocket event contracts
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/                    # FastAPI routes
│   │   ├── routes/             # Endpoint handlers
│   │   │   ├── auth.py
│   │   │   ├── groups.py
│   │   │   ├── filters.py
│   │   │   ├── feed.py
│   │   │   └── notifications.py
│   │   ├── middleware/         # Request/response middleware
│   │   └── dependencies.py     # FastAPI dependencies (auth, DB session injection)
│   ├── models/                 # SQLAlchemy ORM models (SQLite-based)
│   │   ├── user.py             # User entity with SQLite persistence
│   │   ├── telegram_group.py   # TelegramGroup entity
│   │   ├── message.py          # Message entity
│   │   ├── filter.py           # Filter entity
│   │   └── notification.py     # Notification entity
│   ├── services/               # Business logic
│   │   ├── telegram_service.py      # Telegram Bot API integration
│   │   ├── filter_service.py        # Keyword & semantic filtering
│   │   ├── feed_service.py          # Feed aggregation & sorting
│   │   ├── notification_service.py  # Notification delivery
│   │   └── markdown_service.py      # Markdown conversion & validation
│   ├── telegram/               # Telegram-specific modules
│   │   ├── bot_handler.py      # Bot command handlers
│   │   ├── message_listener.py # Message monitoring daemon
│   │   └── auth.py             # Telegram authentication
│   ├── config/                 # Configuration management
│   │   ├── settings.py         # Environment variable loading (includes SQLite path)
│   │   └── database.py         # Database connection (SQLite engine creation, session management)
│   ├── schemas/                # Pydantic models (request/response)
│   │   ├── user.py
│   │   ├── group.py
│   │   ├── message.py
│   │   └── filter.py
│   └── main.py                 # FastAPI application entry point (SQLite session middleware included)
├── tests/
│   ├── contract/               # API contract tests
│   ├── integration/            # Integration tests (with SQLite test DB)
│   └── unit/                   # Unit tests
├── alembic/                    # Database migrations (optional for SQLite)
│   └── versions/
├── requirements.txt            # Python dependencies (SQLAlchemy, SQLite support)
├── .env.example                # Environment variable template (including SQLITE_DB_PATH)
└── README.md                   # Backend setup instructions

frontend/
├── src/
│   ├── components/             # Vue components
│   │   ├── feed/
│   │   │   ├── FeedList.vue
│   │   │   ├── MessageCard.vue
│   │   │   └── HotMatches.vue
│   │   ├── filters/
│   │   │   ├── FilterList.vue
│   │   │   ├── FilterEditor.vue
│   │   │   └── FilterStats.vue
│   │   ├── groups/
│   │   │   ├── GroupList.vue
│   │   │   └── AddGroupModal.vue
│   │   └── common/
│   │       ├── Button.vue
│   │       ├── Input.vue
│   │       └── Modal.vue
│   ├── pages/
│   │   ├── LoginPage.vue
│   │   ├── FeedPage.vue
│   │   ├── FiltersPage.vue
│   │   ├── GroupsPage.vue
│   │   └── SettingsPage.vue
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth-service.ts
│   │   ├── feed-service.ts
│   │   ├── filter-service.ts
│   │   └── group-service.ts
│   ├── stores/
│   │   ├── auth.ts
│   │   ├── feed.ts
│   │   ├── filters.ts
│   │   └── groups.ts
│   ├── types/
│   │   ├── user.ts
│   │   ├── message.ts
│   │   ├── filter.ts
│   │   └── group.ts
│   ├── composables/
│   │   ├── useNotifications.ts
│   │   └── useWebSocket.ts
│   ├── router/
│   │   └── index.ts
│   ├── assets/
│   │   └── styles/
│   │       └── tailwind.css
│   ├── App.vue
│   └── main.ts
├── tests/
│   ├── unit/
│   └── e2e/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
└── README.md

.env.example                    # Template now includes SQLITE_DB_PATH
.gitignore                      # Git ignore rules (includes .env and SQLite DB file)
docker-compose.yml              # Optional local dev environment
README.md                       # Project overview and setup
```

**Structure Decision**: Web application structure (Option 2) selected because:
- Separate concerns: Backend handles Telegram integration and data, frontend handles UI
- Constitution mandates Python FastAPI (backend) + Vue.js/TypeScript (frontend)
- Allows independent scaling and deployment
- Clear API boundary enables mobile app development in future

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. All architecture decisions comply with constitution principles.
