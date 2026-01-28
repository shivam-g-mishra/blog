# Post #20: The Runbook That Saved Our Incident Response
**Week 5 | Saturday | 8:30 AM PT**
**Format:** Text Post
**Blog Link:** Alerting

---

## POST CONTENT (Copy everything below the line)

---

2 hours → 20 minutes.

That's how much our MTTR dropped.

The secret? Runbooks.

𝗕𝗲𝗳𝗼𝗿𝗲 𝗿𝘂𝗻𝗯𝗼𝗼𝗸𝘀:

3 AM page arrives.
Junior engineer on-call.
"What do I do?"
Slack the senior engineer.
Wait for response.
Google the error.
Try random things.
Finally escalate.

𝗔𝗳𝘁𝗲𝗿 𝗿𝘂𝗻𝗯𝗼𝗼𝗸𝘀:

3 AM page arrives.
Click runbook link in alert.
Step 1: Check this dashboard
Step 2: If X, do Y
Step 3: If still failing, escalate to [team]
Done.

𝗪𝗵𝗮𝘁 𝗴𝗼𝗼𝗱 𝗿𝘂𝗻𝗯𝗼𝗼𝗸𝘀 𝗶𝗻𝗰𝗹𝘂𝗱𝗲:

→ What this alert means (plain English)
→ Who's affected and severity
→ Diagnostic steps (with links)
→ Remediation steps
→ When and how to escalate
→ Post-incident actions

𝗧𝗵𝗲 𝗿𝘂𝗹𝗲:

Every alert without a runbook is a failure waiting to happen.

If you can't document what to do, should you even alert on it?

Does your team have runbooks for every alert?

---
#Runbooks #SRE #IncidentResponse #DevOps

💡 Runbook template in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 I wrote about alerting best practices including runbook templates:

https://blog.shivamm.info/docs/observability/alerting?utm_source=linkedin&utm_medium=social&utm_campaign=week5

Key insight: The runbook should be written by someone who's been paged for this alert.

Not by the person who created the alert.
Not by documentation team.
By the person who actually fixed it.

That's where the real knowledge lives.

---

## ENGAGEMENT TIPS

- Very practical, actionable content
- Ask: "What's in your runbook template?"
- Share examples of good vs bad runbooks
- Discuss challenges of keeping runbooks updated
