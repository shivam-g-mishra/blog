---
sidebar_position: 3
title: "Distributed Locking"
description: >-
  Understand distributed locking for system design interviews. Redis locks,
  ZooKeeper, and handling edge cases.
keywords:
  - distributed locking
  - redis lock
  - redlock
  - zookeeper
difficulty: Advanced
estimated_time: 20 minutes
prerequisites:
  - CAP Theorem
companies: [All Companies]
---

# Distributed Locking: Coordination at Scale

When multiple processes need exclusive access to a shared resource, you need distributed locking.

---

## Why It's Hard

```
Single machine: Use mutex/semaphore
Distributed system: 
- Network can fail
- Processes can crash
- Clocks can drift
- Operations aren't atomic
```

---

## Use Cases

| Scenario | Example |
|----------|---------|
| **Avoid double-processing** | Send email once |
| **Prevent race conditions** | Update inventory |
| **Leader election** | Single active worker |
| **Rate limiting** | Per-user limits |

---

## Redis-Based Lock

### Simple Lock (SETNX)

```python
def acquire_lock(redis, key, value, ttl=30):
    # SET if Not eXists, with TTL
    return redis.set(key, value, nx=True, ex=ttl)

def release_lock(redis, key, value):
    # Only release if we own it (Lua script for atomicity)
    script = """
    if redis.call("get", KEYS[1]) == ARGV[1] then
        return redis.call("del", KEYS[1])
    else
        return 0
    end
    """
    return redis.eval(script, 1, key, value)

# Usage
lock_key = "lock:order:123"
lock_value = str(uuid.uuid4())  # Unique identifier

if acquire_lock(redis, lock_key, lock_value):
    try:
        # Do exclusive work
        process_order()
    finally:
        release_lock(redis, lock_key, lock_value)
```

### Problems with Simple Lock

```
1. Single Redis = Single point of failure
2. TTL expiry during slow operation
3. Clock skew issues
```

---

## Redlock Algorithm

Distributed lock across multiple Redis instances.

```python
def acquire_redlock(redis_instances, key, value, ttl=30):
    n = len(redis_instances)
    quorum = n // 2 + 1
    
    start_time = time.time()
    acquired = 0
    
    for redis in redis_instances:
        try:
            if redis.set(key, value, nx=True, px=ttl * 1000):
                acquired += 1
        except:
            pass
    
    elapsed = time.time() - start_time
    validity_time = ttl - elapsed
    
    if acquired >= quorum and validity_time > 0:
        return validity_time
    
    # Failed to acquire - release from all
    for redis in redis_instances:
        try:
            release_lock(redis, key, value)
        except:
            pass
    
    return None
```

---

## ZooKeeper-Based Lock

```
ZooKeeper provides:
- Sequential nodes
- Ephemeral nodes (auto-deleted on disconnect)
- Watch mechanism

Lock algorithm:
1. Create ephemeral sequential node under /locks/resource
2. Get all children, sort by sequence number
3. If your node is smallest, you have the lock
4. Else, watch the node just before yours
5. When watched node deleted, re-check
```

```python
# Conceptual (using kazoo library)
from kazoo.recipe.lock import Lock

zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

lock = Lock(zk, "/locks/my-resource")

with lock:
    # Do exclusive work
    pass
```

---

## Handling Edge Cases

### Lock Holder Crashes

```
Problem: Process crashes while holding lock
Solution: TTL/lease expiration

Redis: SET with EX (expiry)
ZooKeeper: Ephemeral nodes
```

### Slow Operation Exceeds TTL

```
Problem: Work takes longer than lock TTL

Solutions:
1. Lock extension/refresh
   - Periodically extend TTL while working
   - Background thread heartbeats

2. Fencing tokens
   - Each lock acquisition gets monotonic token
   - Resource rejects operations with old tokens
```

### Network Partition

```
Problem: Client thinks it has lock but can't reach Redis

With Redlock:
- Need quorum (majority) to consider lock valid
- If can't reach quorum, lock invalid

Fencing tokens help:
- Even if two think they have lock
- Resource uses token to serialize
```

---

## Fencing Tokens

```
        Client A              Resource              Client B
           │                     │                     │
  Acquire lock (token=1)         │                     │
           │───────────────────▶│                     │
           │                     │     Acquire lock (token=2)
           │                  (slow)                   │
           │                     │◀───────────────────│
           │                     │                     │
  Write with token=1             │                     │
           │───────────────────▶│  Reject (2 > 1)     │
           │                     │                     │
                                 │  Write with token=2 │
                                 │◀───────────────────│
                                 │     Accept          │
```

---

## When to Use What

| Solution | Best For |
|----------|----------|
| **Single Redis lock** | Low risk, single region |
| **Redlock** | Higher reliability needs |
| **ZooKeeper** | Strong consistency required |
| **Database locks** | Already have strong DB |

---

## Key Takeaways

1. **Always use TTL**—prevent deadlocks from crashes.
2. **Fencing tokens** protect against delayed operations.
3. **Redlock needs quorum** across independent Redis instances.
4. **ZooKeeper** for strongest guarantees.
5. **Consider if you really need locking**—often can design around it.
