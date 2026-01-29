---
sidebar_position: 2
title: "Database Scaling Strategies"
description: >-
  Scale databases for system design interviews. Replication, sharding,
  partitioning, and read replicas.
keywords:
  - database scaling
  - sharding
  - replication
  - partitioning
  - read replicas
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - SQL vs NoSQL
companies: [All Companies]
---

# Database Scaling: Handle the Data

Databases are often the bottleneck. Know how to scale them.

---

## Scaling Strategies

```
1. Read Replicas (read scaling)
2. Sharding (write scaling)
3. Caching (read offloading)
4. Denormalization (query optimization)
```

---

## Read Replicas

```
             ┌─────────────┐
  Writes ───▶│   Primary   │
             └──────┬──────┘
                    │ Replication
         ┌──────────┼──────────┐
         ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Replica │ │ Replica │ │ Replica │
    └─────────┘ └─────────┘ └─────────┘
         ▲          ▲          ▲
         └──────────┼──────────┘
                 Reads

Benefits:
- Scale reads horizontally
- Geographic distribution
- Failover capability

Trade-offs:
- Replication lag
- Eventual consistency
- Doesn't help write scaling
```

---

## Sharding (Partitioning)

Distribute data across multiple databases.

```
                    Router
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ Shard 1 │   │ Shard 2 │   │ Shard 3 │
   │ Users   │   │ Users   │   │ Users   │
   │ A-H     │   │ I-P     │   │ Q-Z     │
   └─────────┘   └─────────┘   └─────────┘
```

### Sharding Strategies

| Strategy | How | Pros | Cons |
|----------|-----|------|------|
| **Range** | By value range (A-H, I-P) | Simple, range queries | Hotspots possible |
| **Hash** | hash(key) % N | Even distribution | No range queries |
| **Directory** | Lookup table | Flexible | Extra hop |
| **Geographic** | By region | Low latency | Uneven data |

### Choosing Shard Key

```
Good shard key:
- High cardinality (many unique values)
- Even distribution
- Query pattern aligned

Examples:
- user_id (for user data)
- order_date (for time-series)
- customer_region (for geographic)

Bad shard keys:
- Status fields (few values)
- Timestamps alone (recent data hotspot)
```

---

## Sharding Challenges

```
1. Cross-shard queries
   - JOINs across shards expensive
   - May need application-level joins

2. Rebalancing
   - Adding shards requires data migration
   - Consistent hashing helps

3. Referential integrity
   - Foreign keys across shards don't work
   - Application must enforce

4. Transactions
   - Distributed transactions are hard
   - Saga pattern as alternative
```

---

## Denormalization

Trade storage for query speed.

```sql
-- Normalized (3 tables)
SELECT u.name, COUNT(o.id)
FROM users u
JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Denormalized (1 table)
SELECT name, order_count
FROM users;  -- order_count pre-computed

Trade-offs:
+ Faster reads
+ No JOINs needed
- More storage
- Write complexity (keep in sync)
- Potential inconsistency
```

---

## Caching Layer

```
   Request
      │
      ▼
  ┌───────────┐    Cache
  │   Cache   │◄── Hit ──► Response
  └─────┬─────┘
        │ Miss
        ▼
  ┌───────────┐
  │  Database │───► Update Cache ───► Response
  └───────────┘

Common patterns:
- Cache-aside (lazy loading)
- Write-through
- Write-behind
```

---

## Scaling Decision Tree

```
Problem: Database is slow

Is it reads?
├── Yes → Add read replicas OR caching
└── No (writes) → 
    Is it single table?
    ├── Yes → Vertical scaling first
    └── No → Sharding
```

---

## Key Takeaways

1. **Read replicas** for read-heavy workloads.
2. **Sharding** for write scaling and large datasets.
3. **Choose shard key carefully**—hard to change later.
4. **Caching** offloads reads before scaling DB.
5. **Denormalize** when JOINs become bottleneck.
