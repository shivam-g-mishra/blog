---
sidebar_position: 1
title: "SQL vs NoSQL — The Right Database"
description: >-
  Choose the right database for your system design. SQL vs NoSQL comparison,
  CAP theorem, and decision framework for interviews.
keywords:
  - SQL vs NoSQL
  - database comparison
  - CAP theorem
  - PostgreSQL
  - MongoDB
  - system design database
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Amazon, Meta, Netflix, Uber]
---

# SQL vs NoSQL: There Is No "Best" Database

"What database should we use?"

This question appears in every system design interview. And the worst answer is: "Let's use PostgreSQL" (or MongoDB, or any specific database) without explaining why.

**The right database depends on your access patterns, consistency needs, and scale requirements.**

---

## The Core Difference

### SQL (Relational)

```
┌─────────────────────────────────────────────────────────┐
│                    users table                          │
├────────┬──────────┬─────────────┬─────────────────────┤
│ id     │ name     │ email       │ created_at          │
├────────┼──────────┼─────────────┼─────────────────────┤
│ 1      │ Alice    │ a@email.com │ 2024-01-01          │
│ 2      │ Bob      │ b@email.com │ 2024-01-02          │
└────────┴──────────┴─────────────┴─────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                    orders table                         │
├────────┬──────────┬────────────┬──────────────────────┤
│ id     │ user_id  │ amount     │ status               │
├────────┼──────────┼────────────┼──────────────────────┤
│ 101    │ 1        │ 99.99      │ completed            │
│ 102    │ 1        │ 149.99     │ pending              │
└────────┴──────────┴────────────┴──────────────────────┘

SELECT * FROM orders WHERE user_id = 1;
-- Joins, transactions, ACID guarantees
```

### NoSQL (Document)

```json
{
  "_id": "user_1",
  "name": "Alice",
  "email": "a@email.com",
  "orders": [
    {"id": 101, "amount": 99.99, "status": "completed"},
    {"id": 102, "amount": 149.99, "status": "pending"}
  ]
}
```

---

## Quick Comparison

| Aspect | SQL | NoSQL |
|--------|-----|-------|
| **Schema** | Fixed, predefined | Flexible, dynamic |
| **Scaling** | Vertical (harder horizontal) | Horizontal (easier) |
| **Transactions** | Strong ACID | Usually eventual |
| **Relationships** | Native (JOINs) | Manual (denormalization) |
| **Query language** | SQL (standardized) | Varies by database |
| **Best for** | Complex queries, consistency | Scale, flexibility |

---

## When to Use SQL

### Strong Consistency Matters

```
Banking transaction:
1. Debit Account A: -$100
2. Credit Account B: +$100

Both must succeed or both must fail.
SQL guarantees this with transactions.
```

### Complex Queries Needed

```sql
-- SQL makes this easy
SELECT 
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at > '2024-01-01'
GROUP BY u.id
HAVING total_spent > 1000
ORDER BY total_spent DESC;
```

### Data Integrity is Critical

- Foreign keys enforce relationships
- Constraints prevent bad data
- Transactions ensure consistency

### Examples

- Banking systems
- E-commerce orders
- User authentication
- Inventory management

---

## When to Use NoSQL

### Need Horizontal Scale

```
SQL: Add more powerful server (vertical)
NoSQL: Add more servers (horizontal)

At massive scale, horizontal wins.
```

### Schema Changes Frequently

```json
// Version 1
{"name": "Alice", "email": "a@email.com"}

// Version 2 - just add field
{"name": "Alice", "email": "a@email.com", "phone": "555-1234"}

// No migration needed in NoSQL
```

### High Write Throughput

NoSQL databases like Cassandra are optimized for writes.

### Read Access Patterns are Known

```json
// If you always fetch user with their orders together,
// store them together:
{
  "user_id": "123",
  "name": "Alice",
  "orders": [...]  // Embedded
}
// One read instead of JOIN
```

### Examples

- Social media feeds
- IoT sensor data
- Session storage
- Content management
- Real-time analytics

---

## CAP Theorem

You can only have 2 of 3:

```
         Consistency
            /\
           /  \
          /    \
         /      \
        /   CA   \
       /          \
      /____________\
     AP            CP

C - Consistency: All nodes see same data
A - Availability: System always responds
P - Partition Tolerance: Works despite network failures
```

### In Practice

Network partitions happen. So you're really choosing:

| Type | Behavior During Partition | Examples |
|------|---------------------------|----------|
| **CP** | Reject requests to maintain consistency | MongoDB, HBase |
| **AP** | Accept requests, reconcile later | Cassandra, DynamoDB |

### SQL Databases

Most SQL databases are **CA** (no partition tolerance) or **CP** (sacrifice availability).

### NoSQL Databases

- **Cassandra, DynamoDB:** AP (eventual consistency)
- **MongoDB:** CP (consistency over availability)

---

## Database Types Deep Dive

### Relational (SQL)

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **PostgreSQL** | Feature-rich, JSON support | General purpose |
| **MySQL** | Performance, replication | Web applications |
| **CockroachDB** | Distributed SQL | Global consistency |

### Document (NoSQL)

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **MongoDB** | Flexibility, ecosystem | General NoSQL |
| **Couchbase** | Performance, caching | Mobile, caching |

### Key-Value

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **Redis** | In-memory, data structures | Caching, sessions |
| **DynamoDB** | Serverless, auto-scaling | AWS applications |

### Wide-Column

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **Cassandra** | Write throughput, scale | Time-series, IoT |
| **HBase** | Hadoop integration | Big data |

### Graph

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **Neo4j** | Relationship queries | Social networks |
| **Amazon Neptune** | Managed, AWS | Knowledge graphs |

### Time-Series

| Database | Strengths | Use Case |
|----------|-----------|----------|
| **InfluxDB** | Time-series optimized | Metrics, monitoring |
| **TimescaleDB** | PostgreSQL-based | IoT, analytics |

---

## Decision Framework

```
Start Here
    │
    ▼
Need ACID transactions?
├── Yes → SQL
│   └── Need horizontal scale?
│       ├── Yes → CockroachDB, Spanner
│       └── No → PostgreSQL, MySQL
│
└── No → Continue
    │
    ▼
Read/write pattern?
├── Key-value lookups → Redis, DynamoDB
├── Time-series data → InfluxDB, TimescaleDB
├── Graph relationships → Neo4j
├── Flexible documents → MongoDB
└── High write throughput → Cassandra
```

---

## Hybrid Approaches

Real systems often use multiple databases:

```
┌─────────────────────────────────────────────────────────┐
│                    E-commerce System                     │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  PostgreSQL          Redis              Elasticsearch   │
│  ┌──────────┐       ┌──────────┐       ┌──────────┐    │
│  │ Orders   │       │ Sessions │       │ Product  │    │
│  │ Users    │       │ Cart     │       │ Search   │    │
│  │ Payments │       │ Cache    │       │          │    │
│  └──────────┘       └──────────┘       └──────────┘    │
│                                                         │
│  Source of truth    Performance       Full-text search  │
│  ACID transactions  Sub-ms latency    Faceted queries   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Interview Tips

### How to Answer "Which Database?"

1. **Clarify requirements:**
   - Read vs write ratio?
   - Consistency requirements?
   - Query patterns?
   - Scale expectations?

2. **State your choice with reasoning:**
   - "I'd use PostgreSQL because we need ACID transactions for payments and the query complexity warrants SQL"

3. **Acknowledge trade-offs:**
   - "The trade-off is horizontal scaling will require sharding, but at our projected scale, a single primary with read replicas should suffice"

### Common Mistakes

| Mistake | Better Approach |
|---------|-----------------|
| "MongoDB because it's webscale" | Explain specific use case |
| "SQL for everything" | Consider access patterns |
| "NoSQL is always faster" | Depends on query type |
| Ignoring consistency needs | Always discuss CAP |

---

## Key Takeaways

1. **SQL for consistency**, complex queries, relationships.

2. **NoSQL for scale**, flexibility, simple access patterns.

3. **CAP theorem:** Choose between consistency and availability during partitions.

4. **Hybrid is normal.** Most systems use multiple databases.

5. **Access patterns drive choice.** Know your queries before choosing.

---

## What's Next?

Database sharding for horizontal scale:

👉 [Sharding Strategies →](./sharding)
