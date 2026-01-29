---
sidebar_position: 9
title: "Tries (Prefix Trees)"
description: >-
  Master tries for coding interviews. Prefix operations, autocomplete,
  word search, and implementation details.
keywords:
  - trie
  - prefix tree
  - autocomplete
  - word dictionary
  - trie implementation
difficulty: Intermediate
estimated_time: 25 minutes
prerequisites:
  - Trees
  - Hash Tables
companies: [Google, Amazon, Microsoft, Meta]
---

# Tries: The Prefix Expert

A trie stores strings character by character, enabling O(L) operations where L is string length—regardless of how many strings are stored.

---

## When to Use Tries

| Use Case | Why Trie |
|----------|----------|
| Autocomplete | Find all words with prefix |
| Spell checker | Fast dictionary lookup |
| IP routing | Longest prefix matching |
| Word games | Valid word checking |

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
    t r g    g*
    * |
     /|\
    d* e*
    
* = end of word
```

---

## Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}  # char -> TrieNode
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word: str) -> bool:
        node = self._find_node(word)
        return node is not None and node.is_end
    
    def starts_with(self, prefix: str) -> bool:
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix: str) -> TrieNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
```

---

## Common Operations

### Get All Words with Prefix

```python
def get_words_with_prefix(self, prefix: str) -> list:
    node = self._find_node(prefix)
    if not node:
        return []
    
    results = []
    self._collect_words(node, prefix, results)
    return results

def _collect_words(self, node: TrieNode, path: str, results: list):
    if node.is_end:
        results.append(path)
    
    for char, child in node.children.items():
        self._collect_words(child, path + char, results)
```

### Delete Word

```python
def delete(self, word: str) -> bool:
    def _delete(node, word, depth):
        if depth == len(word):
            if not node.is_end:
                return False
            node.is_end = False
            return len(node.children) == 0
        
        char = word[depth]
        if char not in node.children:
            return False
        
        should_delete = _delete(node.children[char], word, depth + 1)
        
        if should_delete:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end
        
        return False
    
    _delete(self.root, word, 0)
```

---

## Classic Problems

### Word Search II (Find all words in grid)

```python
def find_words(board, words):
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    results = set()
    rows, cols = len(board), len(board[0])
    
    def dfs(r, c, node, path):
        if node.is_end:
            results.add(path)
        
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        
        char = board[r][c]
        if char not in node.children:
            return
        
        board[r][c] = '#'  # Mark visited
        
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, node.children[char], path + char)
        
        board[r][c] = char  # Restore
    
    for r in range(rows):
        for c in range(cols):
            dfs(r, c, trie.root, "")
    
    return list(results)
```

### Design Add and Search Words

```python
class WordDictionary:
    def __init__(self):
        self.root = TrieNode()
    
    def add_word(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        def dfs(index, node):
            if index == len(word):
                return node.is_end
            
            char = word[index]
            
            if char == '.':
                # Wildcard: try all children
                for child in node.children.values():
                    if dfs(index + 1, child):
                        return True
                return False
            else:
                if char not in node.children:
                    return False
                return dfs(index + 1, node.children[char])
        
        return dfs(0, self.root)
```

---

## Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Insert | O(L) | O(L) |
| Search | O(L) | O(1) |
| Prefix search | O(L) | O(1) |
| Delete | O(L) | O(1) |

Where L = length of word/prefix

---

## Practice Problems

| Problem | Difficulty | Company |
|---------|------------|---------|
| Implement Trie | Medium | Google |
| Word Search II | Hard | Amazon |
| Design Search Autocomplete | Hard | Google |
| Replace Words | Medium | Uber |
| Longest Word in Dictionary | Medium | Microsoft |

---

## Key Takeaways

1. **O(L) operations** independent of dictionary size.
2. **Prefix operations** are tries' superpower.
3. **Memory trade-off:** More memory than hash set.
4. **Array vs hash** for children: Array faster, hash more flexible.
