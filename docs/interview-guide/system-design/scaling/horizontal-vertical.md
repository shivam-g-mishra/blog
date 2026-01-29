---
sidebar_position: 1
title: "Horizontal vs Vertical Scaling"
description: >-
  Understand scaling strategies for system design. When to scale up vs out,
  trade-offs, and practical considerations.
keywords:
  - horizontal scaling
  - vertical scaling
  - scale up
  - scale out
  - distributed systems
difficulty: Intermediate
estimated_time: 15 minutes
prerequisites:
  - System Design Introduction
companies: [All Companies]
---

# Scaling: Up vs Out

Every system eventually needs to handle more load. Know your options.

---

## The Two Approaches

### Vertical Scaling (Scale Up)

Add more power to existing machine.

```
Before: 4 CPU, 16 GB RAM
After:  32 CPU, 128 GB RAM

Same machine, more resources
```

### Horizontal Scaling (Scale Out)

Add more machines.

```
Before: 1 server
After:  10 servers behind load balancer

More machines, distribute load
```

---

## Comparison

| Aspect | Vertical | Horizontal |
|--------|----------|------------|
| Complexity | Simple | Complex |
| Cost | Expensive at scale | More linear |
| Limit | Hardware ceiling | Theoretically unlimited |
| Downtime | Often required | Rolling updates |
| Data handling | Simpler | Need distributed data |
| Failure impact | Single point of failure | More resilient |

---

## When to Use Each

### Vertical Scaling Works When

```
✓ Quick fix needed
✓ Simpler architecture preferred
✓ Stateful applications
✓ Strong consistency required
✓ Not at hardware limits yet
```

### Horizontal Scaling Works When

```
✓ Need high availability
✓ Traffic is variable (auto-scale)
✓ Stateless applications
✓ Eventually consistent is OK
✓ Building for long-term growth
```

---

## Real-World Examples

### Vertical Scaling
- Database master (common initial approach)
- Cache server (Redis)
- Monolithic applications
- Legacy systems

### Horizontal Scaling
- Web servers behind load balancer
- Microservices
- NoSQL databases (Cassandra, MongoDB)
- Stateless APIs

---

## Challenges of Horizontal Scaling

```
1. State management
   - Sessions must be externalized
   - Sticky sessions or shared store

2. Data consistency
   - Distributed transactions
   - Eventual consistency

3. Communication overhead
   - Network latency between nodes
   - Service discovery

4. Operational complexity
   - More machines to manage
   - Deployment coordination
```

---

## Key Takeaways

1. **Start vertical** for simplicity, go horizontal for scale.
2. **Stateless design** enables horizontal scaling.
3. **Vertical has limits**—plan for horizontal eventually.
4. **Mix both** in practice (scale up DB, scale out web tier).
