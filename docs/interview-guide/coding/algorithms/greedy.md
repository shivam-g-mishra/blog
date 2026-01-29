---
sidebar_position: 5
title: "Greedy Algorithms"
description: >-
  Master greedy algorithms for coding interviews. When greedy works,
  common patterns, and proving correctness.
keywords:
  - greedy algorithms
  - interval scheduling
  - activity selection
  - interview preparation
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Big-O Notation
  - Sorting
companies: [Google, Amazon, Meta]
---

# Greedy Algorithms: Make the Locally Optimal Choice

Greedy algorithms make the best choice at each step, hoping it leads to a global optimum.

---

## When Greedy Works

```
Greedy works when:
1. Greedy choice property - local optimal leads to global optimal
2. Optimal substructure - optimal solution contains optimal sub-solutions

Greedy does NOT always work. Verify correctness!
```

---

## Classic Greedy Problems

### Activity Selection (Interval Scheduling)

**Problem:** Select maximum non-overlapping activities.

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

**Key insight:** Always pick the activity that ends earliest.

---

### Jump Game

**Problem:** Can you reach the last index?

```python
def can_jump(nums):
    max_reach = 0
    
    for i, jump in enumerate(nums):
        if i > max_reach:
            return False
        max_reach = max(max_reach, i + jump)
        
        if max_reach >= len(nums) - 1:
            return True
    
    return True
```

---

### Jump Game II (Minimum Jumps)

```python
def min_jumps(nums):
    if len(nums) <= 1:
        return 0
    
    jumps = 0
    current_end = 0
    farthest = 0
    
    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        
        if i == current_end:
            jumps += 1
            current_end = farthest
            
            if current_end >= len(nums) - 1:
                break
    
    return jumps
```

---

### Gas Station

```python
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    
    start = 0
    tank = 0
    
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        
        if tank < 0:
            start = i + 1
            tank = 0
    
    return start
```

**Key insight:** If total gas >= total cost, a solution exists. Reset when tank goes negative.

---

### Partition Labels

```python
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    
    result = []
    start = end = 0
    
    for i, c in enumerate(s):
        end = max(end, last[c])
        
        if i == end:
            result.append(end - start + 1)
            start = i + 1
    
    return result
```

---

### Minimum Platforms (Meeting Rooms II)

```python
def min_platforms(arrivals, departures):
    arrivals.sort()
    departures.sort()
    
    platforms = 0
    max_platforms = 0
    i = j = 0
    
    while i < len(arrivals):
        if arrivals[i] < departures[j]:
            platforms += 1
            i += 1
        else:
            platforms -= 1
            j += 1
        
        max_platforms = max(max_platforms, platforms)
    
    return max_platforms
```

---

### Huffman Coding

```python
import heapq

def huffman_coding(freq):
    heap = [[f, [c, ""]] for c, f in freq.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return dict(heap[0][1:])
```

---

## Greedy vs DP

| Greedy | DP |
|--------|-----|
| Make one choice, never reconsider | Consider all choices |
| O(n) or O(n log n) typical | O(n²) or O(n×m) typical |
| Prove correctness is hard | Correctness from recurrence |
| Not always optimal | Always optimal (if correct) |

**Example:** Coin change with {1, 3, 4}, amount = 6
- Greedy: 4 + 1 + 1 = 3 coins
- Optimal: 3 + 3 = 2 coins
- **Greedy fails!**

---

## Practice Problems

| Problem | Key Insight |
|---------|-------------|
| Activity Selection | Sort by end time |
| Jump Game | Track max reachable |
| Gas Station | Reset on negative |
| Partition Labels | Track last occurrence |
| Task Scheduler | Count max frequency |
| Candy | Two passes (L→R, R→L) |
| Boats to Save People | Two pointers on sorted |

---

## Key Takeaways

1. **Greedy isn't always correct**—verify your approach.
2. **Sorting often enables greedy** solutions.
3. **Interval problems** almost always use greedy.
4. **If greedy fails**, consider DP.
5. **Two passes** (forward + backward) solve many problems.
