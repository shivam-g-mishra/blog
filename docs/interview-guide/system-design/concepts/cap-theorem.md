---
sidebar_position: 1
title: "CAP Theorem"
description: >-
  Understand CAP theorem for system design interviews. Consistency, availability,
  partition tolerance, and practical implications.
keywords:
  - CAP theorem
  - consistency
  - availability
  - partition tolerance
  - distributed systems
difficulty: Intermediate
estimated_time: 15 minutes
prerequisites:
  - System Design Introduction
companies: [All Companies]
---

# CAP Theorem: The Distributed Systems Trade-off

In a distributed system, you can only guarantee two of three properties: Consistency, Availability, Partition Tolerance.

---

## The Three Properties

### Consistency (C)

Every read receives the most recent write or an error.

```
Client A writes X=5
Client B reads X → must get 5 (not stale value)
```

### Availability (A)

Every request receives a response (not necessarily the most recent data).

```
System always responds, even during failures
May return stale data rather than error
```

### Partition Tolerance (P)

System continues operating despite network partitions.

```
Network split between nodes
System still functions (maybe degraded)
```

---

## The Trade-off

```
In reality, network partitions WILL happen.
So you're really choosing between:

CP: Consistency + Partition Tolerance
   - May reject requests during partition
   - Examples: MongoDB, HBase, Redis Cluster

AP: Availability + Partition Tolerance
   - Always responds, may be stale
   - Examples: Cassandra, DynamoDB, CouchDB

CA: Not practical in distributed systems
   - Only works if network never fails
   - Single-node systems
```

---

## Visual Example

```
Normal Operation:
┌─────────┐         ┌─────────┐
│ Node A  │◄───────►│ Node B  │
│ X = 5   │         │ X = 5   │
└─────────┘         └─────────┘
     ▲                   ▲
     │                   │
  Client 1            Client 2

Network Partition:
┌─────────┐    ✕    ┌─────────┐
│ Node A  │◄───┼───►│ Node B  │
│ X = 5   │         │ X = 5   │
└─────────┘         └─────────┘

Client 1 writes X=10 to Node A

CP Choice:
- Node A rejects write (can't sync with B)
- Or accepts but Node B rejects reads
- Consistency maintained, availability sacrificed

AP Choice:
- Node A accepts write (X=10)
- Node B still serves X=5
- Availability maintained, consistency sacrificed
```

---

## Real-World Examples

### CP Systems

| System | Trade-off |
|--------|-----------|
| **MongoDB** | Rejects writes without majority |
| **HBase** | Strong consistency, may be unavailable |
| **Zookeeper** | Coordination needs consistency |

### AP Systems

| System | Trade-off |
|--------|-----------|
| **Cassandra** | Eventually consistent, always available |
| **DynamoDB** | Configurable, defaults to eventual |
| **DNS** | Cached data may be stale |

---

## Beyond CAP: PACELC

CAP only considers partitions. PACELC extends it:

```
If Partition:
  Choose Availability or Consistency

Else (normal operation):
  Choose Latency or Consistency

PA/EL: Available during partition, low latency normally (Cassandra)
PC/EC: Consistent always (traditional RDBMS)
PA/EC: Available during partition, consistent normally (rare)
```

---

## Interview Application

When designing a system, consider:

```
Banking/Financial:
- Needs consistency (CP)
- Better to reject than show wrong balance

Social Media Feed:
- Prefers availability (AP)
- Stale post is better than no response

Shopping Cart:
- Usually AP
- Eventually merge conflicting carts
```

---

## Key Takeaways

1. **Partitions are inevitable.** You're really choosing C vs A.
2. **CP systems** sacrifice availability for correctness.
3. **AP systems** sacrifice consistency for uptime.
4. **Context matters.** Different parts of a system can make different choices.
5. **Know examples** and when to use each.
