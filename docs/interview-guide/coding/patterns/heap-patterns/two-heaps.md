---
sidebar_position: 2
title: "Two Heaps Pattern — Track the Middle"
description: >-
  Master the Two Heaps pattern for coding interviews. Median finding,
  sliding window median, and balancing techniques with code in 7 languages.
keywords:
  - two heaps
  - median stream
  - sliding window median
  - find median
  - heap pattern

og_title: "Two Heaps Pattern — Track the Middle"
og_description: "When you need to track the middle of a stream, use two heaps. One for the smaller half, one for the larger half."
og_image: "/img/social-card.svg"

date_published: 2026-01-28
date_modified: 2026-01-28
author: shivam
reading_time: 30
content_type: explanation
---

import { LanguageSelector, TimeEstimate, ConfidenceBuilder, DifficultyBadge } from '@site/src/components/interview-guide';
import { CodeTabs } from '@site/src/components/design-patterns/CodeTabs';
import TabItem from '@theme/TabItem';

# Two Heaps: Track the Middle

When you need to track the **median** of a dynamic stream, use two heaps: one for the smaller half (max-heap) and one for the larger half (min-heap).

<LanguageSelector />

<TimeEstimate
  learnTime="25-30 minutes"
  practiceTime="3-4 hours"
  masteryTime="4-5 problems"
  interviewFrequency="10%"
  difficultyRange="Hard"
  prerequisites="Heaps, Top K Pattern"
/>

---

## The Pattern Visualized

```
Numbers: [1, 3, 5, 7, 9]

Max-Heap (small):    Min-Heap (large):
     [3]                  [7]
    /                    /
   1                    9
   
        5 ← median (top of small or avg of both tops)

Key invariants:
1. All elements in small ≤ all elements in large
2. |small| and |large| differ by at most 1
3. Median is at the "meeting point"
```

---

## Find Median from Data Stream

The classic two-heaps problem.

<CodeTabs>
<TabItem value="python" label="Python">

```python
import heapq

class MedianFinder:
    """
    Find median from a stream of numbers.
    
    Use two heaps:
    - small: max-heap for smaller half (store negative for max behavior)
    - large: min-heap for larger half
    
    Invariants:
    - max(small) <= min(large)
    - len(small) == len(large) OR len(small) == len(large) + 1
    
    Time: O(log n) per add, O(1) for median
    Space: O(n)
    """
    
    def __init__(self):
        self.small: list[int] = []  # Max-heap (store negatives)
        self.large: list[int] = []  # Min-heap
    
    def add_num(self, num: int) -> None:
        # Step 1: Add to appropriate heap
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
        else:
            heapq.heappush(self.large, num)
        
        # Step 2: Balance sizes (small can have 1 more element)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        elif len(self.large) > len(self.small):
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)
    
    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2


# Usage:
# mf = MedianFinder()
# mf.add_num(1)  # small=[1], large=[]          → median=1
# mf.add_num(2)  # small=[1], large=[2]         → median=1.5
# mf.add_num(3)  # small=[2,1], large=[3]       → median=2
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class MedianFinder {
  private small: number[] = []; // Max-heap (store negatives)
  private large: number[] = []; // Min-heap

  addNum(num: number): void {
    // Add to small by default
    this.pushSmall(num);

    // Ensure max(small) <= min(large)
    if (this.small.length > 0 && this.large.length > 0) {
      if (-this.small[0] > this.large[0]) {
        const val = this.popSmall();
        this.pushLarge(val);
      }
    }

    // Balance sizes
    if (this.small.length > this.large.length + 1) {
      const val = this.popSmall();
      this.pushLarge(val);
    } else if (this.large.length > this.small.length) {
      const val = this.popLarge();
      this.pushSmall(val);
    }
  }

  findMedian(): number {
    if (this.small.length > this.large.length) {
      return -this.small[0];
    }
    return (-this.small[0] + this.large[0]) / 2;
  }

  // Heap operations (max-heap via negation)
  private pushSmall(val: number): void {
    this.small.push(-val);
    this.bubbleUp(this.small, this.small.length - 1);
  }

  private popSmall(): number {
    const result = -this.small[0];
    this.small[0] = this.small.pop()!;
    if (this.small.length > 0) this.bubbleDown(this.small, 0);
    return result;
  }

  private pushLarge(val: number): void {
    this.large.push(val);
    this.bubbleUp(this.large, this.large.length - 1);
  }

  private popLarge(): number {
    const result = this.large[0];
    this.large[0] = this.large.pop()!;
    if (this.large.length > 0) this.bubbleDown(this.large, 0);
    return result;
  }

  private bubbleUp(heap: number[], i: number): void {
    while (i > 0) {
      const parent = Math.floor((i - 1) / 2);
      if (heap[parent] <= heap[i]) break;
      [heap[parent], heap[i]] = [heap[i], heap[parent]];
      i = parent;
    }
  }

  private bubbleDown(heap: number[], i: number): void {
    while (true) {
      let smallest = i;
      const left = 2 * i + 1;
      const right = 2 * i + 2;
      if (left < heap.length && heap[left] < heap[smallest]) smallest = left;
      if (right < heap.length && heap[right] < heap[smallest]) smallest = right;
      if (smallest === i) break;
      [heap[smallest], heap[i]] = [heap[i], heap[smallest]];
      i = smallest;
    }
  }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
import "container/heap"

type MedianFinder struct {
    small *MaxHeap // smaller half
    large *MinHeap // larger half
}

func Constructor() MedianFinder {
    small := &MaxHeap{}
    large := &MinHeap{}
    heap.Init(small)
    heap.Init(large)
    return MedianFinder{small, large}
}

func (mf *MedianFinder) AddNum(num int) {
    // Add to appropriate heap
    if mf.small.Len() == 0 || num <= (*mf.small)[0] {
        heap.Push(mf.small, num)
    } else {
        heap.Push(mf.large, num)
    }
    
    // Balance
    if mf.small.Len() > mf.large.Len()+1 {
        heap.Push(mf.large, heap.Pop(mf.small).(int))
    } else if mf.large.Len() > mf.small.Len() {
        heap.Push(mf.small, heap.Pop(mf.large).(int))
    }
}

func (mf *MedianFinder) FindMedian() float64 {
    if mf.small.Len() > mf.large.Len() {
        return float64((*mf.small)[0])
    }
    return float64((*mf.small)[0]+(*mf.large)[0]) / 2.0
}

// MaxHeap implementation
type MaxHeap []int
func (h MaxHeap) Len() int           { return len(h) }
func (h MaxHeap) Less(i, j int) bool { return h[i] > h[j] }
func (h MaxHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MaxHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *MaxHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}

// MinHeap implementation
type MinHeap []int
func (h MinHeap) Len() int           { return len(h) }
func (h MinHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h MinHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }
func (h *MinHeap) Push(x any)        { *h = append(*h, x.(int)) }
func (h *MinHeap) Pop() any {
    old := *h
    n := len(old)
    x := old[n-1]
    *h = old[0 : n-1]
    return x
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
class MedianFinder {
    private PriorityQueue<Integer> small; // Max-heap (smaller half)
    private PriorityQueue<Integer> large; // Min-heap (larger half)
    
    public MedianFinder() {
        small = new PriorityQueue<>(Collections.reverseOrder());
        large = new PriorityQueue<>();
    }
    
    public void addNum(int num) {
        // Add to appropriate heap
        if (small.isEmpty() || num <= small.peek()) {
            small.offer(num);
        } else {
            large.offer(num);
        }
        
        // Balance: small can have at most 1 more element
        if (small.size() > large.size() + 1) {
            large.offer(small.poll());
        } else if (large.size() > small.size()) {
            small.offer(large.poll());
        }
    }
    
    public double findMedian() {
        if (small.size() > large.size()) {
            return small.peek();
        }
        return (small.peek() + large.peek()) / 2.0;
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class MedianFinder {
    priority_queue<int> small; // Max-heap (smaller half)
    priority_queue<int, vector<int>, greater<int>> large; // Min-heap
    
public:
    void addNum(int num) {
        // Add to appropriate heap
        if (small.empty() || num <= small.top()) {
            small.push(num);
        } else {
            large.push(num);
        }
        
        // Balance
        if (small.size() > large.size() + 1) {
            large.push(small.top());
            small.pop();
        } else if (large.size() > small.size()) {
            small.push(large.top());
            large.pop();
        }
    }
    
    double findMedian() {
        if (small.size() > large.size()) {
            return small.top();
        }
        return (small.top() + large.top()) / 2.0;
    }
};
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public class MedianFinder {
    private PriorityQueue<int, int> small; // Max-heap (use negative priority)
    private PriorityQueue<int, int> large; // Min-heap
    
    public MedianFinder() {
        small = new PriorityQueue<int, int>();
        large = new PriorityQueue<int, int>();
    }
    
    public void AddNum(int num) {
        // Add to small by default
        if (small.Count == 0 || num <= -small.Peek()) {
            small.Enqueue(num, -num); // Negative for max behavior
        } else {
            large.Enqueue(num, num);
        }
        
        // Balance
        if (small.Count > large.Count + 1) {
            int val = small.Dequeue();
            large.Enqueue(val, val);
        } else if (large.Count > small.Count) {
            int val = large.Dequeue();
            small.Enqueue(val, -val);
        }
    }
    
    // Custom Peek for small (workaround for PriorityQueue limitations)
    private int PeekSmall() {
        // In real implementation, you'd need to track top element
        // or use a different approach
        return small.Peek();
    }
    
    public double FindMedian() {
        if (small.Count > large.Count) {
            return small.Peek(); // Need custom implementation
        }
        return (small.Peek() + large.Peek()) / 2.0;
    }
}
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="Two Key Invariants">

Always maintain these invariants after each operation:

1. **Ordering:** Every element in `small` ≤ every element in `large`
2. **Balance:** `|small.size - large.size| ≤ 1`

The median is then either the top of `small` (if odd count) or the average of both tops (if even count).

</ConfidenceBuilder>

---

## Alternative Approach: Always Add to Small First

A cleaner implementation that always adds to small first, then rebalances:

<CodeTabs>
<TabItem value="python" label="Python">

```python
import heapq

class MedianFinderCleaner:
    """
    Cleaner implementation: Always add to small, then rebalance.
    
    This approach is easier to reason about:
    1. Push to small (max-heap)
    2. Move top of small to large (ensures ordering)
    3. If large is bigger, move one back to small
    """
    
    def __init__(self):
        self.small: list[int] = []  # Max-heap (negated)
        self.large: list[int] = []  # Min-heap
    
    def add_num(self, num: int) -> None:
        # Always add to small first
        heapq.heappush(self.small, -num)
        
        # Move largest from small to large (maintains ordering)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        
        # Balance: if large is bigger, move one back
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    
    def find_median(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2
```

</TabItem>
<TabItem value="java" label="Java">

```java
class MedianFinderCleaner {
    private PriorityQueue<Integer> small = new PriorityQueue<>(Collections.reverseOrder());
    private PriorityQueue<Integer> large = new PriorityQueue<>();
    
    public void addNum(int num) {
        // Always add to small first
        small.offer(num);
        
        // Move largest from small to large
        large.offer(small.poll());
        
        // Balance
        if (large.size() > small.size()) {
            small.offer(large.poll());
        }
    }
    
    public double findMedian() {
        if (small.size() > large.size()) {
            return small.peek();
        }
        return (small.peek() + large.peek()) / 2.0;
    }
}
```

</TabItem>
</CodeTabs>

---

## 🎯 Pattern Triggers

| Problem Clue | Approach |
|--------------|----------|
| "Median of stream" | Two heaps |
| "Sliding window median" | Two heaps + lazy deletion |
| "Balance two groups" | Two heaps |
| "Track middle element dynamically" | Two heaps |

---

## 💬 How to Communicate

**Explaining the approach:**
> "I'll partition the numbers into two halves using two heaps. The smaller half goes in a max-heap, the larger half in a min-heap. I maintain the invariant that the tops are adjacent to the median..."

**Explaining rebalancing:**
> "After each insertion, I ensure two things: first, that max(small) ≤ min(large) so the partition is valid; second, that the sizes differ by at most one so the median is at the boundary..."

---

## 🏋️ Practice Problems

| Problem | Difficulty | Notes |
|---------|------------|-------|
| [Find Median from Data Stream](https://leetcode.com/problems/find-median-from-data-stream/) | <DifficultyBadge level="hard" /> | Classic two heaps |
| [Sliding Window Median](https://leetcode.com/problems/sliding-window-median/) | <DifficultyBadge level="hard" /> | Two heaps + lazy delete |
| [IPO](https://leetcode.com/problems/ipo/) | <DifficultyBadge level="hard" /> | Two heaps for scheduling |
| [Find Right Interval](https://leetcode.com/problems/find-right-interval/) | <DifficultyBadge level="medium" /> | Heap-based |

---

## Key Takeaways

1. **Two heaps partition data** into smaller and larger halves.

2. **Max-heap for small, min-heap for large** puts median at the boundary.

3. **Always rebalance** to maintain size difference ≤ 1.

4. **"Add to small first" approach** is often cleaner to implement.

5. **O(log n) per operation** for both add and find median.

<ConfidenceBuilder type="youve-got-this">

**Two heaps is about maintaining a partition.**

Small heap holds the smaller half, large heap holds the larger half. The median lives at the boundary—either top of small (odd count) or average of both tops (even count).

</ConfidenceBuilder>

---

## What's Next?

More heap patterns:

**See also:** [Merge K Sorted Lists](/docs/interview-guide/coding/patterns/heap-patterns/merge-k-sorted) — Multi-way Merge with Heaps
