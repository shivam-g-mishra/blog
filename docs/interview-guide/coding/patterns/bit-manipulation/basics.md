---
sidebar_position: 1
title: "Bit Manipulation Patterns"
description: >-
  Master bit manipulation for coding interviews. Common operations,
  tricks, and classic problems.
keywords:
  - bit manipulation
  - bitwise operators
  - bit tricks
  - XOR problems
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Basic programming
companies: [Google, Amazon, Microsoft]
---

# Bit Manipulation: The Low-Level Toolkit

Bit manipulation problems test understanding of how computers actually store and process data.

---

## Basic Operations

| Operation | Syntax | Example |
|-----------|--------|---------|
| AND | `a & b` | `1010 & 1100 = 1000` |
| OR | `a \| b` | `1010 \| 1100 = 1110` |
| XOR | `a ^ b` | `1010 ^ 1100 = 0110` |
| NOT | `~a` | `~1010 = 0101` |
| Left Shift | `a << n` | `0001 << 2 = 0100` |
| Right Shift | `a >> n` | `1000 >> 2 = 0010` |

---

## Common Bit Tricks

```python
# Check if bit at position i is set
def is_bit_set(n, i):
    return (n & (1 << i)) != 0

# Set bit at position i
def set_bit(n, i):
    return n | (1 << i)

# Clear bit at position i
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle bit at position i
def toggle_bit(n, i):
    return n ^ (1 << i)

# Check if power of 2
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0

# Count set bits (Brian Kernighan's algorithm)
def count_bits(n):
    count = 0
    while n:
        n &= (n - 1)  # Clears lowest set bit
        count += 1
    return count

# Get lowest set bit
def lowest_set_bit(n):
    return n & (-n)

# Clear lowest set bit
def clear_lowest_bit(n):
    return n & (n - 1)
```

---

## XOR Properties

```
XOR is incredibly useful:

a ^ 0 = a          (identity)
a ^ a = 0          (self-inverse)
a ^ b = b ^ a      (commutative)
(a ^ b) ^ c = a ^ (b ^ c)  (associative)
```

---

## Classic Problems

### Single Number (XOR)

Find the one element that appears once (others appear twice).

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# [2, 3, 2, 4, 3] → 4
# 2^3^2^4^3 = (2^2)^(3^3)^4 = 0^0^4 = 4
```

### Single Number II (Bit Counting)

Find the one element that appears once (others appear three times).

```python
def single_number_ii(nums):
    result = 0
    for i in range(32):
        bit_sum = sum((num >> i) & 1 for num in nums)
        if bit_sum % 3:
            result |= (1 << i)
    
    # Handle negative numbers in Python
    if result >= 2**31:
        result -= 2**32
    
    return result
```

### Missing Number

Find missing number in [0, n].

```python
def missing_number(nums):
    n = len(nums)
    result = n  # Start with n
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result

# [3, 0, 1] → XOR with indices gives 2
```

### Reverse Bits

```python
def reverse_bits(n):
    result = 0
    for i in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
```

### Counting Bits (1 to n)

```python
def count_bits(n):
    result = [0] * (n + 1)
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    return result

# Uses DP: bits(i) = bits(i/2) + last_bit
```

### Hamming Distance

Count differing bits between two numbers.

```python
def hamming_distance(x, y):
    xor = x ^ y
    count = 0
    while xor:
        count += xor & 1
        xor >>= 1
    return count
```

---

## Bit Manipulation for Subsets

```python
# Generate all subsets using bits
def subsets(nums):
    n = len(nums)
    result = []
    
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        result.append(subset)
    
    return result

# Each bit position represents include/exclude
```

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Single Number | Easy | Amazon |
| Missing Number | Easy | Meta |
| Reverse Bits | Easy | Apple |
| Counting Bits | Easy | Google |
| Power of Two | Easy | All |
| Single Number II | Medium | Google |
| Bitwise AND of Range | Medium | Amazon |

---

## Key Takeaways

1. **XOR finds single elements.** Pairs cancel out.
2. **n & (n-1)** clears lowest set bit—useful for counting.
3. **Bit masks** represent subsets efficiently.
4. **Shift for multiply/divide** by powers of 2.
5. **Know the tricks** but also understand why they work.
