---
sidebar_position: 3
title: "Message Queues — Async Communication"
description: >-
  Master message queues for system design interviews. Kafka vs RabbitMQ,
  pub/sub patterns, exactly-once delivery, and dead letter queues.
keywords:
  - message queue
  - kafka
  - rabbitmq
  - pub/sub
  - async processing
  - event driven
difficulty: Intermediate
estimated_time: 30 minutes
prerequisites:
  - System Design Introduction
companies: [Google, Amazon, Meta, Netflix, Uber, LinkedIn]
---

# Message Queues: Decouple Everything

"How do you handle 10,000 image uploads per second?"

You don't process them all synchronously. You queue them.

**Message queues decouple producers from consumers, enabling async processing at scale.**

---

## Why Message Queues?

### Without Queue

```
┌────────┐     ┌─────────────┐     ┌───────────────┐
│ Client │────▶│ API Server  │────▶│ Image Process │──▶ 5 seconds
└────────┘     └─────────────┘     └───────────────┘
                     │
                     └── Client waits 5 seconds
```

### With Queue

```
┌────────┐     ┌─────────────┐     ┌───────┐     ┌───────────────┐
│ Client │────▶│ API Server  │────▶│ Queue │────▶│ Worker        │
└────────┘     └─────────────┘     └───────┘     └───────────────┘
                     │                                   │
                     └── Client gets 200 OK              └── Process async
                         immediately
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Decoupling** | Producer doesn't know about consumer |
| **Buffering** | Absorb traffic spikes |
| **Async processing** | Don't block on slow operations |
| **Load leveling** | Smooth out peaks |
| **Resilience** | Retry failed messages |
| **Scalability** | Add consumers independently |

---

## Messaging Patterns

### 1. Point-to-Point (Queue)

One message, one consumer.

```
Producer → [Queue] → Consumer

Message is removed after consumption.
```

**Use case:** Task distribution, work queues

### 2. Publish/Subscribe (Topic)

One message, multiple consumers.

```
                    ┌──▶ Consumer A
Publisher → [Topic] ├──▶ Consumer B
                    └──▶ Consumer C

All consumers receive the message.
```

**Use case:** Event broadcasting, notifications

### 3. Fan-out

One message triggers multiple different actions.

```
                        ┌──▶ [Email Queue] ──▶ Email Service
Order Created ──▶ Topic ├──▶ [SMS Queue] ──▶ SMS Service
                        └──▶ [Analytics Queue] ──▶ Analytics
```

### 4. Request/Reply

Async request with correlation ID.

```
┌──────────┐                         ┌──────────┐
│ Service A│                         │ Service B│
├──────────┤                         ├──────────┤
│ 1. Send  │──▶ [Request Queue] ────▶│ Process  │
│ request  │                         │          │
│ (corrID) │                         │          │
│          │◀── [Reply Queue] ◀──────│ 2. Send  │
│ 3. Match │                         │ reply    │
│ corrID   │                         │ (corrID) │
└──────────┘                         └──────────┘
```

---

## Delivery Guarantees

### At-Most-Once

Message may be lost, never duplicated.

```python
# Producer sends, doesn't wait for ack
producer.send(message, acks=0)
```

**Use case:** Metrics, logs (loss acceptable)

### At-Least-Once

Message never lost, may be duplicated.

```python
# Producer waits for ack, retries on failure
producer.send(message, acks='all', retries=3)
```

**Use case:** Most applications (handle duplicates)

### Exactly-Once

Message delivered exactly once.

```python
# Requires idempotency or transactions
producer.send(message, idempotency=True)
```

**Implementation:**
- Idempotent consumers (deduplicate by message ID)
- Transactional outbox pattern
- Kafka transactions

---

## Kafka vs RabbitMQ

| Aspect | Kafka | RabbitMQ |
|--------|-------|----------|
| **Model** | Log-based | Queue-based |
| **Throughput** | Very high (1M+ msg/sec) | High (100K msg/sec) |
| **Message retention** | Configurable (days/forever) | Until consumed |
| **Ordering** | Per partition | Per queue |
| **Replay** | Yes | No |
| **Protocol** | Custom (TCP) | AMQP |
| **Routing** | Topic/partition | Exchange/routing key |
| **Use case** | Event streaming, logs | Task queues, RPC |

### When to Use Kafka

- Event sourcing
- Log aggregation
- Stream processing
- High throughput requirements
- Need message replay

### When to Use RabbitMQ

- Task distribution
- Request/reply patterns
- Complex routing logic
- Lower latency requirements
- Smaller scale

---

## Kafka Deep Dive

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Kafka Cluster                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Topic: user-events                                     │
│  ┌─────────────┬─────────────┬─────────────┐           │
│  │ Partition 0 │ Partition 1 │ Partition 2 │           │
│  │ [0,1,2,3,4] │ [0,1,2,3]   │ [0,1,2]     │           │
│  │    ↑        │    ↑        │    ↑        │           │
│  │  Leader     │  Leader     │  Leader     │           │
│  │  Broker 1   │  Broker 2   │  Broker 3   │           │
│  └─────────────┴─────────────┴─────────────┘           │
│                                                         │
│  Consumer Group: analytics                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐         │
│  │ Consumer 1 │ │ Consumer 2 │ │ Consumer 3 │         │
│  │ (P0)       │ │ (P1)       │ │ (P2)       │         │
│  └────────────┘ └────────────┘ └────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### Key Concepts

```python
# Producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# Send with key (determines partition)
producer.send(
    topic='user-events',
    key=b'user-123',  # Same key → same partition → ordering
    value=b'{"event": "login"}'
)

# Consumer
consumer = KafkaConsumer(
    'user-events',
    group_id='analytics',  # Consumer group for parallel processing
    auto_offset_reset='earliest'
)

for message in consumer:
    process(message.value)
    consumer.commit()  # Manual commit for at-least-once
```

---

## Common Patterns

### Dead Letter Queue (DLQ)

Handle messages that fail processing.

```
┌──────────┐     ┌───────────┐     ┌──────────┐
│ Producer │────▶│Main Queue │────▶│ Consumer │
└──────────┘     └───────────┘     └────┬─────┘
                                        │
                                  Fails 3x?
                                        │
                                        ▼
                                 ┌──────────────┐
                                 │ Dead Letter  │
                                 │ Queue (DLQ)  │
                                 └──────────────┘
                                        │
                              Manual review/retry
```

```python
def process_message(message):
    for attempt in range(3):
        try:
            handle(message)
            return
        except Exception:
            if attempt == 2:
                dlq.send(message)
                raise
```

### Outbox Pattern

Ensure database and queue are in sync.

```
┌─────────────────────────────────────────────────┐
│                   Service                        │
├─────────────────────────────────────────────────┤
│                                                 │
│  1. Single Transaction:                         │
│     - INSERT INTO orders (...)                  │
│     - INSERT INTO outbox (event_data)           │
│                                                 │
│  2. Background Process:                         │
│     - SELECT FROM outbox WHERE sent = false     │
│     - Publish to Kafka                          │
│     - UPDATE outbox SET sent = true             │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Competing Consumers

Multiple consumers process from same queue.

```
            ┌──▶ Consumer 1 ──▶ Process
[Queue] ────┼──▶ Consumer 2 ──▶ Process
            └──▶ Consumer 3 ──▶ Process

Each message processed by exactly one consumer.
```

---

## Handling Failures

### Consumer Failure

```python
# Kafka consumer with manual commit
consumer = KafkaConsumer(
    'orders',
    enable_auto_commit=False  # Don't auto-commit
)

for message in consumer:
    try:
        process(message)
        consumer.commit()  # Commit after successful processing
    except Exception:
        # Message will be redelivered
        log_error(message)
```

### Idempotent Processing

```python
def process_order(order_event):
    order_id = order_event['order_id']
    
    # Check if already processed
    if redis.sismember('processed_orders', order_id):
        return  # Skip duplicate
    
    # Process
    create_shipment(order_event)
    
    # Mark as processed
    redis.sadd('processed_orders', order_id)
```

---

## Interview Tips

### Common Questions

1. **"How do you ensure messages aren't lost?"**
   - At-least-once delivery with acks
   - Persistent storage
   - Replication

2. **"How do you handle duplicates?"**
   - Idempotent consumers
   - Deduplication by message ID
   - Exactly-once semantics (Kafka)

3. **"How do you ensure ordering?"**
   - Single partition (Kafka)
   - Single consumer
   - Sequence numbers

4. **"How do you handle poison messages?"**
   - Retry with backoff
   - Dead letter queue
   - Circuit breaker

### Design Considerations

| Factor | Consideration |
|--------|---------------|
| **Throughput** | Kafka for high, RabbitMQ for moderate |
| **Ordering** | Key-based partitioning |
| **Durability** | Replication factor |
| **Latency** | Memory vs disk |
| **Replay** | Kafka with retention |

---

## Key Takeaways

1. **Decouple** producers and consumers for scalability.

2. **At-least-once** is common; handle duplicates.

3. **Kafka for streaming**, RabbitMQ for task queues.

4. **Dead letter queues** for failed messages.

5. **Outbox pattern** for database-queue consistency.

---

## What's Next?

Databases for persistent storage:

👉 [Database Fundamentals →](../databases/introduction)
