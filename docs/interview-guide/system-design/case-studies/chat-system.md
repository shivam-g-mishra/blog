---
sidebar_position: 13
title: "Design Slack/Teams — Real-Time Chat"
description: >-
  Complete system design for enterprise chat like Slack. Channels, threads,
  presence, and real-time messaging.
keywords:
  - design slack
  - design teams
  - chat system
  - real-time messaging
  - websocket
difficulty: Advanced
estimated_time: 45 minutes
prerequisites:
  - Message Queues
  - WebSockets
companies: [Slack, Microsoft, Discord]
---

# Design Slack: Enterprise Chat at Scale

Slack handles millions of concurrent users sending billions of messages. The challenge: real-time delivery with reliability.

---

## Requirements

### Functional
- 1:1 and group messaging
- Channels (public/private)
- Threads
- File sharing
- Presence (online/offline/away)
- Search
- Notifications

### Non-Functional
- **Latency:** < 100ms message delivery
- **Scale:** Millions of concurrent connections
- **Reliability:** No message loss
- **Ordering:** Messages appear in order

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Clients                                  │
│              (Web, Desktop, Mobile)                             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    WebSocket Gateway                             │
│              (Handles persistent connections)                    │
└──────────────────────────────┬──────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Message   │        │  Presence   │        │  Channel    │
│   Service   │        │   Service   │        │  Service    │
└──────┬──────┘        └──────┬──────┘        └──────┬──────┘
       │                      │                      │
       ▼                      ▼                      ▼
┌─────────────┐        ┌─────────────┐        ┌─────────────┐
│   Kafka     │        │   Redis     │        │  PostgreSQL │
│ (Messages)  │        │ (Presence)  │        │ (Channels)  │
└─────────────┘        └─────────────┘        └─────────────┘
```

---

## WebSocket Connection Management

```
Connection Flow:
1. Client connects to WebSocket gateway
2. Gateway authenticates (JWT)
3. Gateway registers connection in Redis
4. Gateway subscribes to user's channels
5. Messages flow bidirectionally

Connection State:
Redis: user:{user_id}:connections → [conn1, conn2, ...]
Each connection tracks: device, last_seen, subscriptions
```

### Handling Scale

```
Multiple Gateway Servers:
- Each handles ~100K connections
- Stateless (state in Redis)
- Load balanced by user_id hash

Message Routing:
- User's connections may be on different servers
- Use pub/sub to broadcast across servers
```

---

## Message Flow

```
Send Message:
1. Client sends message via WebSocket
2. Gateway forwards to Message Service
3. Message Service:
   - Validates permissions
   - Persists to database
   - Publishes to Kafka
4. Kafka consumers:
   - Update channel's message list
   - Notify relevant users via pub/sub
5. WebSocket gateways receive pub/sub
6. Push message to connected clients
```

### Message Storage

```sql
-- Messages table (partitioned by channel)
CREATE TABLE messages (
    message_id UUID,
    channel_id UUID,
    user_id UUID,
    content TEXT,
    thread_id UUID,  -- NULL if not a reply
    created_at TIMESTAMP,
    edited_at TIMESTAMP,
    PRIMARY KEY (channel_id, message_id)
) PARTITION BY HASH (channel_id);

-- Efficient queries:
-- Get channel messages: WHERE channel_id = X ORDER BY created_at
-- Get thread messages: WHERE thread_id = X ORDER BY created_at
```

---

## Presence System

```
Challenge: Track millions of users' online status

Solution: Heartbeat + Redis

1. Client sends heartbeat every 30s
2. Server updates Redis with TTL
   SET presence:{user_id} {status} EX 60

3. If heartbeat stops, key expires
4. On status change, notify subscribers

Optimization:
- Batch presence updates
- Only notify on state change
- Use Redis pub/sub for real-time
```

---

## Channel Architecture

```
Channel Types:
- Public: Anyone in workspace can join
- Private: Invite only
- DM: 1:1 conversation
- Group DM: Small group, no name

Channel Membership:
┌─────────────────────────────────────────────────────────────────┐
│ channel_members                                                  │
├─────────────────────────────────────────────────────────────────┤
│ channel_id | user_id | role | joined_at | last_read_at         │
└─────────────────────────────────────────────────────────────────┘

Unread Tracking:
- Store last_read_at per user per channel
- Count messages after last_read_at for unread count
```

---

## Search

```
Search Requirements:
- Full-text search across messages
- Filter by channel, user, date
- Handle typos

Implementation:
- Index messages in Elasticsearch
- Include: content, channel, user, timestamp
- Use highlighting for results

Query:
{
  "query": {
    "bool": {
      "must": { "match": { "content": "project update" }},
      "filter": [
        { "term": { "channel_id": "abc123" }},
        { "range": { "timestamp": { "gte": "2024-01-01" }}}
      ]
    }
  }
}
```

---

## File Sharing

```
Upload Flow:
1. Client requests upload URL
2. Server generates pre-signed S3 URL
3. Client uploads directly to S3
4. Client sends message with file reference
5. Server generates thumbnail (if image)

Storage:
- Files in S3
- Metadata in database
- CDN for delivery
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Real-time | WebSocket | Bidirectional, low latency |
| Message queue | Kafka | Ordering, durability |
| Presence | Redis | Fast TTL-based expiry |
| Messages | PostgreSQL + partitioning | Relational, scalable |
| Search | Elasticsearch | Full-text, filtering |

---

## Key Takeaways

1. **WebSocket for real-time** bidirectional communication.
2. **Kafka ensures ordering** and durability for messages.
3. **Redis for ephemeral state** (presence, connections).
4. **Partition by channel** for message storage scaling.
5. **Pub/sub across servers** for multi-server WebSocket.
