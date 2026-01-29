---
sidebar_position: 2
title: "Rate Limiting Algorithms"
description: >-
  Master rate limiting for system design interviews. Token bucket, leaky bucket,
  fixed window, and sliding window algorithms.
keywords:
  - rate limiting
  - token bucket
  - leaky bucket
  - sliding window
  - API throttling
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Amazon, Meta, Stripe, Cloudflare]
---

# Rate Limiting: Protect Your System

Rate limiting prevents abuse and ensures fair resource usage.

---

## Algorithms

### Token Bucket

```python
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.last_refill = time.time()
    
    def allow_request(self):
        self._refill()
        
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now
```

**Pros:** Allows bursts, smooth rate
**Use:** API rate limiting

### Sliding Window Counter

```python
def is_allowed(user_id, limit, window_seconds):
    now = time.time()
    window_start = now - window_seconds
    
    # Count requests in current window
    count = redis.zcount(f"requests:{user_id}", window_start, now)
    
    if count < limit:
        redis.zadd(f"requests:{user_id}", {str(now): now})
        redis.zremrangebyscore(f"requests:{user_id}", 0, window_start)
        return True
    
    return False
```

---

## Comparison

| Algorithm | Burst Handling | Memory | Accuracy |
|-----------|----------------|--------|----------|
| Token Bucket | Allows bursts | Low | Good |
| Leaky Bucket | Smooth rate | Low | Good |
| Fixed Window | Edge bursts | Low | Approximate |
| Sliding Window | No bursts | Higher | Accurate |

---

## Distributed Rate Limiting

```
┌─────────┐     ┌─────────────┐     ┌─────────┐
│Client   │────▶│Rate Limiter │────▶│ Service │
└─────────┘     │  (Redis)    │     └─────────┘
                └─────────────┘
                     │
                ┌────┴────┐
                ▼         ▼
            ┌─────┐   ┌─────┐
            │Node1│   │Node2│
            └─────┘   └─────┘
```

---

## Key Takeaways

1. **Token bucket** for APIs allowing bursts.
2. **Sliding window** for accurate per-user limits.
3. **Use Redis** for distributed rate limiting.
4. **Return 429 Too Many Requests** with Retry-After header.
