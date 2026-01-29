---
sidebar_position: 1
title: "Concurrency Fundamentals"
description: >-
  Master concurrency for coding interviews. Threads, locks, race conditions,
  deadlocks, and common patterns.
keywords:
  - concurrency
  - multithreading
  - race condition
  - deadlock
  - thread safety
difficulty: Advanced
estimated_time: 30 minutes
prerequisites:
  - Basic programming
companies: [Google, Amazon, Microsoft, Apple]
---

# Concurrency: The Parallel World

Concurrency questions test your understanding of shared state, synchronization, and parallel execution.

---

## Key Concepts

### Thread vs Process

| Aspect | Process | Thread |
|--------|---------|--------|
| Memory | Separate | Shared |
| Creation | Expensive | Cheap |
| Communication | IPC (slower) | Shared memory (faster) |
| Isolation | Complete | None |

### Race Condition

Two threads accessing shared data without synchronization.

```python
# UNSAFE
counter = 0

def increment():
    global counter
    counter += 1  # Not atomic: read, increment, write

# Two threads calling increment() simultaneously
# Expected: counter = 2
# Actual: counter might be 1 (lost update)
```

### Critical Section

Code that accesses shared resources—must be synchronized.

```python
import threading

counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    with lock:  # Critical section
        counter += 1
```

---

## Synchronization Primitives

### Mutex (Lock)

```python
import threading

lock = threading.Lock()

def critical_operation():
    lock.acquire()
    try:
        # Only one thread can be here
        pass
    finally:
        lock.release()

# Or use context manager
def critical_operation():
    with lock:
        pass
```

### Semaphore

Allows N threads to access resource simultaneously.

```python
import threading

semaphore = threading.Semaphore(3)  # Allow 3 concurrent

def limited_resource():
    with semaphore:
        # At most 3 threads here
        pass
```

### Condition Variable

Wait for a condition to become true.

```python
import threading

condition = threading.Condition()
queue = []

def producer():
    with condition:
        queue.append(item)
        condition.notify()  # Wake up consumer

def consumer():
    with condition:
        while not queue:
            condition.wait()  # Wait for producer
        item = queue.pop(0)
```

---

## Deadlock

Two or more threads waiting for each other forever.

```python
# DEADLOCK
lock_a = threading.Lock()
lock_b = threading.Lock()

def thread_1():
    with lock_a:
        with lock_b:  # Waiting for lock_b
            pass

def thread_2():
    with lock_b:
        with lock_a:  # Waiting for lock_a
            pass
```

### Deadlock Prevention

1. **Lock ordering:** Always acquire locks in same order
2. **Timeout:** Try to acquire with timeout
3. **Lock-free algorithms:** Use atomic operations

```python
# SAFE: Consistent ordering
def thread_1():
    with lock_a:
        with lock_b:
            pass

def thread_2():
    with lock_a:  # Same order as thread_1
        with lock_b:
            pass
```

---

## Common Patterns

### Producer-Consumer

```python
import threading
from queue import Queue

queue = Queue(maxsize=10)

def producer():
    while True:
        item = produce_item()
        queue.put(item)  # Blocks if full

def consumer():
    while True:
        item = queue.get()  # Blocks if empty
        process(item)
```

### Read-Write Lock

```python
import threading

class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()
        self.write_lock = threading.Lock()
    
    def acquire_read(self):
        with self.lock:
            self.readers += 1
            if self.readers == 1:
                self.write_lock.acquire()
    
    def release_read(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.write_lock.release()
    
    def acquire_write(self):
        self.write_lock.acquire()
    
    def release_write(self):
        self.write_lock.release()
```

### Thread Pool

```python
from concurrent.futures import ThreadPoolExecutor

def process_item(item):
    return item * 2

with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_item, items)
```

---

## Interview Problems

### Print in Order

```python
class Foo:
    def __init__(self):
        self.first_done = threading.Event()
        self.second_done = threading.Event()
    
    def first(self):
        print("first")
        self.first_done.set()
    
    def second(self):
        self.first_done.wait()
        print("second")
        self.second_done.set()
    
    def third(self):
        self.second_done.wait()
        print("third")
```

### Bounded Blocking Queue

```python
import threading

class BoundedBlockingQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue = []
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)
    
    def enqueue(self, element):
        with self.not_full:
            while len(self.queue) >= self.capacity:
                self.not_full.wait()
            self.queue.append(element)
            self.not_empty.notify()
    
    def dequeue(self):
        with self.not_empty:
            while not self.queue:
                self.not_empty.wait()
            element = self.queue.pop(0)
            self.not_full.notify()
            return element
```

---

## Key Takeaways

1. **Race conditions** occur when threads share data without synchronization.
2. **Locks** protect critical sections but can cause deadlocks.
3. **Deadlock prevention:** Consistent lock ordering.
4. **Use high-level abstractions** (queues, thread pools) when possible.
5. **Test concurrent code** with multiple runs—bugs are non-deterministic.
