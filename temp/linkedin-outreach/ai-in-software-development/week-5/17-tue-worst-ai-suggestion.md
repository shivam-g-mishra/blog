# Post #17: The Worst AI Suggestion I Almost Shipped
**Week 5 | Tuesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** None (cautionary tale)

---

## POST CONTENT (Copy everything below the line)

---

I almost shipped AI-generated code with a security vulnerability.

Here's what happened:

I asked Cursor to create an authentication endpoint.

It generated clean, working code.

Tests passed.
Code review looked good.
Ready to merge.

Then I noticed it:

The token validation was checking expiry AFTER processing the request.

Invalid tokens could hit the endpoint before being rejected.

AI understood "validate tokens."
AI didn't understand "validate FIRST."

𝗧𝗵𝗲 𝗹𝗲𝘀𝘀𝗼𝗻:

AI generates plausible code.
Plausible ≠ correct.

What saved us:
✓ Security-focused code review
✓ Explicit test for token order
✓ Not trusting "tests pass" blindly

AI is a powerful tool.
But it doesn't understand security implications the way humans do.

Review EVERYTHING. Especially auth code.

What's the worst AI suggestion you've caught?

---
#AIDevelopment #Security #CodeReview #CodingTips

---

## FIRST COMMENT

The pattern I've noticed:

AI is great at:
• Syntax
• Common patterns
• General structure

AI struggles with:
• Order of operations (security-critical)
• Edge cases in YOUR context
• Domain-specific requirements

The fix: Be MORE rigorous with AI code, not less.

Especially for: Auth, payments, data handling.

What areas do you review most carefully?

---

## ALTERNATIVE HOOKS

**Alt 1:** "AI-generated auth code almost cost us. Here's the story."

**Alt 2:** "Tests passed. Code looked good. The bug was subtle."

**Alt 3:** "Why I review AI code MORE carefully than human code."

---

## ENGAGEMENT TIPS

- Cautionary tales drive engagement
- Vulnerability discussion without specifics
- Ask for their close-call stories
