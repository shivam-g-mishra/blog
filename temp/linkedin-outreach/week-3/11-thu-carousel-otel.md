# Post #11: How OpenTelemetry Works (Visual)
**Week 3 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** OpenTelemetry

---

## CAPTION (Copy everything below the line)

---

OpenTelemetry in 8 slides.

No vendor lock-in.
One SDK for everything.
Send data anywhere.

Here's how it actually works ⬇️

---
#OpenTelemetry #Observability #DevOps #CloudNative

💡 Full guide in comments

---

## FIRST COMMENT (Post within 60 seconds)

📚 Want the complete OpenTelemetry guide?

https://blog.shivam.info/docs/observability/opentelemetry?utm_source=linkedin&utm_medium=social&utm_campaign=week3

It covers concepts, Collector setup, auto-instrumentation, and language-specific guides.

Comment "OTEL" and I'll send you the link directly!

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px)

### Slide 1 (Cover)
```
OPENTELEMETRY
EXPLAINED

The standard for observability
(No vendor lock-in)

[Swipe →]
```

### Slide 2
```
THE PROBLEM:

Every vendor has their own SDK.
Datadog SDK ≠ New Relic SDK ≠ Splunk SDK

Switch vendors = rewrite instrumentation.

Lock-in by design.
```

### Slide 3
```
THE SOLUTION:

OpenTelemetry = ONE standard SDK

Instrument once.
Send data anywhere.

Vendor-neutral by design.
```

### Slide 4
```
THE ARCHITECTURE:

Your App
    ↓ (OTel SDK)
OTel Collector
    ↓ (export)
Any Backend
(Jaeger, Grafana, Datadog, etc.)
```

### Slide 5
```
WHAT IT CAPTURES:

📈 METRICS
   Request rate, latency, errors

🔍 TRACES
   Request journey across services

📝 LOGS
   Events with context
```

### Slide 6
```
AUTO-INSTRUMENTATION:

Many languages need ZERO code changes.

Python: opentelemetry-instrument python app.py
Java: -javaagent:opentelemetry-agent.jar
Node: --require @opentelemetry/auto-instrumentations-node

Instant observability.
```

### Slide 7
```
THE COLLECTOR:

Receives → Processes → Exports

• Buffer and retry
• Sample and filter
• Transform and enrich
• Route to multiple destinations

One config file controls everything.
```

### Slide 8 (CTA)
```
Ready to try OpenTelemetry?

I wrote a complete getting-started guide.

Comment "OTEL" for the link.

Follow for more observability content.

blog.shivam.info
```
