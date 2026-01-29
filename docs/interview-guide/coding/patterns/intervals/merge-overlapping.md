---
sidebar_position: 1
title: "Interval Problems Pattern"
description: >-
  Master interval problems for coding interviews. Merge, insert, intersection,
  and meeting rooms problems.
keywords:
  - interval problems
  - merge intervals
  - meeting rooms
  - overlapping intervals
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Sorting
companies: [Google, Amazon, Meta, Microsoft]
---

# Interval Problems: Overlap Detection

Interval problems appear frequently. The key: sort by start time, then process.

---

## The Pattern

```
Most interval problems:
1. Sort by start time
2. Process left to right
3. Track current interval/state
4. Handle overlaps
```

---

## Merge Intervals

```python
def merge(intervals):
    if not intervals:
        return []
    
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        last_end = merged[-1][1]
        
        if start <= last_end:  # Overlap
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])
    
    return merged

# [[1,3], [2,6], [8,10], [15,18]]
# → [[1,6], [8,10], [15,18]]
```

---

## Insert Interval

```python
def insert(intervals, new_interval):
    result = []
    i = 0
    n = len(intervals)
    
    # Add all intervals before new_interval
    while i < n and intervals[i][1] < new_interval[0]:
        result.append(intervals[i])
        i += 1
    
    # Merge overlapping intervals
    while i < n and intervals[i][0] <= new_interval[1]:
        new_interval[0] = min(new_interval[0], intervals[i][0])
        new_interval[1] = max(new_interval[1], intervals[i][1])
        i += 1
    
    result.append(new_interval)
    
    # Add remaining intervals
    while i < n:
        result.append(intervals[i])
        i += 1
    
    return result
```

---

## Interval Intersection

Find intersection of two sorted interval lists.

```python
def interval_intersection(first_list, second_list):
    result = []
    i = j = 0
    
    while i < len(first_list) and j < len(second_list):
        # Find overlap
        start = max(first_list[i][0], second_list[j][0])
        end = min(first_list[i][1], second_list[j][1])
        
        if start <= end:
            result.append([start, end])
        
        # Move pointer with smaller end
        if first_list[i][1] < second_list[j][1]:
            i += 1
        else:
            j += 1
    
    return result
```

---

## Meeting Rooms I

Can a person attend all meetings?

```python
def can_attend_meetings(intervals):
    intervals.sort(key=lambda x: x[0])
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False  # Overlap found
    
    return True
```

---

## Meeting Rooms II

Minimum number of meeting rooms required.

```python
import heapq

def min_meeting_rooms(intervals):
    if not intervals:
        return 0
    
    intervals.sort(key=lambda x: x[0])
    
    # Min-heap of end times
    heap = [intervals[0][1]]
    
    for start, end in intervals[1:]:
        if start >= heap[0]:  # Can reuse room
            heapq.heappop(heap)
        
        heapq.heappush(heap, end)
    
    return len(heap)
```

### Alternative: Event-based

```python
def min_meeting_rooms_events(intervals):
    events = []
    
    for start, end in intervals:
        events.append((start, 1))   # Meeting starts
        events.append((end, -1))    # Meeting ends
    
    events.sort()
    
    max_rooms = current = 0
    for time, delta in events:
        current += delta
        max_rooms = max(max_rooms, current)
    
    return max_rooms
```

---

## Non-Overlapping Intervals

Minimum intervals to remove to make non-overlapping.

```python
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    
    # Sort by end time (greedy: keep earliest ending)
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    prev_end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            count += 1  # Remove this interval
        else:
            prev_end = intervals[i][1]
    
    return count
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Merge Intervals | Medium | Google |
| Insert Interval | Medium | Meta |
| Meeting Rooms | Easy | Amazon |
| Meeting Rooms II | Medium | Google |
| Non-overlapping Intervals | Medium | Amazon |
| Interval List Intersections | Medium | Meta |

---

## Key Takeaways

1. **Sort by start time** is the first step for most problems.
2. **Sort by end time** for greedy selection (max non-overlapping).
3. **Heap tracks end times** for room scheduling.
4. **Event-based** approach works well for counting concurrent items.
