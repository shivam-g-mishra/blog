---
sidebar_position: 1
title: "Big-O Notation — Time & Space Complexity"
description: >-
  Master Big-O notation to analyze algorithm efficiency. Learn to identify 
  O(1), O(n), O(log n), O(n²) and more with real examples and interview tips.
keywords:
  - big o notation
  - time complexity
  - space complexity
  - algorithm analysis
  - interview preparation
difficulty: Beginner
estimated_time: 30 minutes
prerequisites: []
companies: [All]
---

# Big-O Notation: Understanding Algorithm Efficiency

Three months into my first software job, I proudly showed my tech lead a function I'd written. It worked perfectly—on my test data of 100 items.

"What happens with a million items?" he asked.

I ran it. Twenty minutes later, it was still running.

The function had a nested loop—O(n²) complexity. With 100 items, that's 10,000 operations. Barely noticeable. With 1 million items? A trillion operations. My laptop wasn't slow. My algorithm was.

**That's why Big-O matters. It tells you how your code will behave when the input grows.**

---

## What Big-O Actually Measures

Big-O describes how an algorithm's runtime or memory usage grows relative to input size.

**It doesn't tell you:**
- Exact runtime in seconds
- How fast your specific machine is
- Whether your code is "good"

**It does tell you:**
- How performance scales
- Which approach will handle large inputs
- Where bottlenecks will appear

When you see O(n), read it as: "As the input size grows, the time/space grows proportionally."

---

## The Common Complexities

Here's what you'll encounter in every interview:

```
Speed Ranking (fastest to slowest):

O(1)      → Constant     → Instant, regardless of input
O(log n)  → Logarithmic  → Cuts problem in half each step
O(n)      → Linear       → Grows with input
O(n log n)→ Linearithmic → Efficient sorting territory
O(n²)     → Quadratic    → Nested loops warning
O(2ⁿ)     → Exponential  → Usually means brute force
O(n!)     → Factorial    → Permutation territory
```

Let's make these concrete.

### O(1) — Constant Time

**The time doesn't change, no matter the input size.**

```python
def get_first(items):
    return items[0]  # O(1)

def get_by_key(hashmap, key):
    return hashmap[key]  # O(1) average
```

Array access by index: O(1). Hash table lookup: O(1) average. These are instant operations.

**Interview tip:** When you need O(1) lookup, think hash maps.

### O(log n) — Logarithmic

**Each step eliminates half the remaining elements.**

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

With 1 billion elements, binary search takes at most 30 steps. That's the power of logarithms.

**Interview tip:** If you see "sorted array" in a problem, binary search is probably involved.

### O(n) — Linear

**You touch each element once.**

```python
def find_max(items):
    max_val = items[0]
    for item in items:  # O(n)
        if item > max_val:
            max_val = item
    return max_val
```

Double the input? Double the time. That's linear growth.

**Interview tip:** O(n) is often the best you can do for unsorted data—you have to at least look at everything.

### O(n log n) — Linearithmic

**The sweet spot for comparison-based sorting.**

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # Divide: log n levels
    right = merge_sort(arr[mid:])
    
    return merge(left, right)       # Each level: O(n) work
```

Merge sort, quicksort (average), and heapsort all hit O(n log n). This is mathematically proven to be the best possible for comparison-based sorting.

**Interview tip:** If your solution involves sorting, you're usually looking at O(n log n) minimum.

### O(n²) — Quadratic

**Nested loops over the same data. The first red flag.**

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):           # O(n)
        for j in range(n - 1):   # × O(n) = O(n²)
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
```

1,000 items = 1 million operations. 10,000 items = 100 million operations.

**Interview tip:** If you write nested loops, immediately ask: "Is there a way to avoid this?"

### O(2ⁿ) — Exponential

**Usually means you're computing all subsets or trying all combinations.**

```python
def fibonacci_naive(n):
    if n <= 1:
        return n
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)  # O(2^n)
```

This is almost never acceptable in interviews. If you see exponential, look for dynamic programming or memoization.

### O(n!) — Factorial

**Generating all permutations.**

```python
def permutations(arr):
    if len(arr) <= 1:
        return [arr]
    
    result = []
    for i, item in enumerate(arr):
        rest = arr[:i] + arr[i + 1:]
        for perm in permutations(rest):
            result.append([item] + perm)
    return result
```

10 items = 3.6 million permutations. 20 items = 2.4 quintillion. Factorial explodes fast.

**Interview tip:** If a problem asks for "all permutations," expect exponential time. There's usually no way around it.

---

## Visualizing the Differences

Here's how these complexities compare with real numbers:

| n | O(1) | O(log n) | O(n) | O(n log n) | O(n²) | O(2ⁿ) |
|---|------|----------|------|------------|-------|-------|
| 10 | 1 | 3 | 10 | 33 | 100 | 1,024 |
| 100 | 1 | 7 | 100 | 664 | 10,000 | 10³⁰ |
| 1,000 | 1 | 10 | 1,000 | 9,966 | 1,000,000 | 10³⁰⁰ |
| 10,000 | 1 | 13 | 10,000 | 132,877 | 100,000,000 | ∞ |

**The lesson: O(n²) might work in your test cases but explode in production.**

---

## Space Complexity

Time isn't everything. Memory matters too.

```python
# O(1) space - constant extra memory
def sum_array(arr):
    total = 0
    for num in arr:
        total += num
    return total

# O(n) space - creates new array of same size
def double_array(arr):
    return [x * 2 for x in arr]

# O(n) space - recursion uses call stack
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # n stack frames
```

**Common space complexities:**
- O(1): In-place algorithms (swap, sliding window)
- O(n): Creating a copy, hash map of input size
- O(log n): Balanced tree recursion depth
- O(n²): 2D matrix creation

**Interview tip:** Interviewers love asking "Can you do it in-place?" That means O(1) space.

---

## How to Analyze Complexity

### Rule 1: Drop Constants

O(2n) = O(n). O(100n) = O(n).

Constants don't matter at scale because we care about growth rate, not exact operations.

### Rule 2: Drop Lower-Order Terms

O(n² + n) = O(n²). O(n + log n) = O(n).

As n grows, the dominant term wins.

### Rule 3: Sequential = Add, Nested = Multiply

```python
# Sequential operations: O(n) + O(m) = O(n + m)
for item in list_a:  # O(n)
    process(item)
for item in list_b:  # O(m)
    process(item)

# Nested operations: O(n) × O(m) = O(n × m)
for item_a in list_a:      # O(n)
    for item_b in list_b:  # × O(m)
        compare(item_a, item_b)
```

### Rule 4: Different Inputs = Different Variables

If you have two inputs, use different variables:

```python
def compare_lists(a, b):
    for item_a in a:     # O(a)
        for item_b in b: # O(b)
            if item_a == item_b:
                return True
    return False
# This is O(a × b), not O(n²)
```

---

## Common Interview Patterns

| Pattern | Typical Complexity |
|---------|-------------------|
| Hash map lookup | O(1) |
| Binary search | O(log n) |
| Single loop | O(n) |
| Two pointers | O(n) |
| Sorting | O(n log n) |
| Nested loops | O(n²) |
| All subsets | O(2ⁿ) |
| All permutations | O(n!) |

---

## Practice Problems

Test your understanding:

| Problem | Time | Space | Why? |
|---------|------|-------|------|
| Array sum | O(n) | O(1) | Single pass, one variable |
| Two Sum (hash map) | O(n) | O(n) | Single pass, hash map storage |
| Binary search | O(log n) | O(1) | Halving each step, iterative |
| Merge sort | O(n log n) | O(n) | log n levels, n work each |
| Check duplicates (nested) | O(n²) | O(1) | Compare every pair |
| Check duplicates (hash set) | O(n) | O(n) | Single pass with set |

---

## Interview Tips

**When discussing complexity:**

1. **State it explicitly**: "This solution is O(n) time and O(1) space."

2. **Explain why**: "It's O(n) because we iterate through the array once, and O(1) space because we only use a few variables."

3. **Discuss trade-offs**: "We could reduce time to O(n) by using a hash map, but that increases space to O(n)."

4. **Know the constraints**: If n ≤ 10, even O(n!) might work. If n = 10⁸, you need O(n) or better.

**Typical constraints and what they suggest:**

| Constraint | Acceptable Complexity |
|------------|----------------------|
| n ≤ 10 | O(n!), O(2ⁿ) |
| n ≤ 20 | O(2ⁿ) |
| n ≤ 100 | O(n³) |
| n ≤ 1,000 | O(n²) |
| n ≤ 10⁵ | O(n log n) |
| n ≤ 10⁸ | O(n) |
| n > 10⁸ | O(log n), O(1) |

---

## Key Takeaways

1. **Big-O describes growth, not speed.** A O(n) algorithm with bad constants can be slower than O(n²) for small inputs.

2. **Always ask: "What if the input is huge?"** This is how you catch O(n²) traps.

3. **Hash maps give you O(1) lookup.** When you need to reduce nested loops, think hash maps.

4. **Space-time trade-offs are everywhere.** Using more memory often means faster time.

5. **In interviews, state complexity explicitly.** Don't wait to be asked.

---

## What's Next?

Now that you understand complexity analysis, learn how to choose the right data structure for each problem:

👉 [Choosing Data Structures →](./choosing-data-structures)
