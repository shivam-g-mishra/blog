# Post #27: Debug Any Incident in 10 Minutes
**Week 7 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** Three Pillars

---

## CAPTION (Copy everything below the line)

---

The 10-minute incident debugging framework.

Works for any production issue ⬇️

---
#Debugging #Observability #SRE #DevOps

💡 Full guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 This framework is based on the three pillars working together:

https://blog.shivam.info/docs/observability/three-pillars?utm_source=linkedin&utm_medium=social&utm_campaign=week7

Comment "DEBUG" for the complete guide!

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px)

### Slide 1 (Cover)
```
DEBUG ANY INCIDENT
IN 10 MINUTES

A framework that actually works

[Swipe →]
```

### Slide 2
```
MINUTE 0-2: SCOPE

What's affected?
• Which service?
• Which endpoints?
• Which users?

Check error rate dashboard.
Note the start time.
```

### Slide 3
```
MINUTE 2-4: CORRELATE

What changed at that time?
• Deployment?
• Config change?
• Traffic spike?
• Dependency issue?

Check deployment timeline.
```

### Slide 4
```
MINUTE 4-6: ZOOM IN

Filter logs to affected timeframe.
Look for:
• Error messages
• Stack traces
• Connection issues

The logs tell the story.
```

### Slide 5
```
MINUTE 6-8: TRACE

Pick a failing request.
Follow the trace:
• Where did it slow down?
• Where did it error?
• What's different from success?

The trace shows the path.
```

### Slide 6
```
MINUTE 8-10: ROOT CAUSE

Connect the dots:
• Metrics showed spike at 10:15
• Logs showed "pool exhausted"
• Trace showed N+1 query bug
• Deployment at 10:12

ROOT CAUSE: New code has N+1 bug
```

### Slide 7
```
THE KEY INSIGHT:

Metrics → WHAT is wrong
Logs → WHY it's wrong
Traces → WHERE it's wrong

Use all three together.
Not separately.
```

### Slide 8 (CTA)
```
PRACTICE THIS FRAMEWORK.

It becomes muscle memory.

Want the complete debugging guide?
Comment "DEBUG"

blog.shivam.info
```
