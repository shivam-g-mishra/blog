---
sidebar_position: 4
title: "Data Engineer Interview Guide"
description: >-
  Interview guide for data engineering roles. SQL, ETL, data pipelines,
  and big data technologies.
keywords:
  - data engineer interview
  - SQL interview
  - ETL interview
  - data pipeline
difficulty: Mixed
estimated_time: 20 minutes
prerequisites: []
companies: [Google, Amazon, Meta, Netflix]
---

# Data Engineer Interview Guide

Data engineering interviews blend SQL skills, system design, and big data knowledge.

---

## Interview Structure

```
Typical data engineering loop:

1. Phone Screen (45-60 min)
   - SQL queries
   - Basic coding

2. Onsite (4-5 rounds)
   - SQL Deep Dive × 1
   - Coding × 1-2
   - Data Pipeline Design × 1
   - Behavioral × 1
```

---

## SQL Skills (Critical)

### Must-Know

```sql
-- Window functions
SELECT 
    user_id,
    purchase_date,
    amount,
    SUM(amount) OVER (PARTITION BY user_id ORDER BY purchase_date) as running_total,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY purchase_date) as purchase_num
FROM purchases;

-- CTEs
WITH daily_revenue AS (
    SELECT DATE(created_at) as date, SUM(amount) as revenue
    FROM orders
    GROUP BY DATE(created_at)
)
SELECT date, revenue,
       AVG(revenue) OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as moving_avg
FROM daily_revenue;

-- Self joins
SELECT a.date, COUNT(DISTINCT b.user_id) as retained_users
FROM user_activity a
JOIN user_activity b ON a.user_id = b.user_id 
                    AND b.date = a.date + INTERVAL '7 days'
GROUP BY a.date;
```

---

## Data Pipeline Design

### Common Questions

- Design a data pipeline for user analytics
- Design an ETL system for log processing
- Design a real-time dashboard pipeline

### Framework

```
1. Data Sources
   - What data? Format? Volume? Velocity?

2. Ingestion
   - Batch vs streaming?
   - Tools: Kafka, Kinesis, Airflow

3. Storage
   - Raw: S3, GCS
   - Processed: Data warehouse (Snowflake, BigQuery)
   - Serving: Redis, PostgreSQL

4. Processing
   - Batch: Spark, Hive
   - Streaming: Flink, Spark Streaming

5. Quality
   - Validation, monitoring, alerting
```

---

## Technologies to Know

| Category | Tools |
|----------|-------|
| **Orchestration** | Airflow, Dagster, Prefect |
| **Batch Processing** | Spark, Hive, Presto |
| **Streaming** | Kafka, Flink, Spark Streaming |
| **Storage** | S3, HDFS, Delta Lake |
| **Warehouses** | Snowflake, BigQuery, Redshift |
| **Databases** | PostgreSQL, MySQL |

---

## Coding Questions

### Common Types

```python
# Parse and transform logs
def parse_logs(log_lines):
    results = []
    for line in log_lines:
        parts = line.split()
        results.append({
            'timestamp': parts[0],
            'level': parts[1],
            'message': ' '.join(parts[2:])
        })
    return results

# Aggregate data
from collections import defaultdict

def aggregate_by_user(events):
    user_stats = defaultdict(lambda: {'count': 0, 'total': 0})
    for event in events:
        user_id = event['user_id']
        user_stats[user_id]['count'] += 1
        user_stats[user_id]['total'] += event['amount']
    return dict(user_stats)
```

---

## Data Modeling

```
Know these concepts:
- Star schema vs snowflake
- Fact tables vs dimension tables
- Slowly changing dimensions (SCD)
- Partitioning strategies
- Denormalization trade-offs
```

---

## Key Takeaways

1. **SQL is paramount.** Practice complex queries daily.
2. **Know the ecosystem.** Airflow, Spark, Kafka basics.
3. **Think about scale.** Data volumes matter.
4. **Data quality** is often discussed.
5. **Pipeline design** is system design for data.
