# Data Model: Telegram Content Aggregator (TeleFinder)

**Feature**: 001-telegram-aggregator
**Date**: 2026-02-09
**Database**: PostgreSQL 14+

## Overview

This document defines the complete data model for TeleFinder, including entity schemas, relationships, validation rules, and state transitions.

## Entity Relationship Diagram

```
User (1) ──────< (M) TelegramGroup
  │                      │
  │                      │
  │                      │
  ├─────< (M) Filter     │
  │          │           │
  │          │           │
  │          └───< (M) FilterMatch >───┘
  │                      │
  │                      │
  ├─────< (M) Message <──┘
  │          │
  │          │
  └─────< (M) Notification
             │
             └── references Message
```

## Entities

### 1. User

Represents an individual TeleFinder user with authentication and preferences.

**Table**: `users`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email for web authentication |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `telegram_user_id` | BIGINT | UNIQUE, NULLABLE | Telegram user ID after MTProto auth |
| `telegram_phone` | VARCHAR(20) | NULLABLE | Phone number used for Telegram auth |
| `telegram_session` | TEXT | NULLABLE | Encrypted Pyrogram session string |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account activation status |
| `notification_preferences` | JSONB | DEFAULT '{}' | Notification settings (frequency, channels) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |
| `last_login_at` | TIMESTAMP | NULLABLE | Last successful login |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_users_email` on `email`
- `idx_users_telegram_user_id` on `telegram_user_id`

**Validation Rules**:
- Email must be valid format (validated by Pydantic)
- Password must be minimum 8 characters (enforced at API level)
- `telegram_session` encrypted with Fernet before storage

**State Transitions**:
- `is_active`: `true` (default) → `false` (user deactivation) → `true` (reactivation)

---

### 2. TelegramGroup

Represents a Telegram group being monitored by a user.

**Table**: `telegram_groups`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique group record identifier |
| `user_id` | UUID | FOREIGN KEY → users(id), NOT NULL | Owner of this monitoring configuration |
| `telegram_group_id` | BIGINT | NOT NULL | Telegram's internal group ID |
| `title` | VARCHAR(255) | NOT NULL | Group display name |
| `username` | VARCHAR(255) | NULLABLE | Group username (if public, e.g., @python_jobs) |
| `invite_link` | TEXT | NULLABLE | Invite link for private groups |
| `is_active` | BOOLEAN | DEFAULT TRUE | Monitoring enabled/disabled |
| `status` | VARCHAR(50) | DEFAULT 'active' | Status: active, unavailable, error |
| `last_message_at` | TIMESTAMP | NULLABLE | Timestamp of last received message |
| `message_count` | INTEGER | DEFAULT 0 | Total messages received from this group |
| `match_count` | INTEGER | DEFAULT 0 | Total filter matches from this group |
| `error_message` | TEXT | NULLABLE | Last error (if status = 'error') |
| `added_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When user added this group |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_telegram_groups_user_id` on `user_id`
- `idx_telegram_groups_telegram_group_id` on `telegram_group_id`
- `idx_telegram_groups_user_status` on `(user_id, status)` for active group queries

**Validation Rules**:
- `telegram_group_id` must be negative (Telegram groups/channels have negative IDs)
- Either `username` OR `invite_link` must be present
- `status` ENUM: 'active', 'unavailable', 'error', 'disabled'

**State Transitions**:
- `status`: `active` → `unavailable` (lost access) → `active` (access restored)
- `status`: `active` → `error` (API failure) → `active` (recovered)
- `is_active`: `true` → `false` (user disables) → `true` (user re-enables)

---

### 3. Message

Represents a Telegram message collected from a monitored group.

**Table**: `messages`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique message record identifier |
| `user_id` | UUID | FOREIGN KEY → users(id), NOT NULL | User who owns this message (via group) |
| `telegram_group_id` | UUID | FOREIGN KEY → telegram_groups(id), NOT NULL | Source group |
| `telegram_message_id` | BIGINT | NOT NULL | Telegram's internal message ID |
| `text` | TEXT | NOT NULL | Message text content |
| `author_id` | BIGINT | NULLABLE | Telegram user ID of author |
| `author_name` | VARCHAR(255) | NULLABLE | Display name of author |
| `timestamp` | TIMESTAMP | NOT NULL | When message was sent in Telegram |
| `telegram_link` | TEXT | NOT NULL | Direct link to original message |
| `has_media` | BOOLEAN | DEFAULT FALSE | Whether message has attachments |
| `media_type` | VARCHAR(50) | NULLABLE | Type: photo, video, document, etc. |
| `metadata` | JSONB | DEFAULT '{}' | Additional metadata (reactions, views, etc.) |
| `embedding` | VECTOR(384) | NULLABLE | Sentence embedding for semantic search |
| `processed_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When TeleFinder processed this message |
| `updated_at` | TIMESTAMP | NULLABLE | Last update (if message edited) |

**Indexes**:
- `idx_messages_user_timestamp` on `(user_id, timestamp DESC)` for feed queries
- `idx_messages_telegram_group_id` on `telegram_group_id`
- `idx_messages_telegram_message_id` on `(telegram_group_id, telegram_message_id)` for deduplication
- `idx_messages_embedding` using `vector_cosine_ops` for semantic search (requires pgvector extension)

**Partitioning**:
- Partition by `timestamp` (monthly partitions) for scalability

**Validation Rules**:
- `text` minimum length: 1 character (Telegram minimum)
- `telegram_link` format: `https://t.me/c/{group_id}/{message_id}` or `https://t.me/{username}/{message_id}`
- `media_type` ENUM: 'photo', 'video', 'document', 'audio', 'voice', 'sticker', 'animation'

**Data Retention**:
- Default: 30 days for regular messages
- Hot matches: 90 days
- User can configure per-group retention (7-365 days)

---

### 4. Filter

Represents user-defined filtering criteria for message relevance.

**Table**: `filters`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique filter identifier |
| `user_id` | UUID | FOREIGN KEY → users(id), NOT NULL | Filter owner |
| `name` | VARCHAR(100) | NOT NULL | User-friendly filter name |
| `keywords` | TEXT[] | NOT NULL | Array of keywords (exact/partial match) |
| `negative_keywords` | TEXT[] | DEFAULT '{}' | Exclusion keywords |
| `semantic_enabled` | BOOLEAN | DEFAULT FALSE | Enable semantic (embedding) matching |
| `semantic_threshold` | FLOAT | DEFAULT 0.65 | Cosine similarity threshold (0-1) |
| `priority` | INTEGER | DEFAULT 0 | Priority level (higher = hot match) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Filter enabled/disabled |
| `notification_enabled` | BOOLEAN | DEFAULT FALSE | Send notifications for matches |
| `notification_frequency` | VARCHAR(20) | DEFAULT 'instant' | instant, hourly, daily |
| `match_count` | INTEGER | DEFAULT 0 | Total matches for this filter |
| `last_match_at` | TIMESTAMP | NULLABLE | Timestamp of last match |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Filter creation timestamp |
| `updated_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last update timestamp |

**Indexes**:
- `idx_filters_user_id` on `user_id`
- `idx_filters_user_active` on `(user_id, is_active)` for active filter queries

**Validation Rules**:
- `keywords` array must have at least 1 element
- `semantic_threshold` range: 0.5 - 0.9 (validated at API level)
- `priority` range: 0 (normal) - 10 (critical)
- `notification_frequency` ENUM: 'instant', 'hourly', 'daily', 'none'

**Special Filter Types**:
- Priority >= 7: "Hot match" filter (triggers immediate notification)
- Priority < 7: Regular filter (appears in feed only)

---

### 5. FilterMatch

Represents the many-to-many relationship between messages and filters.

**Table**: `filter_matches`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique match identifier |
| `message_id` | UUID | FOREIGN KEY → messages(id), NOT NULL | Matched message |
| `filter_id` | UUID | FOREIGN KEY → filters(id), NOT NULL | Matching filter |
| `match_type` | VARCHAR(20) | NOT NULL | Type: keyword, semantic, both |
| `relevance_score` | FLOAT | NOT NULL | Relevance score (0-1) |
| `matched_keywords` | TEXT[] | DEFAULT '{}' | Which keywords matched |
| `similarity_score` | FLOAT | NULLABLE | Cosine similarity (if semantic match) |
| `is_hot_match` | BOOLEAN | DEFAULT FALSE | Whether this triggered hot match notification |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | When match was detected |

**Indexes**:
- `idx_filter_matches_message_id` on `message_id`
- `idx_filter_matches_filter_id` on `filter_id`
- `idx_filter_matches_hot` on `is_hot_match` for hot match queries
- UNIQUE constraint on `(message_id, filter_id)` to prevent duplicate matches

**Validation Rules**:
- `match_type` ENUM: 'keyword', 'semantic', 'both'
- `relevance_score` range: 0.0 - 1.0
- `similarity_score` range: 0.0 - 1.0 (if semantic match)

**Business Logic**:
- `relevance_score` calculation:
  - Keyword match: count(matched_keywords) / count(filter.keywords)
  - Semantic match: `similarity_score`
  - Both: `max(keyword_score, similarity_score)`
- `is_hot_match` = `true` if `filter.priority >= 7` AND `relevance_score >= 0.7`

---

### 6. Notification

Represents notifications sent to users about hot matches.

**Table**: `notifications`

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY | Unique notification identifier |
| `user_id` | UUID | FOREIGN KEY → users(id), NOT NULL | Notification recipient |
| `message_id` | UUID | FOREIGN KEY → messages(id), NOT NULL | Referenced message |
| `filter_id` | UUID | FOREIGN KEY → filters(id), NOT NULL | Triggering filter |
| `type` | VARCHAR(20) | DEFAULT 'hot_match' | Notification type |
| `channel` | VARCHAR(20) | NOT NULL | Delivery channel: telegram_bot, web_push |
| `status` | VARCHAR(20) | DEFAULT 'pending' | Status: pending, sent, failed, read |
| `title` | VARCHAR(255) | NOT NULL | Notification title |
| `body` | TEXT | NOT NULL | Notification body (preview) |
| `telegram_link` | TEXT | NOT NULL | Link to original message |
| `sent_at` | TIMESTAMP | NULLABLE | When notification was sent |
| `read_at` | TIMESTAMP | NULLABLE | When user read notification |
| `error_message` | TEXT | NULLABLE | Error details (if status = 'failed') |
| `retry_count` | INTEGER | DEFAULT 0 | Number of delivery retries |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Notification creation timestamp |

**Indexes**:
- `idx_notifications_user_status` on `(user_id, status)` for pending notifications
- `idx_notifications_message_id` on `message_id`
- `idx_notifications_created_at` on `created_at DESC` for notification history

**Validation Rules**:
- `type` ENUM: 'hot_match', 'system', 'group_unavailable'
- `channel` ENUM: 'telegram_bot', 'web_push', 'email'
- `status` ENUM: 'pending', 'sent', 'failed', 'read'
- `retry_count` max: 3 attempts

**State Transitions**:
- `status`: `pending` → `sent` (successful delivery)
- `status`: `pending` → `failed` (delivery failure after retries)
- `status`: `sent` → `read` (user viewed notification)

**Business Logic**:
- Retry logic: Exponential backoff (1min, 5min, 15min)
- Batching: Group notifications if `filter.notification_frequency` != 'instant'

---

## Relationships Summary

| Relationship | Type | Description |
|--------------|------|-------------|
| User → TelegramGroup | 1:M | User monitors multiple groups |
| User → Filter | 1:M | User creates multiple filters |
| User → Message | 1:M | User receives messages from monitored groups |
| User → Notification | 1:M | User receives notifications |
| TelegramGroup → Message | 1:M | Group contains many messages |
| Message → FilterMatch | 1:M | Message can match multiple filters |
| Filter → FilterMatch | 1:M | Filter matches multiple messages |
| Message → Notification | 1:M | Message can trigger multiple notifications (different filters) |
| Filter → Notification | 1:M | Filter triggers notifications for matches |

---

## Database Indexes Strategy

**Primary Indexes** (critical for performance):
1. `users.email` - Authentication queries
2. `telegram_groups(user_id, status)` - Active group lists
3. `messages(user_id, timestamp DESC)` - Feed queries (most critical)
4. `filter_matches.is_hot_match` - Hot match queries
5. `notifications(user_id, status)` - Pending notification delivery

**Secondary Indexes** (optimization):
1. `messages.telegram_group_id` - Per-group message queries
2. `messages.embedding` (vector index) - Semantic search
3. `filter_matches(message_id, filter_id)` - Match lookups

---

## Migrations Strategy

Using **Alembic** for schema versioning:

1. Initial schema (v1.0): All core tables
2. Future migrations:
   - Add message reaction tracking (v1.1)
   - Add user collaboration features (v2.0)
   - Add message translation support (v2.1)

**Migration Files Location**: `backend/alembic/versions/`

---

## Data Retention Policies

| Entity | Default Retention | Rationale |
|--------|-------------------|-----------|
| `messages` (regular) | 30 days | Balance storage vs. history |
| `messages` (hot matches) | 90 days | Important content kept longer |
| `filter_matches` | Same as messages | Tied to message lifecycle |
| `notifications` | 30 days | Audit trail for troubleshooting |
| `users` | Indefinite | Until account deletion |
| `telegram_groups` | Indefinite | User configuration |
| `filters` | Indefinite | User configuration |

**Implementation**: Background job runs daily to purge expired records.

---

## Security Considerations

1. **Encrypted Fields**:
   - `users.telegram_session`: Encrypted with Fernet symmetric key
   - Encryption key stored in `SESSION_ENCRYPTION_KEY` environment variable

2. **Sensitive Data**:
   - `users.password_hash`: Bcrypt with cost factor 12
   - `users.telegram_phone`: GDPR-sensitive, masked in logs

3. **Access Control**:
   - All queries filtered by `user_id` (row-level security)
   - No cross-user data access possible at ORM level

---

## Performance Projections

**Assumptions**:
- 100 users
- 50 groups per user (5,000 groups total)
- 10 messages per group per day (50,000 messages/day)

**Database Size Estimates**:
- `messages`: ~5GB per month (with embeddings)
- `filter_matches`: ~500MB per month
- Total growth: ~6GB per month
- After 30-day retention: ~6GB steady state

**Query Performance Targets**:
- Feed query (100 messages): < 100ms
- Filter matching: < 50ms per message
- Hot match notification: < 5 seconds end-to-end

---

## Next Steps

1. Generate SQLAlchemy ORM models from this schema
2. Create Alembic initial migration
3. Define Pydantic schemas for API request/response validation
4. Document API contracts in OpenAPI specification

