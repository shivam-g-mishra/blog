---
sidebar_position: 1
title: "Consistency Patterns"
description: >-
  Master consistency patterns for system design interviews. Strong, eventual,
  causal consistency, and linearizability.
keywords:
  - consistency patterns
  - strong consistency
  - eventual consistency
  - causal consistency
  - distributed systems
difficulty: Advanced
estimated_time: 25 minutes
prerequisites:
  - Database Replication
companies: [Google, Amazon, Meta, Netflix]
---

# Consistency Patterns: The Trade-offs

"Is your system consistent?" The answer is rarely yes or no—it's "what kind of consistency?"

---

## Consistency Levels

### Strong Consistency (Linearizability)

Every read sees the most recent write.

```
Client A writes: X = 5
Client B reads X immediately
→ Guaranteed to see 5
```

**Cost:** Higher latency, lower availability

### Eventual Consistency

Given enough time, all replicas converge.

```
Client A writes: X = 5
Client B reads X immediately
→ Might see old value
→ Eventually sees 5
```

**Cost:** Inconsistent reads possible

### Causal Consistency

Related operations appear in order.

```
Client A: Write X = 5
Client A: Write Y = 10 (depends on X)

Client B sees Y = 10
→ Guaranteed to see X = 5
```

---

## Read-Your-Writes Consistency

A client always sees their own writes.

```python
def get_user(user_id, last_write_time):
    # Route to primary if recent write
    if time.now() - last_write_time < THRESHOLD:
        return primary.get(user_id)
    return replica.get(user_id)
```

---

## When to Use What

| Use Case | Consistency Level |
|----------|-------------------|
| Banking transactions | Strong |
| Social media feed | Eventual |
| Shopping cart | Read-your-writes |
| Collaborative editing | Causal |

---

## Key Takeaways

1. **Strong consistency** is expensive but necessary for some use cases.
2. **Eventual consistency** enables higher availability and performance.
3. **Most systems** use a combination based on operation type.
