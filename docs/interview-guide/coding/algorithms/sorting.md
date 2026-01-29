---
sidebar_position: 1
title: "Sorting Algorithms — Know When to Use Each"
description: >-
  Master sorting algorithms for coding interviews. Quick sort, merge sort,
  counting sort, and when to use each with code in 7 languages.
keywords:
  - sorting algorithms
  - quick sort
  - merge sort
  - counting sort
  - interview preparation
  - partition algorithm

og_title: "Sorting Algorithms — Know When to Use Each"
og_description: "You rarely implement sorting in interviews, but understanding algorithms helps you choose right and analyze complexity."
og_image: "/img/social-card.svg"

date_published: 2026-01-28
date_modified: 2026-01-28
author: shivam
reading_time: 30
content_type: explanation
---

import { LanguageSelector, TimeEstimate, ConfidenceBuilder, DifficultyBadge } from '@site/src/components/interview-guide';
import { CodeTabs } from '@site/src/components/design-patterns/CodeTabs';
import TabItem from '@theme/TabItem';

# Sorting Algorithms: Know When to Use Each

You rarely implement sorting from scratch in interviews—just use the built-in sort. But understanding the algorithms helps you:
1. Choose the right approach
2. Analyze complexity correctly
3. Recognize when a problem is really about partitioning (like Quick Select for K-th element)

The first time I was asked to find the K-th largest element, I sorted the entire array. O(n log n). The interviewer asked, "Can you do better?" **Quick Select uses the partition logic from Quick Sort to find the K-th element in O(n) average time.**

**Know the algorithms, recognize the patterns.**

<LanguageSelector />

<TimeEstimate
  learnTime="30-40 minutes"
  practiceTime="2-3 hours"
  masteryTime="Understanding, not memorization"
  interviewFrequency="15% (directly), 80% (using built-in)"
  difficultyRange="Easy to Medium"
  prerequisites="Big-O Notation, Arrays"
/>

---

## Comparison at a Glance

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Stable? | Use Case |
|-----------|-------------|------------|--------------|-------|---------|----------|
| **Quick Sort** | O(n log n) | O(n log n) | O(n²) | O(log n) | No | General purpose |
| **Merge Sort** | O(n log n) | O(n log n) | O(n log n) | O(n) | Yes | Need stability |
| **Heap Sort** | O(n log n) | O(n log n) | O(n log n) | O(1) | No | Memory limited |
| **Counting Sort** | O(n + k) | O(n + k) | O(n + k) | O(k) | Yes | Small integer range |

---

## Quick Sort

**Best for:** General-purpose, in-place sorting. Understanding partition is key for Quick Select.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def quick_sort(arr: list[int], low: int = 0, high: int | None = None) -> list[int]:
    """
    Quick Sort: Partition around pivot, recursively sort partitions.
    Time: O(n log n) average, O(n²) worst
    Space: O(log n) for recursion stack
    """
    if high is None:
        high = len(arr) - 1
    
    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    
    return arr


def partition(arr: list[int], low: int, high: int) -> int:
    """
    Lomuto partition: Pick last element as pivot.
    Elements <= pivot go to left, > pivot go to right.
    Returns final position of pivot.
    """
    pivot = arr[high]
    i = low - 1  # Boundary of smaller elements
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Place pivot in its final position
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Quick Select: Find K-th smallest in O(n) average
def quick_select(arr: list[int], k: int) -> int:
    """Find k-th smallest element (1-indexed)."""
    def select(low: int, high: int) -> int:
        pivot_idx = partition(arr, low, high)
        
        if pivot_idx == k - 1:
            return arr[pivot_idx]
        elif pivot_idx > k - 1:
            return select(low, pivot_idx - 1)
        else:
            return select(pivot_idx + 1, high)
    
    return select(0, len(arr) - 1)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function quickSort(arr: number[], low = 0, high = arr.length - 1): number[] {
  if (low < high) {
    const pivotIdx = partition(arr, low, high);
    quickSort(arr, low, pivotIdx - 1);
    quickSort(arr, pivotIdx + 1, high);
  }
  return arr;
}

function partition(arr: number[], low: number, high: number): number {
  const pivot = arr[high];
  let i = low - 1;

  for (let j = low; j < high; j++) {
    if (arr[j] <= pivot) {
      i++;
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
  }

  [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
  return i + 1;
}

function quickSelect(arr: number[], k: number): number {
  function select(low: number, high: number): number {
    const pivotIdx = partition(arr, low, high);

    if (pivotIdx === k - 1) return arr[pivotIdx];
    if (pivotIdx > k - 1) return select(low, pivotIdx - 1);
    return select(pivotIdx + 1, high);
  }

  return select(0, arr.length - 1);
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func quickSort(arr []int, low, high int) {
    if low < high {
        pivotIdx := partition(arr, low, high)
        quickSort(arr, low, pivotIdx-1)
        quickSort(arr, pivotIdx+1, high)
    }
}

func partition(arr []int, low, high int) int {
    pivot := arr[high]
    i := low - 1
    
    for j := low; j < high; j++ {
        if arr[j] <= pivot {
            i++
            arr[i], arr[j] = arr[j], arr[i]
        }
    }
    
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i + 1
}

func quickSelect(arr []int, k int) int {
    var selectK func(low, high int) int
    selectK = func(low, high int) int {
        pivotIdx := partition(arr, low, high)
        
        if pivotIdx == k-1 {
            return arr[pivotIdx]
        } else if pivotIdx > k-1 {
            return selectK(low, pivotIdx-1)
        }
        return selectK(pivotIdx+1, high)
    }
    
    return selectK(0, len(arr)-1)
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public void quickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pivotIdx = partition(arr, low, high);
        quickSort(arr, low, pivotIdx - 1);
        quickSort(arr, pivotIdx + 1, high);
    }
}

private int partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    
    return i + 1;
}

public int quickSelect(int[] arr, int k) {
    return select(arr, 0, arr.length - 1, k - 1);
}

private int select(int[] arr, int low, int high, int k) {
    int pivotIdx = partition(arr, low, high);
    
    if (pivotIdx == k) return arr[pivotIdx];
    if (pivotIdx > k) return select(arr, low, pivotIdx - 1, k);
    return select(arr, pivotIdx + 1, high, k);
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(arr[i], arr[j]);
        }
    }
    
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        int pivotIdx = partition(arr, low, high);
        quickSort(arr, low, pivotIdx - 1);
        quickSort(arr, pivotIdx + 1, high);
    }
}

int quickSelect(vector<int>& arr, int k) {
    function<int(int, int)> select = [&](int low, int high) -> int {
        int pivotIdx = partition(arr, low, high);
        
        if (pivotIdx == k - 1) return arr[pivotIdx];
        if (pivotIdx > k - 1) return select(low, pivotIdx - 1);
        return select(pivotIdx + 1, high);
    };
    
    return select(0, arr.size() - 1);
}
```

</TabItem>
<TabItem value="c" label="C">

```c
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int partition(int* arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quickSort(int* arr, int low, int high) {
    if (low < high) {
        int pivotIdx = partition(arr, low, high);
        quickSort(arr, low, pivotIdx - 1);
        quickSort(arr, pivotIdx + 1, high);
    }
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public void QuickSort(int[] arr, int low, int high) {
    if (low < high) {
        int pivotIdx = Partition(arr, low, high);
        QuickSort(arr, low, pivotIdx - 1);
        QuickSort(arr, pivotIdx + 1, high);
    }
}

private int Partition(int[] arr, int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            (arr[i], arr[j]) = (arr[j], arr[i]);
        }
    }
    
    (arr[i + 1], arr[high]) = (arr[high], arr[i + 1]);
    return i + 1;
}

public int QuickSelect(int[] arr, int k) {
    int Select(int low, int high) {
        int pivotIdx = Partition(arr, low, high);
        
        if (pivotIdx == k - 1) return arr[pivotIdx];
        if (pivotIdx > k - 1) return Select(low, pivotIdx - 1);
        return Select(pivotIdx + 1, high);
    }
    
    return Select(0, arr.Length - 1);
}
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="Quick Select is the Real Interview Application">

You won't implement Quick Sort in interviews, but **Quick Select** (using the same partition logic) appears often:
- K-th Largest Element: O(n) average vs O(n log n) with sorting
- Top K Elements: Partial sort with Quick Select

The partition function is the key—it places one element in its final sorted position.

</ConfidenceBuilder>

---

## Merge Sort

**Best for:** Guaranteed O(n log n), stable sorting, linked lists (no random access needed).

<CodeTabs>
<TabItem value="python" label="Python">

```python
def merge_sort(arr: list[int]) -> list[int]:
    """
    Merge Sort: Divide, recursively sort, merge.
    Time: O(n log n) always
    Space: O(n) for the merge step
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted arrays into one sorted array."""
    result: list[int] = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:  # <= for stability
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Append remaining elements
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function mergeSort(arr: number[]): number[] {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left: number[], right: number[]): number[] {
  const result: number[] = [];
  let i = 0;
  let j = 0;

  while (i < left.length && j < right.length) {
    if (left[i] <= right[j]) {
      result.push(left[i++]);
    } else {
      result.push(right[j++]);
    }
  }

  return result.concat(left.slice(i)).concat(right.slice(j));
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func mergeSort(arr []int) []int {
    if len(arr) <= 1 {
        return arr
    }
    
    mid := len(arr) / 2
    left := mergeSort(arr[:mid])
    right := mergeSort(arr[mid:])
    
    return mergeSorted(left, right)
}

func mergeSorted(left, right []int) []int {
    result := make([]int, 0, len(left)+len(right))
    i, j := 0, 0
    
    for i < len(left) && j < len(right) {
        if left[i] <= right[j] {
            result = append(result, left[i])
            i++
        } else {
            result = append(result, right[j])
            j++
        }
    }
    
    result = append(result, left[i:]...)
    result = append(result, right[j:]...)
    return result
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int[] mergeSort(int[] arr) {
    if (arr.length <= 1) return arr;
    
    int mid = arr.length / 2;
    int[] left = mergeSort(Arrays.copyOfRange(arr, 0, mid));
    int[] right = mergeSort(Arrays.copyOfRange(arr, mid, arr.length));
    
    return merge(left, right);
}

private int[] merge(int[] left, int[] right) {
    int[] result = new int[left.length + right.length];
    int i = 0, j = 0, k = 0;
    
    while (i < left.length && j < right.length) {
        if (left[i] <= right[j]) {
            result[k++] = left[i++];
        } else {
            result[k++] = right[j++];
        }
    }
    
    while (i < left.length) result[k++] = left[i++];
    while (j < right.length) result[k++] = right[j++];
    
    return result;
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<int> mergeSort(vector<int> arr) {
    if (arr.size() <= 1) return arr;
    
    int mid = arr.size() / 2;
    vector<int> left(arr.begin(), arr.begin() + mid);
    vector<int> right(arr.begin() + mid, arr.end());
    
    left = mergeSort(left);
    right = mergeSort(right);
    
    return mergeSorted(left, right);
}

vector<int> mergeSorted(vector<int>& left, vector<int>& right) {
    vector<int> result;
    int i = 0, j = 0;
    
    while (i < left.size() && j < right.size()) {
        if (left[i] <= right[j]) {
            result.push_back(left[i++]);
        } else {
            result.push_back(right[j++]);
        }
    }
    
    while (i < left.size()) result.push_back(left[i++]);
    while (j < right.size()) result.push_back(right[j++]);
    
    return result;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
void merge(int* arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;
    
    int* L = (int*)malloc(n1 * sizeof(int));
    int* R = (int*)malloc(n2 * sizeof(int));
    
    for (int i = 0; i < n1; i++) L[i] = arr[left + i];
    for (int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];
    
    int i = 0, j = 0, k = left;
    
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k++] = L[i++];
        } else {
            arr[k++] = R[j++];
        }
    }
    
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
    
    free(L);
    free(R);
}

void mergeSort(int* arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);
        merge(arr, left, mid, right);
    }
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int[] MergeSort(int[] arr) {
    if (arr.Length <= 1) return arr;
    
    int mid = arr.Length / 2;
    int[] left = MergeSort(arr[..mid]);
    int[] right = MergeSort(arr[mid..]);
    
    return Merge(left, right);
}

private int[] Merge(int[] left, int[] right) {
    var result = new int[left.Length + right.Length];
    int i = 0, j = 0, k = 0;
    
    while (i < left.Length && j < right.Length) {
        if (left[i] <= right[j]) {
            result[k++] = left[i++];
        } else {
            result[k++] = right[j++];
        }
    }
    
    while (i < left.Length) result[k++] = left[i++];
    while (j < right.Length) result[k++] = right[j++];
    
    return result;
}
```

</TabItem>
</CodeTabs>

---

## Counting Sort

**Best for:** Small range of integers. O(n + k) when k (range) is small.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def counting_sort(arr: list[int]) -> list[int]:
    """
    Counting Sort: Count occurrences, calculate positions.
    Time: O(n + k) where k is the range of input
    Space: O(k)
    
    Use when: Range of values is small (like sorting ages, grades, etc.)
    """
    if not arr:
        return arr
    
    min_val, max_val = min(arr), max(arr)
    range_size = max_val - min_val + 1
    
    # Count occurrences
    count: list[int] = [0] * range_size
    for num in arr:
        count[num - min_val] += 1
    
    # Cumulative count (position calculation)
    for i in range(1, range_size):
        count[i] += count[i - 1]
    
    # Build output (reverse iteration for stability)
    output: list[int] = [0] * len(arr)
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
    
    return output
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function countingSort(arr: number[]): number[] {
  if (arr.length === 0) return arr;

  const minVal = Math.min(...arr);
  const maxVal = Math.max(...arr);
  const rangeSize = maxVal - minVal + 1;

  const count: number[] = new Array(rangeSize).fill(0);
  for (const num of arr) {
    count[num - minVal]++;
  }

  for (let i = 1; i < rangeSize; i++) {
    count[i] += count[i - 1];
  }

  const output: number[] = new Array(arr.length);
  for (let i = arr.length - 1; i >= 0; i--) {
    output[count[arr[i] - minVal] - 1] = arr[i];
    count[arr[i] - minVal]--;
  }

  return output;
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public int[] countingSort(int[] arr) {
    if (arr.length == 0) return arr;
    
    int minVal = Arrays.stream(arr).min().getAsInt();
    int maxVal = Arrays.stream(arr).max().getAsInt();
    int rangeSize = maxVal - minVal + 1;
    
    int[] count = new int[rangeSize];
    for (int num : arr) {
        count[num - minVal]++;
    }
    
    for (int i = 1; i < rangeSize; i++) {
        count[i] += count[i - 1];
    }
    
    int[] output = new int[arr.length];
    for (int i = arr.length - 1; i >= 0; i--) {
        output[count[arr[i] - minVal] - 1] = arr[i];
        count[arr[i] - minVal]--;
    }
    
    return output;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func countingSort(arr []int) []int {
    if len(arr) == 0 {
        return arr
    }
    
    minVal, maxVal := arr[0], arr[0]
    for _, num := range arr {
        if num < minVal {
            minVal = num
        }
        if num > maxVal {
            maxVal = num
        }
    }
    
    rangeSize := maxVal - minVal + 1
    count := make([]int, rangeSize)
    
    for _, num := range arr {
        count[num-minVal]++
    }
    
    for i := 1; i < rangeSize; i++ {
        count[i] += count[i-1]
    }
    
    output := make([]int, len(arr))
    for i := len(arr) - 1; i >= 0; i-- {
        output[count[arr[i]-minVal]-1] = arr[i]
        count[arr[i]-minVal]--
    }
    
    return output
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<int> countingSort(vector<int>& arr) {
    if (arr.empty()) return arr;
    
    int minVal = *min_element(arr.begin(), arr.end());
    int maxVal = *max_element(arr.begin(), arr.end());
    int rangeSize = maxVal - minVal + 1;
    
    vector<int> count(rangeSize, 0);
    for (int num : arr) {
        count[num - minVal]++;
    }
    
    for (int i = 1; i < rangeSize; i++) {
        count[i] += count[i - 1];
    }
    
    vector<int> output(arr.size());
    for (int i = arr.size() - 1; i >= 0; i--) {
        output[count[arr[i] - minVal] - 1] = arr[i];
        count[arr[i] - minVal]--;
    }
    
    return output;
}
```

</TabItem>
<TabItem value="c" label="C">

```c
void countingSort(int* arr, int n) {
    if (n == 0) return;
    
    int minVal = arr[0], maxVal = arr[0];
    for (int i = 1; i < n; i++) {
        if (arr[i] < minVal) minVal = arr[i];
        if (arr[i] > maxVal) maxVal = arr[i];
    }
    
    int rangeSize = maxVal - minVal + 1;
    int* count = (int*)calloc(rangeSize, sizeof(int));
    int* output = (int*)malloc(n * sizeof(int));
    
    for (int i = 0; i < n; i++) {
        count[arr[i] - minVal]++;
    }
    
    for (int i = 1; i < rangeSize; i++) {
        count[i] += count[i - 1];
    }
    
    for (int i = n - 1; i >= 0; i--) {
        output[count[arr[i] - minVal] - 1] = arr[i];
        count[arr[i] - minVal]--;
    }
    
    memcpy(arr, output, n * sizeof(int));
    free(count);
    free(output);
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public int[] CountingSort(int[] arr) {
    if (arr.Length == 0) return arr;
    
    int minVal = arr.Min();
    int maxVal = arr.Max();
    int rangeSize = maxVal - minVal + 1;
    
    int[] count = new int[rangeSize];
    foreach (int num in arr) {
        count[num - minVal]++;
    }
    
    for (int i = 1; i < rangeSize; i++) {
        count[i] += count[i - 1];
    }
    
    int[] output = new int[arr.Length];
    for (int i = arr.Length - 1; i >= 0; i--) {
        output[count[arr[i] - minVal] - 1] = arr[i];
        count[arr[i] - minVal]--;
    }
    
    return output;
}
```

</TabItem>
</CodeTabs>

---

## When to Use What

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| General purpose | Built-in sort | Optimized, tested |
| Need stability | Merge Sort | Preserves relative order |
| Memory limited | Heap Sort | O(1) extra space |
| Small integer range | Counting Sort | O(n + k) linear time |
| K-th element | Quick Select | O(n) average |
| Nearly sorted | Insertion Sort | O(n) best case |
| Linked list | Merge Sort | No random access needed |

---

## Interview Applications

| Problem | Sorting Insight |
|---------|-----------------|
| **K-th Largest** | Quick Select (partition) |
| **Merge Intervals** | Sort by start time |
| **Meeting Rooms** | Sort by start/end |
| **Top K Frequent** | Bucket sort by frequency |
| **Sort Colors** | Dutch National Flag (3-way partition) |

---

## 🏋️ Practice Problems

| Problem | Difficulty | Key Insight |
|---------|------------|-------------|
| [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/) | <DifficultyBadge level="medium" /> | Quick Select |
| [Sort Colors](https://leetcode.com/problems/sort-colors/) | <DifficultyBadge level="medium" /> | Dutch National Flag |
| [Top K Frequent](https://leetcode.com/problems/top-k-frequent-elements/) | <DifficultyBadge level="medium" /> | Bucket sort |
| [Merge Intervals](https://leetcode.com/problems/merge-intervals/) | <DifficultyBadge level="medium" /> | Sort by start |
| [Sort List](https://leetcode.com/problems/sort-list/) | <DifficultyBadge level="medium" /> | Merge Sort on linked list |

---

## Key Takeaways

1. **Use built-in sort** in interviews unless asked otherwise.

2. **Know partition**—it's the basis of Quick Select for K-th element problems.

3. **Merge Sort** for stability or linked lists.

4. **Counting Sort** for small integer ranges—beats O(n log n).

5. **Quick Select** finds K-th element in O(n) average—better than sorting.

<ConfidenceBuilder type="youve-got-this">

**Sorting knowledge is about recognition, not implementation.**

In interviews, use the built-in sort and state the complexity. Know when partition-based thinking (Quick Select) can solve K-th element problems faster than sorting.

</ConfidenceBuilder>

---

## What's Next?

Greedy algorithms for interval problems and optimization:

**Next up:** [Greedy Patterns](/docs/interview-guide/coding/patterns/greedy-patterns/intervals) — Interval Scheduling
