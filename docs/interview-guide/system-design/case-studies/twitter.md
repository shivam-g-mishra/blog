---
sidebar_position: 2
title: "Design Twitter — Social Network at Scale"
description: >-
  Complete system design for Twitter. Timeline generation, fan-out strategies,
  celebrity problem, and real-time notifications.
keywords:
  - design twitter
  - social network design
  - timeline
  - fan-out
  - news feed
  - system design
difficulty: Advanced
estimated_time: 60 minutes
prerequisites:
  - URL Shortener Case Study
  - Caching
  - Message Queues
  - SQL vs NoSQL
companies: [Twitter, Meta, Google, Amazon, Microsoft]
---

# Design Twitter: The Timeline Challenge

Twitter seems simple: 280 characters, click tweet. But beneath that simplicity lies one of the most challenging distributed systems problems.

**The core challenge:** When Lady Gaga (80M followers) tweets, how do 80 million timelines update instantly?

---

## Phase 1: Requirements (5 minutes)

### Functional Requirements

| Feature | Priority |
|---------|----------|
| Post tweets (280 chars, images) | Must have |
| Follow/unfollow users | Must have |
| Home timeline (tweets from followed users) | Must have |
| User timeline (user's own tweets) | Must have |
| Search tweets | Nice to have |
| Notifications | Nice to have |
| Trending topics | Nice to have |

### Non-Functional Requirements

| Aspect | Requirement |
|--------|-------------|
| **Scale** | 500M users, 200M DAU |
| **Timeline latency** | < 200ms |
| **Availability** | 99.99% |
| **Consistency** | Eventual (seconds) |

### Clarifying Questions

- "Real-time or near-real-time?" → Near-real-time (seconds OK)
- "Media support?" → Images and videos
- "Celebrity users special handling?" → Yes, discuss later

---

## Phase 2: Capacity Estimation (5 minutes)

### Traffic

```
Users: 500M total, 200M DAU
Average follows: 200 users
Average followers: 200 users

Tweets per day:
- 200M DAU × 2 tweets/day = 400M tweets/day
- 400M / 86,400 = ~4,600 tweets/second
- Peak (2x): ~10,000 tweets/second

Timeline reads:
- 200M DAU × 10 views/day = 2B reads/day
- 2B / 86,400 = ~23,000 reads/second
- Peak: ~50,000 reads/second

Read:Write ratio = 50,000:10,000 = 5:1
```

### Storage

```
Tweet storage:
- Tweet text: 280 bytes
- Metadata: 100 bytes
- Total: ~400 bytes/tweet

Daily: 400M × 400 bytes = 160 GB/day
Yearly: 160 GB × 365 = ~60 TB/year

Media storage:
- 10% of tweets have images
- Average image: 1 MB
- 40M images × 1 MB = 40 TB/day
```

---

## Phase 3: High-Level Design (15 minutes)

### API Design

```
POST /tweets
Request: {
  "user_id": "123",
  "content": "Hello world!",
  "media_ids": ["img_1"]
}
Response: { "tweet_id": "abc123", "created_at": "..." }

GET /timeline/home/{user_id}
Response: {
  "tweets": [...],
  "cursor": "next_page_token"
}

GET /timeline/user/{user_id}
Response: { "tweets": [...] }

POST /follow
Request: { "follower_id": "123", "followee_id": "456" }

GET /search?q=keyword
Response: { "tweets": [...] }
```

### Architecture Overview

```
┌─────────┐     ┌────────────────┐     ┌──────────────────┐
│ Clients │────▶│ Load Balancer  │────▶│   API Gateway    │
└─────────┘     └────────────────┘     └────────┬─────────┘
                                                │
         ┌──────────────────────────────────────┼──────────────────────────────────────┐
         │                                      │                                      │
         ▼                                      ▼                                      ▼
┌─────────────────┐                   ┌─────────────────┐                    ┌─────────────────┐
│  Tweet Service  │                   │Timeline Service │                    │  User Service   │
└────────┬────────┘                   └────────┬────────┘                    └────────┬────────┘
         │                                     │                                      │
         ▼                                     ▼                                      ▼
┌─────────────────┐                   ┌─────────────────┐                    ┌─────────────────┐
│   Tweet DB      │                   │  Timeline Cache │                    │    User DB      │
│  (Cassandra)    │                   │    (Redis)      │                    │  (PostgreSQL)   │
└─────────────────┘                   └─────────────────┘                    └─────────────────┘
         │
         ▼
┌─────────────────┐
│  Message Queue  │──────▶ Fan-out Service
│    (Kafka)      │
└─────────────────┘
```

---

## Phase 4: Deep Dive (15 minutes)

### The Timeline Problem

**How do you generate a user's home timeline?**

Two approaches:

### Approach 1: Fan-out on Write (Push)

When user tweets, push to all followers' timelines.

```
User A tweets
    │
    ▼
┌─────────────────────────────────────────────────┐
│           Fan-out Service                       │
│                                                 │
│   Get followers of A: [B, C, D, ...]           │
│   For each follower:                           │
│       Prepend tweet to their timeline cache    │
│                                                 │
└─────────────────────────────────────────────────┘
    │
    ├──▶ Redis: timeline:B → [new_tweet, ...]
    ├──▶ Redis: timeline:C → [new_tweet, ...]
    └──▶ Redis: timeline:D → [new_tweet, ...]
```

**Pros:**
- Timeline reads are fast (pre-computed)
- Simple read path

**Cons:**
- Celebrity problem: 80M writes per tweet
- Wasted work for inactive users
- Slower write path

### Approach 2: Fan-out on Read (Pull)

When user requests timeline, fetch from followed users.

```
User B requests timeline
    │
    ▼
┌─────────────────────────────────────────────────┐
│           Timeline Service                      │
│                                                 │
│   Get users B follows: [A, X, Y, ...]          │
│   For each followed user:                      │
│       Fetch recent tweets                      │
│   Merge and sort by time                       │
│   Return top N                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Pros:**
- No celebrity problem
- No wasted work

**Cons:**
- Slow reads (N queries + merge)
- High read latency

### Hybrid Approach (Twitter's Solution)

```
┌─────────────────────────────────────────────────────────────┐
│                    Hybrid Fan-out                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Regular users (< 10K followers):                           │
│  └── Fan-out on write (push to followers)                   │
│                                                             │
│  Celebrities (> 10K followers):                             │
│  └── Don't fan-out                                          │
│  └── Merge at read time                                     │
│                                                             │
│  Timeline read:                                             │
│  1. Fetch pre-computed timeline (Redis)                     │
│  2. Fetch recent tweets from followed celebrities           │
│  3. Merge and return                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Data Models

**Tweet Storage (Cassandra)**

```sql
-- Tweets table (write-optimized)
CREATE TABLE tweets (
    tweet_id UUID,
    user_id UUID,
    content TEXT,
    media_urls LIST<TEXT>,
    created_at TIMESTAMP,
    PRIMARY KEY (tweet_id)
);

-- User timeline (for user's own tweets)
CREATE TABLE user_timeline (
    user_id UUID,
    tweet_id UUID,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

**Timeline Cache (Redis)**

```python
# Home timeline: sorted set by timestamp
ZADD timeline:{user_id} {timestamp} {tweet_id}

# Limit to last 800 tweets
ZREMRANGEBYRANK timeline:{user_id} 0 -801

# Fetch timeline
ZREVRANGE timeline:{user_id} 0 100
```

**Social Graph (PostgreSQL or Graph DB)**

```sql
CREATE TABLE follows (
    follower_id BIGINT,
    followee_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);

CREATE INDEX idx_followee ON follows(followee_id);
```

### Tweet Flow

```
1. User creates tweet
   │
   ▼
2. Tweet Service
   ├── Validate content
   ├── Store in Tweet DB
   └── Publish to Kafka
         │
         ▼
3. Fan-out Service (async)
   ├── Check if user is celebrity (>10K followers)
   │   ├── Yes: Skip fan-out
   │   └── No: Continue
   │
   ├── Get follower list
   └── For each active follower:
       └── ZADD to Redis timeline
         │
         ▼
4. Notification Service (async)
   └── Push notifications to mentioned users
```

### Timeline Read Flow

```
1. User requests home timeline
   │
   ▼
2. Timeline Service
   ├── Fetch pre-computed timeline from Redis
   │   └── ZREVRANGE timeline:{user_id} 0 100
   │
   ├── Get list of celebrities user follows
   │
   ├── Fetch recent tweets from each celebrity
   │   └── Query Tweet DB or cache
   │
   ├── Merge all tweets by timestamp
   │
   └── Return top N tweets with pagination
```

### Search

```
┌─────────────────────────────────────────────────────────────┐
│                    Search Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Tweet Created                                              │
│       │                                                     │
│       ▼                                                     │
│  Kafka ──▶ Search Indexer ──▶ Elasticsearch                │
│                                                             │
│  Search Query                                               │
│       │                                                     │
│       ▼                                                     │
│  API ──▶ Elasticsearch ──▶ Tweet IDs ──▶ Tweet DB          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Phase 5: Scaling & Reliability

### Scaling Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    Global Architecture                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                        DNS                                  │
│                         │                                   │
│         ┌───────────────┼───────────────┐                  │
│         │               │               │                  │
│         ▼               ▼               ▼                  │
│    ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│    │  US-West │    │ US-East │    │  Europe  │             │
│    │  Region  │    │  Region │    │  Region  │             │
│    └─────────┘    └─────────┘    └─────────┘             │
│         │               │               │                  │
│    Cassandra       Cassandra       Cassandra              │
│    (replicated)    (replicated)    (replicated)           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Database Sharding

```
Tweet DB: Shard by tweet_id (consistent hashing)
Timeline Cache: Shard by user_id
Social Graph: Shard by user_id
```

### Handling Failures

| Component | Failure Strategy |
|-----------|-----------------|
| Tweet Service | Retry queue, idempotency |
| Timeline Cache | Fallback to DB, rebuild |
| Fan-out Service | Kafka replay, at-least-once |
| Search | Graceful degradation |

---

## Summary

### Key Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Timeline strategy | Hybrid fan-out | Balance celebrity problem |
| Tweet storage | Cassandra | Write throughput |
| Timeline cache | Redis | Fast reads, sorted sets |
| Social graph | PostgreSQL | Relationship queries |
| Async processing | Kafka | Decouple, replay |

### Trade-offs

| Trade-off | Our Choice |
|-----------|------------|
| Consistency vs Latency | Eventual consistency (seconds) |
| Storage vs Compute | Pre-compute timelines (more storage) |
| Complexity vs Performance | Hybrid approach (more complex) |

---

## Key Takeaways

1. **Fan-out on write for regular users**, fan-out on read for celebrities.

2. **Timeline cache in Redis** with sorted sets for O(log N) inserts.

3. **Cassandra for tweets** — write-optimized, time-series friendly.

4. **Async processing via Kafka** for fan-out and notifications.

5. **The celebrity problem** is the key challenge to discuss.

---

## What's Next?

Design a chat system with real-time messaging:

👉 [Design WhatsApp →](./whatsapp)
