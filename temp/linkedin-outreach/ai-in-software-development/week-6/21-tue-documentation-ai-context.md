# Post #21: The Screenshot Debugging Workflow
**Week 6 | Tuesday | 7:00 AM PT**
**Format:** Text Post
**Blog Link:** None (practical technique)

---

## POST CONTENT (Copy everything below the line)

---

Stop describing bugs to AI.

Show them instead.

Here's my debugging workflow that cuts resolution time in half:

𝗦𝘁𝗲𝗽 𝟭: 𝗖𝗮𝗽𝘁𝘂𝗿𝗲 𝗘𝘃𝗲𝗿𝘆𝘁𝗵𝗶𝗻𝗴
Screenshot the error message.
Copy the stack trace.
Grab the relevant logs.

𝗦𝘁𝗲𝗽 𝟮: 𝗣𝗿𝗼𝘃𝗶𝗱𝗲 𝗖𝗼𝗻𝘁𝗲𝘅𝘁
"I expected: [this]"
"I got: [that]"
"Recent changes: [what I modified]"

𝗦𝘁𝗲𝗽 𝟯: 𝗔𝘀𝗸 𝗦𝗽𝗲𝗰𝗶𝗳𝗶𝗰𝗮𝗹𝗹𝘆
"What's causing this?"
"Where should I look first?"
"What's the fix?"

𝗪𝗵𝘆 𝘁𝗵𝗶𝘀 𝘄𝗼𝗿𝗸𝘀:

AI can SEE images now.
Visual context > text descriptions.

Last week: API returning 500 errors randomly.

Old approach: Describe symptoms, guess causes, iterate slowly.

New approach: Screenshot error + logs + recent commits → Root cause in 2 minutes.

The bug? A race condition in connection pooling.

AI spotted it immediately from the log timestamps.

I would have spent an hour on that.

What's your AI debugging workflow?

---
#Debugging #AIDevelopment #DeveloperProductivity #DevTools

---

## FIRST COMMENT

Pro tip for better debugging prompts:

Include MORE than you think necessary:
• The exact error message
• 20-30 lines of logs around the error
• The code that's failing
• What changed recently

AI with context > AI without context.

The extra 30 seconds of gathering info saves 30 minutes of back-and-forth.

What debugging technique has saved you the most time?

---

## ALTERNATIVE HOOKS

**Alt 1:** "Screenshots changed how I debug with AI"

**Alt 2:** "The debugging workflow that cut my fix time in half"

**Alt 3:** "Stop typing bug descriptions. Do this instead."

---

## ENGAGEMENT TIPS

- Super practical content people can use today
- Ask about their debugging workflows
- Share specific examples if people ask
