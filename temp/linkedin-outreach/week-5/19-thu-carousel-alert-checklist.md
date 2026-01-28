# Post #19: The Alert Quality Checklist
**Week 5 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** Alerting

---

## CAPTION (Copy everything below the line)

---

Is your alert worth waking someone up at 3 AM?

Use this checklist before creating any alert ⬇️

---
#Alerting #SRE #OnCall #DevOps

💡 Full alerting guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 Complete alerting best practices:

https://blog.shivamm.info/docs/observability/alerting?utm_source=linkedin&utm_medium=social&utm_campaign=week5

Comment "ALERTS" for the direct link!

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px)

### Slide 1 (Cover)
```
THE ALERT QUALITY
CHECKLIST

Before you create any alert,
ask these 7 questions.

[Swipe →]
```

### Slide 2
```
QUESTION 1:

Does this require
IMMEDIATE human action?

If it can wait until morning,
it's not an alert.
It's a ticket.
```

### Slide 3
```
QUESTION 2:

Is the IMPACT clear?

"High CPU" = unclear
"Checkout failing for 10% of users" = clear

Alerts need business context.
```

### Slide 4
```
QUESTION 3:

Can the responder
actually DO something?

If there's no action to take,
there's no reason to page.
```

### Slide 5
```
QUESTION 4:

Does it have a RUNBOOK?

No runbook = responder guessing
Runbook = clear next steps

Every alert needs documentation.
```

### Slide 6
```
QUESTION 5:

Would YOU want to be
woken up for this?

If the answer is no,
delete the alert.
```

### Slide 7
```
QUESTION 6:

Is this alert UNIQUE?

One incident = one alert
Not 17 alerts for the same problem.

Group and deduplicate.
```

### Slide 8
```
QUESTION 7:

Is it measuring USER IMPACT?

CPU usage = symptom
Failed requests = impact

Alert on impact, not symptoms.
```

### Slide 9 (CTA)
```
THE TARGET:

< 2 pages per on-call shift
Every page = real incident

Want the full alerting guide?
Comment "ALERTS"

blog.shivamm.info
```
