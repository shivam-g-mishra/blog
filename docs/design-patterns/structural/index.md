---
# Required
sidebar_position: 1
title: "Structural Design Patterns — Overview"
description: >-
  Structural patterns help you compose objects and classes into larger
  structures. Learn when to use Adapter, Facade, Decorator, and more.

# SEO
keywords:
  - structural design patterns
  - adapter pattern
  - decorator pattern
  - facade pattern
  - proxy pattern
  - composite pattern

# Social sharing
og_title: "Structural Patterns Overview"
og_description: "A practical guide to structuring objects and integrations."
og_image: "/img/social-card.svg"

# Content management
date_published: 2026-01-25
date_modified: 2026-01-25
author: shivam
reading_time: 8
content_type: explanation
---

# Structural Patterns Overview

When I integrated a legacy authentication system into a modern API, we needed to wrap it, adapt it, and simplify it without breaking the new code. Structural patterns are built for these moments.

**They help you compose systems without rewriting everything.**

## When You Need a Structural Pattern

- You need to integrate incompatible interfaces.
- You want to add behavior without modifying existing classes.
- You need to hide complex subsystems behind a simpler API.

## Quick Comparison

| Pattern | Best for | Trade-off |
|---------|----------|-----------|
| Adapter | Compatibility between interfaces | Extra translation layer |
| Bridge | Separating abstraction from implementation | More types |
| Composite | Treating parts and wholes uniformly | Complexity in tree management |
| Decorator | Adding behavior dynamically | Debugging stacked decorators |
| Facade | Simplifying a subsystem | Risk of hiding useful power |
| Flyweight | Sharing many small objects | Requires careful immutability |
| Proxy | Controlling access | Can hide latency |

## Pattern Index

- [Adapter](/docs/design-patterns/structural/adapter)
- [Bridge](/docs/design-patterns/structural/bridge)
- [Composite](/docs/design-patterns/structural/composite)
- [Decorator](/docs/design-patterns/structural/decorator)
- [Facade](/docs/design-patterns/structural/facade)
- [Flyweight](/docs/design-patterns/structural/flyweight)
- [Proxy](/docs/design-patterns/structural/proxy)

## Navigation

- **Previous:** [Singleton Pattern](/docs/design-patterns/creational/singleton)
- **Next:** [Adapter Pattern](/docs/design-patterns/structural/adapter)
