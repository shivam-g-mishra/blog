---
sidebar_position: 3
title: "Palindrome Problems Pattern"
description: >-
  Master palindrome problems for coding interviews. Check, expand, longest,
  and partition palindrome problems.
keywords:
  - palindrome problems
  - longest palindrome
  - palindrome partition
  - expand around center
difficulty: Intermediate
estimated_time: 20 minutes
prerequisites:
  - Strings
companies: [Google, Amazon, Meta, Microsoft]
---

# Palindrome Problems: Symmetry Mastery

Palindrome problems appear frequently. Know these patterns.

---

## Check Palindrome

```python
def is_palindrome(s):
    return s == s[::-1]

# Two pointer approach (more control)
def is_palindrome_two_pointer(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    
    return True
```

---

## Valid Palindrome (Alphanumeric Only)

```python
def is_valid_palindrome(s):
    left, right = 0, len(s) - 1
    
    while left < right:
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

---

## Longest Palindromic Substring

### Expand Around Center

```python
def longest_palindrome(s):
    if not s:
        return ""
    
    start, end = 0, 0
    
    for i in range(len(s)):
        # Odd length palindrome
        len1 = expand_around_center(s, i, i)
        # Even length palindrome
        len2 = expand_around_center(s, i, i + 1)
        
        max_len = max(len1, len2)
        
        if max_len > end - start:
            start = i - (max_len - 1) // 2
            end = i + max_len // 2
    
    return s[start:end + 1]

def expand_around_center(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return right - left - 1
```

### Manacher's Algorithm (O(n))

```python
def longest_palindrome_manacher(s):
    # Transform: "abc" → "#a#b#c#"
    t = '#' + '#'.join(s) + '#'
    n = len(t)
    p = [0] * n
    center = right = 0
    
    for i in range(n):
        if i < right:
            mirror = 2 * center - i
            p[i] = min(right - i, p[mirror])
        
        # Expand around i
        while (i - p[i] - 1 >= 0 and 
               i + p[i] + 1 < n and 
               t[i - p[i] - 1] == t[i + p[i] + 1]):
            p[i] += 1
        
        # Update center if expanded past right
        if i + p[i] > right:
            center = i
            right = i + p[i]
    
    # Find max
    max_len, center_idx = max((length, idx) for idx, length in enumerate(p))
    start = (center_idx - max_len) // 2
    return s[start:start + max_len]
```

---

## Palindrome Partitioning

Find all ways to partition string into palindromes.

```python
def partition(s):
    result = []
    
    def backtrack(start, path):
        if start == len(s):
            result.append(path[:])
            return
        
        for end in range(start + 1, len(s) + 1):
            substring = s[start:end]
            if substring == substring[::-1]:
                path.append(substring)
                backtrack(end, path)
                path.pop()
    
    backtrack(0, [])
    return result
```

---

## Minimum Cuts for Palindrome Partitioning

```python
def min_cut(s):
    n = len(s)
    
    # is_palindrome[i][j] = True if s[i:j+1] is palindrome
    is_palindrome = [[False] * n for _ in range(n)]
    
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:
                is_palindrome[i][j] = True
            elif length == 2:
                is_palindrome[i][j] = s[i] == s[j]
            else:
                is_palindrome[i][j] = s[i] == s[j] and is_palindrome[i+1][j-1]
    
    # dp[i] = min cuts for s[0:i+1]
    dp = [float('inf')] * n
    
    for i in range(n):
        if is_palindrome[0][i]:
            dp[i] = 0
        else:
            for j in range(i):
                if is_palindrome[j+1][i]:
                    dp[i] = min(dp[i], dp[j] + 1)
    
    return dp[n - 1]
```

---

## Valid Palindrome II (Remove One Char)

```python
def valid_palindrome_ii(s):
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            # Try removing left or right character
            return (is_palindrome(s, left + 1, right) or 
                    is_palindrome(s, left, right - 1))
        left += 1
        right -= 1
    
    return True

def is_palindrome(s, left, right):
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Valid Palindrome | Easy | Meta |
| Longest Palindromic Substring | Medium | Amazon |
| Palindrome Partitioning | Medium | Google |
| Palindromic Substrings (count) | Medium | Meta |
| Valid Palindrome II | Easy | Meta |
| Shortest Palindrome | Hard | Google |

---

## Key Takeaways

1. **Expand around center** for longest palindrome O(n²).
2. **Two pointers** for simple checks.
3. **Backtracking** for partitioning.
4. **DP for min cuts** in partitioning.
5. **Manacher's** for O(n) longest palindrome (know it exists).
