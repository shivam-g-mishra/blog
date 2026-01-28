# Post #25: Tail-Based Sampling
**Week 7 | Tuesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** Scalable Architecture

---

## POST CONTENT (Copy everything below the line)

---

100% of errors. 1% of successes.

That's tail-based sampling. And it cut our storage costs by 80%.

𝗧𝗵𝗲 𝗽𝗿𝗼𝗯𝗹𝗲𝗺:

At scale, storing every trace is expensive.
1M requests/hour × 10 spans × 1KB = 10GB/hour
That's 240GB/day of trace data.

Most of it? Successful requests you'll never look at.

𝗛𝗲𝗮𝗱-𝗯𝗮𝘀𝗲𝗱 𝘀𝗮𝗺𝗽𝗹𝗶𝗻𝗴:
Decide at the START whether to keep a trace.
"Keep 10% of traces"
Problem: You might drop the error you needed.

𝗧𝗮𝗶𝗹-𝗯𝗮𝘀𝗲𝗱 𝘀𝗮𝗺𝗽𝗹𝗶𝗻𝗴:
Decide at the END based on what happened.
"Keep 100% of errors + 1% of successes"
Result: Every error preserved, storage reduced 80%.

𝗢𝘂𝗿 𝗿𝘂𝗹𝗲𝘀:

→ 100% of traces with errors
→ 100% of traces > 2s latency
→ 100% of traces from VIP customers
→ 5% random sample of everything else

𝗧𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁:

Storage reduced 80%.
Every debugging session still has the data we need.

What's your sampling strategy?

---
#Observability #Sampling #Tracing #DevOps

💡 Full sampling guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote about sampling strategies in our architecture guide:

https://blog.shivamm.info/blog/scalable-observability-architecture?utm_source=linkedin&utm_medium=social&utm_campaign=week7

Key insight: Sampling happens at the Collector level, not in your app.

Your app sends everything.
The Collector decides what to keep.

This means you can adjust sampling rules without redeploying.

---

## ENGAGEMENT TIPS

- Technical topic - good for senior engineers
- Discuss specific sampling ratios and rules
- Share cost savings from sampling
- Discuss the trade-off: you might miss something
