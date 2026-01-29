---
sidebar_position: 4
title: "Design Fraud Detection System"
description: >-
  ML system design for fraud detection. Real-time scoring, handling imbalance,
  and adversarial robustness.
keywords:
  - fraud detection
  - ML system design
  - anomaly detection
  - real-time ML
difficulty: Advanced
estimated_time: 35 minutes
prerequisites:
  - ML System Design Introduction
companies: [Stripe, PayPal, Square, Amazon]
---

# Design a Fraud Detection System

Fraud detection balances catching bad actors while not blocking legitimate users.

---

## Requirements

### Functional
- Score transactions in real-time
- Block high-risk transactions
- Learn from analyst feedback
- Reduce false positives

### Non-Functional
- **Latency:** < 100ms per transaction
- **Scale:** Millions of transactions/day
- **Accuracy:** High precision AND recall
- **Adaptability:** Detect new fraud patterns

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Transaction                                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Feature Engineering                           │
│  (Real-time features + Historical aggregates)                   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                        ML Models                                 │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   Rules     │  │   ML Model  │  │  Anomaly    │             │
│  │   Engine    │  │  (XGBoost)  │  │  Detection  │             │
│  └─────────────┘  └─────────────┘  └─────────────┘             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Decision Engine                              │
│  (Combine scores, apply thresholds, take action)                │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                    ┌───────────┼───────────┐
                    │           │           │
                    ▼           ▼           ▼
               Approve      Review       Block
```

---

## Features

### Transaction Features

```
Current transaction:
- Amount, currency
- Merchant category
- Payment method
- Device fingerprint
- IP address, geolocation
- Time of day, day of week
```

### User Historical Features

```
User aggregates:
- Avg transaction amount (7d, 30d)
- Transaction count (1d, 7d)
- Distinct merchants (30d)
- Chargebacks history
- Account age
- Verification status
```

### Velocity Features

```
Real-time counters:
- Transactions in last 1 hour
- Amount in last 24 hours
- Failed attempts today
- New merchants this week
- Devices used today
```

### Derived Features

```
Computed signals:
- Amount vs user average (z-score)
- Distance from last transaction
- Time since last transaction
- Is new merchant?
- Is new device?
- Unusual time for this user?
```

---

## Handling Class Imbalance

```
Problem: Fraud rate ~ 0.1%

Naive model: Predict "not fraud" always → 99.9% accuracy!
But: Catches zero fraud

Solutions:
1. Oversampling (SMOTE)
2. Undersampling
3. Class weights
4. Threshold tuning
5. Anomaly detection approach
6. Ensemble methods
```

---

## Model Architecture

### Multi-Layer Approach

```
Layer 1: Rules Engine (Fast, interpretable)
- Hard blocks: Blocked countries, known bad actors
- Velocity limits: Max transactions/hour

Layer 2: ML Scoring (Nuanced)
- Gradient boosted trees (XGBoost, LightGBM)
- Score from 0-1

Layer 3: Anomaly Detection (Novel patterns)
- Isolation forest
- Autoencoders
- Detect out-of-distribution behavior

Final Decision:
if rules_blocked:
    return BLOCK
elif ml_score > high_threshold or anomaly_detected:
    return BLOCK
elif ml_score > medium_threshold:
    return REVIEW
else:
    return APPROVE
```

---

## Real-Time Feature Serving

```
Challenge: Historical aggregates need to be fresh

Solution: Feature Store architecture

┌─────────────┐     ┌─────────────┐
│   Kafka     │────▶│  Flink/     │
│(Transactions)│    │ Spark       │
└─────────────┘     │ Streaming   │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   Redis     │
                    │ (Counters,  │
                    │  Aggregates)│
                    └─────────────┘

Real-time updates:
- Transaction count increments
- Running sum updates
- Sliding window aggregates
```

---

## Feedback Loop

```
Analyst Review → Label Feedback → Model Retraining

Important:
- Confirmed fraud → Strong positive label
- Analyst approved → Likely negative
- User disputed → Might be fraud
- No dispute → Weak negative (survivorship bias)

Retraining cadence:
- Daily/weekly incremental updates
- Monthly full retraining
- Emergency retraining for new attack patterns
```

---

## Adversarial Considerations

```
Fraudsters adapt:
- Study your rules and evade them
- Mimic legitimate behavior
- Test with small amounts first

Defenses:
- Don't expose exact scores to users
- Randomize some thresholds
- Monitor for probing behavior
- Regular model updates
- Human-in-the-loop for edge cases
```

---

## Metrics

| Metric | Target | Trade-off |
|--------|--------|-----------|
| **Precision** | > 80% | High = fewer false positives |
| **Recall** | > 90% | High = catch more fraud |
| **Fraud Loss** | Minimize $ | Business impact |
| **False Positive Rate** | < 1% | User experience |
| **Latency** | < 100ms | User experience |

---

## Key Takeaways

1. **Multi-layer approach** (rules + ML + anomaly).
2. **Real-time features** critical for fraud detection.
3. **Handle imbalance** carefully—accuracy is misleading.
4. **Fast feedback loop**—fraudsters adapt quickly.
5. **Balance precision/recall** for business impact.
