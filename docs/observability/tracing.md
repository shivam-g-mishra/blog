---
sidebar_position: 3
title: Distributed Tracing Explained
description: A comprehensive guide to distributed tracing - understanding trace and span relationships, context propagation, and debugging microservices effectively.
keywords: [distributed tracing, traces, spans, trace context, microservices, debugging, OpenTelemetry]
---

# Distributed Tracing: Following the Thread

Let me paint a picture that might feel familiar.

It's Tuesday afternoon. A customer reports that checkout is "sometimes slow." Your metrics show elevated p99 latency, but the average looks fine. You check the logs—thousands of entries, no obvious errors. The payment service looks healthy. The inventory service looks healthy. Every individual component looks healthy.

But somewhere in the interaction between these "healthy" services, requests are taking 8 seconds instead of 800 milliseconds.

Without distributed tracing, you're essentially trying to debug a conversation by looking at each participant's notes separately, with no record of what was said to whom, or when. You can see that Alice wrote "OK" at 2:15 PM and Bob wrote "Done" at 2:16 PM, but you have no idea if those notes were even part of the same conversation.

**Distributed tracing solves this by giving every conversation—every request—a unique identifier that follows it through every service it touches.**

---

## What Is a Trace, Really?

A trace is a complete record of a single request's journey through your distributed system. Think of it as a story with chapters—each chapter (called a **span**) represents one operation, and together they tell you exactly what happened.

Here's the mental model that helped me understand it:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      THE STORY OF REQUEST #a]b7x9                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Chapter 1: "User clicks Buy Now"                                          │
│  ├── Who: API Gateway                                                      │
│  ├── When: 14:23:45.100 → 14:23:46.250 (1150ms total)                      │
│  └── What happened: Received request, validated auth, routed to order svc  │
│                                                                            │
│      Chapter 2: "Processing the order"                                     │
│      ├── Who: Order Service                                                │
│      ├── When: 14:23:45.115 → 14:23:46.200 (1085ms)                        │
│      └── What happened: Validated cart, checked inventory, processed pay   │
│                                                                            │
│          Chapter 3: "Checking if items are available"                      │
│          ├── Who: Inventory Service                                        │
│          ├── When: 14:23:45.200 → 14:23:45.650 (450ms) ← SLOW!             │
│          └── What happened: Queried database for 3 SKUs                    │
│                                                                            │
│              Chapter 4: "The database query"                               │
│              ├── Who: Inventory DB                                         │
│              ├── When: 14:23:45.210 → 14:23:45.640 (430ms) ← FOUND IT!     │
│              └── What happened: SELECT with missing index                  │
│                                                                            │
│          Chapter 5: "Charging the customer"                                │
│          ├── Who: Payment Service                                          │
│          ├── When: 14:23:45.660 → 14:23:46.150 (490ms)                     │
│          └── What happened: Called Stripe API, got approval                │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

Looking at this "story," I can immediately see:
- The total request took 1150ms
- The inventory database query alone took 430ms (37% of total time!)
- The payment API took 490ms (expected—external API)
- The actual problem is a slow database query, not any of the services themselves

Without tracing, I might have spent hours checking network latency, service configurations, or blaming the payment provider. The trace told me the answer in seconds.

---

## The Building Blocks: Trace ID, Span ID, and Parent-Child Relationships

Let me break down the anatomy of a trace with a concrete example.

### The Trace ID: One ID to Rule Them All

Every request that enters your system gets a unique **Trace ID**—a 128-bit identifier that stays constant throughout the request's entire journey:

```
Trace ID: 4bf92f3577b34da6a3ce929d0e0e4736
         └──────────────────────────────┘
              32 hex characters (128 bits)
```

This single ID connects every operation across every service. When you're debugging, this is your search key. Find the trace ID, and you find everything that happened.

### Spans: The Individual Operations

Each operation within a trace is a **span**. Every span has:

```
┌─────────────────────────────────────────────────────────────────┐
│  SPAN: "POST /api/orders"                                       │
├─────────────────────────────────────────────────────────────────┤
│  trace_id:    4bf92f3577b34da6a3ce929d0e0e4736                  │
│  span_id:     00f067aa0ba902b7                                  │
│  parent_id:   (none - this is the root span)                    │
│                                                                 │
│  start_time:  2024-06-15T14:23:45.100Z                          │
│  end_time:    2024-06-15T14:23:46.250Z                          │
│  duration:    1150ms                                            │
│                                                                 │
│  status:      OK                                                │
│                                                                 │
│  attributes:                                                    │
│    http.method:        POST                                     │
│    http.url:           /api/orders                              │
│    http.status_code:   201                                      │
│    user.id:            usr_456                                  │
│    order.id:           ord_789                                  │
│    order.item_count:   3                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Parent-Child Relationships: Building the Tree

Spans form a tree structure through parent-child relationships. Each span (except the root) has a `parent_id` pointing to the span that initiated it:

```
                    ┌─────────────────────────────┐
                    │       API Gateway           │
                    │       span_id: aaa111       │
                    │       parent_id: (none)     │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │       Order Service         │
                    │       span_id: bbb222       │
                    │       parent_id: aaa111     │
                    └──────────────┬──────────────┘
                                   │
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
          ▼                        ▼                        ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Inventory    │    │     Payment     │    │      Email      │
│     Service     │    │     Service     │    │     Service     │
│  span_id: ccc   │    │  span_id: ddd   │    │  span_id: eee   │
│  parent: bbb222 │    │  parent: bbb222 │    │  parent: bbb222 │
└────────┬────────┘    └────────┬────────┘    └─────────────────┘
         │                      │
         ▼                      ▼
┌─────────────────┐    ┌─────────────────┐
│    DB Query     │    │   Stripe API    │
│  span_id: fff   │    │  span_id: ggg   │
│  parent: ccc    │    │  parent: ddd    │
└─────────────────┘    └─────────────────┘
```

This tree structure lets you:
1. See the complete hierarchy of operations
2. Understand which operations happened in parallel vs. sequentially
3. Calculate time spent in each service vs. time waiting for children

---

## Context Propagation: How the Magic Happens

Here's a question that puzzled me when I first learned about tracing: how does the Payment Service know it's part of the same trace as the Order Service?

The answer is **context propagation**. When one service calls another, it includes trace context in the request headers.

### The W3C Trace Context Standard

The industry has standardized on W3C Trace Context, which uses two HTTP headers:

```http
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │   │                                │                 │
             │   │                                │                 └── Flags (sampled)
             │   │                                └── Parent Span ID (16 hex)
             │   └── Trace ID (32 hex)
             └── Version (always 00 for now)

tracestate: vendor1=value1,vendor2=value2
            └── Optional vendor-specific data
```

### Propagation in Action

Here's what happens when Order Service calls Payment Service:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                            ORDER SERVICE                                   │
│                                                                            │
│  // Current context                                                        │
│  trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"                             │
│  current_span_id = "bbb222"                                                │
│                                                                            │
│  // Make HTTP call to Payment Service                                      │
│  POST /api/payments HTTP/1.1                                               │
│  Host: payment-service                                                     │
│  traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-bbb222-01                │
│  Content-Type: application/json                                            │
│  ...                                                                       │
└────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      │ HTTP Request
                                      ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                           PAYMENT SERVICE                                  │
│                                                                            │
│  // Extract context from incoming request                                  │
│  traceparent header → trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"        │
│                     → parent_span_id = "bbb222"                            │
│                                                                            │
│  // Create new span as child of the incoming context                       │
│  new_span = {                                                              │
│    trace_id: "4bf92f3577b34da6a3ce929d0e0e4736",  // Same trace!           │
│    span_id: "ddd444",                              // New span ID          │
│    parent_id: "bbb222"                             // Order Service's span │
│  }                                                                         │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

This is why OpenTelemetry (or any tracing library) needs to be configured in every service. Without it, the chain breaks.

### What Happens When Propagation Fails

If a service doesn't extract and propagate trace context, you get a broken trace:

```
WHAT YOU EXPECT:                    WHAT YOU GET:
                                    
    [API Gateway]                       [API Gateway]
         │                                   │
         ▼                                   ▼
    [Order Service]                     [Order Service]
         │                                   │
    ─────┼─────                              X  (context lost)
         ▼                                   
    [Payment Service]                   [Payment Service] ← New trace starts
         │                                   │
         ▼                                   ▼
    [Database]                          [Database]


One connected trace               Two disconnected traces
                                  (impossible to correlate)
```

**Common causes of broken propagation:**
- Service not instrumented with tracing library
- Custom HTTP client that doesn't use instrumented wrapper
- Message queue consumer not extracting context from message headers
- Load balancer or proxy stripping custom headers

---

## The Waterfall View: Reading Traces Like a Pro

Most tracing backends (Jaeger, Tempo, commercial APMs) display traces as a waterfall or Gantt chart. Learning to read this visualization quickly is a superpower.

```
TIME ──────────────────────────────────────────────────────────────────────►
0ms        200ms       400ms       600ms       800ms      1000ms     1200ms
│           │           │           │           │           │           │
│           │           │           │           │           │           │
├───────────────────────────────────────────────────────────────────────┤
│ ████████████████████████████████████████████████████████████████████ │
│ API Gateway: POST /api/orders (1150ms)                                │
├───────────────────────────────────────────────────────────────────────┤
│   │                                                                   │
│   ├─────────────────────────────────────────────────────────────────┤ │
│   │ ██████████████████████████████████████████████████████████████ │ │
│   │ Order Service: process_order (1085ms)                          │ │
│   ├─────────────────────────────────────────────────────────────────┤ │
│   │   │                                                             │ │
│   │   ├──────────────────────────┤                                  │ │
│   │   │ █████████████████████████│                                  │ │
│   │   │ Inventory: check (450ms) │ ◄── WHY SO LONG?                 │ │
│   │   ├──────────────────────────┤                                  │ │
│   │   │   │                      │                                  │ │
│   │   │   ├────────────────────┤ │                                  │ │
│   │   │   │ ██████████████████ │ │                                  │ │
│   │   │   │ DB Query (430ms)   │ │ ◄── THE CULPRIT!                │ │
│   │   │   ├────────────────────┤ │                                  │ │
│   │   │                          │                                  │ │
│   │   │                          ├─────────────────────────┤        │ │
│   │   │                          │ █████████████████████████│        │ │
│   │   │                          │ Payment: charge (490ms) │        │ │
│   │   │                          ├─────────────────────────┤        │ │
│   │   │                                │                    │        │ │
│   │   │                                ├───────────────────┤│        │ │
│   │   │                                │ ██████████████████││        │ │
│   │   │                                │ Stripe API (470ms)││        │ │
│   │   │                                ├───────────────────┤│        │ │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### What to Look For

**1. Long bars:** These are your slow operations. In the diagram above, the database query (430ms) immediately stands out.

**2. Sequential vs. parallel execution:** Notice that Inventory and Payment run sequentially—Payment only starts after Inventory completes. Could they run in parallel?

**3. Gaps between spans:** If there's whitespace between a parent span starting and child spans appearing, that's time spent in the parent's own code (or waiting).

**4. Deep nesting:** Many levels of nesting might indicate over-complicated service interactions.

**5. Missing spans:** If you expect a database call but don't see a span for it, either it's not instrumented or something unexpected is happening (like a cache hit).

---

## Span Attributes: Adding Context That Matters

Raw timing data is useful, but **span attributes** transform traces from timing diagrams into debugging goldmines.

### Essential Attributes to Include

| Category | Attributes | Why They Matter |
|----------|------------|-----------------|
| **Identity** | `user.id`, `tenant.id`, `session.id` | "Who was affected?" |
| **Business** | `order.id`, `product.sku`, `payment.amount` | "What were we processing?" |
| **Technical** | `http.method`, `http.status_code`, `db.system` | "What operation ran?" |
| **Infrastructure** | `service.version`, `deployment.environment`, `k8s.pod.name` | "Where did this run?" |

### Good vs. Bad Attribute Usage

**Sparse attributes (limited debugging value):**

```json
{
  "name": "process_order",
  "duration_ms": 1085,
  "status": "OK"
}
```

**Rich attributes (much more useful):**

```json
{
  "name": "process_order",
  "duration_ms": 1085,
  "status": "OK",
  "attributes": {
    "order.id": "ord_789",
    "order.item_count": 3,
    "order.total_cents": 15999,
    "user.id": "usr_456",
    "user.tier": "premium",
    "inventory.cache_hit": false,
    "payment.provider": "stripe",
    "payment.method": "card",
    "service.version": "2.4.1",
    "feature_flags.new_checkout": true
  }
}
```

With rich attributes, I can now ask questions like:
- "Show me all slow orders for premium users"
- "Did the new checkout feature flag affect latency?"
- "Are inventory cache misses correlated with slow requests?"

### High-Cardinality Attributes: Handle with Care

Some attributes have many unique values (high cardinality):

| Attribute | Cardinality | Storage Impact |
|-----------|-------------|----------------|
| `http.method` | ~10 values | Low (fine) |
| `http.status_code` | ~50 values | Low (fine) |
| `user.id` | Millions | High (careful!) |
| `order.id` | Millions | High (careful!) |
| `request.body` | Unlimited | Very High (avoid!) |

High-cardinality attributes are incredibly valuable for debugging specific issues but can explode storage costs. Most tracing backends handle them well, but be mindful of:
- Not indexing every high-cardinality field
- Using sampling to reduce volume
- Setting retention policies appropriately

---

## Span Events: Capturing Moments in Time

Sometimes you need to record something that happened during a span, but it's not a separate operation worth its own span. That's what **span events** are for.

```
┌────────────────────────────────────────────────────────────────────┐
│  SPAN: "process_payment" (500ms)                                   │
│                                                                    │
│  ├── EVENT @ +50ms: "payment_validated"                            │
│  │   └── attributes: {validation_rules: 5, passed: true}           │
│  │                                                                 │
│  ├── EVENT @ +120ms: "fraud_check_completed"                       │
│  │   └── attributes: {risk_score: 0.15, threshold: 0.7}            │
│  │                                                                 │
│  ├── EVENT @ +180ms: "gateway_request_sent"                        │
│  │   └── attributes: {provider: "stripe", idempotency_key: "xyz"}  │
│  │                                                                 │
│  └── EVENT @ +480ms: "gateway_response_received"                   │
│      └── attributes: {status: "succeeded", provider_id: "pi_123"}  │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

### When to Use Events vs. Child Spans

| Scenario | Use Event | Use Child Span |
|----------|-----------|----------------|
| Quick validation check | ✅ | |
| External API call | | ✅ |
| State transition | ✅ | |
| Database query | | ✅ |
| Logging a decision point | ✅ | |
| Calling another service | | ✅ |

**Rule of thumb:** If it has meaningful duration and you'd want to see it in the waterfall, make it a span. If it's a point-in-time occurrence, make it an event.

### Recording Errors as Events

When exceptions occur, record them as events with full context:

```json
{
  "name": "exception",
  "timestamp": "2024-06-15T14:23:45.500Z",
  "attributes": {
    "exception.type": "PaymentDeclinedException",
    "exception.message": "Card declined: insufficient funds",
    "exception.stacktrace": "at PaymentProcessor.charge(PaymentProcessor.java:142)\n...",
    "exception.escaped": false
  }
}
```

---

## Correlating Traces with Logs

Traces show you the structure and timing. Logs give you the details. The magic happens when you can seamlessly jump between them.

### The Bridge: trace_id and span_id in Logs

Every log entry should include trace context:

```json
{
  "timestamp": "2024-06-15T14:23:45.500Z",
  "level": "error",
  "service": "payment-service",
  "message": "Payment declined by gateway",
  
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "ddd444",
  
  "user_id": "usr_456",
  "payment_amount_cents": 15999,
  "decline_reason": "insufficient_funds"
}
```

### The Debugging Workflow

Here's how I actually use traces and logs together during an incident:

```
┌────────────────────────────────────────────────────────────────────────────┐
│  STEP 1: Alert fires                                                       │
│  "Payment failure rate > 5%"                                               │
└───────────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  STEP 2: Find example failures in traces                                   │
│  Query: status = ERROR AND service.name = "payment-service"                │
│  Result: Several traces showing failures, pick one to examine              │
└───────────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  STEP 3: Examine the trace waterfall                                       │
│  See: Payment span has error, but the error came from Stripe API span      │
│  See: Stripe API span took 50ms (fast), so not a timeout                   │
│  See: Attributes show decline_code = "do_not_honor"                        │
└───────────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  STEP 4: Jump to logs for this trace_id                                    │
│  Query: trace_id = "4bf92f3577b34da6a3ce929d0e0e4736"                       │
│  See full error details, retry attempts, exact request/response data       │
└───────────────────────────────────────┬────────────────────────────────────┘
                                        │
                                        ▼
┌────────────────────────────────────────────────────────────────────────────┐
│  STEP 5: Widen the search                                                  │
│  Query logs: decline_code = "do_not_honor" AND time = last_hour            │
│  Find: 500+ failures, all from same BIN range (card issuer)                │
│  Root cause: Card issuer is having issues, not our system                  │
└────────────────────────────────────────────────────────────────────────────┘
```

This investigation took 5 minutes. Without correlation? I'd still be guessing.

---

## Sampling: Tracing at Scale

Here's an uncomfortable truth: at scale, you cannot store every trace. A service handling 10,000 requests per second generates terabytes of trace data daily. You need a sampling strategy.

### Head-Based Sampling: Simple but Blind

The sampling decision is made at the start of the trace:

```
                   Incoming Requests
                          │
                          ▼
              ┌───────────────────────┐
              │   Sample Decision     │
              │   (e.g., 10% random)  │
              └───────────┬───────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    ┌───────────────┐           ┌───────────────┐
    │   SAMPLED     │           │  NOT SAMPLED  │
    │   (Record)    │           │   (Discard)   │
    │               │           │               │
    │ 10% of traces │           │ 90% of traces │
    └───────────────┘           └───────────────┘
```

**Pros:**
- Simple to implement
- Low overhead
- Consistent decision across all services (via trace flags)

**Cons:**
- Random: might discard the one error you needed
- Can't make decisions based on outcome (latency, errors)

### Tail-Based Sampling: Smart but Complex

The sampling decision is made after the trace completes:

```
                   All Traces Collected
                          │
                          ▼
              ┌───────────────────────┐
              │   Sampling Processor  │
              │   (in OTel Collector) │
              └───────────┬───────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │   Evaluate Policies:  │
              │   • Has error? KEEP   │
              │   • Latency > 2s? KEEP│
              │   • Random 5%? KEEP   │
              │   • Otherwise? DROP   │
              └───────────┬───────────┘
                          │
            ┌─────────────┴─────────────┐
            │                           │
            ▼                           ▼
    ┌───────────────┐           ┌───────────────┐
    │     KEEP      │           │     DROP      │
    │               │           │               │
    │ All errors    │           │ Normal fast   │
    │ All slow      │           │ requests      │
    │ 5% of rest    │           │               │
    └───────────────┘           └───────────────┘
```

**Pros:**
- Keep 100% of errors (never miss a failure)
- Keep all slow requests (catch latency issues)
- Much better signal-to-noise ratio

**Cons:**
- Requires buffering complete traces (memory)
- More complex configuration
- Needs centralized collector (can't do in-app)

### My Recommended Strategy

For most production systems, I recommend tail-based sampling with these policies:

```yaml
# OpenTelemetry Collector tail sampling config
processors:
  tail_sampling:
    decision_wait: 10s           # Wait for trace to complete
    num_traces: 100000           # Buffer size
    policies:
      # Keep all errors
      - name: errors
        type: status_code
        status_code: {status_codes: [ERROR]}
      
      # Keep slow requests (> 2 seconds)
      - name: slow-requests
        type: latency
        latency: {threshold_ms: 2000}
      
      # Keep all traces for specific critical endpoints
      - name: critical-paths
        type: string_attribute
        string_attribute:
          key: http.route
          values: ["/api/checkout", "/api/payments"]
      
      # Sample 5% of everything else
      - name: baseline
        type: probabilistic
        probabilistic: {sampling_percentage: 5}
```

---

## Debugging Microservices: A Real-World Scenario

Let me walk through how I'd debug a real production issue using traces.

### The Scenario

**Symptom:** Users report "Orders are failing intermittently"
**Metrics show:** 3% error rate on order creation (normally < 0.1%)
**When:** Started 30 minutes ago

### Step 1: Find Failing Traces

Query the tracing backend:
```
service.name = "order-service" 
AND status = ERROR 
AND http.route = "POST /api/orders"
AND timestamp > now() - 30m
```

### Step 2: Examine a Representative Trace

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Trace: 8f2e4a1b7c9d3e5f                                                    │
│ Status: ERROR                                                              │
│ Duration: 5,234ms                                                          │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│ [API Gateway] POST /api/orders ────────────────────────────── 5,234ms ERROR│
│   │                                                                        │
│   └─► [Order Service] process_order ───────────────────────── 5,180ms ERROR│
│         │                                                                  │
│         ├─► [Inventory Service] check_availability ─────────────── 45ms OK │
│         │                                                                  │
│         └─► [Payment Service] process_payment ─────────────── 5,100ms ERROR│
│               │                                                            │
│               └─► [Stripe API] charge ───────────────────────── 5,050ms ERR│
│                     │                                                      │
│                     └─► exception: "Connection timeout after 5000ms"       │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

**Immediate insight:** The Stripe API is timing out. Not our code—external dependency.

### Step 3: Check if This is Widespread

Query for Stripe spans:
```
service.name = "payment-service"
AND span.name = "stripe_api_call"
AND timestamp > now() - 1h
```

Results:
```
Last hour: 12,847 Stripe calls
  - Success: 12,459 (97%)
  - Timeout: 388 (3%)
  
Timeouts by time:
  - 60 min ago: 2
  - 50 min ago: 3  
  - 40 min ago: 12
  - 30 min ago: 89    ← Started here
  - 20 min ago: 142
  - 10 min ago: 140
```

### Step 4: Check Stripe Status

Jump to logs for context:
```
trace_id = "8f2e4a1b7c9d3e5f"
```

Logs show:
```json
{
  "message": "Stripe API timeout",
  "stripe_endpoint": "https://api.stripe.com/v1/charges",
  "timeout_ms": 5000,
  "retry_attempt": 3,
  "stripe_request_id": "req_xyz789"
}
```

### Step 5: Correlate and Conclude

Check Stripe status page: "Elevated error rates on payment creation endpoint"

**Root cause:** Stripe is experiencing issues. Our system is working correctly—just waiting for an external dependency that's slow.

**Action:** 
1. Post status update to customers
2. Consider circuit breaker activation
3. Monitor for recovery

**Time to root cause:** ~8 minutes

---

## Best Practices Checklist

Before you ship, ask yourself:

### Instrumentation
- [ ] All services have tracing libraries configured
- [ ] Context propagation works across all service boundaries
- [ ] Database calls are instrumented
- [ ] External API calls are instrumented
- [ ] Message queue producers/consumers propagate context

### Span Quality
- [ ] Span names are descriptive (`POST /api/orders`, not `http_request`)
- [ ] Key business attributes are included (`order.id`, `user.id`)
- [ ] Errors are properly recorded with exception details
- [ ] Status codes are set correctly (OK, ERROR)

### Operational
- [ ] Sampling strategy is defined and configured
- [ ] Trace retention policy is set
- [ ] Team knows how to query traces
- [ ] Logs include `trace_id` for correlation
- [ ] Alerts can link to example traces

---

## Key Takeaways

1. **A trace is a story** — It tells you what happened to a single request across all your services

2. **The trace ID is your search key** — One ID connects everything that happened for one request

3. **Context propagation is critical** — Without it, your traces fragment into useless pieces

4. **Attributes make traces searchable** — Rich metadata transforms traces from timing diagrams to debugging tools

5. **Correlate with logs** — Traces show structure and timing; logs show details. Use both. See [Logging Done Right →](./logging)

6. **Sample intelligently** — Tail-based sampling keeps errors and slow requests while managing costs

7. **Learn to read the waterfall** — Quick pattern recognition in trace visualizations is a debugging superpower

Distributed tracing isn't just a nice-to-have in microservices architecture—it's the difference between "we think it might be the database" and "the inventory service is making an N+1 query that takes 430ms."

Invest in tracing. Your on-call rotation will thank you.

---

**Next**: [Metrics That Matter →](./metrics)
