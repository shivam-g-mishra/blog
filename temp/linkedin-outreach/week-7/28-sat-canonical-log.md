# Post #28: The Canonical Log Line Pattern
**Week 7 | Saturday | 8:30 AM PT**
**Format:** Text Post
**Blog Link:** Logging

---

## POST CONTENT (Copy everything below the line)

---

One log line per request.
Everything you need to debug.

This is the canonical log line pattern.

𝗧𝗵𝗲 𝗽𝗿𝗼𝗯𝗹𝗲𝗺:

Typical request generates 50+ log lines.
Finding context requires piecing together fragments.
Correlation is a nightmare.

𝗧𝗵𝗲 𝘀𝗼𝗹𝘂𝘁𝗶𝗼𝗻:

At request END, emit ONE log with everything:

```json
{
  "timestamp": "2024-01-15T10:23:45Z",
  "trace_id": "abc123",
  "method": "POST",
  "path": "/api/orders",
  "status": 500,
  "duration_ms": 234,
  "user_id": "usr_456",
  "error": "inventory_unavailable",
  "db_queries": 12,
  "cache_hits": 3,
  "cache_misses": 1
}
```

𝗪𝗵𝗮𝘁 𝘆𝗼𝘂 𝗰𝗮𝗻 𝗱𝗼:

→ Query all errors for user_456
→ Find requests with > 10 db_queries
→ Spot cache miss patterns
→ Jump to trace for details
→ One line = complete picture

𝗧𝗵𝗲 𝗿𝘂𝗹𝗲𝘀:

1. Emit at request completion
2. Include all relevant context
3. Always include trace_id
4. Structure as JSON
5. Keep other logs for verbose debugging

Are you using canonical log lines?

---
#Logging #Observability #DevOps

💡 Full logging guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote about canonical log lines and other logging patterns:

https://blog.shivamm.info/docs/observability/logging?utm_source=linkedin&utm_medium=social&utm_campaign=week7

Key insight: Canonical log lines don't REPLACE your other logs.

They provide a summary layer on top.
Use them for dashboards and quick queries.
Use detailed logs for deep debugging.

Both. Not either/or.

---

## ENGAGEMENT TIPS

- Practical pattern engineers can implement immediately
- Share your canonical log line schema
- Discuss what fields to include for different apps
- Ask: "What context do you wish was in your logs?"
