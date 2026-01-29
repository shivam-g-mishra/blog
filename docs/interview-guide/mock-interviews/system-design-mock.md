---
sidebar_position: 3
title: "System Design Interview Mock"
description: >-
  Complete system design mock interview. Practice a 45-minute design session
  with evaluation criteria.
keywords:
  - system design mock
  - practice interview
  - design interview
difficulty: Advanced
estimated_time: 45 minutes
prerequisites:
  - System Design Framework
  - Building Blocks
companies: [All Companies]
---

# System Design Interview Mock

Practice a realistic 45-minute system design interview. Set a timer.

---

## Format

```
0:00 - 0:05  Requirements clarification
0:05 - 0:10  High-level design
0:10 - 0:30  Deep dive into components
0:30 - 0:40  Scaling and trade-offs
0:40 - 0:45  Summary and questions
```

---

## Problem: Design a News Feed System

Design a social media news feed like Facebook or Twitter.

---

## Phase 1: Requirements (5 min)

### Questions to Ask

Before designing, clarify:

1. **Functional:** What actions can users perform?
2. **Scale:** How many users? How many posts per day?
3. **Features:** Just text? Images? Videos?
4. **Access patterns:** How often do users check feed?

### Sample Requirements

```
Functional:
- Users can post updates
- Users can follow other users
- Users see feed of posts from people they follow
- Feed is sorted by recency (or relevance)

Non-Functional:
- 500M DAU
- Users check feed ~10 times/day
- Average user follows 200 people
- Feed load time < 500ms
- Posts appear in feed within seconds
```

### Quick Math

```
Read requests: 500M × 10 = 5B reads/day ≈ 60K reads/sec
Write requests: Assume 1% post daily = 5M writes/day ≈ 60 writes/sec

Read-heavy system (1000:1 ratio)
```

---

## Phase 2: High-Level Design (5 min)

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Client  │────▶│ Load Balancer│────▶│  API Gateway │
└──────────┘     └──────────────┘     └──────────────┘
                                             │
                    ┌────────────────────────┼───────────────────────┐
                    │                        │                       │
                    ▼                        ▼                       ▼
            ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
            │ Post Service │       │ Feed Service │       │ User Service │
            └──────────────┘       └──────────────┘       └──────────────┘
                    │                        │                       │
                    ▼                        ▼                       ▼
            ┌──────────────┐       ┌──────────────┐       ┌──────────────┐
            │   Posts DB   │       │  Feed Cache  │       │   Users DB   │
            └──────────────┘       └──────────────┘       └──────────────┘
```

---

## Phase 3: Deep Dive (20 min)

### Feed Generation: Push vs Pull

**Option 1: Pull (Fan-out on read)**

```
When user opens feed:
1. Get list of people they follow
2. Fetch recent posts from each
3. Merge and sort
4. Return top N

Pros: Simple, no storage for feeds
Cons: Slow for users following many people
```

**Option 2: Push (Fan-out on write)**

```
When user posts:
1. Get list of their followers
2. Push post to each follower's feed cache

Pros: Fast read (feed is pre-computed)
Cons: Expensive for users with millions of followers
```

**Option 3: Hybrid (Best)**

```
For regular users: Push (fan-out on write)
For celebrities (>10K followers): Pull at read time

Why: Avoids writing to millions of feeds for celebrities
```

### Data Storage

```
Users Table:
- user_id (PK)
- name, email, created_at

Posts Table:
- post_id (PK)
- user_id (FK)
- content, media_url
- created_at

Followers Table:
- follower_id, followee_id (composite PK)
- created_at

Feed Cache (Redis):
- Key: user_id
- Value: List of (post_id, timestamp), capped at 1000
```

### Feed Service Flow

```python
def get_feed(user_id, page=1, page_size=20):
    # 1. Get pre-computed feed from cache
    feed_ids = cache.get(f"feed:{user_id}")
    
    # 2. Handle celebrities (pull model)
    celebrity_followees = get_celebrity_followees(user_id)
    for celeb_id in celebrity_followees:
        recent_posts = get_recent_posts(celeb_id)
        feed_ids.extend(recent_posts)
    
    # 3. Sort by timestamp and paginate
    feed_ids.sort(key=lambda x: x.timestamp, reverse=True)
    page_ids = feed_ids[(page-1)*page_size : page*page_size]
    
    # 4. Hydrate with full post data
    posts = get_posts_by_ids(page_ids)
    
    return posts
```

### Post Creation Flow

```python
def create_post(user_id, content):
    # 1. Save to database
    post = Post.create(user_id=user_id, content=content)
    
    # 2. Send to message queue for fan-out
    queue.publish("new_post", {
        "post_id": post.id,
        "user_id": user_id
    })
    
    return post

# Worker process
def fan_out_worker(message):
    post_id = message["post_id"]
    user_id = message["user_id"]
    
    followers = get_followers(user_id)
    
    for follower_id in followers:
        # Add to follower's feed cache
        cache.lpush(f"feed:{follower_id}", post_id)
        cache.ltrim(f"feed:{follower_id}", 0, 999)  # Keep last 1000
```

---

## Phase 4: Scaling & Trade-offs (10 min)

### Database Scaling

```
Posts: Shard by user_id
- All posts from same user on same shard
- Good for fan-out (single query per followee)

Feed Cache: Shard by user_id
- Each user's feed on one Redis node
- Use consistent hashing
```

### Handling Hot Spots

```
Celebrity posts:
- Don't fan out to millions
- Pull at read time + aggressive caching
- CDN for media content
```

### Reliability

```
- Message queue for async fan-out (retry on failure)
- Circuit breaker for celebrity checks
- Fallback to pull if cache miss
- Multi-region replication for availability
```

---

## Evaluation Rubric

| Category | Excellent | Good | Needs Work |
|----------|-----------|------|------------|
| **Requirements** | Clarified scale, features, constraints | Some clarification | Jumped to design |
| **High-Level** | Clean, complete architecture | Mostly complete | Missing components |
| **Deep Dive** | Explained trade-offs, made decisions | Covered basics | Surface level |
| **Scaling** | Addressed bottlenecks, hot spots | Some scaling discussion | Ignored scaling |
| **Communication** | Clear, structured, drove discussion | Decent communication | Disorganized |

---

## Common Follow-Up Questions

1. **How would you implement "like" counts on posts?**
2. **How would you add relevance-based ranking?**
3. **How would you handle spam/abuse?**
4. **What happens if Redis goes down?**
5. **How would you support real-time updates?**

---

## Key Takeaways

1. **Always clarify requirements** before designing.
2. **Start high-level**, then dive deep.
3. **Discuss trade-offs** for every decision.
4. **Address scaling** proactively.
5. **Use numbers** to justify choices.
