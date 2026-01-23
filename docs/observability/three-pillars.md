---
sidebar_position: 2
title: The Three Pillars Deep Dive
description: A practical guide to traces, metrics, and logs - understanding each pillar through the questions they answer.
keywords: [traces, metrics, logs, distributed tracing, prometheus, observability pillars]
---

# The Three Pillars: A Practical Explanation

Let me explain each pillar not in abstract terms, but in terms of the questions they help you answer and the problems they solve.

## Traces: Following a Request's Journey

Imagine you're a detective following a suspect through a city. A trace is like a complete record of everywhere they went, how long they spent at each location, and what they did there.

In software terms, a trace follows a single request as it travels through your distributed system. Here's what that looks like:

```
User Request: Place Order (trace_id: abc123)
│
├── API Gateway (total: 850ms)
│   ├── Request validation (15ms)
│   └── Route to order service
│       │
│       └── Order Service (450ms)
│           ├── Validate cart (25ms)
│           ├── Check inventory (180ms) ← Why so slow?
│           │   └── Database query (175ms) ← Found it!
│           ├── Process payment (200ms)
│           │   └── External API call (195ms)
│           └── Send confirmation (40ms)
│
└── Total response time: 850ms
```

With this trace, you can immediately see that the 850ms response time is primarily caused by a slow inventory database query (175ms) and the external payment API (195ms). Without tracing, you'd be guessing.

### Key Trace Concepts

| Concept | Description |
|---------|-------------|
| **Trace** | The complete journey of a request through all services |
| **Span** | A single operation within a trace (e.g., a database query) |
| **Trace ID** | Unique identifier that links all spans in a trace |
| **Span ID** | Unique identifier for each individual span |
| **Parent Span** | The span that initiated the current span |
| **Attributes** | Key-value metadata attached to spans (user_id, order_id, etc.) |

### When Traces Shine

- "Why did this specific request take so long?"
- "Where in my system did this error originate?"
- "What's the actual call path between my services?"
- "Which downstream service is causing my latency?"

### Trace Instrumentation Example

```go
// Creating a span in Go with OpenTelemetry
ctx, span := tracer.Start(ctx, "process-payment",
    trace.WithAttributes(
        attribute.String("order.id", orderID),
        attribute.Float64("payment.amount", amount),
    ),
)
defer span.End()

// The span automatically captures duration
result, err := paymentGateway.Charge(ctx, amount)
if err != nil {
    span.RecordError(err)
    span.SetStatus(codes.Error, "payment failed")
}
```

---

## Metrics: Understanding System Behavior Over Time

If traces are for investigating individual requests, metrics are for understanding patterns and trends across millions of requests.

Metrics are numerical measurements collected at regular intervals. Think of metrics like your car's dashboard—you don't need to know everything happening inside the engine, but you do need to know the speed, fuel level, and engine temperature.

### Example Metrics

```yaml
# Request throughput
http_requests_total{service="order-api", status="200"}: 1,234,567
http_requests_total{service="order-api", status="500"}: 234

# Latency percentiles
http_request_duration_seconds_p99{service="order-api"}: 0.45
http_request_duration_seconds_p95{service="order-api"}: 0.23
http_request_duration_seconds_p50{service="order-api"}: 0.08

# Resource utilization
active_database_connections{pool="primary"}: 42
order_processing_queue_depth: 127
```

From these numbers, you can understand:
- How much traffic you're serving (1.2M successful requests)
- Your error rate (234/1,234,801 ≈ 0.02%)
- Your worst-case latency (99th percentile at 450ms)
- Database connection pool utilization (42 connections in use)
- Whether you're keeping up with orders (127 in queue)

### The Golden Signals

Google's Site Reliability Engineering book defines four golden signals that capture the essential health of any service:

| Signal | Description | Example Metric |
|--------|-------------|----------------|
| **Latency** | Time to service a request | `http_request_duration_seconds` |
| **Traffic** | Demand on your system | `http_requests_total` |
| **Errors** | Rate of failed requests | `http_errors_total` |
| **Saturation** | How "full" your service is | `cpu_utilization`, `queue_depth` |

### When Metrics Shine

- "What's our error rate trending over the past week?"
- "Are we approaching capacity limits?"
- "How does today's latency compare to yesterday?"
- "Should I wake someone up?" (alerting)

### Metric Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Counter** | Monotonically increasing value | Total requests, total errors |
| **Gauge** | Value that can go up or down | Current queue size, temperature |
| **Histogram** | Distribution of values | Request duration percentiles |
| **Summary** | Similar to histogram, client-side calculation | Legacy systems |

---

## Logs: The Detailed Record

Logs are the narrative of your system—discrete events that describe what happened at specific moments. But there's a crucial distinction between logs that help you debug and logs that just fill up your disk.

### Bad vs. Good Logging

**Unhelpful log:**
```
2024-01-15 10:23:45 ERROR Payment failed
```

This tells you almost nothing. Which payment? Which user? Why did it fail?

**Helpful log:**
```json
{
  "timestamp": "2024-01-15T10:23:45.123Z",
  "level": "error",
  "service": "payment-service",
  "message": "Payment processing failed",
  "trace_id": "abc123def456",
  "user_id": "user_789",
  "order_id": "order_456",
  "payment_amount": 99.99,
  "payment_provider": "stripe",
  "error_code": "card_declined",
  "error_message": "Your card was declined.",
  "request_id": "req_xyz"
}
```

Now you can:
- Find this log entry quickly using any of these fields
- Jump to the related trace using `trace_id`
- See exactly what went wrong (`card_declined`)
- Correlate with other events for the same user or order

### Structured Logging Best Practices

1. **Use JSON format**: Machine-parseable, query-friendly
2. **Include trace context**: `trace_id` and `span_id` for correlation
3. **Add business context**: `user_id`, `order_id`, `customer_tier`
4. **Be consistent**: Same field names across all services
5. **Include the right level**: Don't log everything as ERROR

### Log Levels

| Level | When to Use |
|-------|-------------|
| **ERROR** | Something failed and needs attention |
| **WARN** | Potentially harmful situation, but system continues |
| **INFO** | Significant business events (order placed, user registered) |
| **DEBUG** | Detailed information for troubleshooting (disable in production) |

### When Logs Shine

- "What exactly happened when this error occurred?"
- "What did the user do before the failure?"
- "Are there audit requirements I need to satisfy?"
- "What was the full error message and stack trace?"

---

## The Real Power: Correlation

Each pillar is useful on its own, but the real power comes from combining them. Here's a typical debugging flow:

```
┌─────────────────────────────────────────────────────────────┐
│  1. ALERT FIRES (Metrics)                                   │
│     "Error rate > 1% for order-service"                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  2. INVESTIGATE METRICS                                     │
│     Error rate spiked at 10:15 AM                           │
│     Latency also increased                                  │
│     Database connection pool at 100%                        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  3. SEARCH LOGS                                             │
│     Filter: service=order-service, level=error, time=10:15  │
│     Found: "Connection pool exhausted"                      │
│     Found: "Timeout waiting for database connection"        │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  4. EXAMINE TRACES                                          │
│     Click trace_id from error log                           │
│     See: inventory-service making 50 DB queries per request │
│     See: Each query holding connection for 2+ seconds       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  5. ROOT CAUSE IDENTIFIED                                   │
│     A recent deployment introduced an N+1 query bug         │
│     Under high load, this exhausted the connection pool     │
└─────────────────────────────────────────────────────────────┘
```

This investigation took 10 minutes with proper observability. Without it? Could easily be hours of guessing, adding debug logging, redeploying, and hoping you get lucky.

---

**Next**: [Understanding OpenTelemetry →](./opentelemetry)
