---
sidebar_position: 4
title: "Hash Tables — The Interview Essential"
description: >-
  Master hash tables (hash maps, dictionaries) for coding interviews. The data
  structure that turns O(n²) into O(n) and appears in 40% of interview problems.
keywords:
  - hash table interview
  - hash map coding
  - dictionary data structure
  - hash set
  - collision handling
difficulty: Beginner
estimated_time: 35 minutes
prerequisites:
  - Big-O Notation
  - Arrays & Strings
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Hash Tables: Your Most Powerful Interview Tool

Here's a pattern I noticed after 50+ mock interviews: **candidates who instinctively reach for hash maps solve problems 2-3x faster than those who don't.**

When I see nested loops, my first thought is always: "Can I use a hash map to eliminate the inner loop?"

The answer is usually yes.

**If you master one data structure for interviews, make it the hash table.**

---

## Why Hash Tables Matter

Hash tables give you O(1) average-case lookup. That single property is transformative:

```python
# Without hash table: O(n²)
def has_pair_sum_slow(arr, target):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] + arr[j] == target:
                return True
    return False

# With hash table: O(n)
def has_pair_sum_fast(arr, target):
    seen = set()
    for num in arr:
        if target - num in seen:  # O(1) lookup
            return True
        seen.add(num)
    return False
```

That's a 1000x speedup on an array of 1000 elements.

---

## How Hash Tables Work

### The Core Idea

A hash table uses a **hash function** to convert keys into array indices:

```
key → hash_function(key) → index → value
```

```python
# Simplified hash function concept
def simple_hash(key, table_size):
    return hash(key) % table_size

# "apple" might hash to index 3
# "banana" might hash to index 7
```

### Collision Handling

What happens when two keys hash to the same index? Two main approaches:

**Chaining:** Store a list at each index
```python
# Index 3: ["apple" → 5, "cherry" → 8]
# Multiple items can share an index
```

**Open Addressing:** Find the next available slot
```python
# If index 3 is taken, try 4, then 5, etc.
```

**You don't need to implement these in interviews**, but understanding them helps you reason about worst-case scenarios.

---

## Hash Tables in Python

Python's `dict` and `set` are hash tables:

```python
# Dictionary (hash map) - key-value pairs
phone_book = {
    "Alice": "555-1234",
    "Bob": "555-5678"
}

# Set (hash set) - keys only, no values
seen_numbers = {1, 2, 3, 4, 5}

# Common operations - all O(1) average
phone_book["Alice"]           # Get value
phone_book["Charlie"] = "..."  # Set value
"Alice" in phone_book          # Check existence
del phone_book["Bob"]          # Delete

# Set operations
seen_numbers.add(6)            # Add element
5 in seen_numbers              # Check membership
seen_numbers.remove(3)         # Remove element
```

### Complexity

| Operation | Average | Worst |
|-----------|---------|-------|
| Insert | O(1) | O(n) |
| Lookup | O(1) | O(n) |
| Delete | O(1) | O(n) |
| Iterate | O(n) | O(n) |

**Note:** Worst case O(n) happens with many collisions. In practice, with good hash functions, you get O(1).

---

## The Five Hash Table Patterns

### Pattern 1: Existence Check

**Problem:** Check if a complement/match exists.

```python
# Two Sum - the classic hash map problem
def two_sum(nums, target):
    seen = {}  # value → index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []
```

**When to use:** Any time you need to find "another element that satisfies a condition."

### Pattern 2: Counting/Frequency

**Problem:** Count occurrences of elements.

```python
from collections import Counter

# Find majority element (appears > n/2 times)
def majority_element(nums):
    counts = Counter(nums)
    n = len(nums)
    
    for num, count in counts.items():
        if count > n // 2:
            return num
    
    return None

# Manual counting
def count_frequency(arr):
    freq = {}
    for item in arr:
        freq[item] = freq.get(item, 0) + 1
    return freq
```

**When to use:** "Most frequent," "count occurrences," "appears more than k times."

### Pattern 3: Grouping

**Problem:** Group elements by some property.

```python
from collections import defaultdict

# Group anagrams
def group_anagrams(strs):
    groups = defaultdict(list)
    
    for s in strs:
        # Sort string to create canonical key
        key = tuple(sorted(s))
        groups[key].append(s)
    
    return list(groups.values())

# Input: ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output: [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```

**When to use:** "Group by property," "find all matching," "categorize."

### Pattern 4: Caching/Memoization

**Problem:** Avoid recomputing results.

```python
# Fibonacci with memoization
def fibonacci(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    
    memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
    return memo[n]
```

**When to use:** Recursive problems with overlapping subproblems.

### Pattern 5: Tracking/State

**Problem:** Track state as you process data.

```python
# Longest substring without repeating characters
def length_of_longest_substring(s):
    char_index = {}  # Track last index of each character
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

**When to use:** Sliding window problems, tracking "last seen," maintaining state.

---

## Hash Set vs Hash Map

| Use Hash Set | Use Hash Map |
|--------------|--------------|
| Only need to check existence | Need to store associated values |
| Finding duplicates | Counting occurrences |
| Membership testing | Key-value associations |
| Set operations (union, intersection) | Looking up by key |

```python
# Hash Set - just checking existence
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

# Hash Map - need to store indices
def two_sum(nums, target):
    seen = {}  # Need index, not just existence
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []
```

---

## Classic Interview Problems

### Problem 1: Valid Anagram

```python
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    
    count = {}
    
    # Count characters in s
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    # Subtract characters in t
    for char in t:
        if char not in count:
            return False
        count[char] -= 1
        if count[char] < 0:
            return False
    
    return True
```

### Problem 2: First Unique Character

```python
def first_uniq_char(s):
    count = {}
    
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    for i, char in enumerate(s):
        if count[char] == 1:
            return i
    
    return -1
```

### Problem 3: Subarray Sum Equals K

```python
def subarray_sum(nums, k):
    count = 0
    prefix_sum = 0
    prefix_counts = {0: 1}  # prefix_sum → frequency
    
    for num in nums:
        prefix_sum += num
        
        # If prefix_sum - k exists, we found a subarray
        if prefix_sum - k in prefix_counts:
            count += prefix_counts[prefix_sum - k]
        
        prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1
    
    return count
```

### Problem 4: LRU Cache

```python
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key not in self.cache:
            return -1
        
        # Move to end (most recently used)
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # Remove oldest
```

---

## Common Mistakes

### 1. Modifying While Iterating

```python
# Wrong - RuntimeError
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    if d[key] < 2:
        del d[key]  # Error!

# Right - iterate over copy
for key in list(d.keys()):
    if d[key] < 2:
        del d[key]
```

### 2. Using Mutable Keys

```python
# Wrong - lists can't be keys
d = {}
d[[1, 2, 3]] = "value"  # TypeError!

# Right - use tuples
d[(1, 2, 3)] = "value"
```

### 3. Assuming Order (Pre-Python 3.7)

```python
# In Python 3.7+, dicts maintain insertion order
# But for interviews, don't rely on this
# Use OrderedDict if order matters
```

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Two Sum | Existence Check | Google, Amazon |
| Valid Anagram | Counting | Microsoft |
| Contains Duplicate | Hash Set | Google |
| First Unique Character | Counting | Amazon |
| Happy Number | Cycle Detection | Apple |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| Group Anagrams | Grouping | Meta, Google |
| Top K Frequent Elements | Counting | Amazon |
| Subarray Sum Equals K | Prefix Sum + Hash | Google |
| Longest Consecutive Sequence | Hash Set | Meta |
| LRU Cache | OrderedDict | Amazon, Meta |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Minimum Window Substring | Hash Map + Window | Meta |
| Word Ladder | BFS + Hash Set | Amazon |
| Alien Dictionary | Hash Map + Topo Sort | Meta |

---

## Interview Tips

1. **Default to hash maps** when you see nested loops. Ask: "Can I store something to avoid the inner loop?"

2. **Use `defaultdict` for grouping:**
   ```python
   from collections import defaultdict
   groups = defaultdict(list)  # No KeyError
   ```

3. **Use `Counter` for counting:**
   ```python
   from collections import Counter
   counts = Counter(arr)  # One line
   ```

4. **State the trade-off:** "We're trading O(n) space for O(n) time instead of O(n²)."

5. **For interviews, assume O(1) operations** unless specifically asked about hash function details.

---

## Key Takeaways

1. **Hash tables give O(1) average lookup** — This is their superpower.

2. **Five patterns cover 90% of hash table problems:** Existence, Counting, Grouping, Caching, Tracking.

3. **Hash Set vs Hash Map:** Set for existence only, Map when you need associated values.

4. **`Counter` and `defaultdict` are your friends** — Use them for cleaner code.

5. **When you see O(n²), think hash map** — It's almost always the optimization.

---

## What's Next?

Now that you understand hash tables, let's explore hierarchical data with trees:

👉 [Trees →](./trees)
