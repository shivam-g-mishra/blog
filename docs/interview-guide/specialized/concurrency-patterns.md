---
sidebar_position: 5
title: "Concurrency Patterns"
description: >-
  Common concurrency patterns for coding interviews. Producer-consumer,
  readers-writers, dining philosophers, and more.
keywords:
  - concurrency patterns
  - producer consumer
  - readers writers
  - multithreading
difficulty: Advanced
estimated_time: 25 minutes
prerequisites:
  - Concurrency Basics
companies: [Google, Amazon, Microsoft]
---

# Concurrency Patterns: Classic Problems

These patterns appear repeatedly in concurrency interviews and real systems.

---

## Producer-Consumer

Multiple producers add items, multiple consumers process them.

```python
import threading
from queue import Queue

class ProducerConsumer:
    def __init__(self, max_size=10):
        self.queue = Queue(maxsize=max_size)
    
    def producer(self, item):
        self.queue.put(item)  # Blocks if full
        print(f"Produced: {item}")
    
    def consumer(self):
        item = self.queue.get()  # Blocks if empty
        print(f"Consumed: {item}")
        self.queue.task_done()
        return item

# With manual synchronization
class ManualProducerConsumer:
    def __init__(self, max_size=10):
        self.buffer = []
        self.max_size = max_size
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def produce(self, item):
        with self.not_full:
            while len(self.buffer) >= self.max_size:
                self.not_full.wait()
            
            self.buffer.append(item)
            self.not_empty.notify()
    
    def consume(self):
        with self.not_empty:
            while not self.buffer:
                self.not_empty.wait()
            
            item = self.buffer.pop(0)
            self.not_full.notify()
            return item
```

---

## Readers-Writers

Multiple readers can read simultaneously, but writers need exclusive access.

```python
class ReadersWriters:
    def __init__(self):
        self.readers = 0
        self.resource_lock = threading.Lock()
        self.readers_lock = threading.Lock()
    
    def read_lock(self):
        with self.readers_lock:
            self.readers += 1
            if self.readers == 1:
                self.resource_lock.acquire()
    
    def read_unlock(self):
        with self.readers_lock:
            self.readers -= 1
            if self.readers == 0:
                self.resource_lock.release()
    
    def write_lock(self):
        self.resource_lock.acquire()
    
    def write_unlock(self):
        self.resource_lock.release()

# Writer-preference version prevents writer starvation
class ReadersWritersFair:
    def __init__(self):
        self.readers = 0
        self.writers_waiting = 0
        self.lock = threading.Lock()
        self.readers_ok = threading.Condition(self.lock)
        self.writers_ok = threading.Condition(self.lock)
        self.writing = False
    
    def read_lock(self):
        with self.lock:
            while self.writing or self.writers_waiting > 0:
                self.readers_ok.wait()
            self.readers += 1
    
    def read_unlock(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0:
                self.writers_ok.notify()
    
    def write_lock(self):
        with self.lock:
            self.writers_waiting += 1
            while self.writing or self.readers > 0:
                self.writers_ok.wait()
            self.writers_waiting -= 1
            self.writing = True
    
    def write_unlock(self):
        with self.lock:
            self.writing = False
            self.writers_ok.notify()
            self.readers_ok.notify_all()
```

---

## Dining Philosophers

Avoid deadlock when multiple processes compete for shared resources.

```python
class DiningPhilosophers:
    def __init__(self, n=5):
        self.n = n
        self.forks = [threading.Lock() for _ in range(n)]
    
    def pick_up_forks(self, philosopher_id):
        left = philosopher_id
        right = (philosopher_id + 1) % self.n
        
        # Always pick up lower-numbered fork first (prevents deadlock)
        first, second = (left, right) if left < right else (right, left)
        
        self.forks[first].acquire()
        self.forks[second].acquire()
    
    def put_down_forks(self, philosopher_id):
        left = philosopher_id
        right = (philosopher_id + 1) % self.n
        
        self.forks[left].release()
        self.forks[right].release()
    
    def eat(self, philosopher_id):
        self.pick_up_forks(philosopher_id)
        try:
            # Eating
            pass
        finally:
            self.put_down_forks(philosopher_id)
```

---

## Semaphore-Based Rate Limiter

```python
class RateLimiter:
    def __init__(self, max_requests, per_seconds):
        self.semaphore = threading.Semaphore(max_requests)
        self.per_seconds = per_seconds
    
    def acquire(self):
        self.semaphore.acquire()
        # Release after time window
        threading.Timer(self.per_seconds, self.semaphore.release).start()
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, *args):
        pass  # Released by timer
```

---

## Thread Pool

```python
from concurrent.futures import ThreadPoolExecutor

# Built-in way
with ThreadPoolExecutor(max_workers=4) as executor:
    results = executor.map(process_item, items)

# Manual implementation
class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue()
        self.threads = []
        
        for _ in range(num_threads):
            t = threading.Thread(target=self._worker)
            t.daemon = True
            t.start()
            self.threads.append(t)
    
    def _worker(self):
        while True:
            func, args, kwargs, result_queue = self.tasks.get()
            try:
                result = func(*args, **kwargs)
                result_queue.put(('success', result))
            except Exception as e:
                result_queue.put(('error', e))
            finally:
                self.tasks.task_done()
    
    def submit(self, func, *args, **kwargs):
        result_queue = Queue()
        self.tasks.put((func, args, kwargs, result_queue))
        return result_queue
```

---

## Common Interview Problems

| Problem | Key Concept |
|---------|-------------|
| Print in Order | Semaphores/Events |
| Print FooBar Alternately | Condition variables |
| Building H2O | Barrier synchronization |
| Bounded Blocking Queue | Producer-consumer |
| Web Crawler Multithreaded | Thread pool + visited set |

---

## Key Takeaways

1. **Producer-Consumer:** Use Queue or condition variables.
2. **Readers-Writers:** Allow concurrent reads, exclusive writes.
3. **Dining Philosophers:** Consistent ordering prevents deadlock.
4. **Thread pools** reuse threads for efficiency.
5. **Always consider**: deadlock, starvation, race conditions.
