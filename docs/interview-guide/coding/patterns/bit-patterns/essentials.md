---
sidebar_position: 1
title: "Bit Manipulation Essentials"
description: >-
  Master bit manipulation for coding interviews. XOR tricks, bit counting,
  single number problems, and bitwise operations.
keywords:
  - bit manipulation
  - XOR
  - single number
  - counting bits
  - bitwise operations
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Big-O Notation
companies: [Google, Amazon, Apple, Microsoft]
---

# Bit Manipulation: The Low-Level Superpower

Bit manipulation seems arcane, but a few patterns solve many problems elegantly.

---

## Essential Operations

```python
# Check if bit is set
def is_bit_set(n, i):
    return (n >> i) & 1 == 1

# Set bit
def set_bit(n, i):
    return n | (1 << i)

# Clear bit
def clear_bit(n, i):
    return n & ~(1 << i)

# Toggle bit
def toggle_bit(n, i):
    return n ^ (1 << i)

# Count set bits
def count_bits(n):
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count

# Brian Kernighan's algorithm
def count_bits_fast(n):
    count = 0
    while n:
        n &= (n - 1)  # Clear lowest set bit
        count += 1
    return count
```

---

## XOR Properties

```
a ^ a = 0        (same numbers cancel)
a ^ 0 = a        (identity)
a ^ b ^ a = b    (find missing/single)
```

---

## Single Number (Find Unique)

```python
def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result

# Two unique numbers
def single_number_two_unique(nums):
    xor = 0
    for num in nums:
        xor ^= num
    
    # Find rightmost set bit
    diff_bit = xor & (-xor)
    
    a = b = 0
    for num in nums:
        if num & diff_bit:
            a ^= num
        else:
            b ^= num
    
    return [a, b]
```

---

## Power of Two

```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```

---

## Practice Problems

| Problem | Pattern | Company |
|---------|---------|---------|
| Single Number | XOR | Amazon |
| Single Number II | Bit counting | Google |
| Single Number III | XOR + split | Meta |
| Number of 1 Bits | Counting | Apple |
| Power of Two | n & (n-1) | Amazon |
| Reverse Bits | Bit by bit | Apple |
| Missing Number | XOR | Google |

---

## Key Formulas

```
n & (n-1)    → Clear lowest set bit
n & (-n)     → Isolate lowest set bit
n | (n+1)    → Set lowest unset bit
~n           → Flip all bits
```
