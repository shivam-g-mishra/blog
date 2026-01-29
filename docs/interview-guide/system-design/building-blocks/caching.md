---
sidebar_position: 2
title: "Caching — Speed Up Everything"
description: >-
  Master caching for system design interviews. Cache strategies, invalidation
  patterns, Redis vs Memcached, and distributed caching.
keywords:
  - caching
  - cache invalidation
  - redis
  - memcached
  - cache aside
  - write through
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Amazon, Meta, Netflix, Twitter]
---

# Caching: The Performance Multiplier

There's an old saying in computer science:

> "There are only two hard things: cache invalidation and naming things."

Caching is simple in concept. A database query takes 100ms. Store the result, and subsequent requests take 1ms. 100x improvement.

**The hard part is keeping the cache consistent with the source of truth.**

---

## Why Cache?

```
Without Cache:
Client → Server → Database (100ms)
Client → Server → Database (100ms)
Client → Server → Database (100ms)

With Cache:
Client → Server → Cache HIT (1ms)
Client → Server → Cache HIT (1ms)
Client → Server → Cache MISS → Database → Update Cache (100ms)
Client → Server → Cache HIT (1ms)
```

### Cache Hit Ratio

```
Hit Ratio = Cache Hits / (Cache Hits + Cache Misses)

If 95% hit ratio:
  Average latency = 0.95 × 1ms + 0.05 × 100ms = 5.95ms
  
vs 100ms without cache = 17x improvement
```

---

## Caching Patterns

### 1. Cache-Aside (Lazy Loading)

Application manages cache. Most common pattern.

```python
def get_user(user_id):
    # 1. Check cache
    user = cache.get(f"user:{user_id}")
    if user:
        return user
    
    # 2. Cache miss - fetch from DB
    user = db.query(f"SELECT * FROM users WHERE id = {user_id}")
    
    # 3. Populate cache
    cache.set(f"user:{user_id}", user, ttl=3600)
    
    return user
```

```
┌────────┐     ┌───────┐     ┌──────────┐
│ Client │────▶│ Cache │     │ Database │
└────────┘     └───┬───┘     └────┬─────┘
                   │              │
              1. Check       2. On miss,
                 cache          fetch
                   │              │
                   └──────────────┘
                   3. Populate cache
```

**Pros:** Simple, cache only what's needed
**Cons:** Cache miss = slow, potential stale data

### 2. Read-Through

Cache handles fetching from database.

```
┌────────┐     ┌───────────────────────────┐     ┌──────────┐
│ Client │────▶│ Cache (fetches on miss)   │────▶│ Database │
└────────┘     └───────────────────────────┘     └──────────┘
```

**Pros:** Simpler application code
**Cons:** Initial request always slow

### 3. Write-Through

Write to cache and database synchronously.

```python
def update_user(user_id, data):
    # Write to both
    db.update(f"UPDATE users SET ... WHERE id = {user_id}")
    cache.set(f"user:{user_id}", data)
```

**Pros:** Cache always consistent
**Cons:** Higher write latency

### 4. Write-Behind (Write-Back)

Write to cache immediately, async write to database.

```
┌────────┐     ┌───────┐     ┌──────────┐
│ Client │────▶│ Cache │ ···▶│ Database │
└────────┘     └───────┘     └──────────┘
              (immediate)    (async batch)
```

**Pros:** Fast writes, batching efficiency
**Cons:** Risk of data loss if cache fails

---

## Cache Invalidation Strategies

### 1. Time-To-Live (TTL)

Data expires after fixed time.

```python
cache.set("user:123", user_data, ttl=3600)  # Expires in 1 hour
```

**Use when:** Staleness is acceptable, simple to implement.

### 2. Event-Driven Invalidation

Invalidate when data changes.

```python
def update_user(user_id, data):
    db.update(...)
    cache.delete(f"user:{user_id}")  # Invalidate
```

**Use when:** Consistency is critical.

### 3. Versioning

Include version in cache key.

```python
cache.set(f"user:{user_id}:v{version}", data)
```

**Use when:** Need atomic updates across related data.

---

## Cache Eviction Policies

When cache is full, which items to remove?

| Policy | Description | Use Case |
|--------|-------------|----------|
| **LRU** | Least Recently Used | General purpose |
| **LFU** | Least Frequently Used | When popularity matters |
| **FIFO** | First In First Out | Simple, time-based |
| **Random** | Random eviction | Very simple, decent results |
| **TTL** | Based on expiration | Time-sensitive data |

### LRU Implementation

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity
    
    def get(self, key):
        if key not in self.cache:
            return None
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Remove least recently used
            self.cache.popitem(last=False)
```

---

## Redis vs Memcached

| Feature | Redis | Memcached |
|---------|-------|-----------|
| **Data Structures** | Strings, Lists, Sets, Hashes, Sorted Sets | Strings only |
| **Persistence** | Yes (RDB, AOF) | No |
| **Replication** | Yes | No |
| **Clustering** | Yes (Redis Cluster) | Client-side |
| **Memory Efficiency** | Less efficient | More efficient |
| **Pub/Sub** | Yes | No |
| **Lua Scripting** | Yes | No |

### When to Use Which

**Choose Redis when:**
- Need complex data structures
- Need persistence
- Need pub/sub
- Need atomic operations

**Choose Memcached when:**
- Simple key-value caching
- Maximum memory efficiency
- Simpler operations

---

## Distributed Caching

### Consistent Hashing

Distribute keys across cache nodes with minimal redistribution.

```
Hash Ring:
       Node A
          │
   ┌──────┴──────┐
   │             │
Node D        Node B
   │             │
   └──────┬──────┘
          │
       Node C

key "user:123" → hash → nearest node clockwise
```

**Adding a node:** Only keys between new node and predecessor move.

### Cache Stampede Prevention

When cache expires, all requests hit database simultaneously.

**Solution 1: Locking**
```python
def get_with_lock(key):
    value = cache.get(key)
    if value:
        return value
    
    lock = cache.lock(f"lock:{key}")
    if lock.acquire(timeout=5):
        try:
            value = db.fetch(key)
            cache.set(key, value)
        finally:
            lock.release()
    else:
        # Another process is fetching, wait
        time.sleep(0.1)
        return cache.get(key)
```

**Solution 2: Probabilistic Early Expiration**
```python
def get_with_early_refresh(key, ttl, beta=1):
    value, expiry = cache.get_with_expiry(key)
    
    # Probabilistically refresh before expiry
    if time.now() - random.expovariate(beta) >= expiry:
        # Refresh in background
        refresh_async(key)
    
    return value
```

---

## Multi-Level Caching

```
┌────────────────────────────────────────────────────────┐
│                      L1: Local Cache                   │
│                    (in-process, fastest)               │
└────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   L2: Distributed Cache                │
│                    (Redis, shared)                     │
└────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                   L3: CDN Cache                        │
│                  (static content)                      │
└────────────────────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────┐
│                      Database                          │
└────────────────────────────────────────────────────────┘
```

---

## Interview Tips

### Common Questions

1. **"How do you handle cache consistency?"**
   - TTL for eventual consistency
   - Event-driven invalidation for strong consistency
   - Write-through for always-consistent

2. **"What if cache fails?"**
   - Circuit breaker pattern
   - Fallback to database
   - Local cache as backup

3. **"How to cache paginated results?"**
   - Cache individual items, not pages
   - Or cache first N pages only

### What to Cache

| Cache | Don't Cache |
|-------|-------------|
| Frequently read | Frequently updated |
| Expensive to compute | Rarely accessed |
| Tolerates staleness | Requires real-time |
| Small data | Large data |

---

## Key Takeaways

1. **Cache-aside** is most common. Simple and effective.

2. **Cache invalidation is hard.** TTL is simplest, events are most consistent.

3. **Redis for features, Memcached for simplicity.**

4. **Prevent stampedes** with locking or early refresh.

5. **Multi-level caching** for different latency needs.

---

## What's Next?

Message queues for async processing:

👉 [Message Queues →](./message-queues)
