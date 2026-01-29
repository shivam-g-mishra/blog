---
sidebar_position: 3
title: "Design Search Ranking System"
description: >-
  ML system design for search ranking. Query understanding, retrieval,
  ranking, and personalization.
keywords:
  - search ranking
  - learning to rank
  - ML system design
  - information retrieval
difficulty: Advanced
estimated_time: 40 minutes
prerequisites:
  - ML System Design Introduction
companies: [Google, Amazon, LinkedIn, Airbnb]
---

# Design a Search Ranking System

Search ranking balances relevance, personalization, and business objectives.

---

## Requirements

### Functional
- Return relevant results for queries
- Personalize based on user
- Support filters and facets
- Handle typos and synonyms

### Non-Functional
- **Latency:** < 200ms end-to-end
- **Scale:** Millions of queries/day
- **Relevance:** High precision at top results

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Query                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Query Understanding                           │
│  (Tokenization, spell check, query expansion, intent)           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Retrieval                                │
│  (Get candidate documents - inverted index, ANN)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                          Ranking                                 │
│  (Score and rank using ML model)                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Re-Ranking                                 │
│  (Business rules, diversity, personalization)                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        Search Results
```

---

## Query Understanding

```
"iphone 13 case red"

1. Tokenization: ["iphone", "13", "case", "red"]

2. Spell Correction: 
   "iphon" → "iphone"

3. Query Expansion:
   "iphone" → ["iphone", "apple phone", "iphone 13"]

4. Intent Classification:
   - Navigational (find specific page)
   - Informational (learn something)
   - Transactional (buy something)

5. Entity Recognition:
   - Product: "iphone 13"
   - Attribute: "red"
   - Category: "case"
```

---

## Retrieval

### Inverted Index (Lexical)

```
"iphone" → [doc1, doc5, doc8, doc23, ...]
"case" → [doc2, doc5, doc11, doc23, ...]

Query "iphone case" → intersection → [doc5, doc23, ...]
```

### Semantic Search (Embeddings)

```
Query: "phone cover" 
→ query_embedding = encoder("phone cover")
→ ANN search in document embeddings
→ Returns docs about "iphone case" (semantically similar)
```

### Hybrid Retrieval

```
Lexical results ∪ Semantic results → Combined candidates

Benefits:
- Lexical: Precise matching, handles specific terms
- Semantic: Understands meaning, handles synonyms
```

---

## Ranking Model

### Features

```
Query Features:
- Query length
- Query type/intent
- Historical CTR for query

Document Features:
- Title/description match
- Popularity (views, sales)
- Freshness
- Quality signals (ratings, reviews)

Query-Document Features:
- BM25 score
- Semantic similarity
- Click history for this query-doc pair

User Features:
- Past purchase categories
- Price preference
- Brand affinity
```

### Learning to Rank

```
Approaches:
1. Pointwise: Predict relevance score independently
2. Pairwise: Predict which doc is more relevant
3. Listwise: Optimize ranking metric directly

Common models:
- LambdaMART (gradient boosted trees)
- Neural rankers (BERT-based)
```

---

## Training Data

```
Implicit Signals:
- Clicks (positive)
- Skips (negative)
- Dwell time (engagement)
- Purchases (strong positive)

Label Generation:
click + purchase → highly relevant (3)
click + dwell > 30s → relevant (2)
click + bounce → somewhat relevant (1)
impression only → not relevant (0)

Position Bias Correction:
- Users click top results more often
- Need to debias training data
```

---

## Personalization

```
User History Integration:
- Embed user's past interactions
- Combine with query embedding
- Boost items matching user preferences

Cold Start:
- Use demographic info
- Fallback to popularity
```

---

## Evaluation

### Offline Metrics

```
NDCG@k: Normalized Discounted Cumulative Gain
MRR: Mean Reciprocal Rank
Precision@k: Relevant results in top k
```

### Online Metrics

```
CTR: Click-through rate
Conversion: Purchases per search
Session success: Found what they wanted
Query reformulation: Lower is better
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Retrieval | Hybrid (lexical + semantic) | Best coverage |
| Ranking | LambdaMART or neural | State-of-the-art |
| Features | Query-doc interaction | Most predictive |
| Training | Implicit feedback | Scale |
| Personalization | User embeddings | Real-time adaptation |

---

## Key Takeaways

1. **Multi-stage pipeline** (retrieval → ranking → re-ranking).
2. **Hybrid retrieval** combines lexical precision with semantic understanding.
3. **Learning to rank** on implicit feedback at scale.
4. **Position bias** must be addressed in training.
5. **Balance relevance and personalization** with business objectives.
