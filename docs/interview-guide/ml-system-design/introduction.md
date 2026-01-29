---
sidebar_position: 1
title: "ML System Design Introduction"
description: >-
  Introduction to ML system design interviews. Framework, components,
  and how it differs from traditional system design.
keywords:
  - ML system design
  - machine learning interview
  - ML engineering
  - MLOps
difficulty: Advanced
estimated_time: 20 minutes
prerequisites:
  - System Design Framework
companies: [Google, Meta, Amazon, Netflix, Uber]
---

# ML System Design: Beyond Models

ML System Design isn't about model architecture—it's about building production ML systems.

---

## How It Differs from Traditional System Design

| Aspect | Traditional | ML System Design |
|--------|-------------|------------------|
| **Focus** | Data flow, scaling | ML lifecycle |
| **Data** | Store and retrieve | Transform, feature engineering |
| **Logic** | Deterministic code | Learned models |
| **Updates** | Deploy new code | Retrain models |
| **Testing** | Unit/integration tests | Model evaluation, A/B tests |
| **Monitoring** | Latency, errors | Model drift, performance |

---

## The ML System Design Framework

```
1. PROBLEM DEFINITION (5 min)
   - What are we predicting/classifying/recommending?
   - What metrics matter? (business + ML metrics)
   - What are the constraints?

2. DATA (10 min)
   - What data is available?
   - How do we get labels?
   - Feature engineering approach

3. MODEL (10 min)
   - Model selection rationale
   - Training approach
   - Offline evaluation

4. SERVING (10 min)
   - Online vs batch inference
   - Latency requirements
   - Scaling approach

5. MONITORING & ITERATION (5 min)
   - How do we know it's working?
   - How do we improve over time?
   - Handling model drift
```

---

## Key Components

### Data Pipeline

```
Raw Data → ETL → Feature Store → Training Data
                      ↓
              Feature Serving → Model Inference
```

### Training Pipeline

```
Training Data → Data Validation → Model Training
                                       ↓
Model Validation → Model Registry → Deployment
```

### Serving Infrastructure

```
Request → Feature Lookup → Model Inference → Response
              ↓                  ↓
         Feature Store      Model Server
```

---

## Common ML System Design Questions

| Question | Key Challenges |
|----------|---------------|
| **Recommendation System** | Cold start, real-time personalization |
| **Search Ranking** | Relevance, personalization, latency |
| **Fraud Detection** | Class imbalance, real-time, adversarial |
| **Content Moderation** | Scale, accuracy vs recall |
| **Ad Click Prediction** | Billions of predictions, freshness |
| **Feed Ranking** | Engagement optimization, diversity |

---

## Metrics to Discuss

### Business Metrics

```
- Revenue/engagement impact
- User retention
- Conversion rate
- Time spent
```

### ML Metrics

```
Classification:
- Precision, Recall, F1
- AUC-ROC, AUC-PR
- Log loss

Ranking:
- NDCG, MRR, MAP
- Click-through rate

Regression:
- MSE, MAE, RMSE
```

---

## Key Takeaways

1. **Focus on the system**, not just the model.
2. **Data is often the bottleneck**—discuss data pipeline.
3. **Serving matters**—latency, scale, freshness.
4. **Monitoring is critical**—models degrade over time.
5. **Connect to business metrics**—why does this matter?
