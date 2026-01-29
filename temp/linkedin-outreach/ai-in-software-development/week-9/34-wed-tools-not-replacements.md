# Post #34: The AI Suggestion That Taught Me Something New
**Week 9 | Wednesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** None (learning story)

---

## POST CONTENT (Copy everything below the line)

---

AI taught me a Go pattern I didn't know existed.

I've written Golang for 4 years.

Here's what happened:

I asked Cursor to implement a retry mechanism with exponential backoff.

Expected: Basic retry loop with sleep.

Got: A channel-based implementation with context cancellation and jitter.

My first reaction: "This is over-engineered."

My second reaction: "Wait, this is actually better."

𝗪𝗵𝗮𝘁 𝗜 𝗹𝗲𝗮𝗿𝗻𝗲𝗱:

The channel-based approach:
✓ Cancels immediately when context expires
✓ Doesn't waste resources during backoff
✓ Handles graceful shutdown properly

My approach would have:
✗ Blocked until sleep completes
✗ Ignored cancellation signals
✗ Been harder to test

AI knew a pattern I didn't.

𝗧𝗵𝗲 𝗯𝗶𝗴𝗴𝗲𝗿 𝗶𝗻𝘀𝗶𝗴𝗵𝘁:

AI isn't just a productivity tool.

It's a learning accelerator.

Every suggestion is a chance to ask "Why did you do it that way?"

I've learned more Go idioms in 6 months of AI-assisted development than in the previous 2 years.

What has AI taught you that you didn't know?

---
#AIDevelopment #Golang #Learning #DeveloperProductivity

---

## FIRST COMMENT

How to learn FROM AI suggestions:

1. Don't just accept code—ask WHY
2. Compare to your mental approach
3. Look up unfamiliar patterns
4. Keep a "TIL" list of new things

AI is like pairing with a senior dev who knows every library and pattern.

The key: Stay curious, not defensive.

What unexpected thing has AI taught you recently?

---

## ALTERNATIVE HOOKS

**Alt 1:** "I've been writing Go for 4 years. AI just taught me something new."

**Alt 2:** "The AI suggestion that made me rethink my approach"

**Alt 3:** "AI isn't just productivity. It's education."

---

## ENGAGEMENT TIPS

- Learning stories are relatable
- Shows humility (I didn't know everything)
- Ask for their learning moments
- Specific technical detail adds credibility
