# Tasks: Telegram Content Aggregator (TeleFinder)

**Input**: Design documents from `/specs/001-telegram-aggregator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Database**: SQLite (lightweight, file-based persistence)
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Root**: `.env.example`, `README.md`, `.gitignore`, `docker-compose.yml`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure per plan.md (backend/src/{api,models,services,telegram,config,schemas})
- [x] T002 Create frontend directory structure per plan.md (frontend/src/{components,pages,services,stores,types,composables,router,assets})
- [x] T003 [P] Initialize Python project in backend/requirements.txt with FastAPI, SQLAlchemy, python-telegram-bot, sentence-transformers
- [x] T004 [P] Initialize Node.js project in frontend/package.json with Vue 3, TypeScript, Vite, Tailwind CSS, Pinia
- [x] T005 [P] Create .gitignore at repository root (Python, Node.js, SQLite DB file patterns)
- [x] T006 [P] Create .env.example at repository root with all required environment variables (SQLite path, Telegram credentials)
- [x] T007 [P] Create README.md at repository root with project overview and setup instructions
- [x] T008 [P] Create backend/README.md with backend-specific setup instructions
- [x] T009 [P] Create frontend/README.md with frontend-specific setup instructions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database & Configuration

- [x] T010 Create config/settings.py with Pydantic Settings for environment variable loading (SQLITE_DB_PATH, TELEGRAM_API_ID, etc.)
- [x] T011 Create config/database.py with SQLAlchemy engine for SQLite (create_engine with sqlite:/// URL)
- [x] T012 Create database session management in config/database.py (SessionLocal, get_db dependency)
- [x] T013 [P] Initialize Alembic for database migrations in backend/alembic/ (alembic init)
- [ ] T014 Configure Alembic env.py to use SQLAlchemy models and SQLite database URL

### Core Models (SQLAlchemy ORM with SQLite)

- [ ] T015 [P] Create models/user.py with User model (id, email, password_hash, telegram_user_id, telegram_session, preferences)
- [ ] T016 [P] Create models/telegram_group.py with TelegramGroup model (id, user_id, telegram_group_id, title, status, message_count)
- [ ] T017 [P] Create models/message.py with Message model (id, user_id, group_id, text, timestamp, telegram_link, metadata)
- [ ] T018 [P] Create models/filter.py with Filter model (id, user_id, name, keywords, semantic_enabled, priority, notification_enabled)
- [ ] T019 [P] Create models/notification.py with Notification model (id, user_id, message_id, filter_id, status, sent_at)
- [ ] T020 Create Alembic migration for initial schema (alembic revision --autogenerate -m "initial schema")

### Authentication & Security

- [ ] T021 Create schemas/user.py with Pydantic models (UserCreate, UserResponse, UserLogin)
- [ ] T022 Create api/dependencies.py with JWT authentication dependency (get_current_user)
- [ ] T023 Create api/middleware/cors.py with CORS configuration for frontend origin
- [ ] T024 Create services/auth_service.py with password hashing (bcrypt), JWT token generation/validation
- [ ] T025 Create api/routes/auth.py with /register and /login endpoints

### FastAPI Application Setup

- [ ] T026 Create main.py with FastAPI app initialization, CORS middleware, router registration
- [ ] T027 Add database session middleware to main.py (inject get_db into request context)
- [ ] T028 Add startup event handler to main.py (create SQLite database file if not exists)
- [ ] T029 Add /health endpoint to main.py for application health checks

### Telegram Integration Foundation

- [ ] T030 Create telegram/auth.py with Pyrogram client initialization for MTProto authentication
- [ ] T031 Create telegram/bot_handler.py with python-telegram-bot Bot initialization for notifications
- [ ] T032 Create services/telegram_service.py with methods for group monitoring setup (add_group, remove_group)
- [ ] T033 Implement session encryption in services/telegram_service.py using cryptography.fernet

### Frontend Foundation

- [ ] T034 Create frontend/src/main.ts with Vue app initialization, Pinia, Vue Router
- [ ] T035 [P] Create frontend/src/router/index.ts with route definitions (login, feed, filters, groups, settings)
- [ ] T036 [P] Create frontend/src/services/api.ts with Axios instance (base URL, auth interceptors)
- [ ] T037 [P] Create frontend/src/stores/auth.ts with Pinia auth store (user state, login/logout actions)
- [ ] T038 [P] Create frontend/src/types/user.ts with TypeScript interfaces for User
- [ ] T039 [P] Create frontend/tailwind.config.js with Tailwind CSS configuration
- [ ] T040 [P] Create frontend/src/assets/styles/tailwind.css with Tailwind imports
- [ ] T041 Create frontend/src/App.vue with root layout and router-view

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Job Search Monitoring (Priority: P1) 🎯 MVP

**Goal**: User can add Telegram groups, create keyword filters, and see filtered messages in unified feed

**Independent Test**: Add 5 groups, create filter with ["Python", "Remote"], verify matching messages appear in feed within 1 minute

### Backend - Group Management (US1)

- [ ] T042 [P] [US1] Create schemas/group.py with Pydantic models (GroupCreate, GroupResponse, GroupUpdate)
- [ ] T043 [P] [US1] Create api/routes/groups.py with GET /groups endpoint (list user's groups)
- [ ] T044 [US1] Add POST /groups endpoint to api/routes/groups.py (add new group by username or link)
- [ ] T045 [US1] Add GET /groups/{group_id} endpoint to api/routes/groups.py (get group details)
- [ ] T046 [US1] Add PATCH /groups/{group_id} endpoint to api/routes/groups.py (enable/disable monitoring)
- [ ] T047 [US1] Add DELETE /groups/{group_id} endpoint to api/routes/groups.py (remove group)

### Backend - Message Collection (US1)

- [ ] T048 [US1] Create telegram/message_listener.py with async message monitoring loop using Pyrogram
- [ ] T049 [US1] Implement group message handler in telegram/message_listener.py (on_new_message callback)
- [ ] T050 [US1] Create services/message_service.py with save_message method (store to SQLite)
- [ ] T051 [US1] Add message link generation in services/message_service.py (format Telegram t.me links)
- [ ] T052 [US1] Integrate message_listener with FastAPI startup event (background task)

### Backend - Filter Management (US1)

- [ ] T053 [P] [US1] Create schemas/filter.py with Pydantic models (FilterCreate, FilterResponse, FilterUpdate)
- [ ] T054 [P] [US1] Create api/routes/filters.py with GET /filters endpoint (list user's filters)
- [ ] T055 [US1] Add POST /filters endpoint to api/routes/filters.py (create new filter)
- [ ] T056 [US1] Add GET /filters/{filter_id} endpoint to api/routes/filters.py (get filter details)
- [ ] T057 [US1] Add PUT /filters/{filter_id} endpoint to api/routes/filters.py (update filter)
- [ ] T058 [US1] Add DELETE /filters/{filter_id} endpoint to api/routes/filters.py (delete filter)

### Backend - Keyword Filtering (US1)

- [ ] T059 [US1] Create services/filter_service.py with keyword matching logic (case-insensitive substring search)
- [ ] T060 [US1] Implement negative keyword filtering in services/filter_service.py (exclusion logic)
- [ ] T061 [US1] Add relevance score calculation in services/filter_service.py (matched_keywords / total_keywords)
- [ ] T062 [US1] Create FilterMatch model in models/ (many-to-many: message_id, filter_id, relevance_score)
- [ ] T063 [US1] Integrate filter_service with message_listener (apply filters on new messages)

### Backend - Feed API (US1)

- [ ] T064 [P] [US1] Create schemas/message.py with Pydantic models (MessageResponse, FeedMessageResponse)
- [ ] T065 [P] [US1] Create api/routes/feed.py with GET /feed endpoint (list filtered messages)
- [ ] T066 [US1] Add sorting options to GET /feed (by timestamp, by relevance)
- [ ] T067 [US1] Add pagination to GET /feed (limit, offset parameters)
- [ ] T068 [US1] Add filter_id query parameter to GET /feed (filter by specific filter)
- [ ] T069 [US1] Add group_id query parameter to GET /feed (filter by specific group)

### Frontend - Authentication (US1)

- [ ] T070 [P] [US1] Create frontend/src/pages/LoginPage.vue with login form UI
- [ ] T071 [P] [US1] Create frontend/src/services/auth-service.ts with login/register API calls
- [ ] T072 [US1] Implement login action in frontend/src/stores/auth.ts (call API, save token)
- [ ] T073 [US1] Implement route guards in frontend/src/router/index.ts (redirect unauthenticated users)
- [ ] T074 [US1] Add token persistence in frontend/src/stores/auth.ts (localStorage)

### Frontend - Group Management UI (US1)

- [ ] T075 [P] [US1] Create frontend/src/types/group.ts with TypeScript interfaces for TelegramGroup
- [ ] T076 [P] [US1] Create frontend/src/services/group-service.ts with group CRUD API calls
- [ ] T077 [P] [US1] Create frontend/src/stores/groups.ts with Pinia store (groups state, actions)
- [ ] T078 [P] [US1] Create frontend/src/components/groups/GroupList.vue with group list display
- [ ] T079 [US1] Create frontend/src/components/groups/AddGroupModal.vue with add group form
- [ ] T080 [US1] Create frontend/src/pages/GroupsPage.vue integrating GroupList and AddGroupModal
- [ ] T081 [US1] Add group status indicators to GroupList.vue (active, unavailable, error)

### Frontend - Filter Management UI (US1)

- [ ] T082 [P] [US1] Create frontend/src/types/filter.ts with TypeScript interfaces for Filter
- [ ] T083 [P] [US1] Create frontend/src/services/filter-service.ts with filter CRUD API calls
- [ ] T084 [P] [US1] Create frontend/src/stores/filters.ts with Pinia store (filters state, actions)
- [ ] T085 [P] [US1] Create frontend/src/components/filters/FilterList.vue with filter list display
- [ ] T086 [US1] Create frontend/src/components/filters/FilterEditor.vue with filter create/edit form
- [ ] T087 [US1] Create frontend/src/pages/FiltersPage.vue integrating FilterList and FilterEditor
- [ ] T088 [US1] Add keyword chip input to FilterEditor.vue (add/remove keywords dynamically)

### Frontend - Feed Display (US1)

- [ ] T089 [P] [US1] Create frontend/src/types/message.ts with TypeScript interfaces for Message
- [ ] T090 [P] [US1] Create frontend/src/services/feed-service.ts with feed API calls
- [ ] T091 [P] [US1] Create frontend/src/stores/feed.ts with Pinia store (messages state, actions)
- [ ] T092 [P] [US1] Create frontend/src/components/feed/MessageCard.vue with single message display
- [ ] T093 [US1] Create frontend/src/components/feed/FeedList.vue with virtualized message list
- [ ] T094 [US1] Create frontend/src/pages/FeedPage.vue integrating FeedList
- [ ] T095 [US1] Add matched keywords highlighting in MessageCard.vue
- [ ] T096 [US1] Add "Open in Telegram" link to MessageCard.vue (telegram_link)
- [ ] T097 [US1] Add feed sorting controls to FeedPage.vue (timestamp, relevance)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Smart Filter Management (Priority: P2)

**Goal**: User can enable semantic filtering, see filter performance metrics, and adjust notification settings

**Independent Test**: Create filter, enable semantic matching, verify non-exact matches appear in feed; check filter stats show match count

### Backend - Semantic Filtering (US2)

- [ ] T098 [US2] Install sentence-transformers library and download all-MiniLM-L6-v2 model
- [ ] T099 [US2] Create services/embedding_service.py with model loading and text embedding generation
- [ ] T100 [US2] Add embedding column to Message model (store as JSON array in SQLite)
- [ ] T101 [US2] Create Alembic migration for message embedding column
- [ ] T102 [US2] Integrate embedding_service with message_listener (compute embeddings on new messages)
- [ ] T103 [US2] Add semantic matching logic to services/filter_service.py (cosine similarity calculation)
- [ ] T104 [US2] Implement similarity threshold check in filter_service (configurable per filter)
- [ ] T105 [US2] Update FilterMatch model to store similarity_score and match_type (keyword/semantic/both)

### Backend - Filter Performance Metrics (US2)

- [ ] T106 [US2] Add match_count and last_match_at columns to Filter model
- [ ] T107 [US2] Create Alembic migration for filter performance columns
- [ ] T108 [US2] Update filter_service to increment match_count on each match
- [ ] T109 [US2] Add GET /filters/{filter_id}/stats endpoint to api/routes/filters.py (match count, avg relevance)
- [ ] T110 [US2] Add filter performance to GET /filters response (include match_count, last_match_at)

### Backend - Notification Preferences (US2)

- [ ] T111 [US2] Add notification_frequency column to Filter model (instant, hourly, daily)
- [ ] T112 [US2] Create Alembic migration for notification preferences
- [ ] T113 [US2] Create services/notification_service.py with notification scheduling logic
- [ ] T114 [US2] Implement instant notification in notification_service (send immediately on hot match)
- [ ] T115 [US2] Implement batched notifications in notification_service (hourly/daily cron job)
- [ ] T116 [US2] Add GET /notifications endpoint to api/routes/notifications.py (notification history)
- [ ] T117 [US2] Add POST /notifications/{notification_id}/read endpoint (mark as read)

### Frontend - Semantic Filtering UI (US2)

- [ ] T118 [US2] Add semantic_enabled toggle to FilterEditor.vue
- [ ] T119 [US2] Add semantic_threshold slider to FilterEditor.vue (0.5-0.9 range)
- [ ] T120 [US2] Update filter-service.ts to include semantic options in create/update calls
- [ ] T121 [US2] Add semantic match indicator to MessageCard.vue (show similarity score)

### Frontend - Filter Performance Display (US2)

- [ ] T122 [P] [US2] Create frontend/src/components/filters/FilterStats.vue with performance metrics
- [ ] T123 [US2] Integrate FilterStats.vue into FilterList.vue (show match count per filter)
- [ ] T124 [US2] Add filter performance chart to FiltersPage.vue (matches over time)

### Frontend - Notification Settings (US2)

- [ ] T125 [US2] Add notification_frequency dropdown to FilterEditor.vue (instant, hourly, daily)
- [ ] T126 [US2] Add notification_enabled toggle to FilterEditor.vue
- [ ] T127 [US2] Create frontend/src/pages/SettingsPage.vue with global notification preferences
- [ ] T128 [US2] Add notification history list to SettingsPage.vue

**Checkpoint**: All user stories should now be independently functional

---

## Phase 5: User Story 3 - Multi-Source Content Discovery (Priority: P3)

**Goal**: User can manage 20+ groups, see group activity stats, and preview matches before adding groups

**Independent Test**: Add 20 groups, view sources list with activity indicators, disable noisy group and verify messages stop appearing

### Backend - Group Statistics (US3)

- [ ] T129 [US3] Add last_message_at and match_count columns to TelegramGroup model
- [ ] T130 [US3] Create Alembic migration for group statistics columns
- [ ] T131 [US3] Update message_listener to update last_message_at on new messages
- [ ] T132 [US3] Update filter_service to increment group match_count on matches
- [ ] T133 [US3] Add group statistics to GET /groups response (message_count, match_count, last_message_at)
- [ ] T134 [US3] Add GET /groups/stats endpoint to api/routes/groups.py (top active groups, top matching groups)

### Backend - Group Preview (US3)

- [ ] T135 [US3] Add POST /groups/preview endpoint to api/routes/groups.py (fetch recent messages without saving)
- [ ] T136 [US3] Implement preview logic in services/telegram_service.py (get last 20 messages from group)
- [ ] T137 [US3] Apply user's filters to preview messages in preview endpoint
- [ ] T138 [US3] Return preview results with match count and sample matched messages

### Frontend - Group Management Enhancements (US3)

- [ ] T139 [US3] Add group statistics display to GroupList.vue (message count, match count, last active)
- [ ] T140 [US3] Add sorting options to GroupsPage.vue (by activity, by matches, alphabetical)
- [ ] T141 [US3] Add group search/filter to GroupsPage.vue (filter by name, status)
- [ ] T142 [US3] Create preview mode in AddGroupModal.vue (show sample matches before adding)
- [ ] T143 [US3] Add bulk actions to GroupList.vue (enable/disable multiple groups)

**Checkpoint**: Multi-source management complete

---

## Phase 6: User Story 4 - Mobile-First Experience (Priority: P3)

**Goal**: Optimize UI for mobile devices with responsive layouts and touch-friendly interactions

**Independent Test**: Access app on mobile browser, verify feed scrolls smoothly, filters can be created with minimal taps

### Frontend - Mobile Responsive Layouts (US4)

- [ ] T144 [P] [US4] Add responsive breakpoints to tailwind.config.js (mobile-first approach)
- [ ] T145 [P] [US4] Make FeedPage.vue responsive (single column on mobile, side panels on desktop)
- [ ] T146 [P] [US4] Make GroupsPage.vue responsive (card grid on desktop, list on mobile)
- [ ] T147 [P] [US4] Make FiltersPage.vue responsive (adapt editor modal for mobile screens)
- [ ] T148 [US4] Add mobile navigation menu to App.vue (hamburger menu, bottom nav bar)
- [ ] T149 [US4] Optimize MessageCard.vue for mobile (larger tap targets, condensed info)

### Frontend - Mobile Interactions (US4)

- [ ] T150 [US4] Add swipe gestures to MessageCard.vue (swipe to open in Telegram, swipe to mark read)
- [ ] T151 [US4] Add pull-to-refresh to FeedPage.vue (reload feed on pull down)
- [ ] T152 [US4] Add infinite scroll to FeedList.vue (load more messages on scroll)
- [ ] T153 [US4] Optimize FilterEditor.vue for mobile (simplified keyword input, fewer form fields visible)
- [ ] T154 [US4] Add mobile-optimized date picker to filter creation (if time-based filtering added)

### Frontend - Mobile Performance (US4)

- [ ] T155 [US4] Implement virtual scrolling in FeedList.vue (only render visible messages)
- [ ] T156 [US4] Add image lazy loading to MessageCard.vue (defer media loading)
- [ ] T157 [US4] Optimize bundle size in vite.config.ts (code splitting, tree shaking)

**Checkpoint**: Mobile experience optimized

---

## Phase 7: WebSocket Real-Time Updates (Enhancement)

**Goal**: Add WebSocket support for real-time feed updates without page refresh

### Backend - WebSocket Implementation

- [ ] T158 Create /ws/feed WebSocket endpoint in main.py with JWT authentication
- [ ] T159 Implement connection manager in services/websocket_service.py (track active connections per user)
- [ ] T160 Add new_message event broadcasting in message_listener (send to WebSocket clients)
- [ ] T161 Add filter_match event broadcasting in filter_service (send to WebSocket clients)
- [ ] T162 Add hot_match event broadcasting for high-priority filters (priority >= 7)
- [ ] T163 Add group_status_change event broadcasting (group becomes unavailable)
- [ ] T164 Implement keepalive ping/pong in websocket_service (30-second interval)

### Frontend - WebSocket Integration

- [ ] T165 [P] Create frontend/src/composables/useWebSocket.ts with WebSocket connection management
- [ ] T166 [P] Add automatic reconnection logic to useWebSocket.ts (exponential backoff)
- [ ] T167 [US1] Integrate useWebSocket in FeedPage.vue (listen for new messages)
- [ ] T168 [US1] Handle filter_match events in feed store (add to feed without refresh)
- [ ] T169 [US1] Handle hot_match events in feed store (show notification toast)
- [ ] T170 [US1] Create HotMatches.vue component with prominent hot match display
- [ ] T171 [US3] Handle group_status_change events in groups store (update status in UI)

**Checkpoint**: Real-time updates functional

---

## Phase 8: Hot Matches & Notifications (Enhancement)

**Goal**: Implement high-priority notifications for critical matches

### Backend - Hot Matches

- [ ] T172 Add is_hot_match boolean to FilterMatch model (based on priority >= 7 and relevance >= 0.7)
- [ ] T173 Create Alembic migration for is_hot_match column
- [ ] T174 Add GET /feed/hot-matches endpoint to api/routes/feed.py (high-priority matches)
- [ ] T175 Create notification record in Notification model when hot match detected
- [ ] T176 Implement Telegram bot notification sending in services/notification_service.py
- [ ] T177 Add notification delivery retry logic (exponential backoff, max 3 retries)

### Frontend - Hot Matches UI

- [ ] T178 Add hot matches section to FeedPage.vue (prominent placement at top)
- [ ] T179 Integrate HotMatches.vue into FeedPage.vue
- [ ] T180 Add browser notifications for hot matches in useNotifications.ts composable
- [ ] T181 Add notification permission request on first load
- [ ] T182 Add hot match badge counter to navigation

**Checkpoint**: Hot matches and notifications complete

---

## Phase 9: Markdown Support & Display (Enhancement)

**Goal**: Properly render and validate Telegram Markdown in messages

### Backend - Markdown Processing

- [ ] T183 Install python-markdown and bleach libraries
- [ ] T184 Create services/markdown_service.py with Telegram MarkdownV2 parser
- [ ] T185 Implement HTML sanitization in markdown_service using bleach (XSS prevention)
- [ ] T186 Add markdown_html column to Message model (store rendered HTML)
- [ ] T187 Create Alembic migration for markdown_html column
- [ ] T188 Integrate markdown_service with message_listener (render on message save)
- [ ] T189 Add markdown validation to markdown_service (catch syntax errors)

### Frontend - Markdown Display

- [ ] T190 Add HTML rendering to MessageCard.vue (v-html with sanitized content)
- [ ] T191 Add Markdown preview to message display
- [ ] T192 Style Markdown elements in MessageCard.vue (code blocks, bold, italic, links)

**Checkpoint**: Markdown support complete

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T193 [P] Add error boundary to App.vue (catch and display errors gracefully)
- [ ] T194 [P] Add loading states to all API calls (spinners, skeleton screens)
- [ ] T195 [P] Add empty states to FeedList, GroupList, FilterList (helpful messages when empty)
- [ ] T196 [P] Add toast notifications for user actions (group added, filter created, etc.)
- [ ] T197 [P] Create frontend/src/components/common/Button.vue with consistent button styles
- [ ] T198 [P] Create frontend/src/components/common/Input.vue with consistent input styles
- [ ] T199 [P] Create frontend/src/components/common/Modal.vue with modal base component
- [ ] T200 [P] Add form validation to all forms (email format, required fields, etc.)
- [ ] T201 [P] Add backend request logging middleware in api/middleware/logging.py
- [ ] T202 [P] Add backend error handling middleware in api/middleware/error_handler.py
- [ ] T203 [P] Add rate limiting to authentication endpoints (10 requests/minute)
- [ ] T204 [P] Create backend logging configuration in config/logging.py
- [ ] T205 [P] Add health check enhancements (database connectivity, Telegram API status)
- [ ] T206 Create docker-compose.yml for local development environment (optional)
- [ ] T207 Add documentation comments to all service methods
- [ ] T208 Create API documentation using FastAPI auto-docs (verify /docs endpoint)
- [ ] T209 Run code formatting on backend (black, isort)
- [ ] T210 Run code formatting on frontend (prettier)
- [ ] T211 Final end-to-end test (complete user journey from registration to viewing filtered messages)
- [ ] T212 [P] Add GET /feed/export endpoint in api/routes/feed.py with CSV and JSON format support (FR-030)
- [ ] T213 [P] Add "Export Feed" button to FeedPage.vue with format selection dropdown (CSV/JSON)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Phase 3): No dependencies on other stories - MVP PRIORITY
  - US2 (Phase 4): Can start after US1 models/services, but independent
  - US3 (Phase 5): Can start after Foundational, independent of US1/US2
  - US4 (Phase 6): Depends on US1-US3 UI components being created
- **WebSocket (Phase 7)**: Depends on US1 backend (feed, filters) being complete
- **Hot Matches (Phase 8)**: Depends on US1 (filters) and US2 (semantic filtering)
- **Markdown (Phase 9)**: Depends on US1 (messages) being complete
- **Polish (Phase 10)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - **MVP PRIORITY**
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses Filter and Message models from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses Group model from US1
- **User Story 4 (P3)**: Depends on US1-US3 having UI components to make responsive

### Within Each User Story

- Backend models before services
- Services before API routes
- API routes before frontend services
- Frontend stores before components
- Components before pages
- Story complete before moving to next priority

### Parallel Opportunities

**Phase 1 - Setup** (all can run in parallel):
- T003, T004, T005, T006, T007, T008, T009

**Phase 2 - Foundational** (some parallel opportunities):
- T015, T016, T017, T018, T019 (all models can be created in parallel)
- T034, T035, T036, T037, T038, T039, T040 (frontend foundation tasks in parallel)

**Phase 3 - US1** (parallel within subsections):
- T042, T043 (schemas and routes can start together)
- T053, T054 (filter schemas and routes)
- T064, T065 (feed schemas and routes)
- T070, T071 (frontend auth pages and services)
- T075, T076, T077, T078 (frontend group types, services, stores, components)
- T082, T083, T084, T085 (frontend filter foundation)
- T089, T090, T091, T092 (frontend feed foundation)

**Phase 4 - US2** (fewer parallel opportunities due to dependencies)

**Phase 6 - US4** (mobile responsive):
- T144, T145, T146, T147 (all responsive layout tasks)

**Phase 10 - Polish** (most can run in parallel):
- T193-T210 (different concerns, different files)

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**MVP Deliverable**: User can register, add groups, create filters, see filtered feed

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add enhancements (WebSocket, Hot Matches, Markdown) as needed
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MVP priority)
   - Developer B: User Story 2 (after US1 models complete, can start filters)
   - Developer C: User Story 3 (independent, can start early)
3. After US1-US3:
   - Developer A: WebSocket (Phase 7)
   - Developer B: Hot Matches (Phase 8)
   - Developer C: Mobile optimization (Phase 6)
4. Team collaborates on Polish (Phase 10)

---

## Notes

- **Database**: SQLite file-based database (default: `backend/telefinder.db`)
- **Migrations**: Alembic optional for SQLite but recommended for schema versioning
- **Commit Strategy**: One task = one commit with format `T###: [description]`
- **[P] tasks**: Different files, no dependencies, can run in parallel
- **[Story] label**: Maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Total tasks: 213 (MVP = ~100 tasks for Phases 1-3)

