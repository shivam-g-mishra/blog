---
sidebar_position: 2
title: "Activity Selection & Scheduling"
description: >-
  Master activity selection problems for coding interviews. Greedy scheduling,
  job sequencing, and optimization problems.
keywords:
  - activity selection
  - greedy algorithm
  - job scheduling
  - task scheduler
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Interval Problems
companies: [Google, Amazon, Microsoft]
---

# Activity Selection: Greedy Scheduling

Select maximum non-overlapping activities—classic greedy problem.

---

## The Pattern

**Key insight:** Sort by end time, always pick earliest-ending activity.

```python
def max_activities(activities):
    # Sort by end time
    activities.sort(key=lambda x: x[1])
    
    count = 1
    last_end = activities[0][1]
    
    for start, end in activities[1:]:
        if start >= last_end:
            count += 1
            last_end = end
    
    return count
```

---

## Maximum Number of Events

Attend maximum events (each takes one day).

```python
import heapq

def max_events(events):
    events.sort()  # Sort by start day
    
    count = 0
    day = 0
    i = 0
    heap = []  # Min-heap of end days
    
    while i < len(events) or heap:
        if not heap:
            day = events[i][0]
        
        # Add all events starting on or before current day
        while i < len(events) and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])
            i += 1
        
        # Attend event with earliest deadline
        heapq.heappop(heap)
        count += 1
        day += 1
        
        # Remove events that have passed
        while heap and heap[0] < day:
            heapq.heappop(heap)
    
    return count
```

---

## Task Scheduler (with Cooldown)

```python
from collections import Counter
import heapq

def least_interval(tasks, n):
    count = Counter(tasks)
    max_heap = [-c for c in count.values()]
    heapq.heapify(max_heap)
    
    time = 0
    queue = []  # (available_time, count)
    
    while max_heap or queue:
        time += 1
        
        if max_heap:
            cnt = heapq.heappop(max_heap) + 1
            if cnt != 0:
                queue.append((time + n, cnt))
        
        if queue and queue[0][0] == time:
            heapq.heappush(max_heap, queue.pop(0)[1])
    
    return time

# Simpler math approach
def least_interval_math(tasks, n):
    count = Counter(tasks)
    max_count = max(count.values())
    num_max = sum(1 for c in count.values() if c == max_count)
    
    # Minimum needed based on most frequent task
    return max(len(tasks), (max_count - 1) * (n + 1) + num_max)
```

---

## Job Sequencing with Deadlines

Maximize profit by completing jobs before deadlines.

```python
def job_sequencing(jobs):
    # jobs = [(job_id, deadline, profit)]
    jobs.sort(key=lambda x: -x[2])  # Sort by profit descending
    
    max_deadline = max(j[1] for j in jobs)
    slots = [-1] * max_deadline
    profit = 0
    
    for job_id, deadline, job_profit in jobs:
        # Find latest available slot before deadline
        for i in range(deadline - 1, -1, -1):
            if slots[i] == -1:
                slots[i] = job_id
                profit += job_profit
                break
    
    return profit
```

---

## Practice Problems

| Problem | Pattern | Company |
|---------|---------|---------|
| Activity Selection | Sort by end | Google |
| Maximum Events | Heap + greedy | Amazon |
| Task Scheduler | Cooldown handling | Meta |
| Meeting Rooms II | Min rooms | Google |
| Car Pooling | Timeline sweep | Microsoft |

---

## Key Takeaways

1. **Sort by end time** for activity selection.
2. **Greedy works** when local optimal leads to global optimal.
3. **Use heap** for dynamic selection.
4. **Prove greedy correctness** with exchange argument.
