---
sidebar_position: 2
title: "Substring Problems Pattern"
description: >-
  Master substring problems for coding interviews. Sliding window, hash map
  approaches, and classic problems.
keywords:
  - substring problems
  - longest substring
  - minimum window substring
  - sliding window string
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Sliding Window
  - Hash Tables
companies: [Google, Meta, Amazon, Microsoft]
---

# Substring Problems: Window + Hash Map

Most substring problems combine sliding window with hash maps for character counting.

---

## Longest Substring Without Repeating

```python
def length_of_longest_substring(s):
    char_index = {}  # char -> last seen index
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        if char in char_index and char_index[char] >= start:
            start = char_index[char] + 1
        
        char_index[char] = end
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

---

## Longest Substring with K Distinct Characters

```python
def longest_k_distinct(s, k):
    char_count = {}
    max_length = 0
    start = 0
    
    for end, char in enumerate(s):
        char_count[char] = char_count.get(char, 0) + 1
        
        while len(char_count) > k:
            left_char = s[start]
            char_count[left_char] -= 1
            if char_count[left_char] == 0:
                del char_count[left_char]
            start += 1
        
        max_length = max(max_length, end - start + 1)
    
    return max_length
```

---

## Minimum Window Substring

Find minimum window in `s` that contains all characters of `t`.

```python
from collections import Counter

def min_window(s, t):
    if not t or not s:
        return ""
    
    target_count = Counter(t)
    required = len(target_count)
    
    window_count = {}
    formed = 0
    
    result = (float('inf'), 0, 0)  # (length, left, right)
    left = 0
    
    for right, char in enumerate(s):
        window_count[char] = window_count.get(char, 0) + 1
        
        if char in target_count and window_count[char] == target_count[char]:
            formed += 1
        
        while formed == required:
            # Update result
            if right - left + 1 < result[0]:
                result = (right - left + 1, left, right)
            
            # Shrink window
            left_char = s[left]
            window_count[left_char] -= 1
            if left_char in target_count and window_count[left_char] < target_count[left_char]:
                formed -= 1
            left += 1
    
    return "" if result[0] == float('inf') else s[result[1]:result[2] + 1]
```

---

## Find All Anagrams

```python
from collections import Counter

def find_anagrams(s, p):
    if len(p) > len(s):
        return []
    
    p_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = []
    
    if window_count == p_count:
        result.append(0)
    
    for i in range(len(p), len(s)):
        # Add new character
        window_count[s[i]] += 1
        
        # Remove old character
        old_char = s[i - len(p)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        if window_count == p_count:
            result.append(i - len(p) + 1)
    
    return result
```

---

## Permutation in String

```python
def check_inclusion(s1, s2):
    if len(s1) > len(s2):
        return False
    
    s1_count = Counter(s1)
    window_count = Counter(s2[:len(s1)])
    
    if window_count == s1_count:
        return True
    
    for i in range(len(s1), len(s2)):
        window_count[s2[i]] += 1
        
        old_char = s2[i - len(s1)]
        window_count[old_char] -= 1
        if window_count[old_char] == 0:
            del window_count[old_char]
        
        if window_count == s1_count:
            return True
    
    return False
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Longest Substring Without Repeat | Medium | Amazon |
| Minimum Window Substring | Hard | Meta |
| Find All Anagrams | Medium | Amazon |
| Permutation in String | Medium | Microsoft |
| Longest Substring K Distinct | Medium | Google |
| Longest Repeating Char Replace | Medium | Google |

---

## Key Takeaways

1. **Sliding window + hash map** is the core pattern.
2. **Two pointer approach:** Expand right, shrink left.
3. **Counter comparison** for anagram-type problems.
4. **Track "formed" count** for minimum window problems.
