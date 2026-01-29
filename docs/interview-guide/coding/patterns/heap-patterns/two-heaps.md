---
sidebar_position: 2
title: "Two Heaps Pattern"
description: >-
  Master Two Heaps pattern for coding interviews. Median finding,
  sliding window median, and scheduling problems.
keywords:
  - two heaps
  - median stream
  - sliding window median
  - heap pattern
difficulty: Advanced
estimated_time: 20 minutes
prerequisites:
  - Top K Elements
companies: [Google, Amazon, Meta, Microsoft]
---

# Two Heaps: Track Both Extremes

When you need to track the middle of a stream, use two heaps.

---

## Find Median from Data Stream

```python
import heapq

class MedianFinder:
    def __init__(self):
        self.small = []  # Max-heap (store negative)
        self.large = []  # Min-heap
    
    def add_num(self, num):
        # Add to max-heap (small)
        heapq.heappush(self.small, -num)
        
        # Balance: largest of small <= smallest of large
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        
        # Balance sizes (small can be 1 larger)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self):
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

---

## The Pattern

```
Numbers: [1, 3, 5, 7, 9]

Max-Heap (small):    Min-Heap (large):
     [3]                  [7]
    /                    /
   1                    9
         5 (median)

small stores smaller half, large stores larger half
Median is either top of small or average of both tops
```

---

## Practice Problems

| Problem | Pattern | Company |
|---------|---------|---------|
| Find Median Stream | Two heaps | Amazon |
| Sliding Window Median | Two heaps + removal | Google |
| IPO | Max profit scheduling | Amazon |
