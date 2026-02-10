# WebSocket Event Contracts: TeleFinder

**Feature**: 001-telegram-aggregator
**Date**: 2026-02-09
**Protocol**: WebSocket over HTTP

## Connection

### Endpoint

```
ws://localhost:8000/ws/feed
wss://api.telefinder.app/ws/feed (production)
```

### Authentication

WebSocket connections require JWT authentication via query parameter:

```
ws://localhost:8000/ws/feed?token=<JWT_TOKEN>
```

### Connection Lifecycle

1. **Client connects** with valid JWT token
2. **Server sends** `connection_established` event
3. **Client subscribes** to desired event streams
4. **Server pushes** events as they occur
5. **Client/Server** maintain keepalive ping/pong
6. **Connection closes** on disconnect or auth expiry

### Reconnection Strategy

Client should implement exponential backoff:
- Initial retry: 1 second
- Max retry delay: 30 seconds
- Backoff multiplier: 2x

---

## Server-to-Client Events

Events sent from server to connected clients.

### 1. connection_established

Sent immediately after successful WebSocket connection.

**Event Name**: `connection_established`

**Payload**:
```json
{
  "type": "connection_established",
  "data": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "session_id": "ws_12345abcdef",
    "timestamp": "2026-02-09T14:30:00Z"
  }
}
```

**Frequency**: Once per connection

---

### 2. new_message

New message detected in monitored group (before filtering).

**Event Name**: `new_message`

**Payload**:
```json
{
  "type": "new_message",
  "data": {
    "message_id": "660e8400-e29b-41d4-a716-446655440000",
    "group_id": "770e8400-e29b-41d4-a716-446655440000",
    "group_title": "Python Jobs",
    "text": "Hiring Senior Python Developer - Remote",
    "author_name": "John Recruiter",
    "timestamp": "2026-02-09T14:32:15Z",
    "telegram_link": "https://t.me/python_jobs/12345",
    "has_media": false
  }
}
```

**Frequency**: Real-time as messages arrive

**Note**: This event is informational; not all messages will match filters.

---

### 3. filter_match

Message matched one or more user filters.

**Event Name**: `filter_match`

**Payload**:
```json
{
  "type": "filter_match",
  "data": {
    "message_id": "660e8400-e29b-41d4-a716-446655440000",
    "message": {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "group": {
        "id": "770e8400-e29b-41d4-a716-446655440000",
        "title": "Python Jobs"
      },
      "text": "Hiring Senior Python Developer - Remote",
      "author_name": "John Recruiter",
      "timestamp": "2026-02-09T14:32:15Z",
      "telegram_link": "https://t.me/python_jobs/12345",
      "has_media": false
    },
    "matches": [
      {
        "filter_id": "880e8400-e29b-41d4-a716-446655440000",
        "filter_name": "Python Remote Jobs",
        "match_type": "keyword",
        "relevance_score": 0.85,
        "matched_keywords": ["Python", "Remote"],
        "is_hot_match": false
      }
    ]
  }
}
```

**Frequency**: When message passes filter criteria

**Client Action**: Add message to feed UI, update filter match counters

---

### 4. hot_match

High-priority message matched critical filter (priority >= 7).

**Event Name**: `hot_match`

**Payload**:
```json
{
  "type": "hot_match",
  "data": {
    "message_id": "660e8400-e29b-41d4-a716-446655440000",
    "message": {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "group": {
        "id": "770e8400-e29b-41d4-a716-446655440000",
        "title": "Python Jobs"
      },
      "text": "🔥 Senior Python Backend - $180k - Remote - Apply now!",
      "author_name": "TechRecruiter",
      "timestamp": "2026-02-09T14:35:00Z",
      "telegram_link": "https://t.me/python_jobs/12346",
      "has_media": false
    },
    "matches": [
      {
        "filter_id": "990e8400-e29b-41d4-a716-446655440000",
        "filter_name": "High Priority Python Jobs",
        "match_type": "both",
        "relevance_score": 0.92,
        "matched_keywords": ["Python", "Backend", "Remote"],
        "similarity_score": 0.89,
        "is_hot_match": true
      }
    ],
    "notification_id": "aa0e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Frequency**: When high-priority filter matches

**Client Action**: 
- Display prominent notification (toast/banner)
- Play notification sound
- Add to "Hot Matches" section
- Update badge count

---

### 5. group_status_change

Monitored group status changed (e.g., became unavailable).

**Event Name**: `group_status_change`

**Payload**:
```json
{
  "type": "group_status_change",
  "data": {
    "group_id": "770e8400-e29b-41d4-a716-446655440000",
    "title": "Python Jobs",
    "old_status": "active",
    "new_status": "unavailable",
    "reason": "User lost access to group",
    "timestamp": "2026-02-09T14:40:00Z"
  }
}
```

**Possible Status Values**:
- `active`: Group is being monitored
- `unavailable`: Lost access (user removed, group deleted)
- `error`: Temporary error (will retry)
- `disabled`: User manually disabled monitoring

**Client Action**: Update group status in UI, show warning if unavailable

---

### 6. filter_updated

User's filter was updated (potentially from another device/session).

**Event Name**: `filter_updated`

**Payload**:
```json
{
  "type": "filter_updated",
  "data": {
    "filter_id": "880e8400-e29b-41d4-a716-446655440000",
    "action": "updated",
    "filter": {
      "id": "880e8400-e29b-41d4-a716-446655440000",
      "name": "Python Remote Jobs",
      "keywords": ["Python", "Remote", "Backend"],
      "semantic_enabled": true,
      "priority": 5,
      "is_active": true
    },
    "timestamp": "2026-02-09T14:45:00Z"
  }
}
```

**Action Values**:
- `created`: New filter created
- `updated`: Filter modified
- `deleted`: Filter removed

**Client Action**: Sync filter state across tabs/devices

---

### 7. notification_delivered

Notification was successfully delivered via external channel (Telegram bot).

**Event Name**: `notification_delivered`

**Payload**:
```json
{
  "type": "notification_delivered",
  "data": {
    "notification_id": "aa0e8400-e29b-41d4-a716-446655440000",
    "message_id": "660e8400-e29b-41d4-a716-446655440000",
    "channel": "telegram_bot",
    "status": "sent",
    "delivered_at": "2026-02-09T14:35:05Z"
  }
}
```

**Client Action**: Update notification status, mark as delivered

---

### 8. keepalive_ping

Server sends periodic ping to maintain connection.

**Event Name**: `keepalive_ping`

**Payload**:
```json
{
  "type": "keepalive_ping",
  "data": {
    "timestamp": "2026-02-09T14:50:00Z"
  }
}
```

**Frequency**: Every 30 seconds

**Client Action**: Respond with `keepalive_pong` (see client-to-server events)

---

### 9. error

Server encountered error processing request or event.

**Event Name**: `error`

**Payload**:
```json
{
  "type": "error",
  "data": {
    "code": "FILTER_PROCESSING_ERROR",
    "message": "Failed to process filter match",
    "details": {
      "filter_id": "880e8400-e29b-41d4-a716-446655440000",
      "message_id": "660e8400-e29b-41d4-a716-446655440000"
    },
    "timestamp": "2026-02-09T14:55:00Z"
  }
}
```

**Error Codes**:
- `AUTH_EXPIRED`: JWT token expired (client should reconnect with new token)
- `RATE_LIMIT_EXCEEDED`: Too many requests from client
- `FILTER_PROCESSING_ERROR`: Error applying filter logic
- `INTERNAL_SERVER_ERROR`: Unexpected server error

**Client Action**: Display error to user, log for debugging

---

## Client-to-Server Events

Events sent from client to server (optional, for bidirectional communication).

### 1. subscribe

Subscribe to specific event streams.

**Event Name**: `subscribe`

**Payload**:
```json
{
  "type": "subscribe",
  "data": {
    "streams": ["filter_match", "hot_match", "group_status_change"]
  }
}
```

**Default**: All streams enabled if no subscription specified

---

### 2. keepalive_pong

Client response to server's keepalive_ping.

**Event Name**: `keepalive_pong`

**Payload**:
```json
{
  "type": "keepalive_pong",
  "data": {
    "timestamp": "2026-02-09T14:50:00Z"
  }
}
```

**Frequency**: In response to each `keepalive_ping`

---

### 3. mark_read

Mark message or hot match as read.

**Event Name**: `mark_read`

**Payload**:
```json
{
  "type": "mark_read",
  "data": {
    "message_ids": [
      "660e8400-e29b-41d4-a716-446655440000",
      "770e8400-e29b-41d4-a716-446655440001"
    ],
    "timestamp": "2026-02-09T15:00:00Z"
  }
}
```

**Server Response**: No explicit response (updates read status in database)

---

## Connection Error Handling

### Authentication Errors

If JWT token is invalid or expired, server closes connection with code `4001`:

```json
{
  "code": 4001,
  "reason": "Invalid or expired authentication token"
}
```

**Client Action**: Refresh token and reconnect

---

### Rate Limiting

If client sends too many messages, server sends `error` event:

```json
{
  "type": "error",
  "data": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Maximum 10 messages per minute exceeded",
    "retry_after": 30
  }
}
```

**Limit**: 10 client messages per minute

---

## Implementation Notes

### Backend (FastAPI)

```python
@app.websocket("/ws/feed")
async def websocket_feed(websocket: WebSocket, token: str):
    # Validate JWT
    user = await authenticate_websocket(token)
    
    # Accept connection
    await websocket.accept()
    
    # Send connection_established event
    await websocket.send_json({
        "type": "connection_established",
        "data": {"user_id": str(user.id), ...}
    })
    
    # Subscribe to message stream for this user
    async for event in message_stream(user.id):
        await websocket.send_json(event)
```

### Frontend (Vue 3 Composable)

```typescript
// composables/useWebSocket.ts
import { ref, onMounted, onUnmounted } from 'vue'

export function useWebSocket() {
  const ws = ref<WebSocket | null>(null)
  const messages = ref<any[]>([])
  
  const connect = () => {
    const token = localStorage.getItem('auth_token')
    ws.value = new WebSocket(`ws://localhost:8000/ws/feed?token=${token}`)
    
    ws.value.onmessage = (event) => {
      const data = JSON.parse(event.data)
      handleEvent(data)
    }
  }
  
  const handleEvent = (event: any) => {
    switch (event.type) {
      case 'filter_match':
        messages.value.push(event.data.message)
        break
      case 'hot_match':
        showNotification(event.data)
        break
      // ... handle other events
    }
  }
  
  onMounted(connect)
  onUnmounted(() => ws.value?.close())
  
  return { messages }
}
```

---

## Testing

### Manual Testing with `wscat`

```bash
# Install wscat
npm install -g wscat

# Connect to WebSocket
wscat -c "ws://localhost:8000/ws/feed?token=YOUR_JWT_TOKEN"

# Send keepalive_pong
{"type": "keepalive_pong", "data": {"timestamp": "2026-02-09T15:00:00Z"}}
```

### Automated Testing with `pytest`

```python
@pytest.mark.asyncio
async def test_websocket_filter_match(client, auth_token):
    async with client.websocket_connect(f"/ws/feed?token={auth_token}") as ws:
        # Wait for connection_established
        data = await ws.receive_json()
        assert data["type"] == "connection_established"
        
        # Simulate new message triggering filter
        # ... (inject message into system)
        
        # Expect filter_match event
        data = await ws.receive_json()
        assert data["type"] == "filter_match"
```

---

## Performance Considerations

- **Connection Limit**: 5 concurrent WebSocket connections per user
- **Message Rate**: Server can push up to 100 events/second per connection
- **Keepalive Interval**: 30 seconds (prevents proxy/firewall timeouts)
- **Reconnection**: Client should implement exponential backoff
- **Memory**: Each connection consumes ~50KB server memory

---

## Security

1. **Authentication**: JWT token required in query parameter
2. **Authorization**: Users only receive events for their own data
3. **Rate Limiting**: 10 client messages/minute to prevent abuse
4. **TLS**: Use `wss://` in production (required for browser security)
5. **Token Refresh**: Client should refresh JWT before expiry (typically 1 hour)

---

## Future Enhancements

Potential additions for future versions:

- **Batch Events**: Group multiple `filter_match` events for efficiency
- **Selective Subscriptions**: Client can subscribe to specific groups/filters only
- **Event History**: Replay last N events on reconnection
- **Compression**: Enable WebSocket compression for bandwidth savings
- **Binary Protocol**: Use MessagePack for smaller payloads

