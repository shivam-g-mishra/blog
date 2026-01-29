---
sidebar_position: 3
title: "Prefix Sum — O(1) Range Queries"
description: >-
  Master the prefix sum technique for coding interviews. Range sum queries,
  subarray sum equals K, and 2D matrix prefix sums with code in 7 languages.
keywords:
  - prefix sum
  - cumulative sum
  - range sum query
  - subarray sum
  - 2D prefix sum

og_title: "Prefix Sum — O(1) Range Queries"
og_description: "Turn range queries from O(n) to O(1) with prefix sums. Essential technique for subarray problems."
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

# Prefix Sum: O(1) Range Queries

The first time I saw "find the number of subarrays with sum equal to K," I tried every possible subarray. O(n²).

Then I learned prefix sum + hash map. Same problem, O(n).

**Prefix sum turns range queries from O(n) to O(1).**

<LanguageSelector />

<TimeEstimate
  learnTime="20-30 minutes"
  practiceTime="2-3 hours"
  masteryTime="6-8 problems"
  interviewFrequency="35%"
  difficultyRange="Easy to Medium"
  prerequisites="Arrays, Hash Tables"
/>

---

## The Core Idea

```
Array:      [1, 2, 3, 4, 5]
Prefix:  [0, 1, 3, 6, 10, 15]
              ↑  ↑  ↑   ↑   ↑
            p[1] p[2] ...  p[5]

Sum of arr[1:4] = prefix[4] - prefix[1]
                = 10 - 1 = 9  (2+3+4=9 ✓)
```

**Key formula:** `sum(arr[i:j+1]) = prefix[j+1] - prefix[i]`

The extra 0 at the start handles edge cases elegantly.

---

## Building Prefix Sum Array

<CodeTabs>
<TabItem value="python" label="Python">

```python
def build_prefix_sum(arr: list[int]) -> list[int]:
    """
    Build prefix sum array.
    prefix[i] = sum of arr[0:i]
    prefix[0] = 0 (empty prefix)
    
    Time: O(n), Space: O(n)
    """
    prefix: list[int] = [0] * (len(arr) + 1)
    
    for i in range(len(arr)):
        prefix[i + 1] = prefix[i] + arr[i]
    
    return prefix


def range_sum(prefix: list[int], left: int, right: int) -> int:
    """Get sum of arr[left:right+1] in O(1)."""
    return prefix[right + 1] - prefix[left]


# Example
arr = [1, 2, 3, 4, 5]
prefix = build_prefix_sum(arr)  # [0, 1, 3, 6, 10, 15]
print(range_sum(prefix, 1, 3))  # 2+3+4 = 9
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function buildPrefixSum(arr: number[]): number[] {
  const prefix: number[] = [0];

  for (const num of arr) {
    prefix.push(prefix[prefix.length - 1] + num);
  }

  return prefix;
}

function rangeSum(prefix: number[], left: number, right: number): number {
  return prefix[right + 1] - prefix[left];
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func buildPrefixSum(arr []int) []int {
    prefix := make([]int, len(arr)+1)
    
    for i, num := range arr {
        prefix[i+1] = prefix[i] + num
    }
    
    return prefix
}

func rangeSum(prefix []int, left, right int) int {
    return prefix[right+1] - prefix[left]
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int[] buildPrefixSum(int[] arr) {
    int[] prefix = new int[arr.length + 1];
    
    for (int i = 0; i < arr.length; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    
    return prefix;
}

public int rangeSum(int[] prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<int> buildPrefixSum(vector<int>& arr) {
    vector<int> prefix(arr.size() + 1, 0);
    
    for (int i = 0; i < arr.size(); i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    
    return prefix;
}

int rangeSum(vector<int>& prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}
```

</TabItem>
<TabItem value="c" label="C">

```c
int* buildPrefixSum(int* arr, int n) {
    int* prefix = (int*)calloc(n + 1, sizeof(int));
    
    for (int i = 0; i < n; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    
    return prefix;
}

int rangeSum(int* prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int[] BuildPrefixSum(int[] arr) {
    int[] prefix = new int[arr.Length + 1];
    
    for (int i = 0; i < arr.Length; i++) {
        prefix[i + 1] = prefix[i] + arr[i];
    }
    
    return prefix;
}

public int RangeSum(int[] prefix, int left, int right) {
    return prefix[right + 1] - prefix[left];
}
```

</TabItem>
</CodeTabs>

---

## Pattern 1: Range Sum Query (Class)

Handle multiple range queries efficiently.

<CodeTabs>
<TabItem value="python" label="Python">

```python
class NumArray:
    """
    Range Sum Query - Immutable
    Build once, query many times in O(1).
    """
    
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for num in nums:
            self.prefix.append(self.prefix[-1] + num)
    
    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]


# Usage
nums = [-2, 0, 3, -5, 2, -1]
obj = NumArray(nums)
print(obj.sum_range(0, 2))  # -2+0+3 = 1
print(obj.sum_range(2, 5))  # 3-5+2-1 = -1
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class NumArray {
  private prefix: number[];

  constructor(nums: number[]) {
    this.prefix = [0];
    for (const num of nums) {
      this.prefix.push(this.prefix[this.prefix.length - 1] + num);
    }
  }

  sumRange(left: number, right: number): number {
    return this.prefix[right + 1] - this.prefix[left];
  }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type NumArray struct {
    prefix []int
}

func Constructor(nums []int) NumArray {
    prefix := make([]int, len(nums)+1)
    for i, num := range nums {
        prefix[i+1] = prefix[i] + num
    }
    return NumArray{prefix}
}

func (this *NumArray) SumRange(left int, right int) int {
    return this.prefix[right+1] - this.prefix[left]
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
class NumArray {
    private int[] prefix;
    
    public NumArray(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }
    
    public int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class NumArray {
private:
    vector<int> prefix;
    
public:
    NumArray(vector<int>& nums) {
        prefix.resize(nums.size() + 1, 0);
        for (int i = 0; i < nums.size(); i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }
    
    int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
};
```

</TabItem>
<TabItem value="c" label="C">

```c
typedef struct {
    int* prefix;
    int size;
} NumArray;

NumArray* numArrayCreate(int* nums, int numsSize) {
    NumArray* obj = (NumArray*)malloc(sizeof(NumArray));
    obj->prefix = (int*)calloc(numsSize + 1, sizeof(int));
    obj->size = numsSize + 1;
    
    for (int i = 0; i < numsSize; i++) {
        obj->prefix[i + 1] = obj->prefix[i] + nums[i];
    }
    
    return obj;
}

int numArraySumRange(NumArray* obj, int left, int right) {
    return obj->prefix[right + 1] - obj->prefix[left];
}

void numArrayFree(NumArray* obj) {
    free(obj->prefix);
    free(obj);
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public class NumArray {
    private int[] prefix;
    
    public NumArray(int[] nums) {
        prefix = new int[nums.Length + 1];
        for (int i = 0; i < nums.Length; i++) {
            prefix[i + 1] = prefix[i] + nums[i];
        }
    }
    
    public int SumRange(int left, int right) {
        return prefix[right + 1] - prefix[left];
    }
}
```

</TabItem>
</CodeTabs>

---

## Pattern 2: Subarray Sum Equals K

**The most important prefix sum pattern.** Combine with hash map.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Count subarrays with sum equal to k.
    
    Key insight: If prefix[j] - prefix[i] = k,
    then sum(nums[i+1:j+1]) = k.
    
    We need to count how many prefix sums equal (current_prefix - k).
    
    Time: O(n), Space: O(n)
    """
    count = 0
    prefix_sum = 0
    prefix_counts: dict[int, int] = {0: 1}  # Empty prefix has sum 0
    
    for num in nums:
        prefix_sum += num
        
        # How many previous prefixes give us a subarray with sum k?
        target = prefix_sum - k
        if target in prefix_counts:
            count += prefix_counts[target]
        
        # Record this prefix sum
        prefix_counts[prefix_sum] = prefix_counts.get(prefix_sum, 0) + 1
    
    return count

# [1,1,1], k=2 → 2 (subarrays [1,1] at positions 0-1 and 1-2)
# [1,2,3], k=3 → 2 (subarrays [1,2] and [3])
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function subarraySum(nums: number[], k: number): number {
  let count = 0;
  let prefixSum = 0;
  const prefixCounts: Map<number, number> = new Map([[0, 1]]);

  for (const num of nums) {
    prefixSum += num;

    const target = prefixSum - k;
    if (prefixCounts.has(target)) {
      count += prefixCounts.get(target)!;
    }

    prefixCounts.set(prefixSum, (prefixCounts.get(prefixSum) || 0) + 1);
  }

  return count;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func subarraySum(nums []int, k int) int {
    count := 0
    prefixSum := 0
    prefixCounts := map[int]int{0: 1}
    
    for _, num := range nums {
        prefixSum += num
        
        target := prefixSum - k
        if c, ok := prefixCounts[target]; ok {
            count += c
        }
        
        prefixCounts[prefixSum]++
    }
    
    return count
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int subarraySum(int[] nums, int k) {
    int count = 0;
    int prefixSum = 0;
    Map<Integer, Integer> prefixCounts = new HashMap<>();
    prefixCounts.put(0, 1);
    
    for (int num : nums) {
        prefixSum += num;
        
        int target = prefixSum - k;
        count += prefixCounts.getOrDefault(target, 0);
        
        prefixCounts.put(prefixSum, prefixCounts.getOrDefault(prefixSum, 0) + 1);
    }
    
    return count;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int subarraySum(vector<int>& nums, int k) {
    int count = 0;
    int prefixSum = 0;
    unordered_map<int, int> prefixCounts;
    prefixCounts[0] = 1;
    
    for (int num : nums) {
        prefixSum += num;
        
        int target = prefixSum - k;
        if (prefixCounts.count(target)) {
            count += prefixCounts[target];
        }
        
        prefixCounts[prefixSum]++;
    }
    
    return count;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
// Note: C implementation would need a hash map library
// Here's a simplified version using array (for small value ranges)
int subarraySum(int* nums, int numsSize, int k) {
    // For production, use a proper hash map implementation
    int count = 0;
    
    for (int i = 0; i < numsSize; i++) {
        int sum = 0;
        for (int j = i; j < numsSize; j++) {
            sum += nums[j];
            if (sum == k) count++;
        }
    }
    
    return count;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int SubarraySum(int[] nums, int k) {
    int count = 0;
    int prefixSum = 0;
    Dictionary<int, int> prefixCounts = new() { { 0, 1 } };
    
    foreach (int num in nums) {
        prefixSum += num;
        
        int target = prefixSum - k;
        if (prefixCounts.ContainsKey(target)) {
            count += prefixCounts[target];
        }
        
        if (!prefixCounts.ContainsKey(prefixSum)) {
            prefixCounts[prefixSum] = 0;
        }
        prefixCounts[prefixSum]++;
    }
    
    return count;
}
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="Why This Works">

If `prefix[j] - prefix[i] = k`, then `sum(nums[i+1...j]) = k`.

The hash map counts how many previous prefix sums equal `(current - k)`. Each one represents a valid subarray ending at the current position.

**Don't forget:** Initialize with `{0: 1}` to handle subarrays starting from index 0.

</ConfidenceBuilder>

---

## Pattern 3: 2D Prefix Sum (Matrix)

<CodeTabs>
<TabItem value="python" label="Python">

```python
class NumMatrix:
    """
    2D Range Sum Query.
    Uses inclusion-exclusion principle.
    """
    
    def __init__(self, matrix: list[list[int]]):
        if not matrix or not matrix[0]:
            return
        
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        
        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]      # Above
                    + self.prefix[r + 1][c]      # Left
                    - self.prefix[r][c]          # Double-counted
                )
    
    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        """Sum of matrix[r1:r2+1, c1:c2+1]."""
        return (
            self.prefix[r2 + 1][c2 + 1]
            - self.prefix[r1][c2 + 1]      # Above region
            - self.prefix[r2 + 1][c1]      # Left region
            + self.prefix[r1][c1]          # Add back double-subtracted
        )
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class NumMatrix {
  private prefix: number[][];

  constructor(matrix: number[][]) {
    if (matrix.length === 0 || matrix[0].length === 0) return;

    const rows = matrix.length;
    const cols = matrix[0].length;
    this.prefix = Array(rows + 1)
      .fill(null)
      .map(() => Array(cols + 1).fill(0));

    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        this.prefix[r + 1][c + 1] =
          matrix[r][c] +
          this.prefix[r][c + 1] +
          this.prefix[r + 1][c] -
          this.prefix[r][c];
      }
    }
  }

  sumRegion(r1: number, c1: number, r2: number, c2: number): number {
    return (
      this.prefix[r2 + 1][c2 + 1] -
      this.prefix[r1][c2 + 1] -
      this.prefix[r2 + 1][c1] +
      this.prefix[r1][c1]
    );
  }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type NumMatrix struct {
    prefix [][]int
}

func Constructor(matrix [][]int) NumMatrix {
    if len(matrix) == 0 || len(matrix[0]) == 0 {
        return NumMatrix{}
    }
    
    rows, cols := len(matrix), len(matrix[0])
    prefix := make([][]int, rows+1)
    for i := range prefix {
        prefix[i] = make([]int, cols+1)
    }
    
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            prefix[r+1][c+1] = matrix[r][c] + 
                prefix[r][c+1] + prefix[r+1][c] - prefix[r][c]
        }
    }
    
    return NumMatrix{prefix}
}

func (this *NumMatrix) SumRegion(r1, c1, r2, c2 int) int {
    return this.prefix[r2+1][c2+1] - this.prefix[r1][c2+1] - 
           this.prefix[r2+1][c1] + this.prefix[r1][c1]
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
class NumMatrix {
    private int[][] prefix;
    
    public NumMatrix(int[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) return;
        
        int rows = matrix.length, cols = matrix[0].length;
        prefix = new int[rows + 1][cols + 1];
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c] +
                    prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c];
            }
        }
    }
    
    public int sumRegion(int r1, int c1, int r2, int c2) {
        return prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] -
               prefix[r2 + 1][c1] + prefix[r1][c1];
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class NumMatrix {
private:
    vector<vector<int>> prefix;
    
public:
    NumMatrix(vector<vector<int>>& matrix) {
        if (matrix.empty() || matrix[0].empty()) return;
        
        int rows = matrix.size(), cols = matrix[0].size();
        prefix.assign(rows + 1, vector<int>(cols + 1, 0));
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1][c + 1] = matrix[r][c] +
                    prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c];
            }
        }
    }
    
    int sumRegion(int r1, int c1, int r2, int c2) {
        return prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1] -
               prefix[r2 + 1][c1] + prefix[r1][c1];
    }
};
```

</TabItem>
<TabItem value="c" label="C">

```c
typedef struct {
    int** prefix;
    int rows;
    int cols;
} NumMatrix;

NumMatrix* numMatrixCreate(int** matrix, int matrixSize, int* matrixColSize) {
    NumMatrix* obj = (NumMatrix*)malloc(sizeof(NumMatrix));
    if (matrixSize == 0 || matrixColSize[0] == 0) {
        obj->prefix = NULL;
        return obj;
    }
    
    int rows = matrixSize, cols = matrixColSize[0];
    obj->rows = rows + 1;
    obj->cols = cols + 1;
    
    obj->prefix = (int**)malloc((rows + 1) * sizeof(int*));
    for (int i = 0; i <= rows; i++) {
        obj->prefix[i] = (int*)calloc(cols + 1, sizeof(int));
    }
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            obj->prefix[r + 1][c + 1] = matrix[r][c] +
                obj->prefix[r][c + 1] + obj->prefix[r + 1][c] - obj->prefix[r][c];
        }
    }
    
    return obj;
}

int numMatrixSumRegion(NumMatrix* obj, int r1, int c1, int r2, int c2) {
    return obj->prefix[r2 + 1][c2 + 1] - obj->prefix[r1][c2 + 1] -
           obj->prefix[r2 + 1][c1] + obj->prefix[r1][c1];
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public class NumMatrix {
    private int[,] prefix;
    
    public NumMatrix(int[][] matrix) {
        if (matrix.Length == 0 || matrix[0].Length == 0) return;
        
        int rows = matrix.Length, cols = matrix[0].Length;
        prefix = new int[rows + 1, cols + 1];
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                prefix[r + 1, c + 1] = matrix[r][c] +
                    prefix[r, c + 1] + prefix[r + 1, c] - prefix[r, c];
            }
        }
    }
    
    public int SumRegion(int r1, int c1, int r2, int c2) {
        return prefix[r2 + 1, c2 + 1] - prefix[r1, c2 + 1] -
               prefix[r2 + 1, c1] + prefix[r1, c1];
    }
}
```

</TabItem>
</CodeTabs>

---

## Classic Problem: Contiguous Array (Equal 0s and 1s)

Transform the problem: treat 0 as -1, find longest subarray with sum 0.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def find_max_length(nums: list[int]) -> int:
    """
    Find longest contiguous subarray with equal 0s and 1s.
    
    Trick: Replace 0 with -1. Now find longest subarray with sum 0.
    If prefix[j] == prefix[i], then sum(nums[i+1:j+1]) = 0.
    
    Time: O(n), Space: O(n)
    """
    prefix_sum = 0
    first_occurrence: dict[int, int] = {0: -1}  # Sum 0 at index -1 (before array)
    max_length = 0
    
    for i, num in enumerate(nums):
        # Treat 0 as -1
        prefix_sum += 1 if num == 1 else -1
        
        if prefix_sum in first_occurrence:
            # Found a subarray with sum 0
            length = i - first_occurrence[prefix_sum]
            max_length = max(max_length, length)
        else:
            # First time seeing this prefix sum
            first_occurrence[prefix_sum] = i
    
    return max_length

# [0,1,0] → 2 ([0,1] or [1,0])
# [0,1,0,1,1,0] → 6 (entire array)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function findMaxLength(nums: number[]): number {
  let prefixSum = 0;
  const firstOccurrence: Map<number, number> = new Map([[0, -1]]);
  let maxLength = 0;

  for (let i = 0; i < nums.length; i++) {
    prefixSum += nums[i] === 1 ? 1 : -1;

    if (firstOccurrence.has(prefixSum)) {
      maxLength = Math.max(maxLength, i - firstOccurrence.get(prefixSum)!);
    } else {
      firstOccurrence.set(prefixSum, i);
    }
  }

  return maxLength;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int findMaxLength(int[] nums) {
    int prefixSum = 0;
    Map<Integer, Integer> firstOccurrence = new HashMap<>();
    firstOccurrence.put(0, -1);
    int maxLength = 0;
    
    for (int i = 0; i < nums.length; i++) {
        prefixSum += nums[i] == 1 ? 1 : -1;
        
        if (firstOccurrence.containsKey(prefixSum)) {
            maxLength = Math.max(maxLength, i - firstOccurrence.get(prefixSum));
        } else {
            firstOccurrence.put(prefixSum, i);
        }
    }
    
    return maxLength;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func findMaxLength(nums []int) int {
    prefixSum := 0
    firstOccurrence := map[int]int{0: -1}
    maxLength := 0
    
    for i, num := range nums {
        if num == 1 {
            prefixSum++
        } else {
            prefixSum--
        }
        
        if idx, ok := firstOccurrence[prefixSum]; ok {
            if length := i - idx; length > maxLength {
                maxLength = length
            }
        } else {
            firstOccurrence[prefixSum] = i
        }
    }
    
    return maxLength
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int findMaxLength(vector<int>& nums) {
    int prefixSum = 0;
    unordered_map<int, int> firstOccurrence;
    firstOccurrence[0] = -1;
    int maxLength = 0;
    
    for (int i = 0; i < nums.size(); i++) {
        prefixSum += nums[i] == 1 ? 1 : -1;
        
        if (firstOccurrence.count(prefixSum)) {
            maxLength = max(maxLength, i - firstOccurrence[prefixSum]);
        } else {
            firstOccurrence[prefixSum] = i;
        }
    }
    
    return maxLength;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int FindMaxLength(int[] nums) {
    int prefixSum = 0;
    Dictionary<int, int> firstOccurrence = new() { { 0, -1 } };
    int maxLength = 0;
    
    for (int i = 0; i < nums.Length; i++) {
        prefixSum += nums[i] == 1 ? 1 : -1;
        
        if (firstOccurrence.ContainsKey(prefixSum)) {
            maxLength = Math.Max(maxLength, i - firstOccurrence[prefixSum]);
        } else {
            firstOccurrence[prefixSum] = i;
        }
    }
    
    return maxLength;
}
```

</TabItem>
</CodeTabs>

---

## 🎯 Pattern Triggers

| Problem Clue | Prefix Sum Variant |
|--------------|-------------------|
| "Sum of range [i, j]" | Basic prefix sum |
| "Count subarrays with sum K" | Prefix sum + hash map |
| "Longest subarray with sum K" | Prefix sum + first occurrence |
| "Equal 0s and 1s" | Transform 0→-1, find sum 0 |
| "2D region sum" | 2D prefix with inclusion-exclusion |
| "Divisible by K" | Prefix sum mod K |

---

## 💬 How to Communicate This in Interviews

**Identifying the pattern:**
> "This involves range sums or counting subarrays. I'll use prefix sums to get O(1) range queries after O(n) preprocessing..."

**Explaining the hash map combination:**
> "If prefix[j] - prefix[i] = k, then the subarray from i+1 to j has sum k. I use a hash map to count how many previous prefix sums equal current - k..."

**For the transform trick:**
> "To find equal 0s and 1s, I'll treat 0 as -1. Then equal counts means sum = 0, which is a standard prefix sum problem..."

---

## 🏋️ Practice Problems

### Warm-Up (Build Confidence)

| Problem | Difficulty | Time |
|---------|------------|------|
| [Range Sum Query - Immutable](https://leetcode.com/problems/range-sum-query-immutable/) | <DifficultyBadge level="easy" /> | 15 min |
| [Running Sum of 1d Array](https://leetcode.com/problems/running-sum-of-1d-array/) | <DifficultyBadge level="easy" /> | 10 min |

### Core Practice (Must Do)

| Problem | Difficulty | Companies | Pattern |
|---------|------------|-----------|---------|
| [Subarray Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/) | <DifficultyBadge level="medium" /> | Meta, Google, Amazon | Hash map |
| [Contiguous Array](https://leetcode.com/problems/contiguous-array/) | <DifficultyBadge level="medium" /> | Meta, Amazon | Transform trick |
| [Range Sum Query 2D](https://leetcode.com/problems/range-sum-query-2d-immutable/) | <DifficultyBadge level="medium" /> | Google, Amazon | 2D prefix |
| [Product of Array Except Self](https://leetcode.com/problems/product-of-array-except-self/) | <DifficultyBadge level="medium" /> | Amazon, Meta | Left/right prefix |

### Challenge (For Mastery)

| Problem | Difficulty | Companies | Why It's Hard |
|---------|------------|-----------|---------------|
| [Subarray Sums Divisible by K](https://leetcode.com/problems/subarray-sums-divisible-by-k/) | <DifficultyBadge level="medium" /> | Amazon, Google | Modular arithmetic |
| [Maximum Size Subarray Sum K](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/) | <DifficultyBadge level="medium" /> | Meta | First occurrence only |
| [Count Number of Nice Subarrays](https://leetcode.com/problems/count-number-of-nice-subarrays/) | <DifficultyBadge level="medium" /> | Amazon | Transform odd→1, even→0 |

---

## Key Takeaways

1. **Prefix sum = O(n) precompute, O(1) queries.**

2. **Subarray sum K = prefix sum + hash map.** The most important combination.

3. **Transform problems:** Equal 0s/1s becomes sum = 0 when 0 → -1.

4. **2D works too** with inclusion-exclusion principle.

5. **Initialize correctly:** `{0: 1}` for counting, `{0: -1}` for longest subarray.

<ConfidenceBuilder type="youve-got-this">

**Prefix sum is a building block, not just a standalone pattern.**

Many problems combine prefix sum with other techniques—hash maps, binary search, sliding window. Master the basics here, and you'll recognize when to apply it elsewhere.

</ConfidenceBuilder>

---

## What's Next?

Graph traversal patterns are essential for connectivity problems:

**Next up:** [Graph Traversal Patterns](/docs/interview-guide/coding/patterns/graph-patterns/traversal) — BFS and DFS
