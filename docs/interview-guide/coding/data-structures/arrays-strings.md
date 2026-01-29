---
sidebar_position: 1
title: "Arrays & Strings — Complete Interview Guide"
description: >-
  Master arrays and strings for coding interviews. Learn manipulation techniques,
  common patterns, and practice problems asked at Google, Meta, and Amazon.
keywords:
  - array interview questions
  - string manipulation
  - coding interview arrays
  - two pointers technique
  - sliding window
difficulty: Beginner
estimated_time: 45 minutes
prerequisites:
  - Big-O Notation
companies: [Google, Meta, Amazon, Microsoft, Apple]
---

# Arrays & Strings: The Foundation of Coding Interviews

If I had to guess what data structure will appear in your next coding interview, I'd bet on arrays. They're in roughly 60% of all coding questions.

Why? Because arrays are fundamental. They're how we store sequences. They're the input to most problems. And they're the canvas on which patterns like two pointers and sliding window are painted.

**Master arrays, and you've mastered the majority of coding interviews.**

---

## What You Need to Know

### Arrays in Memory

An array is a contiguous block of memory. This matters because:

- **Access by index is O(1)** — The computer jumps directly to the memory address
- **Insertion/deletion in the middle is O(n)** — Everything after the point must shift
- **Cache-friendly** — Sequential access is fast because of CPU caching

```python
# O(1) access
arr = [10, 20, 30, 40, 50]
value = arr[2]  # Directly accesses memory location

# O(n) insertion in middle
arr.insert(2, 25)  # Everything from index 2 shifts right
```

### Strings Are Arrays

In most languages, strings are essentially arrays of characters:

```python
s = "hello"
print(s[0])    # 'h' - O(1) access
print(len(s))  # 5 - O(1) in most languages

# But strings are often immutable
s[0] = 'H'     # Error in Python!
s = 'H' + s[1:]  # Creates new string - O(n)
```

**Key insight: String operations that look O(1) are often O(n)** because they create new strings.

---

## Essential Array Operations

### Basic Operations Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| Access by index | O(1) | Direct memory access |
| Search (unsorted) | O(n) | Must check each element |
| Search (sorted) | O(log n) | Binary search |
| Insert at end | O(1) amortized | May need resize |
| Insert at beginning | O(n) | Shift all elements |
| Delete at end | O(1) | |
| Delete at beginning | O(n) | Shift all elements |

### Common Array Techniques

**1. In-place modification**
Modify the array without extra space:

```python
# Reverse array in-place: O(n) time, O(1) space
def reverse(arr):
    left, right = 0, len(arr) - 1
    while left < right:
        arr[left], arr[right] = arr[right], arr[left]
        left += 1
        right -= 1
```

**2. Two pointers**
Use two indices moving through the array:

```python
# Remove duplicates from sorted array
def remove_duplicates(nums):
    if not nums:
        return 0
    
    write = 1  # Position to write next unique element
    for read in range(1, len(nums)):
        if nums[read] != nums[read - 1]:
            nums[write] = nums[read]
            write += 1
    
    return write
```

**3. Prefix sum**
Precompute cumulative sums for range queries:

```python
# Build prefix sum array
def build_prefix_sum(arr):
    prefix = [0] * (len(arr) + 1)
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    return prefix

# Query sum of range [i, j] in O(1)
def range_sum(prefix, i, j):
    return prefix[j + 1] - prefix[i]
```

---

## Essential String Operations

### String Manipulation Complexity

| Operation | Time | Notes |
|-----------|------|-------|
| Access character | O(1) | |
| Concatenation | O(n + m) | Creates new string |
| Substring | O(k) | Where k is substring length |
| Search substring | O(n × m) naive | O(n) with KMP/Rabin-Karp |
| Compare | O(min(n, m)) | |

### String Techniques

**1. StringBuilder pattern**
When building strings, avoid repeated concatenation:

```python
# Bad: O(n²) - each += creates new string
result = ""
for char in chars:
    result += char

# Good: O(n) - join list at end
result = []
for char in chars:
    result.append(char)
return "".join(result)
```

**2. Character frequency**
Count occurrences with hash map:

```python
from collections import Counter

def char_frequency(s):
    return Counter(s)

# Or manually:
def char_frequency_manual(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq
```

**3. Two-pointer for palindromes**
Check from both ends:

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

---

## The Most Common Patterns

### Pattern 1: Two Pointers

**When to use:** Sorted arrays, finding pairs, removing elements in-place

```python
# Two Sum II (sorted array)
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1  # Need larger sum
        else:
            right -= 1  # Need smaller sum
    
    return []
```

### Pattern 2: Sliding Window

**When to use:** Contiguous subarrays/substrings with a condition

```python
# Maximum sum subarray of size k
def max_sum_subarray(arr, k):
    if len(arr) < k:
        return None
    
    # Initial window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

### Pattern 3: Hash Map for O(1) Lookup

**When to use:** Finding pairs, counting, checking existence

```python
# Two Sum (unsorted)
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
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
    
    for char in s:
        count[char] = count.get(char, 0) + 1
    
    for char in t:
        if char not in count:
            return False
        count[char] -= 1
        if count[char] == 0:
            del count[char]
    
    return len(count) == 0
```

### Problem 2: Container With Most Water

```python
def max_area(height):
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        # Calculate area
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move pointer with smaller height
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_water
```

### Problem 3: Longest Substring Without Repeating Characters

```python
def length_of_longest_substring(s):
    char_index = {}  # char -> last index seen
    max_length = 0
    start = 0  # Window start
    
    for end, char in enumerate(s):
        # If char seen and within current window
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

### Problem 4: Product of Array Except Self

```python
def product_except_self(nums):
    n = len(nums)
    result = [1] * n
    
    # Left products
    left_product = 1
    for i in range(n):
        result[i] = left_product
        left_product *= nums[i]
    
    # Right products
    right_product = 1
    for i in range(n - 1, -1, -1):
        result[i] *= right_product
        right_product *= nums[i]
    
    return result
```

---

## Edge Cases to Always Consider

### Arrays
- Empty array: `[]`
- Single element: `[5]`
- All same elements: `[3, 3, 3, 3]`
- Already sorted: `[1, 2, 3, 4, 5]`
- Reverse sorted: `[5, 4, 3, 2, 1]`
- Negative numbers: `[-1, -2, 3, 4]`
- Contains zero: `[0, 1, 2]`

### Strings
- Empty string: `""`
- Single character: `"a"`
- All same characters: `"aaaa"`
- Palindrome: `"racecar"`
- With spaces: `"hello world"`
- Unicode/special chars: `"héllo"`
- Case sensitivity: `"Hello"` vs `"hello"`

---

## Practice Problems

### Easy

| Problem | Pattern | Company |
|---------|---------|---------|
| Two Sum | Hash Map | Google, Amazon, Meta |
| Valid Anagram | Hash Map | Microsoft, Bloomberg |
| Reverse String | Two Pointers | Apple, Facebook |
| Valid Palindrome | Two Pointers | Meta, Amazon |
| Contains Duplicate | Hash Set | Google, Microsoft |

### Medium

| Problem | Pattern | Company |
|---------|---------|---------|
| 3Sum | Two Pointers + Sort | Google, Meta, Amazon |
| Container With Most Water | Two Pointers | Amazon, Microsoft |
| Longest Substring Without Repeating | Sliding Window | Google, Amazon, Meta |
| Product of Array Except Self | Prefix/Suffix | Amazon, Microsoft |
| Group Anagrams | Hash Map | Google, Meta |

### Hard

| Problem | Pattern | Company |
|---------|---------|---------|
| Trapping Rain Water | Two Pointers/DP | Google, Amazon |
| Minimum Window Substring | Sliding Window | Meta, Google |
| First Missing Positive | In-place Hash | Google, Amazon |

---

## Interview Tips

1. **Always clarify input constraints** — Can there be duplicates? Negative numbers? Empty input?

2. **Start with brute force** — "The naive approach would be O(n²), but I think we can do better..."

3. **Think about sorting** — If the problem involves pairs or searching, sorted input often helps.

4. **Hash maps reduce O(n²) to O(n)** — When you have nested loops, ask: "Can I use a hash map?"

5. **For strings, ask about case sensitivity and special characters.**

6. **Watch out for string concatenation** — Build lists and join at the end.

---

## Key Takeaways

1. **Arrays are O(1) access, O(n) insertion/deletion in middle.**

2. **Strings are often immutable** — concatenation is O(n).

3. **Two pointers work on sorted arrays or when you need pairs.**

4. **Sliding window is for contiguous subarrays/substrings.**

5. **Hash maps turn O(n²) into O(n)** — your most powerful tool.

---

## What's Next?

Arrays often involve hash tables for O(1) lookup. Let's dive deep into hash-based data structures:

👉 [Hash Tables →](./hash-tables)
