---
sidebar_position: 1
title: "Bit Manipulation — The Low-Level Toolkit"
description: >-
  Master bit manipulation for coding interviews. XOR tricks, counting bits,
  power of two, and subset generation with code in 7 languages.
keywords:
  - bit manipulation
  - bitwise operators
  - XOR problems
  - single number
  - counting bits

og_title: "Bit Manipulation — The Low-Level Toolkit"
og_description: "XOR finds single elements. n & (n-1) clears bits. Master the tricks that make interviewers smile."
og_image: "/img/social-card.svg"

date_published: 2026-01-28
date_modified: 2026-01-28
author: shivam
reading_time: 25
content_type: explanation
---

import { LanguageSelector, TimeEstimate, ConfidenceBuilder, DifficultyBadge } from '@site/src/components/interview-guide';
import { CodeTabs } from '@site/src/components/design-patterns/CodeTabs';
import TabItem from '@theme/TabItem';

# Bit Manipulation: The Low-Level Toolkit

Bit manipulation problems test understanding of how computers actually store and process data.

The first time I saw "find the single number in an array where every other number appears twice," I used a hash map. O(n) space.

Then I learned XOR. **Same problem, O(1) space.** The interviewer was impressed.

<LanguageSelector />

<TimeEstimate
  learnTime="25-30 minutes"
  practiceTime="2-3 hours"
  masteryTime="8-10 problems"
  interviewFrequency="15%"
  difficultyRange="Easy to Medium"
  prerequisites="Basic binary representation"
/>

---

## Basic Operations Reference

| Operation | Syntax | Example | Result |
|-----------|--------|---------|--------|
| AND | `a & b` | `1010 & 1100` | `1000` |
| OR | `a \| b` | `1010 \| 1100` | `1110` |
| XOR | `a ^ b` | `1010 ^ 1100` | `0110` |
| NOT | `~a` | `~1010` | `0101` |
| Left Shift | `a << n` | `0001 << 2` | `0100` |
| Right Shift | `a >> n` | `1000 >> 2` | `0010` |

---

## XOR Properties (Most Important!)

```
a ^ 0 = a          (identity)
a ^ a = 0          (self-inverse)
a ^ b = b ^ a      (commutative)
(a ^ b) ^ c = a ^ (b ^ c)  (associative)
```

**Why XOR is magical:** Pairs cancel out! `2 ^ 3 ^ 2 = (2 ^ 2) ^ 3 = 0 ^ 3 = 3`

---

## Essential Bit Tricks

<CodeTabs>
<TabItem value="python" label="Python">

```python
# Check if bit at position i is set (0-indexed from right)
def is_bit_set(n: int, i: int) -> bool:
    return (n & (1 << i)) != 0

# Set bit at position i
def set_bit(n: int, i: int) -> int:
    return n | (1 << i)

# Clear bit at position i
def clear_bit(n: int, i: int) -> int:
    return n & ~(1 << i)

# Toggle bit at position i
def toggle_bit(n: int, i: int) -> int:
    return n ^ (1 << i)

# Check if power of 2
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

# Count set bits (Brian Kernighan's algorithm)
def count_bits(n: int) -> int:
    count = 0
    while n:
        n &= (n - 1)  # Clears lowest set bit
        count += 1
    return count

# Get lowest set bit
def lowest_set_bit(n: int) -> int:
    return n & (-n)

# Clear lowest set bit
def clear_lowest_bit(n: int) -> int:
    return n & (n - 1)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function isBitSet(n: number, i: number): boolean {
  return (n & (1 << i)) !== 0;
}

function setBit(n: number, i: number): number {
  return n | (1 << i);
}

function clearBit(n: number, i: number): number {
  return n & ~(1 << i);
}

function toggleBit(n: number, i: number): number {
  return n ^ (1 << i);
}

function isPowerOfTwo(n: number): boolean {
  return n > 0 && (n & (n - 1)) === 0;
}

function countBits(n: number): number {
  let count = 0;
  while (n) {
    n &= n - 1;
    count++;
  }
  return count;
}

function lowestSetBit(n: number): number {
  return n & -n;
}

function clearLowestBit(n: number): number {
  return n & (n - 1);
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func isBitSet(n int, i int) bool {
    return (n & (1 << i)) != 0
}

func setBit(n int, i int) int {
    return n | (1 << i)
}

func clearBit(n int, i int) int {
    return n & ^(1 << i)
}

func toggleBit(n int, i int) int {
    return n ^ (1 << i)
}

func isPowerOfTwo(n int) bool {
    return n > 0 && (n & (n - 1)) == 0
}

func countBits(n int) int {
    count := 0
    for n != 0 {
        n &= n - 1
        count++
    }
    return count
}

func lowestSetBit(n int) int {
    return n & (-n)
}

func clearLowestBit(n int) int {
    return n & (n - 1)
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
boolean isBitSet(int n, int i) {
    return (n & (1 << i)) != 0;
}

int setBit(int n, int i) {
    return n | (1 << i);
}

int clearBit(int n, int i) {
    return n & ~(1 << i);
}

int toggleBit(int n, int i) {
    return n ^ (1 << i);
}

boolean isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int countBits(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}

int lowestSetBit(int n) {
    return n & (-n);
}

int clearLowestBit(int n) {
    return n & (n - 1);
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
bool isBitSet(int n, int i) {
    return (n & (1 << i)) != 0;
}

int setBit(int n, int i) {
    return n | (1 << i);
}

int clearBit(int n, int i) {
    return n & ~(1 << i);
}

int toggleBit(int n, int i) {
    return n ^ (1 << i);
}

bool isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int countBits(int n) {
    int count = 0;
    while (n) {
        n &= (n - 1);
        count++;
    }
    return count;
}

int lowestSetBit(int n) {
    return n & (-n);
}

int clearLowestBit(int n) {
    return n & (n - 1);
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int isBitSet(int n, int i) {
    return (n & (1 << i)) != 0;
}

int setBit(int n, int i) {
    return n | (1 << i);
}

int clearBit(int n, int i) {
    return n & ~(1 << i);
}

int toggleBit(int n, int i) {
    return n ^ (1 << i);
}

int isPowerOfTwo(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

int countBits(int n) {
    int count = 0;
    while (n) {
        n &= (n - 1);
        count++;
    }
    return count;
}

int lowestSetBit(int n) {
    return n & (-n);
}

int clearLowestBit(int n) {
    return n & (n - 1);
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
bool IsBitSet(int n, int i) => (n & (1 << i)) != 0;

int SetBit(int n, int i) => n | (1 << i);

int ClearBit(int n, int i) => n & ~(1 << i);

int ToggleBit(int n, int i) => n ^ (1 << i);

bool IsPowerOfTwo(int n) => n > 0 && (n & (n - 1)) == 0;

int CountBits(int n) {
    int count = 0;
    while (n != 0) {
        n &= (n - 1);
        count++;
    }
    return count;
}

int LowestSetBit(int n) => n & (-n);

int ClearLowestBit(int n) => n & (n - 1);
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="The Power of n & (n-1)">

`n & (n-1)` clears the lowest set bit. This is the most useful trick:
- **Power of 2?** `n & (n-1) == 0` (only one bit set)
- **Count bits?** Clear lowest bit repeatedly, count iterations
- **Clear lowest bit?** Just use `n & (n-1)` directly

</ConfidenceBuilder>

---

## Single Number (XOR Classic)

<CodeTabs>
<TabItem value="python" label="Python">

```python
def single_number(nums: list[int]) -> int:
    """
    Find the element that appears once (others appear twice).
    
    XOR properties:
    - a ^ a = 0 (pairs cancel)
    - a ^ 0 = a (identity)
    
    So XOR of all elements leaves only the unique one.
    Time: O(n), Space: O(1)
    """
    result = 0
    for num in nums:
        result ^= num
    return result

# [2, 3, 2, 4, 3] → 4
# 2^3^2^4^3 = (2^2)^(3^3)^4 = 0^0^4 = 4
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function singleNumber(nums: number[]): number {
  let result = 0;
  for (const num of nums) {
    result ^= num;
  }
  return result;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func singleNumber(nums []int) int {
    result := 0
    for _, num := range nums {
        result ^= num
    }
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int singleNumber(int[] nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int singleNumber(vector<int>& nums) {
    int result = 0;
    for (int num : nums) {
        result ^= num;
    }
    return result;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int singleNumber(int* nums, int numsSize) {
    int result = 0;
    for (int i = 0; i < numsSize; i++) {
        result ^= nums[i];
    }
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int SingleNumber(int[] nums) {
    int result = 0;
    foreach (int num in nums) {
        result ^= num;
    }
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Missing Number

<CodeTabs>
<TabItem value="python" label="Python">

```python
def missing_number(nums: list[int]) -> int:
    """
    Find missing number in [0, n].
    
    XOR approach: XOR all indices [0..n] with all values.
    Pairs cancel, leaving the missing one.
    """
    n = len(nums)
    result = n  # Include n since array has n elements
    
    for i, num in enumerate(nums):
        result ^= i ^ num
    
    return result

# [3, 0, 1] for n=3 → 2 is missing
# XOR: 3 ^ (0^3) ^ (1^0) ^ (2^1) = 3 ^ 3 ^ 1 ^ 3 = 2
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function missingNumber(nums: number[]): number {
  const n = nums.length;
  let result = n;

  for (let i = 0; i < n; i++) {
    result ^= i ^ nums[i];
  }

  return result;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func missingNumber(nums []int) int {
    n := len(nums)
    result := n
    
    for i, num := range nums {
        result ^= i ^ num
    }
    
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int missingNumber(int[] nums) {
    int n = nums.length;
    int result = n;
    
    for (int i = 0; i < n; i++) {
        result ^= i ^ nums[i];
    }
    
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int missingNumber(vector<int>& nums) {
    int n = nums.size();
    int result = n;
    
    for (int i = 0; i < n; i++) {
        result ^= i ^ nums[i];
    }
    
    return result;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int missingNumber(int* nums, int numsSize) {
    int result = numsSize;
    
    for (int i = 0; i < numsSize; i++) {
        result ^= i ^ nums[i];
    }
    
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int MissingNumber(int[] nums) {
    int n = nums.Length;
    int result = n;
    
    for (int i = 0; i < n; i++) {
        result ^= i ^ nums[i];
    }
    
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Counting Bits (DP + Bit Manipulation)

<CodeTabs>
<TabItem value="python" label="Python">

```python
def count_bits(n: int) -> list[int]:
    """
    Count set bits for all numbers from 0 to n.
    
    DP insight: bits(i) = bits(i >> 1) + (i & 1)
    i >> 1 is i/2 (drop last bit), i & 1 is last bit.
    
    Time: O(n), Space: O(n)
    """
    result = [0] * (n + 1)
    
    for i in range(1, n + 1):
        result[i] = result[i >> 1] + (i & 1)
    
    return result

# count_bits(5) → [0, 1, 1, 2, 1, 2]
# 0=0b000, 1=0b001, 2=0b010, 3=0b011, 4=0b100, 5=0b101
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function countBits(n: number): number[] {
  const result: number[] = new Array(n + 1).fill(0);

  for (let i = 1; i <= n; i++) {
    result[i] = result[i >> 1] + (i & 1);
  }

  return result;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func countBits(n int) []int {
    result := make([]int, n+1)
    
    for i := 1; i <= n; i++ {
        result[i] = result[i>>1] + (i & 1)
    }
    
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int[] countBits(int n) {
    int[] result = new int[n + 1];
    
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<int> countBits(int n) {
    vector<int> result(n + 1, 0);
    
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int* countBits(int n, int* returnSize) {
    *returnSize = n + 1;
    int* result = (int*)calloc(n + 1, sizeof(int));
    
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int[] CountBits(int n) {
    int[] result = new int[n + 1];
    
    for (int i = 1; i <= n; i++) {
        result[i] = result[i >> 1] + (i & 1);
    }
    
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Reverse Bits

<CodeTabs>
<TabItem value="python" label="Python">

```python
def reverse_bits(n: int) -> int:
    """
    Reverse bits of a 32-bit unsigned integer.
    
    Process: Take LSB from n, add as MSB to result.
    Repeat 32 times.
    """
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)  # Shift result left, add LSB of n
        n >>= 1  # Shift n right
    return result

# 0b00000010100101000001111010011100
# → 0b00111001011110000010100101000000
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function reverseBits(n: number): number {
  let result = 0;
  for (let i = 0; i < 32; i++) {
    result = (result << 1) | (n & 1);
    n >>>= 1; // Unsigned right shift
  }
  return result >>> 0; // Convert to unsigned
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func reverseBits(n uint32) uint32 {
    var result uint32 = 0
    for i := 0; i < 32; i++ {
        result = (result << 1) | (n & 1)
        n >>= 1
    }
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int reverseBits(int n) {
    int result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>>= 1; // Unsigned right shift
    }
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
uint32_t reverseBits(uint32_t n) {
    uint32_t result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
uint32_t reverseBits(uint32_t n) {
    uint32_t result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public uint ReverseBits(uint n) {
    uint result = 0;
    for (int i = 0; i < 32; i++) {
        result = (result << 1) | (n & 1);
        n >>= 1;
    }
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Bit Manipulation for Subsets

<CodeTabs>
<TabItem value="python" label="Python">

```python
def subsets_bitmask(nums: list[int]) -> list[list[int]]:
    """
    Generate all subsets using bit manipulation.
    
    For n elements, there are 2^n subsets.
    Each bit position represents include (1) or exclude (0).
    
    mask = 0b101 for [a,b,c] → include a and c → [a, c]
    """
    n = len(nums)
    result: list[list[int]] = []
    
    for mask in range(1 << n):  # 0 to 2^n - 1
        subset: list[int] = []
        for i in range(n):
            if mask & (1 << i):  # If bit i is set
                subset.append(nums[i])
        result.append(subset)
    
    return result

# [1, 2, 3] → [[], [1], [2], [1,2], [3], [1,3], [2,3], [1,2,3]]
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function subsetsBitmask(nums: number[]): number[][] {
  const n = nums.length;
  const result: number[][] = [];

  for (let mask = 0; mask < 1 << n; mask++) {
    const subset: number[] = [];
    for (let i = 0; i < n; i++) {
      if (mask & (1 << i)) {
        subset.push(nums[i]);
      }
    }
    result.push(subset);
  }

  return result;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func subsetsBitmask(nums []int) [][]int {
    n := len(nums)
    result := [][]int{}
    
    for mask := 0; mask < (1 << n); mask++ {
        subset := []int{}
        for i := 0; i < n; i++ {
            if mask & (1 << i) != 0 {
                subset = append(subset, nums[i])
            }
        }
        result = append(result, subset)
    }
    
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public List<List<Integer>> subsetsBitmask(int[] nums) {
    int n = nums.length;
    List<List<Integer>> result = new ArrayList<>();
    
    for (int mask = 0; mask < (1 << n); mask++) {
        List<Integer> subset = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.add(nums[i]);
            }
        }
        result.add(subset);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<vector<int>> subsetsBitmask(vector<int>& nums) {
    int n = nums.size();
    vector<vector<int>> result;
    
    for (int mask = 0; mask < (1 << n); mask++) {
        vector<int> subset;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) {
                subset.push_back(nums[i]);
            }
        }
        result.push_back(subset);
    }
    
    return result;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public IList<IList<int>> SubsetsBitmask(int[] nums) {
    int n = nums.Length;
    IList<IList<int>> result = new List<IList<int>>();
    
    for (int mask = 0; mask < (1 << n); mask++) {
        List<int> subset = new();
        for (int i = 0; i < n; i++) {
            if ((mask & (1 << i)) != 0) {
                subset.Add(nums[i]);
            }
        }
        result.Add(subset);
    }
    
    return result;
}
```

</TabItem>
</CodeTabs>

---

## 🎯 Pattern Triggers

| Problem Clue | Bit Trick |
|--------------|-----------|
| "Single element, others appear twice" | XOR all elements |
| "Missing number in [0, n]" | XOR indices and values |
| "Power of 2" | `n & (n-1) == 0` |
| "Count set bits" | `n & (n-1)` repeatedly |
| "All subsets" | Bitmask iteration |
| "Toggle/flip bit" | XOR with 1 |

---

## 💬 How to Communicate This in Interviews

**Identifying XOR solution:**
> "Since pairs cancel out with XOR, I can XOR all elements and the unique one will remain..."

**Explaining n & (n-1):**
> "n & (n-1) clears the lowest set bit. For power of 2, there's only one bit set, so the result is 0..."

**Subset generation:**
> "I'll use a bitmask where each bit represents include or exclude. Iterating from 0 to 2^n-1 covers all subsets..."

---

## 🏋️ Practice Problems

| Problem | Difficulty | Companies | Key Trick |
|---------|------------|-----------|-----------|
| [Single Number](https://leetcode.com/problems/single-number/) | <DifficultyBadge level="easy" /> | Amazon | XOR |
| [Missing Number](https://leetcode.com/problems/missing-number/) | <DifficultyBadge level="easy" /> | Meta, Amazon | XOR with indices |
| [Reverse Bits](https://leetcode.com/problems/reverse-bits/) | <DifficultyBadge level="easy" /> | Apple | Bit by bit |
| [Counting Bits](https://leetcode.com/problems/counting-bits/) | <DifficultyBadge level="easy" /> | Google | DP + bits |
| [Power of Two](https://leetcode.com/problems/power-of-two/) | <DifficultyBadge level="easy" /> | All | n & (n-1) |
| [Single Number II](https://leetcode.com/problems/single-number-ii/) | <DifficultyBadge level="medium" /> | Google | Bit counting |
| [Subsets](https://leetcode.com/problems/subsets/) | <DifficultyBadge level="medium" /> | Meta, Amazon | Bitmask |

---

## Key Takeaways

1. **XOR finds single elements.** Pairs cancel out.

2. **n & (n-1)** clears lowest set bit—the most useful trick.

3. **Bit masks** represent subsets efficiently (2^n possibilities).

4. **Shift for multiply/divide** by powers of 2.

5. **Know the tricks** but also understand why they work.

<ConfidenceBuilder type="youve-got-this">

**Bit manipulation is a toolkit, not a mystery.**

There are maybe 5-6 essential tricks. Master those, and you can handle any bit manipulation problem by combining them.

</ConfidenceBuilder>

---

## What's Next?

Continue exploring more algorithm patterns:

**See also:** [Dynamic Programming](/docs/interview-guide/coding/patterns/dp-patterns/introduction) — Optimization Problems
