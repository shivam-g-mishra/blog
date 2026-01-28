# Post #13: Why Your Logs Are Useless
**Week 4 | Tuesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** Logging

---

## POST CONTENT (Copy everything below the line)

---

"ERROR: Payment failed for user"

Great.
Which user?
Which payment?
Why did it fail?

This log helps no one at 3 AM.

Here's the difference:

𝗕𝗮𝗱 𝗹𝗼𝗴:
ERROR Payment failed

𝗚𝗼𝗼𝗱 𝗹𝗼𝗴:
{
  "error": "card_declined",
  "user_id": "usr_456",
  "trace_id": "abc123",
  "duration_ms": 234
}

Now I can:
✓ Query all failures for this user
✓ Jump to the distributed trace
✓ See exactly what went wrong
✓ Correlate with other events

𝗧𝗵𝗲 𝗿𝘂𝗹𝗲𝘀:

1. Structured JSON (not strings)
2. Always include trace_id
3. Add business context
4. Use log levels correctly
5. Never log secrets

What's the worst log message you've seen in production?

---
#Logging #Observability #DevOps

💡 Complete guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote a complete logging guide - structured logging, correlation, and common mistakes:

https://blog.shivamm.info/docs/observability/logging?utm_source=linkedin&utm_medium=social&utm_campaign=week4

Key sections:
→ Structured logging best practices
→ The canonical log line pattern
→ Log levels and when to use them
→ Correlating logs with traces
→ What NOT to log (secrets, PII)

Good logging is the foundation of good observability.

---

## ALTERNATIVE HOOKS

**Alt 1:** "Your logs are lying to you. Here's proof."

**Alt 2:** "I reviewed 1000 log messages. 900 were useless."

**Alt 3:** "The worst log message I've ever seen (and how to fix it)."

---

## ENGAGEMENT TIPS

- People LOVE sharing bad log examples
- This post tends to get lots of "worst log" stories
- Engage with humor - logging war stories are relatable
- Example reply: "Oh no, I've definitely written that exact log before 😅"
