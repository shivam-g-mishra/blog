---
sidebar_position: 2
title: "Consistency Patterns"
description: >-
  Understand consistency models for system design. Strong, eventual,
  causal consistency, and when to use each.
keywords:
  - consistency patterns
  - eventual consistency
  - strong consistency
  - causal consistency
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - CAP Theorem
companies: [All Companies]
---

# Consistency Patterns: Levels of Agreement

Different applications need different consistency guarantees. Know your options.

---

## Consistency Spectrum

```
Strong ◄───────────────────────────► Eventual

Strong Consistency
  │
  ├── Linearizability
  │
  ├── Sequential Consistency
  │
  ├── Causal Consistency
  │
  ├── Read-your-writes
  │
  ├── Monotonic reads
  │
  └── Eventual Consistency
```

---

## Strong Consistency

Every read returns the most recent write.

```
Timeline:
Client A: ────Write(X=5)────────────────────►
Client B: ─────────────────Read(X)──────────►
                              │
                              └─► Always returns 5

Cost:
- Higher latency (coordination needed)
- Lower availability (may reject during partitions)

Use when:
- Financial transactions
- Inventory counts
- Anything where stale = wrong
```

---

## Eventual Consistency

If no new updates, all reads will eventually return the same value.

```
Timeline:
Client A: ────Write(X=5)────────────────────►
Client B: ─────────────────Read(X)──Read(X)─►
                              │        │
                              └─► 3    └─► 5 (eventually)

Characteristics:
- Fast writes (no waiting for consensus)
- May read stale data
- Conflicts resolved later

Use when:
- Social media posts
- Product reviews
- DNS
```

---

## Read-Your-Writes

A client always sees their own writes.

```
Timeline:
Client A: ────Write(X=5)────Read(X)─────────►
                              │
                              └─► Always 5 for Client A
                              
Client B: ─────────────────Read(X)──────────►
                              │
                              └─► Might be stale

Implementation:
- Route client to same replica
- Track client's latest write timestamp
```

---

## Monotonic Reads

Once a client sees a value, they never see an older value.

```
Timeline:
Client A: ────Read(X)────Read(X)────Read(X)──►
               │           │          │
               └─► 3       └─► 5      └─► 5 or newer
                           
               Never goes backwards

Implementation:
- Track client's last read timestamp
- Only return data at least that fresh
```

---

## Causal Consistency

Operations that are causally related are seen in the same order by all.

```
Client A: Write(X=1) ──────────────────────►
Client B: ─────Read(X)=1───Write(Y=2)──────►
Client C: ─────────────────Read(Y)=2──Read(X)──►
                                        │
                                        └─► Must see X=1
                                        
If C sees Y=2 (which depended on X=1),
C must also see X=1

Implementation:
- Vector clocks
- Dependency tracking
```

---

## Comparison Table

| Model | Guarantee | Performance | Use Case |
|-------|-----------|-------------|----------|
| **Strong** | Latest value | Slowest | Banking |
| **Eventual** | Will converge | Fastest | Social media |
| **Read-your-writes** | See own writes | Medium | User sessions |
| **Monotonic** | No going back | Medium | Progress tracking |
| **Causal** | Preserve causality | Medium | Collaborative editing |

---

## Implementation Strategies

### Quorum Reads/Writes

```
N = total replicas
W = write quorum
R = read quorum

Strong consistency if: W + R > N

Example (N=3):
W=2, R=2: Strong (overlap guaranteed)
W=1, R=1: Eventual (no overlap)
```

### Conflict Resolution

```
For eventual consistency, need conflict resolution:

1. Last-Writer-Wins (LWW)
   - Timestamp determines winner
   - May lose updates

2. Application-specific merge
   - Shopping cart: union of items
   - Counter: sum of increments

3. CRDTs (Conflict-free Replicated Data Types)
   - Math guarantees convergence
   - G-Counter, PN-Counter, OR-Set
```

---

## Interview Application

```
Asked: "What consistency model would you use?"

Consider:
1. What happens if user sees stale data?
   - Financial loss → Strong
   - Minor inconvenience → Eventual

2. What's the read/write pattern?
   - Read-heavy → Can cache, eventual OK
   - Write-heavy → Consider async

3. Is there natural ordering?
   - Causal relationships → Causal consistency
   - Independent operations → Eventual OK
```

---

## Key Takeaways

1. **Strong consistency** is expensive—only use when needed.
2. **Eventual consistency** is usually sufficient for user-facing features.
3. **Read-your-writes** prevents confusing user experience.
4. **Quorum** math: W + R > N for strong consistency.
5. **Know trade-offs** and justify your choice.
