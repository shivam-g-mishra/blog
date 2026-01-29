---
sidebar_position: 3
title: "Greedy Interval Problems"
description: >-
  Master greedy interval problems for coding interviews. Non-overlapping
  intervals, minimum arrows, and scheduling.
keywords:
  - greedy intervals
  - non overlapping intervals
  - minimum arrows
  - interval scheduling
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Interval Problems
companies: [Google, Amazon, Meta]
---

# Greedy Interval Problems

When greedy works for intervals: optimal substructure + greedy choice property.

---

## Non-Overlapping Intervals

Remove minimum intervals to make non-overlapping.

**Key insight:** Keep intervals that end earliest.

```python
def erase_overlap_intervals(intervals):
    if not intervals:
        return 0
    
    # Sort by end time
    intervals.sort(key=lambda x: x[1])
    
    count = 0
    end = intervals[0][1]
    
    for i in range(1, len(intervals)):
        if intervals[i][0] < end:
            # Overlap - remove this interval
            count += 1
        else:
            # No overlap - update end
            end = intervals[i][1]
    
    return count
```

---

## Minimum Arrows to Burst Balloons

Find minimum arrows to burst all balloons (intervals).

```python
def find_min_arrow_shots(points):
    if not points:
        return 0
    
    # Sort by end position
    points.sort(key=lambda x: x[1])
    
    arrows = 1
    end = points[0][1]
    
    for start, balloon_end in points[1:]:
        if start > end:
            # Need new arrow
            arrows += 1
            end = balloon_end
        # else: current arrow covers this balloon
    
    return arrows
```

---

## Video Stitching

Minimum clips to cover [0, time].

```python
def video_stitching(clips, time):
    # Sort by start, then by end descending
    clips.sort(key=lambda x: (x[0], -x[1]))
    
    count = 0
    current_end = 0
    farthest = 0
    i = 0
    
    while current_end < time:
        # Find clip that extends farthest
        while i < len(clips) and clips[i][0] <= current_end:
            farthest = max(farthest, clips[i][1])
            i += 1
        
        if farthest <= current_end:
            return -1  # Can't extend
        
        count += 1
        current_end = farthest
    
    return count
```

---

## Jump Game II

Minimum jumps to reach end.

```python
def jump(nums):
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

## Merge Intervals (Greedy perspective)

```python
def merge(intervals):
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged
```

---

## When Greedy Works

```
For intervals, greedy works when:

1. Activity Selection
   - Want max non-overlapping
   - Sort by END time
   
2. Covering Problems  
   - Want min intervals to cover range
   - Sort by START time
   
3. Counting Problems
   - Want max/min count of something
   - Usually sort by end
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Non-overlapping Intervals | Medium | Amazon |
| Minimum Arrows | Medium | Meta |
| Video Stitching | Medium | Google |
| Jump Game II | Medium | Amazon |
| Insert Interval | Medium | Google |
| Merge Intervals | Medium | Meta |

---

## Key Takeaways

1. **Sort by end** for selection problems (max non-overlapping).
2. **Sort by start** for coverage problems.
3. **Greedy choice:** Pick locally optimal, prove globally optimal.
4. **Track current coverage** and extend greedily.
