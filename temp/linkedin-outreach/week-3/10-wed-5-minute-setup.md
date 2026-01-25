# Post #10: Set Up Observability in 5 Minutes
**Week 3 | Wednesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** Single-Node Setup

---

## POST CONTENT (Copy everything below the line)

---

"Observability is too complex to self-host."

I used to believe this.

Then I built a setup that takes 5 minutes:

Step 1: Clone the repo
Step 2: Run "make up"
Step 3: Open localhost:3000

That's it. Full observability stack running.

𝗪𝗵𝗮𝘁 𝘆𝗼𝘂 𝗴𝗲𝘁:

→ Grafana (dashboards)
→ Prometheus (metrics)
→ Loki (logs)
→ Tempo or Jaeger (traces)
→ OpenTelemetry Collector (unified ingestion)
→ Pre-built dashboards
→ Sample alerting rules

𝗛𝗮𝗻𝗱𝗹𝗲𝘀:
~50K events/second on a single node.

That's enough for most teams to start.

𝗧𝗵𝗲 𝗽𝗼𝗶𝗻𝘁:

Don't wait for the "perfect" observability setup.
Start with something that works.
Iterate as you learn what you actually need.

Most teams over-engineer on day one.
Start simple. Scale when you need to.

Have you tried running your own observability stack?

---
#Observability #OpenTelemetry #DevOps #Grafana

💡 Full setup guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote a complete setup guide with everything you need:

https://blog.shivam.info/blog/single-node-observability-setup?utm_source=linkedin&utm_medium=social&utm_campaign=week3

It covers:
→ Architecture overview
→ Resource requirements
→ Configuration for each component
→ How to send your first traces/metrics/logs
→ Scaling path when you outgrow single-node

Repo: github.com/shivam-g-mishra/opensource-otel-setup

Star it, fork it, improve it. PRs welcome!

---

## ENGAGEMENT TIPS

- This is a "try it now" post - drives GitHub traffic
- Engage with people who try it and share results
- Ask: "What's preventing you from running self-hosted?"
- Be ready to help with common setup issues
