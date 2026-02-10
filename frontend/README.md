# TeleFinder Frontend

Vue.js 3 + TypeScript frontend for TeleFinder Telegram content aggregator.

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Language**: TypeScript (strict mode)
- **State**: Pinia
- **Routing**: Vue Router 4
- **Styling**: Tailwind CSS
- **Build**: Vite
- **HTTP**: Axios
- **Testing**: Vitest + Testing Library

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Ensure backend is running at `http://localhost:8000` or update `API_BASE_URL` in `src/services/api.ts`.

## Running

### Development Server

```bash
npm run dev
```

Access at: http://localhost:5173

### Production Build

```bash
npm run build
npm run preview  # Preview production build
```

## Testing

```bash
npm run test        # Run tests
npm run test:ui     # Tests with UI
```

## Code Quality

```bash
npm run lint        # ESLint
npm run format      # Prettier
```

## Project Structure

```
frontend/
├── src/
│   ├── components/       # Vue components
│   │   ├── feed/        # Feed display components
│   │   ├── filters/     # Filter management
│   │   ├── groups/      # Group management
│   │   └── common/      # Shared components
│   ├── pages/           # Page views
│   │   ├── LoginPage.vue
│   │   ├── FeedPage.vue
│   │   ├── FiltersPage.vue
│   │   ├── GroupsPage.vue
│   │   └── SettingsPage.vue
│   ├── services/        # API clients
│   │   ├── api.ts      # Axios instance
│   │   ├── auth-service.ts
│   │   ├── feed-service.ts
│   │   ├── filter-service.ts
│   │   └── group-service.ts
│   ├── stores/          # Pinia stores
│   │   ├── auth.ts     # Authentication state
│   │   ├── feed.ts     # Feed messages
│   │   ├── filters.ts  # Filters
│   │   └── groups.ts   # Telegram groups
│   ├── types/           # TypeScript types
│   │   ├── user.ts
│   │   ├── message.ts
│   │   ├── filter.ts
│   │   └── group.ts
│   ├── composables/     # Vue composables
│   │   ├── useNotifications.ts
│   │   └── useWebSocket.ts
│   ├── router/          # Vue Router config
│   │   └── index.ts
│   ├── assets/          # Static assets
│   │   └── styles/
│   │       └── tailwind.css
│   ├── App.vue          # Root component
│   └── main.ts          # App entry point
├── tests/
│   ├── unit/            # Unit tests
│   └── e2e/             # E2E tests
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Key Features

### Pages

- **LoginPage**: User registration and login
- **FeedPage**: Unified message feed with hot matches
- **FiltersPage**: Create and manage filters
- **GroupsPage**: Add and manage Telegram groups
- **SettingsPage**: User preferences and notifications

### Components

- **MessageCard**: Individual message display with highlighting
- **FeedList**: Virtualized message list
- **FilterEditor**: Create/edit filters with keywords
- **GroupList**: Display monitored groups with status
- **HotMatches**: Prominent display for high-priority matches

### Stores (Pinia)

- **auth**: User authentication, JWT token management
- **feed**: Message feed state, sorting, filtering
- **filters**: Filter CRUD operations, performance metrics
- **groups**: Group management, status tracking

### Services (API Clients)

- **auth-service**: Register, login, Telegram authentication
- **feed-service**: Fetch messages, hot matches
- **filter-service**: Filter CRUD operations
- **group-service**: Group CRUD operations

### Composables

- **useWebSocket**: WebSocket connection management, real-time updates
- **useNotifications**: Browser notification API integration

## Tailwind Configuration

Configured with mobile-first responsive breakpoints:
- `sm`: 640px
- `md`: 768px
- `lg`: 1024px
- `xl`: 1280px

Custom colors and utilities for TeleFinder branding.

## TypeScript Configuration

Strict mode enabled with:
- `strict`: true
- `noUnusedLocals`: true
- `noUnusedParameters`: true
- `noImplicitReturns`: true

## WebSocket Events

Real-time updates via WebSocket:
- `new_message`: New message detected
- `filter_match`: Message matched filter
- `hot_match`: High-priority match
- `group_status_change`: Group status updated

## State Management Patterns

### Authentication Flow

1. User logs in via `LoginPage`
2. `auth` store calls `auth-service.login()`
3. JWT token stored in localStorage
4. Token added to all API requests via Axios interceptor
5. Router guards redirect unauthenticated users

### Feed Updates

1. User opens `FeedPage`
2. `feed` store loads initial messages
3. WebSocket connection established
4. Real-time updates append to feed
5. User can sort, filter, and refresh

## Development Tips

- Use Vue DevTools for debugging stores and components
- Check browser console for WebSocket events
- Use `/docs` on backend for API testing
- Tailwind classes can be added via DevTools for quick styling
- TypeScript errors appear in IDE and build output

## Troubleshooting

### API Connection Fails
- Ensure backend is running at http://localhost:8000
- Check CORS configuration in backend

### WebSocket Connection Fails
- Verify JWT token is valid
- Check WebSocket URL in `useWebSocket.ts`
- Ensure backend WebSocket endpoint is working

### Build Errors
```bash
npm install  # Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

---

For full documentation, see `/specs/001-telegram-aggregator/`

