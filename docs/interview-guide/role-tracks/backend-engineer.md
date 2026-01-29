---
sidebar_position: 2
title: "Backend Engineer Interview Guide"
description: >-
  Comprehensive guide for backend engineering interviews. System design,
  databases, APIs, and distributed systems.
keywords:
  - backend interview
  - system design
  - API design
  - distributed systems
difficulty: Mixed
estimated_time: 20 minutes
prerequisites: []
companies: [Google, Amazon, Meta, Uber]
---

# Backend Engineer Interview Guide

Backend interviews focus on algorithms, system design, and distributed systems knowledge.

---

## Interview Structure

```
Typical backend interview loop:

1. Phone Screen (45-60 min)
   - Coding (data structures/algorithms)

2. Onsite (5-6 rounds)
   - Coding × 2
   - System Design × 1-2
   - Behavioral × 1
   - Domain-specific × 1 (optional)
```

---

## Key Topics

### System Design

| Topic | Must Know |
|-------|-----------|
| **Scalability** | Horizontal vs vertical, load balancing |
| **Databases** | SQL vs NoSQL, sharding, replication |
| **Caching** | Redis, cache strategies, invalidation |
| **Message Queues** | Kafka, RabbitMQ, async processing |
| **Microservices** | Service communication, API gateway |
| **Reliability** | Redundancy, failover, circuit breakers |

### Databases

```sql
-- Know how to:
-- 1. Design schemas
-- 2. Write complex queries
-- 3. Optimize with indexes
-- 4. Understand query plans

-- Example: Find users with most orders
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id
ORDER BY order_count DESC
LIMIT 10;
```

### API Design

```
REST:
GET    /users/{id}      - Retrieve
POST   /users           - Create
PUT    /users/{id}      - Replace
PATCH  /users/{id}      - Update
DELETE /users/{id}      - Delete

GraphQL:
query {
  user(id: "123") {
    name
    orders {
      id
      total
    }
  }
}
```

---

## Coding Focus Areas

### Data Structures

```
High priority:
- Hash tables
- Trees (BST, tries)
- Graphs
- Heaps

Medium priority:
- Linked lists
- Stacks/queues
- Union-find
```

### Algorithms

```
High priority:
- BFS/DFS
- Binary search
- Dynamic programming
- Two pointers

Medium priority:
- Topological sort
- Dijkstra's
- Backtracking
```

---

## Distributed Systems

```
Key concepts:
- CAP theorem
- Consistency models
- Consensus (Raft, Paxos basics)
- Distributed transactions
- Event-driven architecture
```

---

## Language-Specific

### Java

```java
// Concurrency
ExecutorService executor = Executors.newFixedThreadPool(10);
CompletableFuture.supplyAsync(() -> fetchData())
    .thenApply(data -> process(data))
    .exceptionally(e -> handleError(e));

// Know: Collections, Streams, Generics, JVM basics
```

### Python

```python
# Concurrency
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return data

# Know: Generators, decorators, context managers
```

### Go

```go
// Concurrency
func worker(jobs <-chan int, results chan<- int) {
    for j := range jobs {
        results <- process(j)
    }
}

// Know: Goroutines, channels, interfaces
```

---

## Common Interview Questions

### Coding
- Implement LRU cache
- Design a rate limiter
- Find shortest path in graph
- Serialize/deserialize binary tree

### System Design
- Design Twitter
- Design URL shortener
- Design notification system
- Design rate limiter

### Behavioral
- Technical disagreement
- Debugging production issue
- Leading a project

---

## Key Takeaways

1. **System design** is crucial for backend roles.
2. **Database knowledge** (SQL + NoSQL) is expected.
3. **Distributed systems** concepts are often tested.
4. **API design** comes up in most interviews.
5. **Know your language** deeply (concurrency, internals).
