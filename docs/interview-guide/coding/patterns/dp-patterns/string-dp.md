---
sidebar_position: 4
title: "String DP Pattern"
description: >-
  Master string dynamic programming for coding interviews. Edit distance,
  longest common subsequence, and regex matching.
keywords:
  - string dp
  - edit distance
  - longest common subsequence
  - regex matching
  - dynamic programming
difficulty: Advanced
estimated_time: 30 minutes
prerequisites:
  - DP Introduction
companies: [Google, Amazon, Meta, Microsoft]
---

# String DP: Two Sequences

String DP problems typically involve two strings and a 2D DP table.

---

## The Pattern

```
dp[i][j] = answer for first i chars of s1 and first j chars of s2
```

---

## Longest Common Subsequence

```python
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]
```

**Recurrence:**
- Match: `dp[i][j] = dp[i-1][j-1] + 1`
- No match: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

---

## Edit Distance (Levenshtein)

Minimum operations (insert, delete, replace) to convert word1 to word2.

```python
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases
    for i in range(m + 1):
        dp[i][0] = i  # Delete all chars
    for j in range(n + 1):
        dp[0][j] = j  # Insert all chars
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # No operation needed
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )
    
    return dp[m][n]
```

---

## Longest Common Substring

```python
def longest_common_substring(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_length = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                max_length = max(max_length, dp[i][j])
            # else: dp[i][j] = 0 (substring must be contiguous)
    
    return max_length
```

---

## Distinct Subsequences

Count ways to form `t` as a subsequence of `s`.

```python
def num_distinct(s, t):
    m, n = len(s), len(t)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Empty t is subsequence of any s
    for i in range(m + 1):
        dp[i][0] = 1
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
            else:
                dp[i][j] = dp[i - 1][j]
    
    return dp[m][n]
```

---

## Regular Expression Matching

```python
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    # Handle patterns like a*, a*b*, etc.
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                # Zero occurrences or one+ occurrences
                dp[i][j] = dp[i][j - 2] or (
                    dp[i - 1][j] and (p[j - 2] == s[i - 1] or p[j - 2] == '.')
                )
            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                dp[i][j] = dp[i - 1][j - 1]
    
    return dp[m][n]
```

---

## Interleaving String

Check if s3 is formed by interleaving s1 and s2.

```python
def is_interleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    
    if m + n != len(s3):
        return False
    
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True
    
    for i in range(1, m + 1):
        dp[i][0] = dp[i - 1][0] and s1[i - 1] == s3[i - 1]
    
    for j in range(1, n + 1):
        dp[0][j] = dp[0][j - 1] and s2[j - 1] == s3[j - 1]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = (
                (dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]) or
                (dp[i][j - 1] and s2[j - 1] == s3[i + j - 1])
            )
    
    return dp[m][n]
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Longest Common Subsequence | Medium | Google |
| Edit Distance | Medium | Amazon |
| Distinct Subsequences | Hard | Google |
| Regular Expression | Hard | Meta |
| Wildcard Matching | Hard | Google |
| Interleaving String | Medium | Amazon |

---

## Key Takeaways

1. **2D table:** `dp[i][j]` for i chars of s1, j chars of s2.
2. **Base cases:** Usually `dp[0][j]` and `dp[i][0]`.
3. **Match vs no-match:** Different recurrence relations.
4. **Space optimization** possible to O(n).
