---
sidebar_position: 3
title: "Design WhatsApp — Messaging System"
description: >-
  Complete system design for WhatsApp/chat system. Real-time messaging,
  delivery receipts, presence, and group chat.
keywords:
  - design whatsapp
  - chat system design
  - messaging system
  - real-time communication
  - websocket
difficulty: Advanced
estimated_time: 50 minutes
prerequisites:
  - Message Queues
  - Caching
companies: [Meta, WhatsApp, Slack, Discord, Microsoft]
---

# Design WhatsApp: Real-Time Messaging

Chat systems seem simple until you consider: real-time delivery, offline handling, read receipts, group messaging, and end-to-end encryption.

---

## Requirements

### Functional
- One-on-one messaging
- Group messaging (up to 256 members)
- Online/offline status
- Read receipts (delivered, read)
- Media sharing (images, videos)

### Non-Functional
- **Latency:** < 100ms message delivery
- **Scale:** 2B users, 100B messages/day
- **Availability:** 99.99%
- **Ordering:** Messages appear in order

---

## Capacity Estimation

```
Messages:
- 100B messages/day
- 100B / 86,400 ≈ 1.2M messages/second

Storage:
- Average message: 100 bytes
- 100B × 100 bytes = 10 TB/day

Connections:
- 2B users, 500M online at peak
- 500M concurrent WebSocket connections
```

---

## High-Level Design

```
┌─────────┐     ┌────────────────┐     ┌─────────────────┐
│ Clients │◄───►│ Gateway Servers│◄───►│ Chat Service    │
│(WebSocket)    │ (Connection)   │     │ (Business Logic)│
└─────────┘     └────────────────┘     └────────┬────────┘
                                                │
                    ┌───────────────────────────┼───────────────────────────┐
                    │                           │                           │
                    ▼                           ▼                           ▼
             ┌─────────────┐            ┌─────────────┐            ┌─────────────┐
             │ Message DB  │            │ Session     │            │ Push        │
             │ (Cassandra) │            │ (Redis)     │            │ Notification│
             └─────────────┘            └─────────────┘            └─────────────┘
```

---

## Message Flow

### Online User to Online User

```
1. Alice sends message via WebSocket
2. Gateway routes to Chat Service
3. Chat Service:
   - Stores message in DB
   - Looks up Bob's gateway server
   - Forwards to Bob's gateway
4. Bob receives via WebSocket
5. Bob's client sends "delivered" ack
6. Alice receives delivery receipt
```

### Online to Offline User

```
1. Alice sends message
2. Chat Service stores in DB
3. Bob is offline → store in "undelivered" queue
4. Send push notification to Bob
5. When Bob comes online:
   - Fetch undelivered messages
   - Send "delivered" receipts
```

---

## Data Models

### Messages (Cassandra)

```sql
CREATE TABLE messages (
    conversation_id UUID,
    message_id TIMEUUID,
    sender_id UUID,
    content TEXT,
    media_url TEXT,
    status TEXT,  -- sent, delivered, read
    created_at TIMESTAMP,
    PRIMARY KEY (conversation_id, message_id)
) WITH CLUSTERING ORDER BY (message_id DESC);
```

### User Sessions (Redis)

```
user:{user_id}:session → {
    "gateway_server": "gateway-5",
    "device_id": "device-123",
    "last_seen": 1706500000
}
```

---

## WebSocket Connection Management

```python
class GatewayServer:
    def __init__(self):
        self.connections = {}  # user_id → WebSocket
    
    async def on_connect(self, user_id, websocket):
        self.connections[user_id] = websocket
        await redis.set(f"user:{user_id}:gateway", self.server_id)
    
    async def send_to_user(self, user_id, message):
        if user_id in self.connections:
            await self.connections[user_id].send(message)
        else:
            # User on different gateway
            gateway = await redis.get(f"user:{user_id}:gateway")
            await self.forward_to_gateway(gateway, user_id, message)
```

---

## Group Messaging

```
Group message flow:
1. Alice sends to group
2. Chat Service gets group members
3. For each member:
   - Queue message delivery
   - Handle online/offline separately
4. Store single message with group_id
```

### Group Table

```sql
CREATE TABLE groups (
    group_id UUID PRIMARY KEY,
    name TEXT,
    created_by UUID,
    members SET<UUID>,
    created_at TIMESTAMP
);
```

---

## Read Receipts

```
Status flow:
sent → delivered → read

Implementation:
- Client sends ack on receive → "delivered"
- Client sends ack when viewed → "read"
- Batch updates to reduce traffic
```

---

## Presence (Online Status)

```python
# Heartbeat approach
async def heartbeat_loop(user_id):
    while connected:
        await redis.setex(f"online:{user_id}", 30, "1")
        await asyncio.sleep(15)

def is_online(user_id):
    return redis.exists(f"online:{user_id}")
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Protocol | WebSocket | Full duplex, real-time |
| Message DB | Cassandra | Write-heavy, time-series |
| Session store | Redis | Fast lookups |
| Message ordering | TIMEUUID | Guaranteed order |
| Group limit | 256 members | Fan-out manageable |

---

## Key Takeaways

1. **WebSocket for real-time** bidirectional communication.
2. **Gateway servers** manage connections, separate from business logic.
3. **Cassandra** for message storage with conversation partitioning.
4. **Redis** for session management and presence.
5. **Push notifications** for offline users.
