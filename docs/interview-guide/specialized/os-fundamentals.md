---
sidebar_position: 3
title: "OS Fundamentals for Interviews"
description: >-
  Essential operating system concepts for coding interviews. Processes, threads,
  memory, scheduling, and common interview questions.
keywords:
  - operating systems
  - process vs thread
  - memory management
  - scheduling algorithms
  - OS interview
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites: []
companies: [Google, Amazon, Microsoft, Apple]
---

# OS Fundamentals: What Every Developer Should Know

OS questions appear in systems interviews. Know these core concepts.

---

## Process vs Thread

| Aspect | Process | Thread |
|--------|---------|--------|
| Memory | Separate address space | Shared within process |
| Creation | Expensive (fork) | Cheap |
| Communication | IPC (pipes, sockets) | Shared memory |
| Crash impact | Isolated | Can crash process |
| Context switch | Expensive | Cheaper |

```
Process A                    Process B
┌─────────────────┐         ┌─────────────────┐
│ Code            │         │ Code            │
│ Data            │         │ Data            │
│ Heap            │         │ Heap            │
├─────────────────┤         ├─────────────────┤
│ Thread 1 │ Thread 2 │     │ Thread 1 │
│ Stack    │ Stack    │     │ Stack    │
└─────────────────┘         └─────────────────┘
```

---

## Memory Layout

```
High Address
┌─────────────────┐
│     Stack       │  ← Local variables, function calls
│       ↓         │
├─────────────────┤
│                 │
│   (Free Space)  │
│                 │
├─────────────────┤
│       ↑         │
│      Heap       │  ← Dynamic allocation (malloc, new)
├─────────────────┤
│   BSS Segment   │  ← Uninitialized globals
├─────────────────┤
│  Data Segment   │  ← Initialized globals
├─────────────────┤
│  Text Segment   │  ← Code (read-only)
└─────────────────┘
Low Address
```

---

## Virtual Memory

```
Virtual Address Space          Physical Memory
┌─────────────────┐            ┌─────────────┐
│    Process A    │            │             │
│   Page 0  ──────┼────────────▶  Frame 3   │
│   Page 1  ──────┼────┐       │             │
│   Page 2  ──────┼────┼───────▶  Frame 7   │
└─────────────────┘    │       │             │
                       │       │             │
┌─────────────────┐    │       │             │
│    Process B    │    └───────▶  Frame 1   │
│   Page 0  ──────┼────────────▶  Frame 5   │
└─────────────────┘            └─────────────┘

Benefits:
- Isolation between processes
- Each process sees contiguous memory
- Memory larger than physical RAM (swapping)
```

---

## CPU Scheduling Algorithms

| Algorithm | Description | Pros | Cons |
|-----------|-------------|------|------|
| **FCFS** | First Come First Served | Simple | Convoy effect |
| **SJF** | Shortest Job First | Optimal average wait | Starvation |
| **Round Robin** | Time slices | Fair | Context switch overhead |
| **Priority** | Higher priority first | Important tasks first | Starvation |
| **Multilevel Queue** | Multiple queues | Flexibility | Complex |

---

## Context Switch

```
Process A Running → Interrupt/System Call → Save A's State
                                               ↓
Process B Running ← Restore B's State ← Select B (Scheduler)

What's saved:
- Program counter
- CPU registers
- Memory mappings
- Stack pointer
```

---

## Common Interview Questions

### What happens when you type a URL?

```
1. DNS lookup (URL → IP)
2. TCP connection (3-way handshake)
3. TLS handshake (if HTTPS)
4. HTTP request
5. Server processes request
6. HTTP response
7. Browser renders page
```

### What is a deadlock?

```
Four conditions (all must hold):
1. Mutual Exclusion: Resource held exclusively
2. Hold and Wait: Process holds resource while waiting for another
3. No Preemption: Can't forcibly take resource
4. Circular Wait: Circular chain of waiting

Prevention:
- Break any one condition
- Lock ordering
- Timeout with retry
```

### What is thrashing?

```
System spends more time swapping than executing.

Cause: Too many processes, not enough physical memory

Solution:
- Add RAM
- Reduce multiprogramming
- Better page replacement algorithm
```

---

## Page Replacement Algorithms

| Algorithm | Description |
|-----------|-------------|
| **FIFO** | Replace oldest page |
| **LRU** | Replace least recently used |
| **Optimal** | Replace page not used longest (theoretical) |
| **Clock** | Approximation of LRU |

---

## Synchronization Primitives

```python
# Mutex (Mutual Exclusion)
mutex.lock()
# Critical section
mutex.unlock()

# Semaphore (Counter)
semaphore.wait()  # Decrement, block if 0
# Access resource
semaphore.signal()  # Increment

# Condition Variable
while not condition:
    cond_var.wait(mutex)
# Proceed when condition true
```

---

## Key Takeaways

1. **Process = isolation**, Thread = shared memory.
2. **Virtual memory** enables isolation and exceeding physical RAM.
3. **Deadlock** requires four conditions—break any one.
4. **Context switches** are expensive—minimize them.
5. **LRU** is the practical page replacement choice.
