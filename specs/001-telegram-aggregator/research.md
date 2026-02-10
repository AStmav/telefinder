# Technical Research: Telegram Content Aggregator (TeleFinder)

**Feature**: 001-telegram-aggregator
**Date**: 2026-02-09
**Purpose**: Document technical decisions, research findings, and rationale for implementation choices

## Overview

This document consolidates technical research for TeleFinder, covering architecture decisions, library selections, and implementation patterns that resolve any ambiguities from the technical context.

## 1. Telegram Integration Strategy

### Decision: Hybrid User Bot + Bot API Approach

**Chosen**: Use Telegram Bot API with MTProto user session for group monitoring

**Rationale**:
- **Bot API** alone cannot read messages from groups (bots must be explicitly added and have limited access)
- **MTProto User Session** (via `telethon` or `pyrogram`) allows reading messages from groups the user is already a member of
- Hybrid approach: MTProto for monitoring, Bot API for notifications

**Implementation**:
- Primary library: `pyrogram` (modern, async-first, well-documented MTProto client)
- Fallback option: `telethon` (more mature, but older async patterns)
- Bot API via `python-telegram-bot` for sending notifications to users

**Alternatives Considered**:
- ❌ **Bot API only**: Cannot read group messages without being added to each group
- ❌ **MTProto only**: More complex for simple notification delivery
- ✅ **Hybrid**: Best of both worlds - read access via user session, notification delivery via bot

**Authentication Flow**:
1. User logs into TeleFinder web interface (email/password or Telegram Login Widget)
2. User authorizes TeleFinder with Telegram via MTProto (phone number + verification code)
3. TeleFinder stores encrypted session string in database
4. Backend uses session to monitor groups user is member of
5. Notifications sent via separate Bot API bot

### Decision: Message Polling vs Webhooks

**Chosen**: Long polling with `pyrogram` for message monitoring

**Rationale**:
- User sessions don't support webhooks (MTProto limitation)
- Long polling is efficient with `pyrogram`'s async implementation
- Simpler deployment (no public URL or SSL certificate required)

**Performance Impact**:
- Minimal latency (< 1 second for new messages)
- Low CPU usage with async/await patterns
- Scales to hundreds of groups per user

---

## 2. Semantic Filtering Implementation

### Decision: Embedding-Based Similarity with Sentence Transformers

**Chosen**: Use `sentence-transformers` with lightweight model (`all-MiniLM-L6-v2`)

**Rationale**:
- Fast inference (< 50ms per message on CPU)
- Excellent multilingual support (critical for Russian Telegram groups)
- No external API dependencies (privacy-preserving, no costs)
- Proven effective for short-text similarity

**Implementation**:
1. Pre-compute embeddings for user filter keywords/phrases
2. Compute embeddings for incoming messages
3. Calculate cosine similarity between message and filter embeddings
4. Threshold: > 0.65 similarity = match

**Alternatives Considered**:
- ❌ **GPT-4 / OpenAI**: Too expensive ($0.01 per 1K tokens), external API dependency
- ❌ **BERT full model**: Too slow (200ms+ per message), overkill for short text
- ✅ **Sentence-Transformers (MiniLM)**: Fast, accurate, self-hosted

**Model Details**:
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Embedding size: 384 dimensions
- Speed: ~50ms per message (CPU), ~5ms (GPU)
- Memory: ~80MB model size

---

## 3. Database Schema & Storage

### Decision: PostgreSQL with JSONB for Flexible Metadata

**Chosen**: PostgreSQL 14+ with SQLAlchemy ORM

**Rationale**:
- Robust relational database for structured data (users, groups, filters)
- JSONB support for flexible message metadata (attachments, reactions, etc.)
- Full-text search capabilities (PostgreSQL `tsvector` for keyword matching)
- Mature Python ecosystem (SQLAlchemy, Alembic for migrations)

**Schema Highlights**:
- **users**: User accounts, authentication, preferences
- **telegram_groups**: Group metadata, monitoring status
- **messages**: Message content, embeddings (as JSONB or separate table), timestamps
- **filters**: Filter definitions, keywords, semantic rules, thresholds
- **filter_matches**: Many-to-many relationship between messages and filters
- **notifications**: Notification queue and delivery status

**Scaling Considerations**:
- Partition `messages` table by month for performance
- Index on `(user_id, timestamp)` for feed queries
- Consider Redis cache for hot feed data (future optimization)

**Alternatives Considered**:
- ❌ **MongoDB**: Less mature Python ecosystem, no strong consistency guarantees
- ❌ **SQLite**: Not suitable for concurrent writes in production
- ✅ **PostgreSQL**: Industry-standard, excellent performance, rich feature set

---

## 4. Real-Time Feed Updates

### Decision: WebSocket with FastAPI + Vue.js Composable

**Chosen**: FastAPI WebSocket endpoints with Vue 3 composables for connection management

**Rationale**:
- FastAPI has built-in WebSocket support
- Vue 3 composables provide clean reactive WebSocket integration
- Low-latency feed updates without polling
- Efficient server-to-client push for new messages

**Implementation**:
- Backend: FastAPI WebSocket route at `/ws/feed`
- Frontend: `useWebSocket` composable managing connection lifecycle
- Events: `new_message`, `filter_match`, `hot_match`, `group_status_change`
- Reconnection logic: Exponential backoff on disconnect

**Alternatives Considered**:
- ❌ **HTTP polling**: Higher latency, more server load
- ❌ **Server-Sent Events**: One-way only, less flexible than WebSocket
- ✅ **WebSocket**: Bidirectional, low-latency, standard browser support

---

## 5. Frontend State Management

### Decision: Pinia for Vue 3 State Management

**Chosen**: Pinia (official Vue 3 state management)

**Rationale**:
- Official recommendation for Vue 3 (replaces Vuex)
- TypeScript-first design (better type inference)
- Simpler API than Vuex (no mutations, just actions)
- Excellent DevTools support

**Stores**:
- `auth`: User authentication state
- `feed`: Message feed state, pagination
- `filters`: Filter definitions, performance metrics
- `groups`: Group list, status monitoring
- `notifications`: Notification preferences, history

**Alternatives Considered**:
- ❌ **Vuex**: Older, more verbose, less TypeScript-friendly
- ❌ **Plain reactive state**: No structure, hard to debug
- ✅ **Pinia**: Modern, type-safe, officially recommended

---

## 6. Testing Strategy

### Decision: Pytest + Vitest with Contract Tests Priority

**Chosen**: 
- Backend: `pytest` with `pytest-asyncio` for async tests
- Frontend: `vitest` (Vite-native, fast)
- Contract tests: OpenAPI schema validation

**Rationale**:
- Constitution emphasizes testing discipline
- Contract tests ensure frontend-backend compatibility
- Async test support critical for Telegram polling and WebSocket tests

**Test Pyramid**:
1. **Contract tests** (highest priority): Validate API compliance with OpenAPI spec
2. **Integration tests**: Test Telegram service, filter service, database interactions
3. **Unit tests**: Test individual functions, components

**Key Testing Libraries**:
- `pytest-asyncio`: Async test support
- `httpx`: Async HTTP client for API testing
- `pytest-mock`: Mocking Telegram API responses
- `@testing-library/vue`: Component testing for Vue

---

## 7. Deployment & Environment

### Decision: Docker Compose for Local, Docker + PostgreSQL for Production

**Chosen**: Dockerized services with docker-compose for development

**Rationale**:
- Consistent development environment
- Easy onboarding (single `docker-compose up` command)
- Production-ready containerization
- Matches constitution's environment variable management

**Services**:
- `backend`: FastAPI application (Python 3.10+)
- `frontend`: Vite dev server (development) / Nginx (production)
- `db`: PostgreSQL 14+
- `redis` (future): Caching layer for feed data

**Environment Variables** (documented in `.env.example`):
- `DATABASE_URL`: PostgreSQL connection string
- `TELEGRAM_API_ID`: Telegram API credentials (from my.telegram.org)
- `TELEGRAM_API_HASH`: Telegram API hash
- `TELEGRAM_BOT_TOKEN`: Bot token for notifications
- `SECRET_KEY`: JWT signing key for authentication
- `EMBEDDING_MODEL`: Sentence transformer model name

---

## 8. Security Considerations

### Decision: Encrypted Session Storage + JWT Authentication

**Chosen**: 
- Telegram session strings encrypted with Fernet (symmetric encryption)
- JWT tokens for web API authentication
- HTTPS mandatory in production

**Rationale**:
- Telegram sessions are sensitive (full account access)
- Symmetric encryption with key stored in environment variable
- JWT provides stateless authentication for API

**Implementation**:
- `cryptography.fernet` for session encryption
- `python-jose` for JWT handling
- Session encryption key in `SESSION_ENCRYPTION_KEY` environment variable

**Security Practices**:
- Rate limiting on authentication endpoints (10 requests/minute)
- Input sanitization for filters (prevent injection attacks)
- CORS configuration for frontend domain only
- Regular dependency updates (Dependabot)

---

## 9. Performance Optimizations

### Decision: Async-First Architecture with Background Workers

**Chosen**:
- FastAPI async endpoints for all I/O-bound operations
- Background worker pattern for message processing
- Database connection pooling

**Rationale**:
- Async allows handling thousands of concurrent WebSocket connections
- Background workers prevent blocking API responses
- Connection pooling reduces database overhead

**Implementation**:
- `asyncio.create_task()` for background message processing
- SQLAlchemy async engine with connection pool
- Pyrogram async client for Telegram operations

**Expected Performance**:
- API response time: < 100ms (p95)
- Message processing latency: < 30 seconds (from Telegram to database)
- Feed load time: < 500ms for 100 messages
- WebSocket throughput: 1000+ concurrent connections per instance

---

## 10. Markdown Handling

### Decision: Python-Markdown with Bleach Sanitization

**Chosen**: 
- `python-markdown` for parsing
- `bleach` for HTML sanitization
- Custom extension for Telegram-specific formatting

**Rationale**:
- Telegram uses its own Markdown variant (MarkdownV2)
- Need to safely render in browser (XSS prevention)
- Python-markdown is extensible and well-maintained

**Implementation**:
1. Parse Telegram MarkdownV2 from message
2. Convert to standard Markdown
3. Render to HTML with `python-markdown`
4. Sanitize HTML with `bleach` (whitelist safe tags)
5. Send sanitized HTML to frontend

**Alternatives Considered**:
- ❌ **Client-side parsing**: Risk of XSS if malicious Markdown injected
- ❌ **Plain text only**: Loses formatting, poor UX
- ✅ **Server-side + sanitization**: Safe, preserves formatting

---

## Summary of Key Decisions

| Area | Decision | Primary Library/Tool |
|------|----------|---------------------|
| Telegram Monitoring | MTProto User Session | `pyrogram` |
| Telegram Notifications | Bot API | `python-telegram-bot` |
| Semantic Filtering | Sentence Embeddings | `sentence-transformers` |
| Database | PostgreSQL | `SQLAlchemy` + `Alembic` |
| Backend Framework | FastAPI (async) | `fastapi` |
| Frontend Framework | Vue 3 + TypeScript | `vue` + `vite` |
| State Management | Pinia | `pinia` |
| Real-Time Updates | WebSocket | FastAPI WebSocket + Vue composable |
| Styling | Tailwind CSS | `tailwindcss` |
| Testing | Pytest + Vitest | `pytest`, `vitest` |
| Markdown Processing | Python-Markdown | `python-markdown` + `bleach` |
| Authentication | JWT + Encrypted Sessions | `python-jose` + `cryptography` |
| Deployment | Docker Compose | `docker`, `docker-compose` |

---

## Next Steps (Phase 1)

1. Create detailed data model (data-model.md) with entity schemas
2. Generate OpenAPI contract specifications (contracts/api-spec.yaml)
3. Document WebSocket event contracts (contracts/websocket.md)
4. Create developer quickstart guide (quickstart.md)
5. Update agent context with technology stack

---

## Open Questions Resolved

**Q: How do users authenticate with Telegram?**
A: Two-step process - web authentication (JWT), then MTProto phone verification stored as encrypted session

**Q: How does the system read messages from private groups?**
A: Uses user's own Telegram session (MTProto) - can read any group the user is a member of

**Q: What semantic filtering technology?**
A: Sentence-transformers with MiniLM model (fast, accurate, self-hosted)

**Q: How are real-time updates delivered?**
A: WebSocket connection with event-driven updates for new messages, matches, and hot matches

**Q: How long are messages stored?**
A: Configurable retention (default: 30 days for feed, 90 days for hot matches) - see data-model.md

