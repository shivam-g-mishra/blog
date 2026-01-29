---
sidebar_position: 2
title: "Database Sharding Strategies"
description: >-
  Master database sharding for system design interviews. Horizontal partitioning,
  shard keys, rebalancing, and consistent hashing.
keywords:
  - database sharding
  - horizontal partitioning
  - shard key
  - consistent hashing
  - distributed database
difficulty: Advanced
estimated_time: 30 minutes
prerequisites:
  - SQL vs NoSQL
companies: [Google, Amazon, Meta, Netflix, Uber]
---

# Database Sharding: Horizontal Scaling

When one database can't handle the load, you split data across multiple databases.

---

## Why Shard?

```
Before: One DB handling 100K QPS → Bottleneck

After: 10 shards, each handling 10K QPS → Scalable
```

---

## Sharding Strategies

### Range-Based Sharding

```
Shard by user_id ranges:
Shard 0: user_id 0 - 999,999
Shard 1: user_id 1,000,000 - 1,999,999
Shard 2: user_id 2,000,000 - 2,999,999
```

**Pros:** Simple, range queries efficient
**Cons:** Hotspots if data unevenly distributed

### Hash-Based Sharding

```python
def get_shard(user_id, num_shards):
    return hash(user_id) % num_shards
```

**Pros:** Even distribution
**Cons:** Adding shards requires rehashing

### Consistent Hashing

```
Hash Ring:
    Shard A
       │
┌──────┴──────┐
│             │
Shard D    Shard B
│             │
└──────┬──────┘
       │
    Shard C

Add Shard E: Only keys between D and E move
```

**Pros:** Minimal redistribution when adding/removing shards
**Cons:** More complex implementation

---

## Choosing a Shard Key

| Shard Key | Good For | Bad For |
|-----------|----------|---------|
| user_id | User-centric apps | Cross-user queries |
| timestamp | Time-series data | Recent data hotspot |
| geo_region | Location-based apps | Global queries |
| hash(id) | Even distribution | Range queries |

---

## Cross-Shard Queries

```
Query: Get all orders for last week

Without sharding: Single query

With sharding:
1. Query each shard in parallel
2. Aggregate results
3. Return combined result

→ More complex, potentially slower
```

---

## Rebalancing

When adding shards:

```python
# Before: 3 shards
# After: 4 shards

# With consistent hashing:
# Only ~25% of keys move

# With hash mod:
# Most keys need to move
```

---

## Practice Questions

1. "How would you shard a user database?"
2. "What happens when you add a new shard?"
3. "How do you handle cross-shard transactions?"

---

## Key Takeaways

1. **Choose shard key based on access patterns.**
2. **Consistent hashing** minimizes rebalancing.
3. **Cross-shard queries are expensive.** Design to avoid them.
4. **Plan for rebalancing** from the start.
