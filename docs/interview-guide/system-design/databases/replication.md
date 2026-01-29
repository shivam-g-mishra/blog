---
sidebar_position: 3
title: "Database Replication"
description: >-
  Master database replication for system design interviews. Primary-replica,
  multi-primary, synchronous vs async replication.
keywords:
  - database replication
  - primary replica
  - leader follower
  - synchronous replication
  - async replication
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - SQL vs NoSQL
companies: [Google, Amazon, Meta, Netflix]
---

# Database Replication: Availability & Read Scaling

Replication copies data to multiple servers for availability and read performance.

---

## Replication Strategies

### Primary-Replica (Leader-Follower)

```
┌─────────────┐
│   Primary   │ ← All writes
└──────┬──────┘
       │ Replicate
   ┌───┴───┐
   ▼       ▼
┌─────┐ ┌─────┐
│Rep 1│ │Rep 2│  ← Reads
└─────┘ └─────┘
```

**Writes:** Primary only
**Reads:** Any replica

### Multi-Primary

```
┌─────────┐     ┌─────────┐
│Primary A│◄───►│Primary B│
└─────────┘     └─────────┘
     ▲               ▲
     │               │
  Writes          Writes
```

**Use case:** Multi-region active-active

---

## Sync vs Async Replication

| Type | Behavior | Trade-off |
|------|----------|-----------|
| **Synchronous** | Wait for replica ack | Strong consistency, higher latency |
| **Asynchronous** | Don't wait | Lower latency, potential data loss |
| **Semi-sync** | Wait for 1 replica | Balance |

---

## Replication Lag

```
Write to Primary
     │
     ▼
Primary: [A, B, C, D]
     │ (async replication)
     ▼
Replica: [A, B, C]     ← Lag: missing D

User writes D, then reads from replica
→ Doesn't see their own write
```

**Solutions:**
- Read-your-writes: Route user reads to primary after write
- Monotonic reads: Stick user to same replica
- Causal consistency: Track dependencies

---

## Failover

```
1. Primary fails
2. Detect failure (heartbeat timeout)
3. Elect new primary (most up-to-date replica)
4. Update clients to new primary
5. Old primary rejoins as replica
```

---

## Key Takeaways

1. **Primary-replica** for read scaling and availability.
2. **Async replication** trades consistency for performance.
3. **Replication lag** causes read-your-writes issues.
4. **Automatic failover** requires consensus protocol.
