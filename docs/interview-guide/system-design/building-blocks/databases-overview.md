---
sidebar_position: 5
title: "Database Selection Guide"
description: >-
  Choose the right database for your system design. SQL, NoSQL, time-series,
  graph databases and when to use each.
keywords:
  - database selection
  - SQL vs NoSQL
  - database comparison
  - system design databases
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - SQL vs NoSQL
companies: [All Companies]
---

# Database Selection: Right Tool for the Job

Different databases excel at different things. Know when to use each.

---

## Database Categories

| Category | Examples | Best For |
|----------|----------|----------|
| **Relational (SQL)** | PostgreSQL, MySQL | Structured data, transactions |
| **Document** | MongoDB, CouchDB | Flexible schemas, JSON data |
| **Key-Value** | Redis, DynamoDB | Caching, sessions, simple lookups |
| **Wide-Column** | Cassandra, HBase | Time-series, write-heavy |
| **Graph** | Neo4j, Neptune | Relationships, social networks |
| **Time-Series** | InfluxDB, TimescaleDB | Metrics, IoT, logs |
| **Search** | Elasticsearch | Full-text search, analytics |

---

## Decision Framework

```
Ask yourself:

1. What's the data structure?
   - Fixed schema → SQL
   - Variable/nested → Document
   - Simple K-V → Key-Value
   - Heavily connected → Graph

2. What's the access pattern?
   - Complex queries/joins → SQL
   - Single key lookups → Key-Value
   - Range scans by time → Time-Series
   - Full-text search → Search engine

3. What's the scale requirement?
   - Moderate (TB) → SQL can work
   - Massive (PB) → NoSQL often better

4. What consistency is needed?
   - Strong (financial) → SQL
   - Eventual is OK → NoSQL options
```

---

## When to Use Each

### PostgreSQL / MySQL

```
✓ Transactions (ACID)
✓ Complex queries and JOINs
✓ Structured, relational data
✓ Strong consistency required
✓ Moderate scale

Examples:
- User accounts
- Orders and inventory
- Financial transactions
```

### MongoDB

```
✓ Flexible, evolving schemas
✓ Document-oriented data
✓ Rapid development
✓ Horizontal scaling needed

Examples:
- Product catalogs
- Content management
- User profiles with varying fields
```

### Redis

```
✓ Caching
✓ Session storage
✓ Real-time leaderboards
✓ Pub/sub messaging
✓ Rate limiting

Examples:
- API response cache
- User sessions
- Real-time analytics
```

### Cassandra

```
✓ Write-heavy workloads
✓ Time-series data
✓ Geographic distribution
✓ No single point of failure

Examples:
- IoT sensor data
- Activity logs
- Message storage
```

### Elasticsearch

```
✓ Full-text search
✓ Log aggregation
✓ Analytics dashboards
✓ Faceted search

Examples:
- Product search
- Log analysis
- Application monitoring
```

---

## Common Combinations

```
Typical architecture uses multiple databases:

Web Application:
- PostgreSQL: Users, orders (primary data)
- Redis: Caching, sessions
- Elasticsearch: Product search

Social Network:
- PostgreSQL: Users, posts
- Cassandra: Activity feeds (write-heavy)
- Redis: Real-time notifications
- Neo4j: Friend recommendations

IoT Platform:
- TimescaleDB: Sensor readings
- PostgreSQL: Device metadata
- Redis: Real-time dashboards
```

---

## Interview Tips

```
When choosing a database, explain:

1. Why this type? (relational vs document vs...)
2. Specific product if relevant (PostgreSQL vs MySQL)
3. Trade-offs acknowledged
4. How it fits the access pattern
5. Scaling considerations
```

---

## Key Takeaways

1. **No universal best database**—context matters.
2. **SQL for transactions** and complex queries.
3. **NoSQL for scale** and flexible schemas.
4. **Use multiple databases** when appropriate.
5. **Match database to access pattern.**
