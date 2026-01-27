---
# Required
sidebar_position: 6
title: "Logging Done Right — Structured Logging Guide"
description: >-
  Master structured logging with this practical guide. Learn what to log, 
  how to log it, and patterns that help you debug production issues at 3 AM.

# SEO
keywords:
  - logging
  - structured logging
  - log levels
  - canonical log lines
  - observability
  - debugging
  - JSON logging
  - log correlation

# Social sharing
og_title: "Logging Done Right: A Practical Guide"
og_description: "The difference between a 10-minute investigation and a 3-hour nightmare is logging quality."
og_image: "/img/observability-fundamentals.svg"

# Content management
date_published: 2025-01-22
date_modified: 2025-01-24
author: shivam
reading_time: 18
content_type: explanation
---

# Logging Done Right: A Practical Guide

I've spent years debugging production systems, and I'll tell you this: the difference between a 10-minute investigation and a 3-hour nightmare often comes down to logging quality. Not log volume—quality.

Most engineering teams approach logging as an afterthought. They sprinkle `console.log` or `logger.info` statements throughout the codebase, dump entire objects when errors occur, and call it a day. Then at 3 AM, when production is on fire and hundreds of customers are affected, they find themselves staring at walls of useless text like:

```
INFO Processing request...
INFO Done.
ERROR Something went wrong
```

Sound familiar? Let's fix that.

## The Problem with Traditional Logging

Here's a log line I've seen in production more times than I'd like to admit:

```
2024-06-15 14:23:45 ERROR Payment failed for user
```

When you're on call and you see this, your brain immediately asks a dozen questions:
- Which user? Which payment?
- What was the amount? What payment method?
- Was this a timeout, a validation error, or a gateway rejection?
- Is this a one-off or are payments failing across the board?
- What request triggered this? Can I correlate it with anything else?

That single log line answers none of these questions. It's noise masquerading as signal.

Now compare it to this:

```json
{
  "timestamp": "2024-06-15T14:23:45.891Z",
  "level": "error",
  "service": "payment-service",
  "version": "2.4.1",
  "message": "Payment processing failed",
  "trace_id": "7b3e9f2a4c1d8e5b",
  "span_id": "a1b2c3d4e5f6",
  "request_id": "req_abc123xyz",
  "user_id": "usr_456",
  "order_id": "ord_789",
  "payment": {
    "amount_cents": 9999,
    "currency": "USD",
    "provider": "stripe",
    "method": "card"
  },
  "error": {
    "code": "card_declined",
    "message": "The card was declined due to insufficient funds",
    "retriable": false
  },
  "duration_ms": 234
}
```

With this structured log entry, I can:
- Query all payment failures for this specific user
- Find all `card_declined` errors in the last hour
- Jump directly to the distributed trace
- See exactly how long the operation took
- Identify if this affects a specific payment provider
- Correlate with other events in the same request flow

The difference isn't just formatting—it's the difference between being able to do your job and fumbling in the dark.

---

## Structured Logging: The Foundation

Structured logging means treating logs as data, not text. Instead of constructing human-readable sentences, you emit key-value pairs that machines can parse, index, and query efficiently.

### Why JSON?

JSON has become the de facto standard for structured logs, and for good reason:

| Benefit | Description |
|---------|-------------|
| **Machine parseable** | Log aggregators can automatically extract fields |
| **Self-describing** | Field names provide context without external schema |
| **Queryable** | Filter by any field: `user_id = "usr_456" AND level = "error"` |
| **Extensible** | Add new fields without breaking existing queries |
| **Universal** | Every language and tool understands JSON |

### The Anatomy of a Good Log Entry

Every structured log entry should include these foundational fields:

```json
{
  "timestamp": "2024-06-15T14:23:45.891Z",  // ISO 8601 with milliseconds
  "level": "info",                           // Log severity
  "service": "order-service",                // Which service emitted this
  "version": "1.2.3",                        // Service version (crucial for debugging)
  "environment": "production",               // Environment context
  "host": "pod-xyz-123",                     // Where this ran
  "message": "Order placed successfully"     // Human-readable summary
}
```

Beyond these basics, add context relevant to what you're logging:

```json
{
  // ... base fields ...
  "trace_id": "7b3e9f2a4c1d8e5b",           // For distributed tracing correlation
  "span_id": "a1b2c3d4e5f6",                // Current span
  "request_id": "req_abc123",               // Request correlation
  "user_id": "usr_456",                     // Who triggered this
  "order_id": "ord_789",                    // Business entity
  "duration_ms": 145,                        // How long it took
  // ... domain-specific fields ...
}
```

---

## Log Levels: Using Them Correctly

Log levels exist to help you filter signal from noise. But I've seen codebases where everything is logged as INFO, or where ERROR is used for expected business conditions. Here's how to think about each level:

### ERROR: Something Broke

Use ERROR when something failed and likely needs attention. This should trigger alerts or at least warrant investigation.

```json
{
  "level": "error",
  "message": "Database connection pool exhausted",
  "error": {
    "type": "ConnectionPoolException",
    "message": "Waited 30000ms for connection, pool exhausted",
    "pool_size": 20,
    "active_connections": 20,
    "waiting_requests": 47
  }
}
```

**Not an ERROR**: A user entering an invalid email. That's expected behavior, not a system failure.

### WARN: Something's Off, But We Recovered

Use WARN for situations that are unusual or degraded but didn't cause a failure. These are early warning signs.

```json
{
  "level": "warn",
  "message": "Response time degradation detected",
  "endpoint": "/api/search",
  "p99_latency_ms": 2400,
  "threshold_ms": 1000,
  "sample_window": "5m"
}
```

**Good use cases**: Cache miss rates increasing, retry succeeded after failure, deprecated API called, resource utilization approaching limits.

### INFO: Significant Business Events

Use INFO for events that represent meaningful state changes or business transactions. Someone reading only INFO logs should understand what the system accomplished.

```json
{
  "level": "info",
  "message": "Order completed",
  "order_id": "ord_789",
  "user_id": "usr_456",
  "total_cents": 15999,
  "item_count": 3,
  "payment_method": "card",
  "duration_ms": 892
}
```

**Good INFO candidates**: User registered, order placed, payment processed, job completed, configuration changed.

**Not INFO**: "Entering function X" or "Loop iteration 47 of 100"—that's DEBUG or TRACE.

### DEBUG: Development and Troubleshooting

DEBUG is for detailed information useful during development or active troubleshooting. This level should typically be disabled in production but easily enabled when investigating issues.

```json
{
  "level": "debug",
  "message": "Cache lookup result",
  "cache_key": "inventory:sku_123",
  "hit": false,
  "lookup_duration_ms": 2
}
```

**Production consideration**: Have a mechanism to temporarily enable DEBUG logging for specific services or requests without redeploying.

### TRACE: The Firehose

TRACE is for extremely detailed execution flow. This level generates massive volume and should essentially never run in production.

| Level | When to Use | Production Default |
|-------|-------------|-------------------|
| ERROR | System failures requiring attention | ✅ Always on |
| WARN | Degraded conditions, potential problems | ✅ Always on |
| INFO | Business events, state changes | ✅ Always on |
| DEBUG | Troubleshooting details | ❌ Off (enable when needed) |
| TRACE | Execution flow details | ❌ Never in production |

---

## The Canonical Log Line Pattern

One of the most impactful logging patterns I've adopted comes from engineering teams at companies like Stripe. It's called the **canonical log line**, and the concept is simple but powerful:

**Emit one comprehensive log entry per request that contains everything you'd want to know about that request.**

Instead of scattering 10 log lines throughout a request's lifecycle:

```
INFO Request started
INFO Validated input
INFO User authenticated
INFO Checked inventory
DEBUG Cache miss for inventory
INFO Inventory reserved
INFO Payment initiated
INFO Payment completed
INFO Order created
INFO Request completed
```

You emit a single, rich log entry when the request completes:

```json
{
  "timestamp": "2024-06-15T14:23:46.234Z",
  "level": "info",
  "message": "HTTP request completed",
  "service": "api-gateway",
  
  "http": {
    "method": "POST",
    "path": "/api/v1/orders",
    "status_code": 201,
    "request_size_bytes": 1247,
    "response_size_bytes": 892
  },
  
  "timing": {
    "total_ms": 892,
    "auth_ms": 12,
    "validation_ms": 3,
    "inventory_check_ms": 145,
    "payment_ms": 623,
    "database_ms": 89
  },
  
  "auth": {
    "user_id": "usr_456",
    "method": "jwt",
    "scopes": ["orders:write"]
  },
  
  "business": {
    "order_id": "ord_789",
    "item_count": 3,
    "total_cents": 15999
  },
  
  "performance": {
    "cache_hits": 2,
    "cache_misses": 1,
    "db_queries": 4
  },
  
  "trace_id": "7b3e9f2a4c1d8e5b",
  "request_id": "req_abc123"
}
```

### Why This Works

1. **One query finds everything**: Instead of correlating multiple log lines, a single query by `request_id` or `trace_id` gives you the complete picture.

2. **Easy anomaly detection**: You can query for requests where `timing.payment_ms > 1000` or `performance.db_queries > 10`.

3. **Metrics derivation**: You can derive metrics like p99 latency, error rates by endpoint, or cache hit ratios directly from logs.

4. **Reduced volume**: Counterintuitively, canonical log lines often reduce total log volume because you're not emitting partial information repeatedly.

### Implementation Approach

Build up context throughout the request lifecycle, then emit it all at once:

```go
func HandleRequest(w http.ResponseWriter, r *http.Request) {
    // Initialize request context with timing
    ctx := NewRequestContext(r)
    
    // Each step adds to the context
    user, err := authenticate(ctx, r)
    ctx.Set("auth.user_id", user.ID)
    ctx.SetTiming("auth_ms", time.Since(authStart))
    
    order, err := processOrder(ctx, payload)
    ctx.Set("business.order_id", order.ID)
    ctx.SetTiming("processing_ms", time.Since(processStart))
    
    // Single log entry at the end
    defer ctx.EmitCanonicalLog()
}
```

---

## What to Log: A Practical Checklist

Over the years, I've developed a mental checklist for what information genuinely helps during incident response.

### Always Log

| Category | Examples | Why It Matters |
|----------|----------|----------------|
| **Identity** | `user_id`, `account_id`, `tenant_id` | "Who was affected?" |
| **Correlation** | `trace_id`, `request_id`, `session_id` | "What else happened in this flow?" |
| **Timing** | `duration_ms`, `started_at`, `queue_time_ms` | "Where did we spend time?" |
| **Outcome** | `status_code`, `success`, `error_code` | "Did it work?" |
| **Context** | `endpoint`, `operation`, `service_version` | "What were we trying to do?" |

### Log Conditionally

Include these when they're relevant to the operation:

| Category | Examples | When to Include |
|----------|----------|-----------------|
| **Business entities** | `order_id`, `product_sku`, `invoice_id` | When that entity is involved |
| **Quantities** | `item_count`, `amount_cents`, `retry_count` | When they affect behavior |
| **Performance** | `db_queries`, `cache_hits`, `bytes_processed` | For performance-sensitive paths |
| **Decision points** | `feature_flag`, `experiment_variant`, `rate_limited` | When decisions affect the flow |

### Never Log

This is critical. Some data should never appear in logs:

| Category | Examples | Risk |
|----------|----------|------|
| **Credentials** | Passwords, API keys, tokens, secrets | Credential theft |
| **Payment data** | Full card numbers, CVVs, bank accounts | PCI compliance violation |
| **PII (unmasked)** | SSN, full name + DOB, medical records | Privacy regulations, GDPR |
| **Internal topology** | Internal IPs, database hostnames | Attack surface exposure |

Instead, log derived or masked values:

```json
{
  "payment_method": "card",
  "card_last_four": "4242",
  "card_brand": "visa"
}
```

Not:

```json
{
  "card_number": "4242424242424242",
  "cvv": "123"
}
```

---

## Error Logging: Capturing the Full Picture

When errors occur, the quality of your error logs determines how quickly you can resolve them. Here's a pattern that works:

```json
{
  "timestamp": "2024-06-15T14:23:45.891Z",
  "level": "error",
  "message": "Failed to process payment",
  "service": "payment-service",
  
  "error": {
    "type": "PaymentGatewayError",
    "code": "gateway_timeout",
    "message": "Request to payment provider timed out after 30000ms",
    "retriable": true,
    "stack": "PaymentGatewayError: Request timed out\n    at PaymentClient.charge (payment-client.js:142)\n    at OrderProcessor.processPayment (order-processor.js:89)\n    ..."
  },
  
  "context": {
    "user_id": "usr_456",
    "order_id": "ord_789",
    "amount_cents": 9999,
    "provider": "stripe",
    "attempt": 2,
    "max_attempts": 3
  },
  
  "request": {
    "trace_id": "7b3e9f2a4c1d8e5b",
    "request_id": "req_abc123",
    "endpoint": "POST /api/orders"
  }
}
```

### Error Logging Best Practices

**1. Log errors once, at the right level**

Don't catch an error, log it, then rethrow it for the next layer to log again. You end up with:

```
ERROR Failed to query database
ERROR Failed to fetch user
ERROR Failed to authenticate
ERROR Failed to process request
```

Four log entries for one error. Instead, let errors propagate and log once at the handler level with full context.

**2. Include the original error**

When wrapping errors, preserve the original:

```json
{
  "error": {
    "type": "OrderProcessingError",
    "message": "Failed to complete order",
    "cause": {
      "type": "PaymentError",
      "message": "Card declined",
      "code": "card_declined"
    }
  }
}
```

**3. Distinguish expected from unexpected errors**

A user entering invalid data isn't the same as a database connection failure. Consider using INFO or WARN for expected business errors:

```json
{
  "level": "warn",
  "message": "Payment declined",
  "error_type": "business",
  "reason": "insufficient_funds",
  "user_id": "usr_456"
}
```

Reserve ERROR for genuine system failures.

**4. Include retry context**

If operations can retry, log where you are in that process:

```json
{
  "level": "warn",
  "message": "Payment attempt failed, will retry",
  "attempt": 2,
  "max_attempts": 3,
  "next_retry_in_ms": 5000,
  "backoff_strategy": "exponential"
}
```

---

## Correlation: Connecting the Dots

In a distributed system, a single user action might touch ten different services. The ability to follow that action across all services is essential.

### The Trace ID is Your Best Friend

Always propagate and log the trace ID from your distributed tracing system. For a complete guide to distributed tracing concepts, see [Distributed Tracing Explained →](./tracing).

```json
{
  "trace_id": "7b3e9f2a4c1d8e5b",
  "span_id": "a1b2c3d4e5f6",
  "parent_span_id": "f6e5d4c3b2a1"
}
```

When investigating an issue:
1. Find a relevant log entry
2. Copy the `trace_id`
3. Search all logs for that `trace_id`
4. Or jump directly to the distributed trace in Jaeger/Tempo

### Request IDs for Non-Traced Flows

Not everything participates in distributed tracing (batch jobs, scheduled tasks). Generate and propagate a `request_id` or `correlation_id` for these:

```json
{
  "request_id": "job_20240615_142300_abc123",
  "job_type": "invoice_generation",
  "batch_id": "batch_456"
}
```

### User Session Correlation

For user-facing issues, being able to query all logs for a user session is invaluable:

```json
{
  "session_id": "sess_xyz789",
  "user_id": "usr_456"
}
```

---

## Performance Considerations

Logging isn't free. Here are patterns to keep logging performant:

### Conditional Logging

Check the log level before constructing expensive log data:

```go
// Good: check level first
if logger.IsDebugEnabled() {
    logger.Debug("Cache state", 
        "entries", cache.DumpAllEntries()) // Expensive operation
}

// Bad: always compute, then filter
logger.Debug("Cache state", 
    "entries", cache.DumpAllEntries()) // Computed even if DEBUG is off
```

### Asynchronous Logging

In high-throughput systems, consider async logging with bounded buffers:

```
App Thread → Log Queue → Background Writer → Output
              (bounded)
```

But be aware of the tradeoff: if the application crashes, buffered logs may be lost.

### Sampling

For extremely high-volume paths, consider sampling:

```json
{
  "message": "Cache lookup completed",
  "sampled": true,
  "sample_rate": 0.01
}
```

Only log 1% of these events but include the `sample_rate` so you can extrapolate when analyzing.

### Keep Log Entries Reasonably Sized

Avoid logging entire request/response bodies. If you need payload data, log specific fields:

```json
{
  "request_body_size_bytes": 15234,
  "response_body_size_bytes": 892,
  "item_count": 47
}
```

Not:

```json
{
  "request_body": "... 15KB of JSON ...",
  "response_body": "... more JSON ..."
}
```

---

## Logging in Practice: A Service Example

Let me tie this together with a realistic example. Here's how logging might look in a payment service:

### Request Entry Point

```json
{
  "timestamp": "2024-06-15T14:23:45.100Z",
  "level": "info",
  "message": "Payment request received",
  "trace_id": "7b3e9f2a4c1d8e5b",
  "request_id": "req_abc123",
  "user_id": "usr_456",
  "endpoint": "POST /api/payments",
  "amount_cents": 9999,
  "currency": "USD"
}
```

### External Service Call

```json
{
  "timestamp": "2024-06-15T14:23:45.500Z",
  "level": "info",
  "message": "Payment gateway response",
  "trace_id": "7b3e9f2a4c1d8e5b",
  "request_id": "req_abc123",
  "provider": "stripe",
  "provider_request_id": "pi_xyz789",
  "status": "succeeded",
  "duration_ms": 389
}
```

### On Error (if it had failed)

```json
{
  "timestamp": "2024-06-15T14:23:45.500Z",
  "level": "error",
  "message": "Payment gateway error",
  "trace_id": "7b3e9f2a4c1d8e5b",
  "request_id": "req_abc123",
  "user_id": "usr_456",
  "provider": "stripe",
  "error": {
    "code": "rate_limited",
    "message": "Too many requests",
    "provider_status": 429,
    "retriable": true,
    "retry_after_seconds": 30
  },
  "duration_ms": 89
}
```

### Canonical Request Complete

```json
{
  "timestamp": "2024-06-15T14:23:45.650Z",
  "level": "info",
  "message": "Payment request completed",
  "trace_id": "7b3e9f2a4c1d8e5b",
  "request_id": "req_abc123",
  "user_id": "usr_456",
  "endpoint": "POST /api/payments",
  "status_code": 200,
  "success": true,
  
  "timing": {
    "total_ms": 550,
    "validation_ms": 5,
    "gateway_ms": 389,
    "database_ms": 45
  },
  
  "payment": {
    "id": "pay_123",
    "amount_cents": 9999,
    "currency": "USD",
    "provider": "stripe",
    "provider_ref": "pi_xyz789"
  }
}
```

---

## Checklist: Before You Ship

Before deploying changes, ask yourself these questions about your logging:

### Completeness
- [ ] Can I reconstruct what happened during a request from logs alone?
- [ ] Are all error paths logging sufficient context?
- [ ] Can I correlate logs across services using trace_id or request_id?

### Quality
- [ ] Am I using structured fields, not string interpolation?
- [ ] Are log levels appropriate (ERROR for failures, INFO for events)?
- [ ] Are field names consistent with other services?

### Security
- [ ] Have I verified no secrets or credentials are logged?
- [ ] Is PII masked or excluded?
- [ ] Are log files protected with appropriate access controls?

### Performance
- [ ] Is expensive data only computed when the log level is enabled?
- [ ] Are log entries reasonably sized (no huge payloads)?
- [ ] Am I sampling high-volume debug logs appropriately?

---

## Key Takeaways

1. **Treat logs as data, not text** — structured JSON with queryable fields
2. **Use log levels correctly** — ERROR for failures, INFO for business events, DEBUG for troubleshooting
3. **Adopt canonical log lines** — one rich entry per request beats scattered fragments
4. **Always include correlation IDs** — trace_id and request_id are non-negotiable
5. **Never log secrets** — no credentials, tokens, or unmasked PII
6. **Log at the right moment** — prefer one comprehensive entry over many partial ones
7. **Think about the 3 AM debugger** — will future-you thank present-you for this log?

Good logging is an investment that pays dividends every time something goes wrong in production—and something always goes wrong in production.

---

**Next**: [Understanding OpenTelemetry →](./opentelemetry)
