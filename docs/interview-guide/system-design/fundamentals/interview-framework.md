---
sidebar_position: 2
title: "System Design Interview Framework"
description: >-
  A step-by-step framework for approaching any system design interview.
  Requirements, estimation, design, and deep dive phases explained.
keywords:
  - system design framework
  - system design approach
  - interview structure
  - requirements gathering
  - capacity estimation
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Meta, Amazon, Microsoft, Netflix, Uber]
---

# The System Design Interview Framework

A 45-minute system design interview is a structured conversation. Without a framework, you'll ramble. With one, you'll demonstrate exactly the skills interviewers look for.

**This framework works for any system design problem.**

---

## Phase 1: Requirements Clarification (5 minutes)

**Never start designing without understanding the problem.**

### Functional Requirements

What should the system do?

```
Example: Design Twitter

Ask:
- Can users post tweets? (Yes)
- Can users follow other users? (Yes)
- Is there a feed showing tweets from followed users? (Yes)
- Can users like/retweet? (Keep it simple, focus on core)
- Is there direct messaging? (Out of scope)
- Is there search? (Out of scope for now)

Confirm:
"So the core features are: post tweets, follow users, view timeline.
Is that correct?"
```

### Non-Functional Requirements

How should it behave?

| Aspect | Questions to Ask |
|--------|------------------|
| **Scale** | How many users? How many DAU? |
| **Availability** | What's acceptable downtime? |
| **Latency** | Expected response time? |
| **Consistency** | Strong or eventual? |
| **Data retention** | How long to keep data? |

```
Example questions:
- "How many daily active users?"
- "What's more important: consistency or availability?"
- "What latency is acceptable for the feed?"
- "Should this work globally or single region?"
```

---

## Phase 2: Capacity Estimation (5 minutes)

**Back-of-envelope math to understand scale.**

### The Numbers to Calculate

1. **QPS (Queries Per Second)**
2. **Storage requirements**
3. **Bandwidth**

### Example: Twitter Estimation

```
Given:
- 500M DAU
- Each user views feed 5 times/day
- Each user tweets 2 times/day

Read QPS:
500M × 5 / 86,400 ≈ 30,000 QPS
Peak (2x): 60,000 QPS

Write QPS:
500M × 2 / 86,400 ≈ 12,000 QPS
Peak: 24,000 QPS

Storage (tweets):
- 500M users × 2 tweets/day = 1B tweets/day
- Average tweet: 300 bytes (text + metadata)
- Daily: 1B × 300 bytes = 300 GB/day
- Yearly: 300 GB × 365 = ~100 TB/year
```

### Quick Reference Numbers

| Metric | Value |
|--------|-------|
| Seconds in a day | 86,400 ≈ 100,000 |
| Seconds in a year | ~30 million |
| 1 million seconds | ~12 days |
| 1 byte | 8 bits |
| 1 KB | 1,000 bytes |
| 1 MB | 1,000 KB |
| 1 GB | 1,000 MB |
| 1 TB | 1,000 GB |

---

## Phase 3: High-Level Design (15 minutes)

**Draw the main components and data flow.**

### Step 1: Identify Core Components

```
Twitter example:
- Client (web/mobile)
- Load balancer
- API servers
- Tweet service
- Timeline service
- User service
- Database(s)
- Cache
- Message queue (for async)
```

### Step 2: Draw the Architecture

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐
│ Clients │────▶│ Load Balancer│────▶│ API Gateway │
└─────────┘     └──────────────┘     └──────┬──────┘
                                            │
          ┌─────────────────────────────────┼─────────────────────────────────┐
          │                                 │                                 │
          ▼                                 ▼                                 ▼
    ┌──────────┐                    ┌──────────────┐                  ┌──────────┐
    │ Tweet    │                    │  Timeline    │                  │  User    │
    │ Service  │                    │  Service     │                  │ Service  │
    └────┬─────┘                    └──────┬───────┘                  └────┬─────┘
         │                                 │                               │
         ▼                                 ▼                               ▼
    ┌──────────┐                    ┌──────────────┐                  ┌──────────┐
    │ Tweet DB │                    │    Cache     │                  │ User DB  │
    └──────────┘                    └──────────────┘                  └──────────┘
```

### Step 3: Define APIs

```
POST /tweets
  Request: { user_id, content }
  Response: { tweet_id, timestamp }

GET /timeline/{user_id}
  Response: { tweets: [...] }

POST /follow
  Request: { follower_id, followee_id }
```

### Step 4: Discuss Data Flow

Walk through a user action:

```
"When a user posts a tweet:
1. Request hits load balancer
2. Routed to API server
3. Tweet service validates and stores in Tweet DB
4. Async message sent to update followers' timelines
5. Timeline service updates cache for each follower"
```

---

## Phase 4: Deep Dive (15 minutes)

**Go deep on 2-3 components or challenges.**

### What Interviewers Want to See

| Area | Questions |
|------|-----------|
| **Database design** | Schema, indexing, sharding strategy |
| **Caching** | What to cache, invalidation, consistency |
| **Scaling** | How to handle 10x traffic |
| **Failure handling** | What if this component fails? |
| **Trade-offs** | Why this choice over alternatives? |

### Example Deep Dives

**Timeline generation:**
```
Two approaches:

1. Fan-out on write (push model)
   - When user tweets, push to all followers' timelines
   - Pro: Fast reads
   - Con: Expensive for celebrities (millions of followers)

2. Fan-out on read (pull model)
   - When user views timeline, fetch from followed users
   - Pro: Efficient writes
   - Con: Slow reads, needs caching

Hybrid approach:
- Push for regular users
- Pull for celebrities
- Cache hot timelines
```

**Database choice:**
```
"For tweets, I'd use a NoSQL database like Cassandra:
- Write-heavy workload
- Time-series data (recent tweets matter most)
- Need horizontal scaling
- Eventual consistency is acceptable

For user data and follow relationships:
- Use PostgreSQL for ACID properties
- Follow graph could use graph database for complex queries"
```

---

## Phase 5: Wrap Up (5 minutes)

### Summarize Trade-offs

```
"To summarize the trade-offs:
- We chose push model for timeline, optimizing for read latency
- We accepted eventual consistency for better availability
- Caching reduces database load but adds complexity"
```

### Discuss Improvements

```
"Given more time, I'd add:
- Search functionality with Elasticsearch
- Analytics pipeline for trending topics
- Better spam detection
- Multi-region deployment"
```

### Answer Questions

Be prepared for:
- "What if X fails?"
- "How would you handle Y edge case?"
- "What metrics would you monitor?"

---

## Framework Checklist

```
□ REQUIREMENTS (5 min)
  □ Clarify functional requirements
  □ Clarify non-functional requirements
  □ Define scope

□ ESTIMATION (5 min)
  □ Calculate QPS (read/write)
  □ Calculate storage
  □ Calculate bandwidth

□ HIGH-LEVEL DESIGN (15 min)
  □ Draw main components
  □ Show data flow
  □ Define APIs
  □ Choose databases

□ DEEP DIVE (15 min)
  □ Database design
  □ Caching strategy
  □ Handle scale
  □ Failure scenarios
  □ Discuss trade-offs

□ WRAP UP (5 min)
  □ Summarize approach
  □ Discuss improvements
  □ Answer questions
```

---

## Key Takeaways

1. **Always start with requirements.** 5 minutes here saves 15 minutes later.

2. **Do the math.** Numbers drive design decisions.

3. **Draw as you talk.** Visuals help communication.

4. **Discuss trade-offs.** There's no single right answer.

5. **Be interactive.** Check in with the interviewer.

---

## What's Next?

Learn to estimate capacity accurately:

👉 [Capacity Estimation →](./capacity-estimation)
