---
sidebar_position: 8
title: "Design Instagram — Photo Sharing Platform"
description: >-
  Complete system design for Instagram. Photo upload, feed generation,
  stories, and social graph.
keywords:
  - design instagram
  - photo sharing
  - social media design
  - feed generation
  - image processing
difficulty: Advanced
estimated_time: 45 minutes
prerequisites:
  - Twitter Case Study
  - CDN Concepts
companies: [Meta, Pinterest, Snapchat, TikTok]
---

# Design Instagram: Photos at Scale

Instagram handles 2B+ monthly users sharing photos, stories, and reels. The challenge: fast uploads, engaging feeds, and real-time stories.

---

## Requirements

### Functional
- Upload photos/videos
- Follow users
- News feed (photos from followed users)
- Stories (24-hour ephemeral content)
- Like and comment
- Direct messaging
- Explore/discover

### Non-Functional
- **Availability:** 99.99%
- **Upload latency:** < 5 seconds for photo
- **Feed latency:** < 200ms
- **Scale:** 2B users, 500M daily active

---

## High-Level Architecture

```
┌─────────┐     ┌─────────────────┐     ┌─────────────────────────────────┐
│ Clients │────▶│  Load Balancer  │────▶│         API Gateway             │
└─────────┘     └─────────────────┘     └──────────────┬──────────────────┘
                                                       │
       ┌───────────────────────────────────────────────┼───────────────────────────────────────────────┐
       │                                               │                                               │
       ▼                                               ▼                                               ▼
┌─────────────┐                               ┌─────────────┐                               ┌─────────────┐
│   Upload    │                               │    Feed     │                               │   User      │
│   Service   │                               │   Service   │                               │   Service   │
└──────┬──────┘                               └──────┬──────┘                               └──────┬──────┘
       │                                             │                                             │
       ▼                                             ▼                                             ▼
┌─────────────┐                               ┌─────────────┐                               ┌─────────────┐
│   Media     │                               │    Feed     │                               │   Social    │
│   Processing│                               │    Cache    │                               │   Graph     │
└──────┬──────┘                               └─────────────┘                               └─────────────┘
       │
       ▼
┌─────────────┐
│   CDN       │
│   (Images)  │
└─────────────┘
```

---

## Photo Upload Flow

```
1. Client uploads photo
   │
   ▼
2. Upload Service
   ├── Generate unique ID
   ├── Store original in S3
   └── Queue for processing
   │
   ▼
3. Media Processing Service
   ├── Generate thumbnails (multiple sizes)
   ├── Apply filters (if selected)
   ├── Extract metadata (EXIF)
   ├── Content moderation (ML)
   └── Store processed versions in S3
   │
   ▼
4. CDN Distribution
   │
   ▼
5. Post Service
   ├── Create post record
   ├── Update user's timeline
   └── Fan-out to followers' feeds
   │
   ▼
6. Return success to client
```

### Image Sizes

```
Original: Full resolution (stored but rarely served)
Large: 1080px width (feed view)
Medium: 640px width (grid view)
Small: 320px width (thumbnails)
Tiny: 150px width (profile grid)
```

---

## Feed Generation

### Hybrid Approach (Like Twitter)

```
Regular Users (< 10K followers):
- Fan-out on write
- Push post to followers' feed cache

Celebrities (> 10K followers):
- Fan-out on read
- Pull at feed request time

Feed Assembly:
1. Get pre-computed feed from cache
2. Merge with celebrity posts
3. Rank by relevance (ML model)
4. Return top N posts
```

### Feed Ranking Signals

```
Ranking factors:
- Recency
- Relationship strength (interaction history)
- Content type preference
- Engagement prediction (ML)
- Session context (time of day, device)
```

---

## Stories Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Stories Service                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Upload:                                                         │
│  - Store media in S3 with 24-hour TTL                           │
│  - Create story record in Cassandra                             │
│  - Fan-out story ID to followers' story feed                    │
│                                                                  │
│  View:                                                           │
│  - Fetch story IDs for followed users                           │
│  - Filter expired stories                                        │
│  - Sort by recency                                              │
│  - Return story tray                                            │
│                                                                  │
│  Cleanup:                                                        │
│  - Background job deletes expired media                         │
│  - Cassandra TTL auto-deletes records                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Posts (Cassandra)

```sql
CREATE TABLE posts (
    post_id UUID,
    user_id UUID,
    media_urls LIST<TEXT>,
    caption TEXT,
    location TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY (post_id)
);

-- User's posts (for profile view)
CREATE TABLE user_posts (
    user_id UUID,
    post_id UUID,
    created_at TIMESTAMP,
    PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
```

### Feed Cache (Redis)

```python
# User's feed: sorted set by timestamp
ZADD feed:{user_id} {timestamp} {post_id}

# Keep last 500 posts
ZREMRANGEBYRANK feed:{user_id} 0 -501
```

### Social Graph (PostgreSQL or Graph DB)

```sql
CREATE TABLE follows (
    follower_id BIGINT,
    followee_id BIGINT,
    created_at TIMESTAMP,
    PRIMARY KEY (follower_id, followee_id)
);
```

---

## Explore/Discover

```
Explore Page Generation:
1. Candidate Generation
   - Popular posts from non-followed users
   - Posts liked by followed users
   - Similar content to user's interests

2. Ranking
   - ML model predicts engagement probability
   - Diversity injection (avoid repetitive content)

3. Caching
   - Pre-compute for active users
   - Update periodically (not real-time)
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Image storage | S3 + CDN | Scalable, global |
| Feed storage | Redis | Fast reads |
| Feed strategy | Hybrid push/pull | Handle celebrities |
| Stories TTL | Cassandra TTL | Auto-cleanup |
| Ranking | ML models | Personalization |

---

## Key Takeaways

1. **Hybrid feed generation** handles both regular users and celebrities.
2. **Multiple image sizes** optimize for different views.
3. **Stories use TTL** for automatic expiration.
4. **ML ranking** drives engagement beyond chronological feeds.
5. **CDN is critical** for global image delivery.
