---
# Required
sidebar_position: 3
title: "Choosing Design Patterns — A Practical Decision Framework"
description: >-
  Learn how to choose the right design pattern using a repeatable framework.
  Avoid over-engineering and make decisions based on real constraints.

# SEO
keywords:
  - how to choose design pattern
  - when to use design patterns
  - design pattern decision framework
  - pattern selection guide
  - which design pattern

# Social sharing
og_title: "Choosing Design Patterns: A Practical Decision Framework"
og_description: "A battle-tested framework for picking the right pattern without over-engineering."
og_image: "/img/social-card.svg"

# Content management
date_published: 2026-01-25
date_modified: 2026-01-25
author: shivam
reading_time: 12
content_type: explanation
---

# Pattern Selection Framework

The worst design pattern is the one you commit to too early.

I learned this the hard way in 2020, building platform tooling at NVIDIA. We were designing a new configuration system, and someone on the team had just finished reading about the Abstract Factory pattern. "This is perfect," they said. "We can have different factories for production, staging, and development environments."

Three weeks later, we had a beautiful hierarchy of factories producing families of configuration objects. The code was elegant. The UML diagram was impressive. And then we realized: we only needed two configuration variants, both known at compile time. A simple if-else would have taken an afternoon. Instead, we'd built an aircraft carrier to cross a puddle.

The configuration system worked, but it was harder to understand, harder to modify, and harder to onboard new team members to. The pattern wasn't wrong—it just didn't fit the problem we actually had.

**A pattern should reduce the total cost of change.** If it doesn't, you've made things worse, not better. This framework helps you figure out when that's actually true.

---

## Step 1: Name the Pain

Patterns are answers. Before you pick one, make sure you understand the question.

Ask yourself these specific questions about the code you're working with:

- **What breaks when this code changes?** If you add a new variant, how many files do you touch? If the answer is "just one," you probably don't need a pattern.

- **Where do new requirements consistently add friction?** Every time product asks for a new notification channel, do you find yourself copying and modifying existing code? That's a sign.

- **What part of the code do people avoid touching?** In every codebase, there's a file or module that engineers route around because changes there are risky. That's often where a pattern is needed—or where a pattern was misapplied.

- **Is this pain recurring or one-time?** If it's a one-time problem, solve it simply. Patterns pay off through repetition.

**If you can't name the pain, you're not ready to pick a pattern.**

Here's a concrete example from our CI/CD platform. Engineers kept complaining about adding new deployment targets. I dug in and found the pain: every new target required changes to the core deployment service, the API layer, the UI, and the test suite. Four files minimum, often more. The pain was real, recurring, and measurable. That's when we introduced Strategy—and it reduced new target integration from four files to one.

---

## Step 2: Map the Problem to a Family

Once you've named the pain, narrow down to a pattern family before picking a specific pattern.

### Creational: "Object creation is the problem"

You need a Creational pattern when:
- Construction logic is duplicated across the codebase
- You need to create different variants but keep a stable API
- Object creation is complex (many parameters, initialization steps)
- You want to defer decisions about which concrete class to instantiate

**Symptoms in code:**
- Multiple places calling `new ConcreteClass()` with the same configuration
- Switch statements that choose which class to instantiate
- Constructors with 8+ parameters
- Comments like "// TODO: make this configurable"

### Structural: "Object composition is the problem"

You need a Structural pattern when:
- You're integrating incompatible interfaces
- You want to add behavior without modifying existing classes
- You need to simplify a complex subsystem
- You're managing hierarchical or tree-like structures

**Symptoms in code:**
- Wrapper classes that translate between interfaces
- Inheritance hierarchies that are getting out of control
- Multiple classes that need the same cross-cutting behavior
- Complex initialization sequences that callers keep getting wrong

### Behavioral: "Object interaction is the problem"

You need a Behavioral pattern when:
- Multiple objects need to respond to the same events
- Algorithms vary independently of the objects that use them
- You need to encapsulate operations as objects
- Complex conditional logic determines behavior

**Symptoms in code:**
- Large switch statements or if-else chains for behavior selection
- Tight coupling between objects that shouldn't know about each other
- Duplicated conditional logic across multiple methods
- Hard-coded sequences that need to become flexible

---

## Step 3: Choose the Simplest Pattern That Works

Within a family, multiple patterns might fit. Always start with the simplest option.

### Decision Matrix by Family

**Creational Patterns:**

| If your problem is... | Consider... | Before using the more complex... |
|----------------------|-------------|----------------------------------|
| Need to create variants of one thing | Factory Method | Abstract Factory |
| Complex construction with many options | Builder | Factory + Builder |
| Cloning is cheaper than constructing | Prototype | (use directly) |
| Exactly one instance, globally | Singleton | (be sure you need this) |
| Need families of related objects | Abstract Factory | (this is the right level) |

**Structural Patterns:**

| If your problem is... | Consider... | Before using the more complex... |
|----------------------|-------------|----------------------------------|
| Making interfaces compatible | Adapter | Bridge |
| Adding optional behavior | Decorator | Composite + Decorator |
| Simplifying a complex subsystem | Facade | (use directly) |
| Treating parts/wholes uniformly | Composite | (use directly) |
| Controlling access | Proxy | (use directly) |

**Behavioral Patterns:**

| If your problem is... | Consider... | Before using the more complex... |
|----------------------|-------------|----------------------------------|
| Swapping algorithms | Strategy | State |
| Notifying multiple observers | Observer | Mediator |
| Encapsulating requests | Command | Chain of Responsibility |
| Traversing structures | Iterator | Visitor |

**When two patterns could work, choose the one with the smallest surface area.** More classes, more interfaces, more abstraction layers—all of these have ongoing maintenance costs.

---

## Step 4: Validate Against Red Flags

Before you commit to a pattern, check for these warning signs:

### 🚩 Red Flag: More classes than clarity

If the pattern adds more classes than it removes confusion, you're over-engineering.

I've seen PRs that introduce four new files—interface, abstract class, two concrete implementations—to solve a problem that existed in exactly one place. That's not a pattern; that's speculation about future requirements disguised as architecture.

**The test:** Can you explain the pattern's benefit in one sentence that a junior developer would understand? If not, reconsider.

### 🚩 Red Flag: The pattern is the goal

Listen for phrases like "we should use a Factory here" without a clear explanation of why. When the pattern becomes the goal rather than the solution, you've lost the plot.

**The test:** Can you articulate the specific pain this pattern solves? Not "it's more flexible" but "adding a new payment provider currently requires changes to 6 files, and with this pattern it requires 1."

### 🚩 Red Flag: You can't explain it in one minute

If describing your design takes a whiteboard session, it's too complex for the problem at hand.

**The test:** Explain the design to a teammate in 60 seconds. If you can't, or if they look confused, simplify.

### 🚩 Red Flag: Every caller must change

A good pattern localizes change. If adopting the pattern requires modifying every call site, you might be creating more work than you're saving.

**The test:** How many files need to change when you introduce this pattern? How many will need to change when you add the next variant?

---

## Step 5: Document the Intent

Patterns fail when future engineers don't understand why they exist.

Every time you introduce a pattern, leave a trail:

### In the code

```python
# We use Strategy here to keep deployment backends isolated from the
# deployment service. Adding a new backend requires implementing the
# DeploymentBackend interface, not modifying this class.
# See: docs/architecture/deployment-strategy.md
```

### In architecture docs

```markdown
## Deployment Backend Strategy

**Why:** Deployment targets vary (K8s, VM, serverless) and change 
independently of the core deployment logic.

**Pattern:** Strategy pattern with DeploymentBackend interface.

**Adding a new backend:**
1. Implement DeploymentBackend interface
2. Register in DeploymentBackendFactory
3. Add configuration schema
```

Without this documentation, the next engineer will either:
- Not understand the pattern and work around it
- Understand the pattern but not why it was chosen, and refactor it away
- Add new code that duplicates what the pattern already provides

---

## Decision Checklist

Before you commit, walk through this list:

**Problem Validation:**
- [ ] Can I name the specific pain this pattern solves?
- [ ] Is this pain recurring, not one-time?
- [ ] Have I felt this pain at least twice already?

**Pattern Fit:**
- [ ] Is this the simplest pattern that addresses the pain?
- [ ] Can I explain the benefit in one sentence?
- [ ] Will the team understand it quickly?

**Trade-off Analysis:**
- [ ] Does the pattern improve testability?
- [ ] Does it reduce the number of files touched for common changes?
- [ ] Is the added complexity proportional to the problem's frequency?

**Documentation:**
- [ ] Have I documented why this pattern exists?
- [ ] Is there a clear guide for extending it?

If you can't answer "yes" to most of these, reconsider. The goal isn't to use patterns—it's to build software that's easy to change.

---

## Real Example: Choosing a Pattern for Notifications

Let me walk through this framework with a real problem we faced at NVIDIA.

### Step 1: Name the Pain

Our CI/CD platform needed to send notifications—build started, build failed, deployment complete. Initially, we had inline code:

```python
def on_build_complete(build):
    send_email(build.owner, f"Build {build.id} complete")
    post_to_slack(build.channel, f"Build {build.id} complete")
```

The pain became clear when product asked for PagerDuty integration. And then Microsoft Teams. And then custom webhooks. Each addition required:
- Modifying the core build service
- Adding conditional logic for which channels to use
- Duplicating retry and error handling logic

**Pain:** Adding a notification channel requires changes to core business logic.

### Step 2: Map to a Family

This is a **Behavioral** problem. The core logic (something happened) is stable; what varies is how we respond (which channels, what format).

### Step 3: Choose the Simplest Pattern

Within Behavioral patterns:
- **Observer:** Objects subscribe to events and get notified
- **Strategy:** Swap algorithms without changing clients
- **Chain of Responsibility:** Pass request along a chain

Observer fits best. The build service shouldn't know about notification channels—it should just emit events. Channels subscribe and handle their own logic.

### Step 4: Validate Against Red Flags

- **More classes than clarity?** We're adding one interface and one class per channel. Each class is small and focused. ✓
- **Pattern is the goal?** No—we have measurable pain and a clear benefit. ✓
- **Explain in one minute?** "Build service emits events. Channels subscribe. Adding a channel means adding a subscriber." ✓
- **Every caller must change?** No—the build service just emits events, same as before. Channels register themselves. ✓

### Step 5: Document the Intent

We added this to our architecture docs:

> **Notification System:** Uses Observer pattern. Build service emits events via NotificationBus. Channels (EmailNotifier, SlackNotifier, etc.) subscribe to relevant events. Adding a channel requires implementing NotificationHandler and registering with the bus. Core build logic never changes when channels are added.

### Result

Adding PagerDuty took two hours: one file for the handler, one line to register it. No changes to the build service. No changes to existing channels. The pattern paid for itself immediately.

---

## When Not to Use This Framework

This framework assumes you have time to think. Sometimes you don't.

**During an incident:** Fix the problem, then refactor later. Don't introduce patterns during production firefighting.

**For throwaway code:** If you're prototyping or building something that will be deleted next month, skip the patterns. YAGNI (You Aren't Gonna Need It).

**When the team doesn't know the pattern:** A pattern that only one person understands isn't improving the codebase. Either teach the team or choose something simpler.

---

## Navigation

- **Previous:** [Pattern Catalog](/docs/design-patterns/catalog)
- **Next:** [How to Read Pattern Docs](/docs/design-patterns/reading-patterns)
