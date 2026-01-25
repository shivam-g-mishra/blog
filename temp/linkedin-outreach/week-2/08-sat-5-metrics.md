# Post #8: 5 Metrics That Actually Matter
**Week 2 | Saturday | 8:30 AM PT**
**Format:** Text Post
**Blog Link:** Metrics

---

## POST CONTENT (Copy everything below the line)

---

Most teams track 100+ metrics.
Only 5 actually matter during incidents.

Here are the metrics we alert on at NVIDIA:

𝟭. 𝗘𝗿𝗿𝗼𝗿 𝗿𝗮𝘁𝗲 (𝗯𝘆 𝘀𝗲𝗿𝘃𝗶𝗰𝗲)
Not total errors - error RATE.
1000 errors in 1M requests = fine.
1000 errors in 1K requests = problem.

𝟮. 𝗣𝟵𝟵 𝗹𝗮𝘁𝗲𝗻𝗰𝘆
Average lies. P99 tells the truth.
If 1% of users wait 10 seconds, you have a problem.

𝟯. 𝗦𝗮𝘁𝘂𝗿𝗮𝘁𝗶𝗼𝗻
CPU, memory, disk, connections.
When you're at 80%, you're one spike from disaster.

𝟰. 𝗧𝗿𝗮𝗳𝗳𝗶𝗰 𝗱𝗲𝗹𝘁𝗮
Not absolute traffic - change from baseline.
50% drop at 2 PM on Tuesday = investigate.

𝟱. 𝗗𝗲𝗽𝗲𝗻𝗱𝗲𝗻𝗰𝘆 𝗵𝗲𝗮𝗹𝘁𝗵
Database latency, cache hit rate, external API status.
Your service is only as healthy as its dependencies.

Everything else? Nice to have for debugging.
But these 5 will catch 90% of issues.

What metrics does your team prioritize?

---
#Observability #Metrics #SRE #DevOps

💡 Full guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote a complete guide on metrics - what to track, how to alert, and common mistakes:

https://blog.shivam.info/docs/observability/metrics?utm_source=linkedin&utm_medium=social&utm_campaign=week2

Key insight: More metrics ≠ better observability.

The teams with the best incident response have fewer, better metrics with proper alerting thresholds.

---

## ENGAGEMENT TIPS

- Numbered lists perform well - easy to scan and discuss
- Ask: "Which of these does your team NOT track?"
- Great for sparking "we also track X" discussions
- Engage with disagreements respectfully
