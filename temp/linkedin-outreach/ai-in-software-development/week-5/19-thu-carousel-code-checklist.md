# Post #19: AI Code Checklist Before Merging
**Week 5 | Thursday | 7:00 AM PT**
**Format:** Carousel (PDF upload)
**Blog Link:** None (practical checklist)

---

## CAPTION (Copy everything below the line)

---

AI-generated code checklist.

Before you merge, check these 10 things.

Save this—you'll need it ⬇️

---
#AIDevelopment #CodeReview #DevOps #CodingTips

💡 Full checklist in comments

---

## CAROUSEL SLIDES (Create in Canva - 1080x1350px portrait)

### Slide 1 (Cover)
```
AI CODE CHECKLIST
BEFORE YOU MERGE

10 things to verify
with AI-generated code

(From 200K lines of experience)

[Swipe →]
```

### Slide 2
```
1. SECURITY REVIEW

□ Auth/authz logic correct?
□ Input validation present?
□ No hardcoded secrets?
□ SQL injection prevention?
□ XSS protection?

AI misses security context.
Always review manually.
```

### Slide 3
```
2. ERROR HANDLING

□ All error paths covered?
□ Errors propagated correctly?
□ User-facing errors clear?
□ Logging appropriate?
□ No swallowed errors?

AI often generates happy path only.
```

### Slide 4
```
3. EDGE CASES

□ Empty inputs handled?
□ Null/nil checks present?
□ Boundary conditions tested?
□ Concurrent access safe?
□ Timeout handling?

List edge cases BEFORE asking AI.
```

### Slide 5
```
4. PERFORMANCE

□ No N+1 queries?
□ Appropriate caching?
□ No unnecessary loops?
□ Memory efficient?
□ Database indexes used?

AI optimizes for readability,
not always performance.
```

### Slide 6
```
5. TESTS

□ Tests actually test logic?
□ Edge cases covered?
□ Mocks appropriate?
□ No false positives?
□ Coverage sufficient?

"Tests pass" ≠ "Tests are good"
```

### Slide 7
```
6. DEPENDENCIES

□ Imports actually needed?
□ No hallucinated packages?
□ Versions compatible?
□ Licenses acceptable?
□ No security vulnerabilities?

AI hallucinates imports often.
```

### Slide 8
```
7. NAMING & STRUCTURE

□ Names match conventions?
□ Functions right size?
□ Single responsibility?
□ File structure correct?
□ Comments accurate?

Easy to fix, easy to miss.
```

### Slide 9
```
8-10. FINAL CHECKS

□ Matches requirements?
□ Fits architecture?
□ Documentation updated?

If unsure about ANY of these:
Ask AI to explain its choices.
```

### Slide 10 (CTA)
```
Save this checklist.

Use it EVERY time you review
AI-generated code.

Future you will thank you.

What would you add?
```

---

## FIRST COMMENT

📋 Quick reference (copy this):

```
AI CODE REVIEW CHECKLIST:
□ Security: Auth order, input validation, no secrets
□ Errors: All paths covered, proper logging
□ Edge cases: Nulls, empty, boundaries, concurrency
□ Performance: No N+1, appropriate caching
□ Tests: Actually test logic, not just coverage
□ Imports: No hallucinated packages
□ Structure: Naming conventions, file organization
□ Requirements: Actually solves the problem
```

My top 3 catches:
1. Hallucinated imports (every time)
2. Missing error handling
3. Security order-of-operations

What would you add to this checklist?

---

## ENGAGEMENT TIPS

- Practical content gets saved/shared
- Provide value directly in comments
- Ask what they'd add to encourage discussion
