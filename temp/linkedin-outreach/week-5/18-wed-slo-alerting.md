# Post #18: SLO-Based Alerting
**Week 5 | Wednesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** Alerting

---

## POST CONTENT (Copy everything below the line)

---

High CPU. Memory at 90%. Error count spiking.

None of these tell you if users are actually affected.

Stop alerting on symptoms. Start alerting on user impact.

𝗧𝗵𝗲 𝗼𝗹𝗱 𝘄𝗮𝘆:
→ CPU > 80%? Alert!
→ Memory > 90%? Alert!
→ Error count > 100? Alert!

The problem: These don't tell you if users are affected.

𝗧𝗵𝗲 𝗦𝗟𝗢 𝘄𝗮𝘆:
→ 99.9% of requests succeed (error budget: 0.1%)
→ 95% of requests complete in < 200ms
→ Availability target: 99.95%

Alert when you're burning through your error budget too fast.

𝗛𝗲𝗿𝗲'𝘀 𝘁𝗵𝗲 𝗺𝗮𝗴𝗶𝗰:

High CPU but users are fine? No alert.
Low CPU but users are failing? Alert!

You're alerting on what actually matters:
User experience.

𝗧𝗵𝗲 𝗺𝗮𝘁𝗵:

99.9% SLO = 43 minutes of downtime/month
If you burn 20 minutes in 1 hour = you're in trouble
Alert when burn rate > threshold

This is called "error budget burn rate alerting."

Game changer for on-call sanity.

Has your team adopted SLOs?

---
#SLO #SRE #Alerting #Observability

💡 Complete SLO guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote about implementing SLO-based alerting in practice:

https://blog.shivam.info/docs/observability/alerting?utm_source=linkedin&utm_medium=social&utm_campaign=week5

It covers:
→ How to define meaningful SLOs
→ Error budget calculation
→ Burn rate alerting setup
→ Multi-window alerting
→ Getting buy-in from leadership

The shift from symptom-based to SLO-based alerting transformed our on-call experience.

---

## ENGAGEMENT TIPS

- SLOs are hot topic in SRE community
- Be prepared for "but management wants uptime" discussions
- Acknowledge SLOs require organizational buy-in
- Share concrete examples of SLO improvements
