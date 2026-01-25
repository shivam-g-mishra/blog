---
# Required
sidebar_position: 16
title: "CI/CD Anti-patterns and Migration for DevOps"
description: >-
  Learn CI/CD anti-patterns to avoid and DevOps migration strategies between CI/CD
  platforms. Covers snowflake pipelines, manual steps, and parallel run playbooks.

# SEO
keywords:
  - ci/cd anti-patterns
  - pipeline migration
  - jenkins migration
  - gitlab to github
  - ci/cd best practices
  - pipeline mistakes
  - ci/cd debt
  - migration strategy
  - ci/cd modernization
  - devops migration
  - learn ci/cd

# Social sharing
og_title: "CI/CD Anti-patterns & Migration: What to Avoid"
og_description: "Avoid common CI/CD mistakes and use safe migration strategies between platforms."
og_image: "/img/ci-cd-social-card.svg"

# Content management
date_published: 2025-01-24
date_modified: 2026-01-25
author: shivam
reading_time: 18
content_type: explanation
---

# CI/CD Anti-patterns and Platform Migration

Every team I've worked with has inherited at least one anti-pattern. Pipelines that "evolved" over years without design. Manual steps that "we'll automate later." Configuration drift that nobody can explain. These patterns don't appear overnight—they accumulate slowly until someone realizes the CI/CD system is more hindrance than help.

If you're dealing with CI/CD anti-patterns or planning a CI/CD migration, these shortcuts are the ones that slowly turn automation into a liability.

This document covers two related topics: the anti-patterns you should avoid (or fix if you've inherited them), and strategies for migrating between CI/CD platforms when you need a fresh start.

**What you'll learn in this guide:**
- The most damaging CI/CD anti-patterns and how to fix them
- How to recognize when a platform migration is justified
- A safe, parallel-run migration playbook
- Warning signs that your pipeline is accruing debt

---

## Common Anti-patterns

### The Snowflake Pipeline

**What it looks like:** Every project has its own unique, artisanal pipeline configuration. No two pipelines work the same way. Some use Makefiles, some use npm scripts, some use custom shell scripts nobody documented.

**Why it happens:** Teams optimize for their specific needs without organizational coordination. "We just need to get this working" compounds over time.

**The cost:**
- Onboarding takes weeks per project
- Knowledge is siloed
- Updates require touching every repo
- Debugging requires learning each snowflake

**The fix:** Create standardized templates that cover 80% of use cases. Allow customization but make the default path so easy that teams choose it voluntarily.

```yaml
# Instead of custom logic, use shared templates
jobs:
  build:
    uses: myorg/templates/.github/workflows/node-build.yml@v1
    with:
      node-version: 20
    secrets: inherit
```

### Manual Steps in "Automated" Pipelines

**What it looks like:** Pipeline passes, but someone still needs to SSH somewhere, run a script, click a button in a dashboard, or update a spreadsheet before the release is "done."

**Why it happens:** The automation stopped when it got hard. "We'll automate the database migration later" becomes permanent.

**The cost:**
- Not actually continuous
- Dependent on specific people
- Error-prone
- Scales poorly

**The fix:** Audit your pipeline for manual steps. Automate them or eliminate the need for them. If something can't be automated, document why and review regularly.

### Testing in Production (Without Safeguards)

**What it looks like:** "We'll just push it and see if it works." No staging environment. No feature flags. No canary. YOLO deployment.

**Why it happens:** Setting up proper testing is work. Production is right there. "It works on my machine."

**The cost:**
- Customers find bugs
- Incidents disrupt users
- Trust erodes
- Fear of deploying develops

**The fix:** Implement progressive deployment. Start with staging. Add canary. Use feature flags. Make production deployment boring, not exciting.

### The Flaky Test Graveyard

**What it looks like:** "Oh that test? It's just flaky, rerun it." Tests that sometimes pass, sometimes fail, and everyone knows to ignore them.

**Why it happens:** Fixing flaky tests is hard. Ignoring them is easy. The ratio of ignored-to-investigated grows over time.

**The cost:**
- Real failures get missed
- Trust in tests erodes
- "It passed on the second run" becomes acceptable
- Pipeline becomes noise

**The fix:** Track flakiness metrics. Quarantine flaky tests. Dedicate time to fix them. A small reliable test suite beats a large flaky one.

### Secrets in Plain Sight

**What it looks like:** API keys in environment variables that get logged. Credentials committed to repos. Tokens shared in Slack.

**Why it happens:** Secrets management is overhead. "It's just an internal key." "We'll fix it before prod."

**The cost:**
- Security breach waiting to happen
- Credentials in git history forever
- No rotation capability
- Audit nightmare

**The fix:** Use proper secrets management from day one. HashiCorp Vault, cloud secret managers, or at minimum platform-native secrets with proper scoping.

### The 90-Minute Pipeline

**What it looks like:** Pipeline takes so long that developers push and go home. Results arrive after context is lost.

**Why it happens:** Tests accumulate. Caching isn't configured. Nobody optimized because nobody measured.

**The cost:**
- No fast feedback
- Developers skip the pipeline
- Batch changes to reduce waits
- CI becomes a checkbox, not a tool

**The fix:** Profile your pipeline. Implement caching. Parallelize independent jobs. Target under 15 minutes for the full pipeline.

### Over-Engineering for Small Teams

**What it looks like:** A 5-person startup with multi-environment GitOps, Kubernetes, service mesh, and enterprise governance that a Fortune 500 would envy.

**Why it happens:** Someone read about how Google does it. Resume-driven development. "We'll need this when we scale."

**The cost:**
- Complexity without benefit
- Maintenance burden
- Slower velocity
- Distraction from product

**The fix:** Match complexity to actual needs. Start simple. Add sophistication when you feel pain, not in anticipation of it.

### Under-Investing for Large Teams

**What it looks like:** A 500-person org sharing a single Jenkins server from 2015. No templates. No governance. Everyone does their own thing.

**Why it happens:** "It worked when we were 20 people." No investment in platform as product. CI/CD is nobody's job.

**The cost:**
- Everyone reinvents wheels
- No consistency
- Security and compliance risk
- Scaling pain

**The fix:** Invest in platform engineering. Treat CI/CD as a product with dedicated owners. Build shared infrastructure that enables teams.

---

## Detecting Anti-patterns

### Smell Tests

Answer these questions about your CI/CD:

| Question | Bad Sign |
|----------|----------|
| How long does CI take? | >30 minutes |
| How often do you rerun for flaky tests? | >10% of runs |
| Can a new engineer deploy on day one? | No |
| Is every step automated? | No |
| Can you deploy on Friday afternoon? | "We don't do that" |
| What's the change failure rate? | >15% |
| How long to roll back? | >5 minutes |

### Metrics That Indicate Problems

- **Low deployment frequency** → Fear of deploying
- **High change failure rate** → Inadequate testing
- **Long lead time** → Process bottlenecks
- **Long MTTR** → Poor observability/rollback

### Team Surveys

Ask your team:
- What frustrates you about CI/CD?
- What manual steps do you do for releases?
- How confident are you when deploying?
- What would you change first?

---

## Platform Migration Strategies

Sometimes the best fix is a fresh start. Here's how to migrate CI/CD platforms safely.

### When to Migrate

**Good reasons:**
- Current platform doesn't support your needs
- Cost is prohibitive at scale
- Integration with other systems is needed
- Current platform is EOL or unsupported
- Organization is consolidating tools

**Bad reasons:**
- "Everyone else uses X"
- "I heard Y is better"
- Avoiding fixing underlying problems

### Migration Approaches

**Big bang (not recommended):**
```
Day 1: Old platform
Day 2: New platform
```

High risk. If anything goes wrong, you're stuck.

**Parallel running (recommended):**
```
Week 1-4: Both platforms run on every change
Week 5-6: Validate parity
Week 7: Old platform disabled
Week 8+: Old platform decommissioned
```

**Gradual migration:**
```
Month 1: New projects on new platform
Month 2: Low-risk existing projects migrate
Month 3: Medium-risk projects migrate
Month 4+: High-risk projects migrate
```

### Jenkins to GitHub Actions Migration

**Before:**
```groovy
// Jenkinsfile
pipeline {
    agent any
    stages {
        stage('Install') {
            steps {
                sh 'npm ci'
            }
        }
        stage('Test') {
            steps {
                sh 'npm test'
            }
        }
        stage('Build') {
            steps {
                sh 'npm run build'
            }
        }
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                sh './deploy.sh'
            }
        }
    }
}
```

**After:**
```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test
      - run: npm run build

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: ./deploy.sh
```

**Key differences:**
- YAML vs Groovy
- Built-in caching
- Managed runners
- GitHub-native integration

### GitLab CI to GitHub Actions

**Common mappings:**

| GitLab CI | GitHub Actions |
|-----------|----------------|
| `stages` | Jobs with `needs` |
| `script` | `run` |
| `only/except` | `if` conditions |
| `artifacts` | `actions/upload-artifact` |
| `cache` | `actions/cache` |
| `services` | `services` |
| `variables` | `env` |

### Secrets Migration

**Critical considerations:**
1. **Inventory all secrets** — Document what exists
2. **Don't migrate in plain text** — Never export/import secrets directly
3. **Rotate during migration** — Good opportunity for hygiene
4. **Verify access** — Test that new platform can access external systems

```bash
# Example: Moving from Jenkins credentials to GitHub secrets
# Don't do this - exposes secret:
# echo $JENKINS_SECRET | gh secret set API_KEY

# Do this - generate new secret:
# Generate new API key in the service
# Add directly to GitHub: Settings → Secrets → New secret
# Update any references
# Revoke old Jenkins credential
```

### Validation Checklist

Before decommissioning old platform:

- [ ] All pipelines migrated and working
- [ ] Secrets rotated and verified
- [ ] Build artifacts accessible
- [ ] Deployment permissions configured
- [ ] Notifications working
- [ ] Team trained on new platform
- [ ] Documentation updated
- [ ] Rollback plan in place
- [ ] Parallel running completed successfully

---

## Migration Playbook Template

### Phase 1: Assessment (Week 1-2)

1. Inventory all pipelines
2. Document secrets and credentials
3. Identify dependencies (registries, services)
4. Assess team skills
5. Define success criteria

### Phase 2: Pilot (Week 3-4)

1. Select low-risk project
2. Migrate pipeline to new platform
3. Run both platforms in parallel
4. Document issues and solutions
5. Gather team feedback

### Phase 3: Expansion (Week 5-8)

1. Migrate remaining projects in priority order
2. Continue parallel running
3. Monitor for issues
4. Update documentation
5. Train team members

### Phase 4: Cutover (Week 9-10)

1. Disable old platform triggers
2. Monitor new platform closely
3. Keep old platform accessible (read-only)
4. Verify all systems working

### Phase 5: Cleanup (Week 11+)

1. Decommission old platform
2. Revoke old credentials
3. Archive old configurations
4. Update all documentation
5. Conduct retrospective

---

## What's Next?

Understanding anti-patterns helps you avoid creating them and recognize them when you inherit them. Knowing how to migrate safely gives you options when a fresh start is the right choice.

The next document in this series provides **Case Studies**: real-world deployment scenarios from simple VPS to complex multi-region Kubernetes, showing how to apply everything we've covered.

**Ready to see real-world examples?** Continue to [Case Studies →](./case-studies)

---

## Quick Reference

### Anti-pattern Symptoms

| Symptom | Likely Anti-pattern |
|---------|---------------------|
| "It's different in every repo" | Snowflake pipelines |
| "Then you need to manually..." | Manual steps |
| "Just rerun it" | Flaky test graveyard |
| "Works for me" | Environment inconsistency |
| "Don't deploy Friday" | Fear from past failures |
| Pipeline >30 min | Unoptimized pipeline |

### Migration Decision Matrix

| Situation | Recommendation |
|-----------|---------------|
| Current platform works | Stay and improve |
| Minor issues | Fix issues, stay |
| Major limitations | Consider migration |
| Platform EOL | Must migrate |
| Team wants change | Evaluate objectively |

### Migration Safety

1. **Never migrate big bang** — Parallel run first
2. **Rotate secrets** — Don't copy credentials
3. **Start with low-risk** — Prove it works
4. **Keep old platform** — Until confident
5. **Document everything** — Future you will thank you

---

## FAQ: CI/CD Anti-patterns and Migration

### When should a DevOps team migrate CI/CD platforms?

When the current platform blocks security, scalability, or developer experience and the cost of fixing exceeds the cost of migration.

### What's the safest way to migrate?

Run pipelines in parallel, start with low-risk services, and only cut over once results match. Avoid big-bang migrations.

### How do we avoid reintroducing anti-patterns after migration?

Standardize templates, automate manual steps, and document golden paths so teams don't rebuild one-off pipelines.

## Related Reading

- [Enterprise CI/CD: Governance that prevents drift →](./enterprise-cicd)
- [Platform Examples: Reference best-practice configs →](./platform-examples)
- [Troubleshooting: Debug migration failures →](./troubleshooting)

---

**Remember:** The best pipeline is one that works reliably and nobody thinks about. Fix anti-patterns before they compound. Migrate when you have good reasons, not just preferences.
