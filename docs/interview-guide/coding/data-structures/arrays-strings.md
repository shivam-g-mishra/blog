---
sidebar_position: 1
title: "Arrays & Strings — The Foundation"
description: >-
  Master arrays and strings for coding interviews. Learn the essential operations,
  common patterns, and the techniques that solve 40% of interview problems.
keywords:
  - arrays
  - strings
  - coding interview
  - array problems
  - string manipulation
  - data structures
difficulty: Beginner
estimated_time: 25 minutes
prerequisites:
  - Big-O Notation
companies: [All Companies]
---

# Arrays & Strings: Where Every Interview Begins

If you had to master just one data structure for coding interviews, this would be it.

I've tracked the problems I've encountered across 50+ technical interviews. Roughly 40% involved arrays or strings as the primary data structure. Another 30% used arrays as part of a larger solution. That's 70% of problems where array fluency directly impacted my performance.

**Arrays are deceptively simple.** Every programmer knows how to loop through an array. But interviews don't test whether you can loop—they test whether you can recognize when two pointers would eliminate a nested loop, when sorting enables a better solution, or when the problem is really about finding patterns in indices.

This guide will give you that fluency.

---

## Why Arrays Dominate Interviews

Arrays are the default choice for interview questions because:

1. **They're universal.** Every language has arrays. No time wasted explaining the data structure.

2. **They reveal algorithmic thinking.** You can solve most array problems with brute force. The question is whether you can do better.

3. **They scale well in complexity.** Easy array problems are truly easy. Hard array problems require combining multiple patterns.

4. **They're practical.** Arrays reflect real problems—processing logs, analyzing sequences, transforming data.

**When you see an array problem, your first question should be:** "What am I trying to find or optimize?" The answer guides your approach.

---

## The Mental Model

Before diving into techniques, let me share the mental model that transformed how I approach array problems.

**An array is a contiguous block of memory.** This gives you:

- **O(1) access by index** — Jump directly to any position
- **O(n) search** — Without extra information, you must check every element
- **Spatial locality** — Elements near each other are cheap to access together

This means arrays are great when you need:
- Random access (arr[i])
- Sequential processing (iterate start to end)
- In-place modifications (change elements without extra space)

And less ideal when you need:
- Frequent insertions/deletions in the middle
- Fast lookups by value (use a hash set instead)
- Dynamic resizing (use a list/ArrayList)

**Keep this model in mind.** When you see an array problem, ask: "Am I leveraging contiguous memory, or fighting against it?"

---

## Essential Operations

Let me show you the building blocks that combine into solutions.

### Traversal: Forward, Backward, and Indexed

```python
arr = [1, 2, 3, 4, 5]

# Forward traversal - most common
for num in arr:
    print(num)

# Forward with index - when position matters
for i in range(len(arr)):
    print(f"arr[{i}] = {arr[i]}")

# Pythonic indexed traversal
for i, num in enumerate(arr):
    print(f"arr[{i}] = {num}")

# Backward traversal - useful for building results
for i in range(len(arr) - 1, -1, -1):
    print(arr[i])

# Backward with reversed() - cleaner but creates iterator
for num in reversed(arr):
    print(num)
```

**Interview tip:** Use `enumerate()` in Python when you need both index and value. It signals you know the language idioms.

### Slicing: The Power Tool

Slicing lets you work with subarrays elegantly:

```python
arr = [0, 1, 2, 3, 4, 5]

arr[2:5]    # [2, 3, 4] - elements from index 2 to 4
arr[:3]     # [0, 1, 2] - first 3 elements
arr[3:]     # [3, 4, 5] - from index 3 to end
arr[-2:]    # [4, 5] - last 2 elements
arr[::2]    # [0, 2, 4] - every other element
arr[::-1]   # [5, 4, 3, 2, 1, 0] - reversed

# Copy the array (shallow copy)
arr_copy = arr[:]
```

**Important:** Slicing creates a new array, which is O(n) time and space. Don't slice in a loop unless you've accounted for this.

### Common In-Place Operations

```python
arr = [3, 1, 4, 1, 5]

# Swap elements - foundational for many algorithms
arr[0], arr[1] = arr[1], arr[0]  # Now [1, 3, 4, 1, 5]

# Fill with a value
arr = [0] * 5  # [0, 0, 0, 0, 0]

# Reverse in place
arr = [1, 2, 3, 4, 5]
left, right = 0, len(arr) - 1
while left < right:
    arr[left], arr[right] = arr[right], arr[left]
    left += 1
    right -= 1
```

---

## String Essentials

Strings are arrays of characters with extra complexity: **they're immutable in most languages.**

This means every modification creates a new string:

```python
s = "hello"
s = s + " world"  # Creates NEW string, doesn't modify original
# This is O(n) per concatenation!
```

**The immutability trap:** Concatenating in a loop is O(n²):

```python
# BAD - O(n²) because each += creates a new string
result = ""
for char in chars:
    result += char  # Creates new string each time

# GOOD - O(n) using join
result = "".join(chars)

# GOOD - O(n) using list then join
parts = []
for char in chars:
    parts.append(char)  # O(1) append
result = "".join(parts)  # Single O(n) operation
```

**Interview tip:** If you're building a string in a loop, always use a list and join at the end. Interviewers notice this.

### Essential String Operations

```python
s = "hello world"

# Length
len(s)  # 11

# Access (strings are indexable)
s[0]    # 'h'
s[-1]   # 'd'

# Slicing (same as arrays)
s[0:5]  # 'hello'
s[::-1] # 'dlrow olleh'

# Split into array
s.split()       # ['hello', 'world']
s.split('o')    # ['hell', ' w', 'rld']

# Join array into string
'-'.join(['a', 'b', 'c'])  # 'a-b-c'

# Character checks
s.isalpha()     # False (contains space)
s.isdigit()     # False
s.isalnum()     # False
'hello'.isalpha()  # True

# Case
s.lower()       # 'hello world'
s.upper()       # 'HELLO WORLD'

# Find
s.find('world') # 6 (index of first occurrence)
s.find('xyz')   # -1 (not found)
'world' in s    # True
```

### Character-Level Processing

Many string problems require character-by-character analysis:

```python
s = "Hello World"

# Count character occurrences
from collections import Counter
counts = Counter(s.lower())  # {'l': 3, 'o': 2, 'h': 1, ...}

# Check if two strings are anagrams
def is_anagram(s1, s2):
    return Counter(s1.lower()) == Counter(s2.lower())

# Convert to character codes (useful for problems about letters)
ord('a')  # 97
ord('A')  # 65
chr(97)   # 'a'

# Character index (0-25 for lowercase letters)
char = 'c'
index = ord(char) - ord('a')  # 2
```

---

## The Patterns That Solve Most Problems

Here's where fluency develops. These patterns appear again and again.

### Pattern 1: Two Pointers

When you need to find pairs, reverse, or partition:

```python
def reverse_string(s):
    """Reverse array in-place using two pointers."""
    chars = list(s)
    left, right = 0, len(chars) - 1
    
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    
    return ''.join(chars)

def is_palindrome(s):
    """Check if string is palindrome, ignoring non-alphanumeric."""
    left, right = 0, len(s) - 1
    
    while left < right:
        # Skip non-alphanumeric characters
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True
```

**When to use:** The problem involves pairs from different ends, or you're partitioning the array.

### Pattern 2: Sliding Window

When you need to analyze contiguous subarrays:

```python
def max_sum_subarray(arr, k):
    """Find maximum sum of subarray of size k."""
    if len(arr) < k:
        return 0
    
    # Calculate first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum

def longest_unique_substring(s):
    """Find length of longest substring without repeating characters."""
    char_index = {}
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

**When to use:** The problem mentions "contiguous," "subarray," or "substring," and you need to optimize over all possible windows.

### Pattern 3: Hash Map for O(1) Lookup

Converting O(n²) to O(n):

```python
def two_sum(nums, target):
    """Find indices of two numbers that sum to target."""
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []

def group_anagrams(strs):
    """Group strings that are anagrams of each other."""
    groups = {}  # sorted string -> list of anagrams
    
    for s in strs:
        key = ''.join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
    
    return list(groups.values())
```

**When to use:** You're looking for pairs, checking existence, or grouping by some property.

### Pattern 4: Prefix Sum

When you need quick range sum queries:

```python
def range_sum(arr, queries):
    """Answer multiple range sum queries efficiently."""
    n = len(arr)
    
    # Build prefix sum: prefix[i] = sum of arr[0..i-1]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + arr[i]
    
    # Answer queries in O(1) each
    results = []
    for left, right in queries:
        range_total = prefix[right + 1] - prefix[left]
        results.append(range_total)
    
    return results

def subarray_sum_equals_k(nums, k):
    """Count subarrays with sum equal to k."""
    count = 0
    current_sum = 0
    prefix_counts = {0: 1}  # sum -> count of occurrences
    
    for num in nums:
        current_sum += num
        
        # If (current_sum - k) exists, we found a valid subarray
        if current_sum - k in prefix_counts:
            count += prefix_counts[current_sum - k]
        
        prefix_counts[current_sum] = prefix_counts.get(current_sum, 0) + 1
    
    return count
```

**When to use:** Multiple range queries, or finding subarrays with a target sum.

---

## Common Interview Problems

Here are problems you should be able to solve confidently:

| Problem | Pattern | Key Insight |
|---------|---------|-------------|
| Two Sum | Hash map | Store complement as you iterate |
| Valid Palindrome | Two pointers | Compare from both ends |
| Container With Most Water | Two pointers | Move pointer with smaller height |
| Longest Substring Without Repeating | Sliding window | Track last seen index |
| Product of Array Except Self | Prefix/Suffix | Left products × Right products |
| Maximum Subarray | Kadane's | Reset or extend current sum |
| Merge Intervals | Sort + scan | Sort by start, merge overlaps |
| Valid Anagram | Counter/Sort | Same character frequencies |

---

## Complexity Reference

| Operation | Array | String |
|-----------|-------|--------|
| Access by index | O(1) | O(1) |
| Search | O(n) | O(n) |
| Insert at end | O(1)* | O(n) |
| Insert at beginning | O(n) | O(n) |
| Concatenation | O(n) | O(n) |
| Slice | O(k) | O(k) |
| Reverse | O(n) | O(n) |
| Sort | O(n log n) | O(n log n) |

*Amortized for dynamic arrays (Python lists)

---

## Key Takeaways

1. **Arrays and strings dominate interviews.** Fluency here pays dividends across all problems.

2. **Strings are immutable.** Build with lists, join at the end. Never concatenate in loops.

3. **Two pointers convert O(n²) to O(n)** when working with pairs from opposite ends.

4. **Hash maps convert O(n²) to O(n)** when you need fast lookups.

5. **Sliding window handles contiguous subarray problems** efficiently.

6. **Always consider sorted order.** Sometimes sorting first enables a better algorithm.

---

## What's Next?

Now that you have the foundation, learn the patterns that make array problems tractable:

👉 [Two Pointers Pattern →](../patterns/array-patterns/two-pointers)
