# Post #14: Python Zero-Code Instrumentation
**Week 4 | Wednesday | 7:00 AM PT**
**Format:** Code Snippet Post
**Blog Link:** Python Integration

---

## POST CONTENT (Copy everything below the line)

---

Add observability to Python with zero code changes.

Seriously. Zero.

𝗦𝘁𝗲𝗽 𝟭: Install the packages
→ pip install opentelemetry-distro opentelemetry-exporter-otlp
→ opentelemetry-bootstrap -a install

𝗦𝘁𝗲𝗽 𝟮: Run with the wrapper
→ opentelemetry-instrument python app.py

That's it. You now have:
✓ Automatic traces for HTTP requests
✓ Database query instrumentation
✓ Framework-specific spans (Flask, Django, FastAPI)
✓ Metrics out of the box

𝗡𝗼 𝗰𝗼𝗱𝗲 𝗰𝗵𝗮𝗻𝗴𝗲𝘀.

The magic? OpenTelemetry's auto-instrumentation hooks into your existing libraries.

Works with: Flask, Django, FastAPI, SQLAlchemy, psycopg2, requests, aiohttp, and 50+ more.

What language does your team use most?

---
#Python #OpenTelemetry #Observability #DevOps

💡 Full guide with examples in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote a complete Python instrumentation guide with real examples:

https://blog.shivamm.info/docs/observability/integrations/python?utm_source=linkedin&utm_medium=social&utm_campaign=week4

It covers:
→ Auto-instrumentation setup
→ Manual instrumentation for custom spans
→ Adding business context to traces
→ Best practices for production
→ Common pitfalls to avoid

Also have guides for Go, Java, Node.js, and .NET.

---

## ENGAGEMENT TIPS

- Code posts do well with the right audience
- Ask follow-up: "What framework are you using?"
- Offer to create guides for requested languages
- Engage with people who share their setup challenges
