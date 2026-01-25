# Post #15: Structured Logging - Good vs Bad
**Week 4 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** Logging

---

## CAPTION (Copy everything below the line)

---

Good logs vs bad logs.

The difference between 10-minute debugging and 10-hour debugging.

Here's a visual guide ⬇️

---
#Logging #Observability #DevOps

💡 Complete guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 Full logging best practices guide:

https://blog.shivam.info/docs/observability/logging?utm_source=linkedin&utm_medium=social&utm_campaign=week4

Comment "LOGS" for the direct link!

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px)

### Slide 1 (Cover)
```
STRUCTURED LOGGING

Good vs Bad
(A Visual Guide)

[Swipe →]
```

### Slide 2
```
BAD LOG:

"Payment failed"

❌ Which payment?
❌ Which user?
❌ Why did it fail?
❌ Can't query or filter
```

### Slide 3
```
GOOD LOG:

{
  "event": "payment_failed",
  "user_id": "usr_123",
  "amount": 99.99,
  "error": "card_declined",
  "trace_id": "abc123"
}
```

### Slide 4
```
BAD: String concatenation

"User " + userId + " failed payment"

GOOD: Structured fields

{"user_id": userId, "event": "payment_failed"}

Fields are queryable. Strings are not.
```

### Slide 5
```
BAD: Missing context

ERROR: Connection timeout

GOOD: Full context

{
  "error": "connection_timeout",
  "service": "payment-gateway",
  "latency_ms": 30000,
  "retry_count": 3
}
```

### Slide 6
```
THE TRACE_ID RULE:

ALWAYS include trace_id in every log.

It's the link between:
• Your logs
• Your traces
• Your metrics

One ID to connect everything.
```

### Slide 7
```
LOG LEVELS (Use them right):

DEBUG - Development only
INFO - Normal operations
WARN - Unexpected but handled
ERROR - Failures requiring attention
FATAL - System cannot continue
```

### Slide 8 (CTA)
```
Want the complete logging guide?

Comment "LOGS" for the link.

Follow for more observability content.

blog.shivam.info
```
