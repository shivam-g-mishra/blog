---
sidebar_position: 1
title: "Big-O Notation — Time & Space Complexity"
description: >-
  Learn Big-O notation for coding interviews. Understand time and space complexity,
  analyze algorithms, and know what interviewers actually want to hear.
keywords:
  - big o notation
  - time complexity
  - space complexity
  - algorithm analysis
  - coding interview
  - complexity analysis
difficulty: Beginner
estimated_time: 20 minutes
prerequisites: []
companies: [All Companies]
---

# Big-O Notation: The Language of Efficiency

I bombed my first technical interview because of Big-O.

Not because I didn't know what O(n) meant—I'd memorized the definitions. The problem was deeper. The interviewer asked me to optimize a solution, and I froze. I could see my code was slow, but I couldn't articulate *why* it was slow or *how* to make it faster.

Here's what I wish someone had told me: **Big-O isn't about memorizing complexity tables. It's about developing intuition for how code behaves as data grows.**

That intuition is what separates candidates who can only solve problems they've seen before from those who can reason through novel challenges.

---

## Why Big-O Matters in Interviews

Every coding interview eventually reaches the same question: "What's the time and space complexity of your solution?"

This isn't a trivia question. When an interviewer asks about complexity, they're really asking:

1. **Do you understand your own code?** Can you trace through what happens when input grows?
2. **Can you identify bottlenecks?** Where is your code spending time?
3. **Can you reason about trade-offs?** Is using more memory worth it for faster execution?
4. **Can you optimize?** If this solution is too slow, what would you change?

I've interviewed candidates who could solve hard LeetCode problems but couldn't explain why their solution was O(n²). That's a red flag. It suggests memorization without understanding.

**The goal isn't to recite complexity—it's to think in complexity.**

---

## The Core Idea: How Does Growth Scale?

Big-O describes how an algorithm's resource usage grows as input size increases. We care about the *shape* of growth, not the exact numbers.

Imagine you're searching for a name in a phone book:

**Linear search (O(n))**: Start at A, check every name until you find it. Double the names, double the time.

**Binary search (O(log n))**: Open to the middle. Is your name before or after? Eliminate half. Repeat. Double the names, add just one more step.

The phone book with 1,000 names might take 500 checks on average with linear search. With binary search? About 10 checks. With 1,000,000 names? Linear search: 500,000 checks. Binary search: about 20.

**That's the power of understanding complexity.** The right algorithm choice can be the difference between a solution that works and one that times out.

---

## The Common Complexities

Let me walk you through each complexity class with real intuition, not just definitions.

### O(1) — Constant Time

**What it means:** No matter how big the input gets, the operation takes the same amount of time.

**The intuition:** You're doing a fixed amount of work regardless of input size. You know exactly where to look.

```python
def get_first_element(arr):
    return arr[0]  # Always one operation

def get_from_hashmap(hashmap, key):
    return hashmap[key]  # Hash lookup is O(1) average
```

**Where you see it:**
- Array access by index
- Hash map get/set (average case)
- Push/pop from a stack
- Basic arithmetic

**Interview tip:** When you achieve O(1) for an operation that seems like it should be slower, call it out. "By using a hash map here, we get O(1) lookup instead of O(n) search."

---

### O(log n) — Logarithmic Time

**What it means:** Every step eliminates a constant fraction of the remaining work.

**The intuition:** You're dividing the problem in half (or thirds, or tenths) each iteration. This is incredibly powerful—a million elements only needs about 20 steps.

```python
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1  # Eliminate left half
        else:
            right = mid - 1  # Eliminate right half
    
    return -1
```

**Where you see it:**
- Binary search
- Balanced tree operations (BST, AVL, Red-Black)
- Heap operations (insert, extract)
- Finding a number's digits

**Interview tip:** When you see sorted data, your mind should immediately think "Can I use binary search?" That's O(log n) instead of O(n).

---

### O(n) — Linear Time

**What it means:** You touch each element once (or a constant number of times).

**The intuition:** You need to look at every item at least once. You can't do better if you need to process all the data.

```python
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # Touch each element once
        if num > max_val:
            max_val = num
    return max_val

def two_sum_optimized(nums, target):
    seen = {}
    for i, num in enumerate(nums):  # One pass through
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
```

**Where you see it:**
- Finding min/max in unsorted array
- Linear search
- Counting elements
- Most optimal array problems

**Interview tip:** O(n) is often the target complexity for array problems. If your solution is O(n²), ask yourself: "Can I use a hash map to eliminate the inner loop?"

---

### O(n log n) — Linearithmic Time

**What it means:** You're doing O(log n) work for each of the n elements.

**The intuition:** This is usually the result of sorting, or divide-and-conquer algorithms that process all elements while splitting the problem.

```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])   # Recursively sort halves
    right = merge_sort(arr[mid:])
    
    return merge(left, right)  # Merge is O(n)
# log n levels of recursion × O(n) work per level = O(n log n)
```

**Where you see it:**
- Efficient sorting (merge sort, quick sort average, heap sort)
- Problems that require sorting as preprocessing
- Some divide-and-conquer algorithms

**Interview tip:** If sorting helps solve your problem, you're looking at O(n log n) minimum. That's often acceptable—many optimal solutions use sorting.

---

### O(n²) — Quadratic Time

**What it means:** For each element, you're doing work proportional to the number of elements.

**The intuition:** Nested loops over the same data. Comparing every pair of elements.

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):           # n iterations
        for j in range(n - 1):   # n iterations each
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

def two_sum_brute_force(nums, target):
    for i in range(len(nums)):        # For each element
        for j in range(i + 1, len(nums)):  # Check every other
            if nums[i] + nums[j] == target:
                return [i, j]
```

**Where you see it:**
- Brute force pair comparisons
- Simple sorting algorithms (bubble, selection, insertion)
- Matrix traversal (when matrix is n×n)

**Interview tip:** O(n²) is often the naive solution. When you present it, immediately say: "This works, but it's O(n²). Let me see if I can do better with a hash map."

---

### O(2^n) — Exponential Time

**What it means:** Each additional element doubles the work.

**The intuition:** You're exploring all possible subsets or combinations. Each element can be included or excluded, giving you 2^n possibilities.

```python
def all_subsets(nums):
    result = []
    
    def backtrack(index, current):
        if index == len(nums):
            result.append(current[:])
            return
        
        # Include this element
        current.append(nums[index])
        backtrack(index + 1, current)
        current.pop()
        
        # Exclude this element
        backtrack(index + 1, current)
    
    backtrack(0, [])
    return result
```

**Where you see it:**
- Generating all subsets
- Naive recursive Fibonacci
- Some backtracking problems

**Interview tip:** If you see O(2^n), check if memoization can help. Fibonacci goes from O(2^n) to O(n) with memoization.

---

## Space Complexity: The Other Half

Time isn't the only resource. Space complexity measures how much memory your algorithm needs.

**The key question:** How much extra memory does your algorithm allocate as input grows?

```python
# O(1) space - only using a few variables
def find_max(arr):
    max_val = arr[0]
    for num in arr:
        max_val = max(max_val, num)
    return max_val

# O(n) space - creating a new data structure proportional to input
def reverse_array(arr):
    result = []
    for i in range(len(arr) - 1, -1, -1):
        result.append(arr[i])
    return result

# O(n) space - recursive call stack
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)  # Stack depth is n
```

**Interview tip:** Always mention space complexity alongside time. "This is O(n) time and O(1) space, since we only use a constant number of variables."

---

## The Cheat Sheet

Here's the reference table, but remember—understanding beats memorization.

| Complexity | Name | Example | Feeling |
|------------|------|---------|---------|
| O(1) | Constant | Hash lookup | Instant |
| O(log n) | Logarithmic | Binary search | Barely grows |
| O(n) | Linear | Find max | Fair |
| O(n log n) | Linearithmic | Merge sort | Acceptable |
| O(n²) | Quadratic | Nested loops | Getting slow |
| O(2^n) | Exponential | All subsets | Very slow |
| O(n!) | Factorial | All permutations | Unusable |

---

## How to Analyze Your Code

When the interviewer asks "What's the complexity?", here's how to reason through it:

### Step 1: Identify the Loops

```python
def example(arr):
    for i in range(len(arr)):      # O(n)
        for j in range(len(arr)):  # O(n) for each i
            print(arr[i], arr[j])  # O(1) operation
# Total: O(n) × O(n) × O(1) = O(n²)
```

### Step 2: Watch for Hidden Loops

```python
def example(arr):
    for i in range(len(arr)):
        if arr[i] in arr:  # 'in' on a list is O(n)!
            print("found")
# Total: O(n) × O(n) = O(n²), not O(n)
```

### Step 3: Consider Recursive Depth

```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
# Two recursive calls each time = O(2^n)
# With memoization: O(n)
```

### Step 4: Account for Built-in Operations

| Operation | Complexity |
|-----------|------------|
| `list.append()` | O(1) amortized |
| `list.insert(0, x)` | O(n) |
| `list.pop()` | O(1) |
| `list.pop(0)` | O(n) |
| `x in list` | O(n) |
| `x in set` | O(1) |
| `x in dict` | O(1) |
| `sorted(list)` | O(n log n) |

---

## What Interviewers Actually Want to Hear

When analyzing complexity, follow this pattern:

1. **State the complexity clearly:** "This solution is O(n) time and O(n) space."

2. **Justify it:** "We iterate through the array once, and we store up to n elements in the hash map."

3. **Identify the bottleneck:** "The time complexity is dominated by the single loop through the array."

4. **Discuss trade-offs (if relevant):** "We could do this in O(1) space, but it would require O(n²) time."

5. **Consider improvements:** "If the array were sorted, we could use binary search and get O(log n) lookup."

---

## Common Interview Patterns

| Pattern | Typical Complexity | Example |
|---------|-------------------|---------|
| Hash map to eliminate nested loop | O(n²) → O(n) | Two Sum |
| Sorting to enable binary search | O(n²) → O(n log n) | Find pairs |
| Memoization to avoid recomputation | O(2^n) → O(n) | Fibonacci |
| Two pointers instead of brute force | O(n²) → O(n) | Container with most water |
| Heap for top K elements | O(n log n) → O(n log k) | Kth largest |

---

## Practice Problems

| Problem | Brute Force | Optimal | Key Insight |
|---------|-------------|---------|-------------|
| Two Sum | O(n²) | O(n) | Hash map |
| Contains Duplicate | O(n²) | O(n) | Hash set |
| Maximum Subarray | O(n²) | O(n) | Kadane's algorithm |
| Search Rotated Array | O(n) | O(log n) | Modified binary search |
| Merge Intervals | O(n²) | O(n log n) | Sort first |

---

## Key Takeaways

1. **Big-O describes growth patterns**, not exact measurements. O(2n) simplifies to O(n).

2. **Always explain your reasoning.** "This is O(n) because we iterate once" beats "This is O(n)."

3. **Hash maps are your best friend.** They convert O(n) lookups to O(1), often taking O(n²) solutions to O(n).

4. **Mention both time and space.** Interviewers want to see you consider trade-offs.

5. **Don't optimize prematurely.** A working O(n²) solution is better than an incomplete O(n) solution.

---

## What's Next?

Now that you can analyze code complexity, learn how to choose the right data structure for the job:

👉 [Choosing the Right Data Structure →](./choosing-data-structures)
