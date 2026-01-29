---
sidebar_position: 2
title: "Design Recommendation System"
description: >-
  ML system design for recommendation systems. Collaborative filtering,
  content-based, and hybrid approaches at scale.
keywords:
  - recommendation system
  - collaborative filtering
  - ML system design
  - personalization
difficulty: Advanced
estimated_time: 40 minutes
prerequisites:
  - ML System Design Introduction
companies: [Netflix, Amazon, Spotify, YouTube]
---

# Design a Recommendation System

Recommendation systems drive engagement for Netflix, Amazon, Spotify, and more. Here's how to design one.

---

## Requirements

### Functional
- Recommend items to users
- Handle new users (cold start)
- Update in real-time based on activity
- Support multiple surfaces (home, search, email)

### Non-Functional
- **Latency:** < 100ms for real-time
- **Scale:** Millions of users, millions of items
- **Freshness:** Incorporate recent activity

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Request                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Candidate Generation                         │
│  (Retrieve 1000s of potentially relevant items)                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │Collaborative│  │ Content-    │  │  Trending/  │             │
│  │ Filtering   │  │   Based     │  │  Popular    │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Ranking                                  │
│  (Score and rank candidates using ML model)                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Post-Processing                             │
│  (Diversity, business rules, filtering)                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                       Final Recommendations
```

---

## Stage 1: Candidate Generation

### Collaborative Filtering

```
"Users who liked X also liked Y"

Matrix Factorization:
- Decompose user-item matrix into embeddings
- User embedding × Item embedding = predicted score

user_embedding = [0.2, 0.8, -0.1, ...]
item_embedding = [0.3, 0.7, 0.1, ...]
score = dot_product(user_embedding, item_embedding)
```

### Content-Based Filtering

```
"Items similar to what you've liked"

- Compute item embeddings from features
- Find items similar to user's history

item_features = [genre, director, actors, ...]
item_embedding = model(item_features)
similar_items = nearest_neighbors(user_history_embeddings)
```

### Two-Tower Architecture

```
┌─────────────┐        ┌─────────────┐
│  User Tower │        │  Item Tower │
│  (features) │        │  (features) │
└──────┬──────┘        └──────┬──────┘
       │                      │
       ▼                      ▼
┌─────────────┐        ┌─────────────┐
│    User     │        │    Item     │
│  Embedding  │        │  Embedding  │
└──────┬──────┘        └──────┬──────┘
       │                      │
       └──────────┬───────────┘
                  │
                  ▼
             Similarity Score

Pre-compute item embeddings for fast retrieval
Compute user embedding at request time
Use ANN (Approximate Nearest Neighbors) for lookup
```

---

## Stage 2: Ranking

```
Input: User features + Item features + Context
Output: Engagement probability

Features:
- User: demographics, history, preferences
- Item: category, popularity, freshness
- Context: time, device, location
- Cross: user-item interaction features

Model: Gradient boosted trees or neural network
Target: Click, watch time, purchase, etc.
```

---

## Stage 3: Post-Processing

```
Business Rules:
- Filter already seen items
- Enforce content policies
- Apply A/B test buckets

Diversity:
- Avoid too many similar items
- Mix categories/genres
- Include some exploration

Freshness:
- Boost new content
- Decay old recommendations
```

---

## Handling Cold Start

### New Users

```
1. Use popular/trending items
2. Ask onboarding questions
3. Leverage demographics
4. Quick learning from first interactions
```

### New Items

```
1. Content-based features (don't need history)
2. Show to exploration bucket
3. Boost initially for data collection
4. Leverage similar items' performance
```

---

## Training Pipeline

```
Historical Data → Feature Engineering → Training
       │                                    │
       ▼                                    ▼
   Labels                              Model
   (clicks,                            Registry
    purchases,                              │
    watch time)                            ▼
                                      A/B Testing
                                           │
                                           ▼
                                      Production
```

---

## Metrics

| Metric | What It Measures |
|--------|------------------|
| **CTR** | Click-through rate |
| **Engagement** | Time spent, interactions |
| **Conversion** | Purchases, subscriptions |
| **NDCG** | Ranking quality |
| **Coverage** | % of catalog recommended |
| **Diversity** | Variety in recommendations |

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Architecture | Two-stage (retrieval + ranking) | Scale |
| Candidate gen | Multiple sources | Coverage |
| Embeddings | Pre-computed | Latency |
| ANN index | FAISS/ScaNN | Fast similarity |
| Ranking model | Neural network | Expressiveness |

---

## Key Takeaways

1. **Two-stage architecture** (candidate gen + ranking) for scale.
2. **Multiple candidate sources** for coverage and diversity.
3. **Pre-compute embeddings** for latency.
4. **Handle cold start** explicitly.
5. **Optimize for business metrics**, not just ML metrics.
