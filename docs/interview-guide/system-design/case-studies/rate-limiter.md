---
sidebar_position: 6
title: "Design Rate Limiter"
description: >-
  Complete system design for rate limiter. Token bucket, sliding window,
  distributed implementation with Redis.
keywords:
  - design rate limiter
  - api throttling
  - token bucket
  - sliding window
  - distributed rate limiting
difficulty: Intermediate
estimated_time: 35 minutes
prerequisites:
  - Rate Limiting Algorithms
companies: [Google, Amazon, Cloudflare, Stripe]
---

# Design a Rate Limiter

Rate limiters protect your system from abuse. Simple concept, tricky at scale.

---

## Requirements

### Functional
- Limit requests per user/IP/API key
- Return 429 when limit exceeded
- Support different limits for different APIs
- Accurate rate limiting

### Non-Functional
- **Latency:** < 1ms overhead
- **Availability:** 99.99%
- **Scale:** 10M requests/second

---

## Algorithm Comparison

| Algorithm | Burst Handling | Memory | Implementation |
|-----------|----------------|--------|----------------|
| Token Bucket | Allows bursts | Low | Medium |
| Leaky Bucket | Smooth output | Low | Medium |
| Fixed Window | Edge bursts | Low | Simple |
| Sliding Window Log | None | High | Complex |
| Sliding Window Counter | Minimal | Medium | Medium |

**Recommendation:** Token Bucket for most use cases.

---

## High-Level Design

```
┌─────────┐     ┌──────────────┐     ┌─────────────┐
│ Client  │────▶│ Rate Limiter │────▶│ API Server  │
└─────────┘     │   (Redis)    │     └─────────────┘
                └──────────────┘
                       │
                 ┌─────┴─────┐
                 ▼           ▼
            ┌───────┐   ┌───────┐
            │Rules  │   │Counter│
            │Config │   │Store  │
            └───────┘   └───────┘
```

---

## Token Bucket Implementation

```python
import time
import redis

class TokenBucketRateLimiter:
    def __init__(self, redis_client, capacity, refill_rate):
        self.redis = redis_client
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
    
    def is_allowed(self, key):
        now = time.time()
        bucket_key = f"ratelimit:{key}"
        
        # Lua script for atomicity
        lua_script = """
        local tokens_key = KEYS[1]
        local timestamp_key = KEYS[2]
        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])
        
        local last_tokens = tonumber(redis.call('GET', tokens_key)) or capacity
        local last_time = tonumber(redis.call('GET', timestamp_key)) or now
        
        local elapsed = now - last_time
        local new_tokens = math.min(capacity, last_tokens + elapsed * refill_rate)
        
        if new_tokens >= 1 then
            redis.call('SET', tokens_key, new_tokens - 1)
            redis.call('SET', timestamp_key, now)
            redis.call('EXPIRE', tokens_key, 60)
            redis.call('EXPIRE', timestamp_key, 60)
            return 1
        else
            return 0
        end
        """
        
        result = self.redis.eval(
            lua_script,
            2,
            f"{bucket_key}:tokens",
            f"{bucket_key}:timestamp",
            self.capacity,
            self.refill_rate,
            now
        )
        
        return result == 1
```

---

## Sliding Window Counter

```python
def is_allowed_sliding_window(redis_client, user_id, limit, window_seconds):
    now = time.time()
    window_start = now - window_seconds
    key = f"ratelimit:{user_id}"
    
    pipe = redis_client.pipeline()
    
    # Remove old entries
    pipe.zremrangebyscore(key, 0, window_start)
    
    # Count current window
    pipe.zcard(key)
    
    # Add current request
    pipe.zadd(key, {str(now): now})
    
    # Set expiry
    pipe.expire(key, window_seconds)
    
    results = pipe.execute()
    current_count = results[1]
    
    if current_count < limit:
        return True
    else:
        # Remove the request we just added
        redis_client.zrem(key, str(now))
        return False
```

---

## Rules Configuration

```json
{
  "rules": [
    {
      "api": "/api/login",
      "limit": 5,
      "window": 60,
      "key": "ip"
    },
    {
      "api": "/api/search",
      "limit": 100,
      "window": 60,
      "key": "user_id"
    },
    {
      "api": "/api/*",
      "limit": 1000,
      "window": 60,
      "key": "api_key"
    }
  ]
}
```

---

## Distributed Rate Limiting

### Challenge
Multiple rate limiter instances need consistent counts.

### Solution: Centralized Redis

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Rate Limiter│     │ Rate Limiter│     │ Rate Limiter│
│  Instance 1 │     │  Instance 2 │     │  Instance 3 │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       └───────────────────┼───────────────────┘
                           │
                    ┌──────▼──────┐
                    │ Redis Cluster│
                    │  (Shared)    │
                    └─────────────┘
```

---

## Response Headers

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1706500000
Retry-After: 30
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Algorithm | Token Bucket | Allows bursts, simple |
| Storage | Redis | Fast, distributed |
| Atomicity | Lua scripts | Prevent race conditions |
| Key format | `{type}:{identifier}` | Flexible |

---

## Key Takeaways

1. **Token Bucket** for most use cases—simple and allows bursts.
2. **Redis Lua scripts** for atomic operations.
3. **Return helpful headers** (remaining, reset time).
4. **Different limits** for different APIs/users.
5. **Graceful degradation** if Redis is unavailable.
