---
sidebar_position: 1
title: "Design URL Shortener (TinyURL)"
description: >-
  Complete system design for URL shortener. Requirements, encoding strategies,
  database choice, and scaling to billions of URLs.
keywords:
  - url shortener
  - tinyurl
  - system design
  - base62 encoding
  - short url
difficulty: Intermediate
estimated_time: 45 minutes
prerequisites:
  - Interview Framework
  - Load Balancers
  - Caching
companies: [Google, Amazon, Meta, Microsoft, Twitter]
---

# Design a URL Shortener (TinyURL)

This is the "Hello World" of system design interviews. Simple enough to cover in 45 minutes, complex enough to showcase design skills.

**Goal:** Convert long URLs to short URLs and redirect users.

---

## Phase 1: Requirements (5 minutes)

### Functional Requirements

| Feature | Required |
|---------|----------|
| Shorten URL | Yes |
| Redirect to original URL | Yes |
| Custom short URLs | Nice to have |
| URL expiration | Nice to have |
| Analytics (click count) | Nice to have |

### Non-Functional Requirements

| Aspect | Requirement |
|--------|-------------|
| **Availability** | 99.99% (redirects must work) |
| **Latency** | < 100ms for redirect |
| **Scale** | 100M URLs created/month |
| **Durability** | URLs should never be lost |

### Clarifying Questions

- "Should short URLs expire?" → Let's say optional, default no expiry
- "Can users choose custom URLs?" → Yes, if available
- "Analytics needed?" → Basic click counting

---

## Phase 2: Capacity Estimation (5 minutes)

### Traffic

```
Write (URL creation):
- 100M URLs/month
- 100M / (30 × 24 × 3600) ≈ 40 URLs/second

Read (redirects):
- Assume 100:1 read/write ratio
- 40 × 100 = 4,000 redirects/second
- Peak (2x): 8,000 redirects/second
```

### Storage

```
Per URL record:
- Short URL: 7 chars = 7 bytes
- Long URL: average 100 chars = 100 bytes
- Created at: 8 bytes
- Expiry: 8 bytes
- User ID: 8 bytes
- Total: ~150 bytes

5 years of data:
- 100M × 12 × 5 = 6B URLs
- 6B × 150 bytes = 900 GB ≈ 1 TB
```

### Short URL Length

```
Using base62 (a-z, A-Z, 0-9):
- 6 chars: 62^6 = 56.8 billion combinations
- 7 chars: 62^7 = 3.5 trillion combinations

7 characters is plenty for our scale.
```

---

## Phase 3: High-Level Design (15 minutes)

### API Design

```
POST /api/shorten
Request:  { "long_url": "https://example.com/very/long/path" }
Response: { "short_url": "https://tiny.url/abc1234" }

GET /{short_code}
Response: 301 Redirect to original URL
```

### Architecture

```
┌─────────┐     ┌────────────────┐     ┌─────────────────┐
│ Clients │────▶│ Load Balancer  │────▶│   API Servers   │
└─────────┘     └────────────────┘     └────────┬────────┘
                                                │
                       ┌────────────────────────┼────────────────────────┐
                       │                        │                        │
                       ▼                        ▼                        ▼
                ┌─────────────┐          ┌───────────┐           ┌───────────┐
                │    Cache    │          │  Database │           │    Key    │
                │   (Redis)   │          │ (Primary) │           │ Generator │
                └─────────────┘          └───────────┘           └───────────┘
```

### Flow: Create Short URL

```
1. Client sends long URL
2. API server generates unique short code
3. Store mapping (short_code → long_url) in database
4. Return short URL to client
```

### Flow: Redirect

```
1. Client requests short URL
2. Check cache for mapping
3. If cache miss, query database
4. Return 301 redirect to long URL
5. Optionally increment click count
```

---

## Phase 4: Deep Dive (15 minutes)

### Key Generation Strategy

Three main approaches:

#### Option 1: Counter + Base62

```python
class Counter:
    def __init__(self, start=100000000):
        self.counter = start
    
    def get_next(self):
        self.counter += 1
        return self.counter

def to_base62(num):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = []
    while num > 0:
        result.append(chars[num % 62])
        num //= 62
    return ''.join(reversed(result))

# counter.get_next() = 100000001
# to_base62(100000001) = "6LAze"
```

**Pros:** Sequential, no collisions
**Cons:** Predictable, single point of failure

#### Option 2: Hash + Collision Check

```python
import hashlib

def generate_short_code(long_url):
    hash_value = hashlib.md5(long_url.encode()).hexdigest()
    short_code = to_base62(int(hash_value[:8], 16))[:7]
    return short_code

# Handle collision by appending timestamp or counter
```

**Pros:** Deterministic (same URL = same code)
**Cons:** Collision handling needed

#### Option 3: Pre-generated Keys (Recommended)

```
┌─────────────────────────────────────────────────────┐
│                  Key Generation Service             │
│                                                     │
│   Generate keys in batches (1M at a time)           │
│   Store in two tables: unused_keys, used_keys       │
└─────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│                    API Servers                      │
│                                                     │
│   Each server fetches batch of keys (1000)          │
│   Uses keys from local pool                         │
└─────────────────────────────────────────────────────┘
```

```python
class KeyService:
    def __init__(self):
        self.unused_keys = self.generate_batch()
        self.used_keys = set()
    
    def generate_batch(self, size=1000000):
        # Generate 1M random 7-char base62 strings
        return [random_base62(7) for _ in range(size)]
    
    def get_key(self):
        key = self.unused_keys.pop()
        self.used_keys.add(key)
        return key
```

**Pros:** Fast, no collision check, no single point of failure
**Cons:** Pre-generation overhead, need to handle server failures

### Database Schema

```sql
-- URL mappings
CREATE TABLE urls (
    short_code VARCHAR(7) PRIMARY KEY,
    long_url VARCHAR(2048) NOT NULL,
    user_id BIGINT,
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    click_count BIGINT DEFAULT 0
);

-- Index for user lookups
CREATE INDEX idx_user_id ON urls(user_id);

-- Index for cleanup of expired URLs
CREATE INDEX idx_expires_at ON urls(expires_at);
```

### Database Choice

| Option | Pros | Cons |
|--------|------|------|
| **PostgreSQL** | ACID, familiar, reliable | Scaling writes harder |
| **MySQL** | Same as Postgres | Same |
| **DynamoDB** | Massive scale, fast | Limited queries |
| **Cassandra** | Write-optimized, scale | Eventually consistent |

**Recommendation:** Start with PostgreSQL. Shard later if needed.

### Caching Strategy

```python
def redirect(short_code):
    # 1. Check cache (Redis)
    long_url = cache.get(short_code)
    
    if long_url:
        # Cache hit - increment counter async
        increment_click_async(short_code)
        return redirect_301(long_url)
    
    # 2. Cache miss - query database
    long_url = db.query("SELECT long_url FROM urls WHERE short_code = ?", short_code)
    
    if not long_url:
        return 404
    
    # 3. Populate cache
    cache.set(short_code, long_url, ttl=86400)  # 24 hours
    
    return redirect_301(long_url)
```

**Cache considerations:**
- High hit ratio (same URLs accessed repeatedly)
- TTL of 24 hours balances freshness and hit ratio
- Cache popular URLs longer

### Scaling

```
                    ┌─────────────┐
                    │     DNS     │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │  LB 1  │   │  LB 2  │   │  LB 3  │
         └────────┘   └────────┘   └────────┘
              │            │            │
    ┌─────────┼────────────┼────────────┼─────────┐
    │         │            │            │         │
    ▼         ▼            ▼            ▼         ▼
┌──────┐  ┌──────┐    ┌──────┐    ┌──────┐  ┌──────┐
│ API1 │  │ API2 │    │ API3 │    │ API4 │  │ API5 │
└──────┘  └──────┘    └──────┘    └──────┘  └──────┘
    │         │            │            │         │
    └─────────┴────────────┴────────────┴─────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │Cache 1 │   │Cache 2 │   │Cache 3 │
         └────────┘   └────────┘   └────────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
         ┌────────┐   ┌────────┐   ┌────────┐
         │ DB     │   │ DB     │   │ DB     │
         │Shard 1 │   │Shard 2 │   │Shard 3 │
         └────────┘   └────────┘   └────────┘
```

**Database sharding:** Shard by first character of short_code (62 shards possible).

---

## Phase 5: Wrap Up (5 minutes)

### Trade-offs Made

| Decision | Trade-off |
|----------|-----------|
| Pre-generated keys | Complexity vs. speed |
| PostgreSQL | Familiarity vs. NoSQL scale |
| 301 redirect | Cacheability vs. analytics accuracy |
| 7-char codes | URL length vs. key space |

### Potential Improvements

1. **Analytics service:** Track clicks, geographic data, referrers
2. **Rate limiting:** Prevent abuse
3. **Custom domains:** Allow branded short URLs
4. **Link preview:** Fetch page metadata for sharing
5. **Geo-routing:** Route to nearest data center

### Monitoring

- URL creation rate
- Redirect latency (p50, p99)
- Cache hit ratio
- Database query latency
- Error rates (404s, 5xxs)

---

## Complete Code Reference

```python
# models.py
from datetime import datetime

class URL:
    def __init__(self, short_code, long_url, user_id=None, expires_at=None):
        self.short_code = short_code
        self.long_url = long_url
        self.user_id = user_id
        self.created_at = datetime.now()
        self.expires_at = expires_at
        self.click_count = 0

# service.py
class URLShortener:
    def __init__(self, db, cache, key_service):
        self.db = db
        self.cache = cache
        self.key_service = key_service
    
    def shorten(self, long_url, user_id=None, custom_code=None):
        # Use custom code or generate new one
        short_code = custom_code or self.key_service.get_key()
        
        # Check if custom code is available
        if custom_code and self.db.exists(custom_code):
            raise ValueError("Custom code already taken")
        
        # Store in database
        url = URL(short_code, long_url, user_id)
        self.db.save(url)
        
        # Warm cache
        self.cache.set(short_code, long_url)
        
        return f"https://tiny.url/{short_code}"
    
    def redirect(self, short_code):
        # Check cache
        long_url = self.cache.get(short_code)
        
        if not long_url:
            # Cache miss
            url = self.db.get(short_code)
            if not url:
                return None
            
            # Check expiration
            if url.expires_at and url.expires_at < datetime.now():
                return None
            
            long_url = url.long_url
            self.cache.set(short_code, long_url)
        
        # Async increment
        self.increment_async(short_code)
        
        return long_url
```

---

## Key Takeaways

1. **Pre-generated keys** avoid collision handling complexity.

2. **Cache-heavy architecture** — reads vastly outnumber writes.

3. **301 vs 302:** 301 is cached by browsers, better for SEO; 302 for analytics.

4. **Base62 encoding** gives short, URL-safe codes.

5. **Start simple, scale later.** PostgreSQL handles 40 writes/sec easily.

---

## What's Next?

Design a more complex system:

👉 [Design Twitter →](./twitter)
