---
sidebar_position: 9
title: "Tries (Prefix Trees)"
description: >-
  Master tries for coding interviews. Prefix operations, autocomplete,
  word search, and implementation with code in 7 languages.
keywords:
  - trie
  - prefix tree
  - autocomplete
  - word dictionary
  - trie implementation
  - word search

og_title: "Tries (Prefix Trees)"
og_description: "Tries make prefix operations O(L) regardless of dictionary size. Master autocomplete, word search, and spell checking."
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

# Tries: The Prefix Expert

The first time I needed to implement autocomplete in an interview, I reached for a hash set and tried to filter words by prefix. That's O(n × L) where n is dictionary size. The interviewer asked, "What if we have a million words?"

**Tries store strings character by character, enabling O(L) operations where L is string length—regardless of how many strings are stored.**

When you see "prefix," "autocomplete," or "dictionary lookup," think trie.

<LanguageSelector />

<TimeEstimate
  learnTime="25-35 minutes"
  practiceTime="3-4 hours"
  masteryTime="8-10 problems"
  interviewFrequency="25%"
  difficultyRange="Medium to Hard"
  prerequisites="Trees, Hash Tables"
/>

---

## Trie Structure

```
Words: ["cat", "car", "card", "care", "dog"]

        root
       /    \
      c      d
      |      |
      a      o
     /|\     |
    t r*     g*
    * |
     /|\
    d* e*
    
* = end of word
```

Each node contains:
- Map of children (character → child node)
- Boolean flag for "is this a complete word?"

---

## When to Use Tries

| Problem Type | Why Trie Wins |
|--------------|---------------|
| Autocomplete | Find all words with prefix in O(L + results) |
| Spell checker | Fast dictionary lookup in O(L) |
| IP routing | Longest prefix matching |
| Word games | Valid word checking |
| Search suggestions | Ranked prefix matches |

---

## Core Implementation

<CodeTabs>
<TabItem value="python" label="Python">

```python
class TrieNode:
    def __init__(self):
        self.children: dict[str, 'TrieNode'] = {}
        self.is_end: bool = False


class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        """Insert word into trie. Time: O(L)"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        """Check if word exists (exact match). Time: O(L)"""
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        """Check if any word starts with prefix. Time: O(L)"""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode | None:
        """Navigate to node representing prefix."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
class TrieNode {
  children: Map<string, TrieNode> = new Map();
  isEnd: boolean = false;
}

class Trie {
  private root: TrieNode = new TrieNode();

  insert(word: string): void {
    let node = this.root;
    for (const char of word) {
      if (!node.children.has(char)) {
        node.children.set(char, new TrieNode());
      }
      node = node.children.get(char)!;
    }
    node.isEnd = true;
  }

  search(word: string): boolean {
    const node = this.findNode(word);
    return node !== null && node.isEnd;
  }

  startsWith(prefix: string): boolean {
    return this.findNode(prefix) !== null;
  }

  private findNode(prefix: string): TrieNode | null {
    let node = this.root;
    for (const char of prefix) {
      if (!node.children.has(char)) {
        return null;
      }
      node = node.children.get(char)!;
    }
    return node;
  }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
type TrieNode struct {
    children map[rune]*TrieNode
    isEnd    bool
}

type Trie struct {
    root *TrieNode
}

func NewTrie() *Trie {
    return &Trie{
        root: &TrieNode{children: make(map[rune]*TrieNode)},
    }
}

func (t *Trie) Insert(word string) {
    node := t.root
    for _, char := range word {
        if _, exists := node.children[char]; !exists {
            node.children[char] = &TrieNode{children: make(map[rune]*TrieNode)}
        }
        node = node.children[char]
    }
    node.isEnd = true
}

func (t *Trie) Search(word string) bool {
    node := t.findNode(word)
    return node != nil && node.isEnd
}

func (t *Trie) StartsWith(prefix string) bool {
    return t.findNode(prefix) != nil
}

func (t *Trie) findNode(prefix string) *TrieNode {
    node := t.root
    for _, char := range prefix {
        if _, exists := node.children[char]; !exists {
            return nil
        }
        node = node.children[char]
    }
    return node
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
class TrieNode {
    Map<Character, TrieNode> children = new HashMap<>();
    boolean isEnd = false;
}

class Trie {
    private TrieNode root = new TrieNode();
    
    public void insert(String word) {
        TrieNode node = root;
        for (char c : word.toCharArray()) {
            node.children.putIfAbsent(c, new TrieNode());
            node = node.children.get(c);
        }
        node.isEnd = true;
    }
    
    public boolean search(String word) {
        TrieNode node = findNode(word);
        return node != null && node.isEnd;
    }
    
    public boolean startsWith(String prefix) {
        return findNode(prefix) != null;
    }
    
    private TrieNode findNode(String prefix) {
        TrieNode node = root;
        for (char c : prefix.toCharArray()) {
            if (!node.children.containsKey(c)) {
                return null;
            }
            node = node.children.get(c);
        }
        return node;
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class TrieNode {
public:
    unordered_map<char, TrieNode*> children;
    bool isEnd = false;
};

class Trie {
private:
    TrieNode* root;
    
    TrieNode* findNode(const string& prefix) {
        TrieNode* node = root;
        for (char c : prefix) {
            if (node->children.find(c) == node->children.end()) {
                return nullptr;
            }
            node = node->children[c];
        }
        return node;
    }
    
public:
    Trie() {
        root = new TrieNode();
    }
    
    void insert(const string& word) {
        TrieNode* node = root;
        for (char c : word) {
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->isEnd = true;
    }
    
    bool search(const string& word) {
        TrieNode* node = findNode(word);
        return node != nullptr && node->isEnd;
    }
    
    bool startsWith(const string& prefix) {
        return findNode(prefix) != nullptr;
    }
};
```

</TabItem>
<TabItem value="c" label="C">

```c
#define ALPHABET_SIZE 26

typedef struct TrieNode {
    struct TrieNode* children[ALPHABET_SIZE];
    bool isEnd;
} TrieNode;

typedef struct {
    TrieNode* root;
} Trie;

TrieNode* createNode() {
    TrieNode* node = (TrieNode*)calloc(1, sizeof(TrieNode));
    return node;
}

Trie* trieCreate() {
    Trie* trie = (Trie*)malloc(sizeof(Trie));
    trie->root = createNode();
    return trie;
}

void trieInsert(Trie* obj, char* word) {
    TrieNode* node = obj->root;
    while (*word) {
        int idx = *word - 'a';
        if (!node->children[idx]) {
            node->children[idx] = createNode();
        }
        node = node->children[idx];
        word++;
    }
    node->isEnd = true;
}

bool trieSearch(Trie* obj, char* word) {
    TrieNode* node = obj->root;
    while (*word) {
        int idx = *word - 'a';
        if (!node->children[idx]) return false;
        node = node->children[idx];
        word++;
    }
    return node->isEnd;
}

bool trieStartsWith(Trie* obj, char* prefix) {
    TrieNode* node = obj->root;
    while (*prefix) {
        int idx = *prefix - 'a';
        if (!node->children[idx]) return false;
        node = node->children[idx];
        prefix++;
    }
    return true;
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public class TrieNode {
    public Dictionary<char, TrieNode> Children { get; } = new();
    public bool IsEnd { get; set; }
}

public class Trie {
    private readonly TrieNode root = new();
    
    public void Insert(string word) {
        var node = root;
        foreach (char c in word) {
            if (!node.Children.ContainsKey(c)) {
                node.Children[c] = new TrieNode();
            }
            node = node.Children[c];
        }
        node.IsEnd = true;
    }
    
    public bool Search(string word) {
        var node = FindNode(word);
        return node != null && node.IsEnd;
    }
    
    public bool StartsWith(string prefix) {
        return FindNode(prefix) != null;
    }
    
    private TrieNode? FindNode(string prefix) {
        var node = root;
        foreach (char c in prefix) {
            if (!node.Children.ContainsKey(c)) {
                return null;
            }
            node = node.Children[c];
        }
        return node;
    }
}
```

</TabItem>
</CodeTabs>

---

## Get All Words with Prefix (Autocomplete)

<CodeTabs>
<TabItem value="python" label="Python">

```python
def get_words_with_prefix(self, prefix: str) -> list[str]:
    """
    Get all words starting with prefix.
    Time: O(L + total characters in matching words)
    """
    node = self._find_node(prefix)
    if not node:
        return []
    
    results: list[str] = []
    self._collect_words(node, prefix, results)
    return results

def _collect_words(self, node: TrieNode, path: str, results: list[str]) -> None:
    """DFS to collect all complete words."""
    if node.is_end:
        results.append(path)
    
    for char, child in node.children.items():
        self._collect_words(child, path + char, results)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
getWordsWithPrefix(prefix: string): string[] {
  const node = this.findNode(prefix);
  if (!node) return [];

  const results: string[] = [];
  this.collectWords(node, prefix, results);
  return results;
}

private collectWords(node: TrieNode, path: string, results: string[]): void {
  if (node.isEnd) {
    results.push(path);
  }

  for (const [char, child] of node.children) {
    this.collectWords(child, path + char, results);
  }
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public List<String> getWordsWithPrefix(String prefix) {
    TrieNode node = findNode(prefix);
    if (node == null) return Collections.emptyList();
    
    List<String> results = new ArrayList<>();
    collectWords(node, new StringBuilder(prefix), results);
    return results;
}

private void collectWords(TrieNode node, StringBuilder path, List<String> results) {
    if (node.isEnd) {
        results.add(path.toString());
    }
    
    for (Map.Entry<Character, TrieNode> entry : node.children.entrySet()) {
        path.append(entry.getKey());
        collectWords(entry.getValue(), path, results);
        path.deleteCharAt(path.length() - 1);
    }
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func (t *Trie) GetWordsWithPrefix(prefix string) []string {
    node := t.findNode(prefix)
    if node == nil {
        return []string{}
    }
    
    var results []string
    t.collectWords(node, prefix, &results)
    return results
}

func (t *Trie) collectWords(node *TrieNode, path string, results *[]string) {
    if node.isEnd {
        *results = append(*results, path)
    }
    
    for char, child := range node.children {
        t.collectWords(child, path+string(char), results)
    }
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
vector<string> getWordsWithPrefix(const string& prefix) {
    TrieNode* node = findNode(prefix);
    if (!node) return {};
    
    vector<string> results;
    collectWords(node, prefix, results);
    return results;
}

void collectWords(TrieNode* node, string path, vector<string>& results) {
    if (node->isEnd) {
        results.push_back(path);
    }
    
    for (auto& [c, child] : node->children) {
        collectWords(child, path + c, results);
    }
}
```

</TabItem>
<TabItem value="c" label="C">

```c
void collectWords(TrieNode* node, char* path, int pathLen, 
                  char** results, int* resultCount) {
    if (node->isEnd) {
        results[*resultCount] = (char*)malloc(pathLen + 1);
        strcpy(results[*resultCount], path);
        (*resultCount)++;
    }
    
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) {
            path[pathLen] = 'a' + i;
            path[pathLen + 1] = '\0';
            collectWords(node->children[i], path, pathLen + 1, results, resultCount);
        }
    }
}
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public List<string> GetWordsWithPrefix(string prefix) {
    var node = FindNode(prefix);
    if (node == null) return new List<string>();
    
    var results = new List<string>();
    CollectWords(node, new StringBuilder(prefix), results);
    return results;
}

private void CollectWords(TrieNode node, StringBuilder path, List<string> results) {
    if (node.IsEnd) {
        results.Add(path.ToString());
    }
    
    foreach (var (c, child) in node.Children) {
        path.Append(c);
        CollectWords(child, path, results);
        path.Length--;
    }
}
```

</TabItem>
</CodeTabs>

---

## Word Search II (Trie + DFS)

Find all dictionary words in a grid—the classic trie problem.

<CodeTabs>
<TabItem value="python" label="Python">

```python
def find_words(board: list[list[str]], words: list[str]) -> list[str]:
    """
    Find all words from dictionary that exist in the grid.
    Time: O(M × N × 4^L) where L is max word length
    """
    # Build trie from dictionary
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    results: set[str] = set()
    rows, cols = len(board), len(board[0])
    
    def dfs(r: int, c: int, node: TrieNode, path: str) -> None:
        # Check bounds and visited
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        
        char = board[r][c]
        if char == '#' or char not in node.children:
            return
        
        node = node.children[char]
        path += char
        
        if node.is_end:
            results.add(path)
            # Don't return - might find longer words
        
        # Mark visited
        board[r][c] = '#'
        
        # Explore all 4 directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, node, path)
        
        # Restore cell
        board[r][c] = char
    
    # Start DFS from every cell
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    
    return list(results)
```

</TabItem>
<TabItem value="typescript" label="TypeScript">

```typescript
function findWords(board: string[][], words: string[]): string[] {
  const trie = new Trie();
  for (const word of words) {
    trie.insert(word);
  }

  const results = new Set<string>();
  const rows = board.length;
  const cols = board[0].length;
  const directions = [
    [0, 1],
    [0, -1],
    [1, 0],
    [-1, 0],
  ];

  function dfs(r: number, c: number, node: TrieNode, path: string): void {
    if (r < 0 || r >= rows || c < 0 || c >= cols) return;

    const char = board[r][c];
    if (char === '#' || !node.children.has(char)) return;

    node = node.children.get(char)!;
    path += char;

    if (node.isEnd) {
      results.add(path);
    }

    board[r][c] = '#';

    for (const [dr, dc] of directions) {
      dfs(r + dr, c + dc, node, path);
    }

    board[r][c] = char;
  }

  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      dfs(r, c, trie.root, '');
    }
  }

  return Array.from(results);
}
```

</TabItem>
<TabItem value="java" label="Java">

```java
public List<String> findWords(char[][] board, String[] words) {
    Trie trie = new Trie();
    for (String word : words) {
        trie.insert(word);
    }
    
    Set<String> results = new HashSet<>();
    int rows = board.length;
    int cols = board[0].length;
    int[][] directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            dfs(board, r, c, trie.root, "", results, directions);
        }
    }
    
    return new ArrayList<>(results);
}

private void dfs(char[][] board, int r, int c, TrieNode node, 
                 String path, Set<String> results, int[][] directions) {
    if (r < 0 || r >= board.length || c < 0 || c >= board[0].length) return;
    
    char ch = board[r][c];
    if (ch == '#' || !node.children.containsKey(ch)) return;
    
    node = node.children.get(ch);
    path += ch;
    
    if (node.isEnd) {
        results.add(path);
    }
    
    board[r][c] = '#';
    
    for (int[] dir : directions) {
        dfs(board, r + dir[0], c + dir[1], node, path, results, directions);
    }
    
    board[r][c] = ch;
}
```

</TabItem>
<TabItem value="go" label="Go">

```go
func findWords(board [][]byte, words []string) []string {
    trie := NewTrie()
    for _, word := range words {
        trie.Insert(word)
    }
    
    results := make(map[string]bool)
    rows, cols := len(board), len(board[0])
    directions := [][]int{{0, 1}, {0, -1}, {1, 0}, {-1, 0}}
    
    var dfs func(r, c int, node *TrieNode, path string)
    dfs = func(r, c int, node *TrieNode, path string) {
        if r < 0 || r >= rows || c < 0 || c >= cols {
            return
        }
        
        char := rune(board[r][c])
        if char == '#' {
            return
        }
        if _, exists := node.children[char]; !exists {
            return
        }
        
        node = node.children[char]
        path += string(char)
        
        if node.isEnd {
            results[path] = true
        }
        
        board[r][c] = '#'
        
        for _, dir := range directions {
            dfs(r+dir[0], c+dir[1], node, path)
        }
        
        board[r][c] = byte(char)
    }
    
    for r := 0; r < rows; r++ {
        for c := 0; c < cols; c++ {
            dfs(r, c, trie.root, "")
        }
    }
    
    result := make([]string, 0, len(results))
    for word := range results {
        result = append(result, word)
    }
    return result
}
```

</TabItem>
<TabItem value="cpp" label="C++">

```cpp
class Solution {
    Trie trie;
    set<string> results;
    int rows, cols;
    vector<pair<int, int>> directions = {{0, 1}, {0, -1}, {1, 0}, {-1, 0}};
    
    void dfs(vector<vector<char>>& board, int r, int c, TrieNode* node, string& path) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return;
        
        char ch = board[r][c];
        if (ch == '#' || node->children.find(ch) == node->children.end()) return;
        
        node = node->children[ch];
        path += ch;
        
        if (node->isEnd) {
            results.insert(path);
        }
        
        board[r][c] = '#';
        
        for (auto& [dr, dc] : directions) {
            dfs(board, r + dr, c + dc, node, path);
        }
        
        board[r][c] = ch;
        path.pop_back();
    }
    
public:
    vector<string> findWords(vector<vector<char>>& board, vector<string>& words) {
        for (const string& word : words) {
            trie.insert(word);
        }
        
        rows = board.size();
        cols = board[0].size();
        
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                string path;
                dfs(board, r, c, trie.root, path);
            }
        }
        
        return vector<string>(results.begin(), results.end());
    }
};
```

</TabItem>
<TabItem value="csharp" label="C#">

```csharp
public IList<string> FindWords(char[][] board, string[] words) {
    var trie = new Trie();
    foreach (var word in words) {
        trie.Insert(word);
    }
    
    var results = new HashSet<string>();
    int rows = board.Length;
    int cols = board[0].Length;
    int[][] directions = { new[] {0, 1}, new[] {0, -1}, new[] {1, 0}, new[] {-1, 0} };
    
    void Dfs(int r, int c, TrieNode node, StringBuilder path) {
        if (r < 0 || r >= rows || c < 0 || c >= cols) return;
        
        char ch = board[r][c];
        if (ch == '#' || !node.Children.ContainsKey(ch)) return;
        
        node = node.Children[ch];
        path.Append(ch);
        
        if (node.IsEnd) {
            results.Add(path.ToString());
        }
        
        board[r][c] = '#';
        
        foreach (var dir in directions) {
            Dfs(r + dir[0], c + dir[1], node, path);
        }
        
        board[r][c] = ch;
        path.Length--;
    }
    
    for (int r = 0; r < rows; r++) {
        for (int c = 0; c < cols; c++) {
            Dfs(r, c, trie.Root, new StringBuilder());
        }
    }
    
    return results.ToList();
}
```

</TabItem>
</CodeTabs>

<ConfidenceBuilder type="remember" title="Why Trie + DFS for Word Search II?">

Without a trie, you'd check each cell against each word—O(M × N × W × L) where W is number of words.

With a trie, you traverse the board once, and the trie tells you instantly whether to continue or prune. The trie acts as a "guide" that prevents exploring paths that can't form dictionary words.

</ConfidenceBuilder>

---

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(L) | O(L) per word |
| Search | O(L) | O(1) |
| Prefix search | O(L) | O(1) |
| Get all with prefix | O(L + results) | O(results) |
| Delete | O(L) | O(1) |

Where L = length of word/prefix

---

## 💬 How to Communicate This in Interviews

**Identifying trie problems:**
> "This is a prefix-based problem with dictionary lookup. A trie gives us O(L) operations regardless of dictionary size, compared to O(n × L) with a hash set..."

**Explaining the structure:**
> "Each node represents a character position. We traverse one character at a time. The `isEnd` flag marks complete words..."

**For Word Search II:**
> "I'll build a trie from the dictionary, then DFS from each cell. The trie lets me prune paths early—if the current path isn't a prefix of any word, I stop exploring..."

---

## 🏋️ Practice Problems

### Warm-Up (Build Confidence)

| Problem | Difficulty | Time |
|---------|------------|------|
| [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/) | <DifficultyBadge level="medium" /> | 25 min |
| [Longest Word in Dictionary](https://leetcode.com/problems/longest-word-in-dictionary/) | <DifficultyBadge level="medium" /> | 20 min |

### Core Practice (Must Do)

| Problem | Difficulty | Companies | Key Insight |
|---------|------------|-----------|-------------|
| [Word Search II](https://leetcode.com/problems/word-search-ii/) | <DifficultyBadge level="hard" /> | Amazon, Google, Meta | Trie + DFS pruning |
| [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | <DifficultyBadge level="medium" /> | Meta, Amazon | Wildcard with DFS |
| [Replace Words](https://leetcode.com/problems/replace-words/) | <DifficultyBadge level="medium" /> | Uber, Google | Shortest prefix |
| [Map Sum Pairs](https://leetcode.com/problems/map-sum-pairs/) | <DifficultyBadge level="medium" /> | Amazon | Prefix sum |

### Challenge (For Mastery)

| Problem | Difficulty | Companies | Why It's Hard |
|---------|------------|-----------|---------------|
| [Design Search Autocomplete](https://leetcode.com/problems/design-search-autocomplete-system/) | <DifficultyBadge level="hard" /> | Google, Amazon | Ranking + real-time |
| [Palindrome Pairs](https://leetcode.com/problems/palindrome-pairs/) | <DifficultyBadge level="hard" /> | Google, Airbnb | Trie + palindrome logic |

---

## Key Takeaways

1. **O(L) operations** independent of dictionary size—this is the key advantage.

2. **Prefix operations** are tries' superpower—autocomplete, spell check, longest prefix.

3. **Trie + DFS** is powerful for grid word search problems.

4. **Memory trade-off:** More memory than hash set, but faster prefix operations.

5. **Array vs hash** for children: Array (26 elements) is faster, hash is more flexible for Unicode.

<ConfidenceBuilder type="youve-got-this">

**Tries have a clear use case.**

If you see "prefix," "autocomplete," or "dictionary," think trie. The implementation is straightforward once you understand the node structure.

</ConfidenceBuilder>

---

## What's Next?

Union-Find for tracking connected components with near-O(1) operations:

**Next up:** [Union-Find](/docs/interview-guide/coding/data-structures/union-find) — Track Connected Components
