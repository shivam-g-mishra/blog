---
# Required
sidebar_position: 13
title: "CI/CD Troubleshooting Guide"
description: >-
  Diagnose and fix common CI/CD problems: build failures, test issues, deployment errors, 
  secrets problems, and platform-specific issues. Practical solutions for when things go wrong.

# SEO
keywords:
  - ci/cd troubleshooting
  - pipeline debugging
  - build failures
  - deployment errors
  - flaky tests
  - ci/cd problems
  - pipeline errors
  - github actions errors
  - gitlab ci problems
  - jenkins troubleshooting
  - docker build errors

# Social sharing
og_title: "CI/CD Troubleshooting: Fix Common Pipeline Problems"
og_description: "Practical solutions for build failures, test issues, deployment errors, and secrets problems in CI/CD."
og_image: "/img/ci-cd-social-card.png"

# Content management
date_published: 2025-01-24
date_modified: 2025-01-24
author: shivam
reading_time: 20
content_type: reference
---

# CI/CD Troubleshooting Guide

Things will go wrong. Builds will fail. Deployments will break. Tests will flake. The difference between a frustrating day and a quick fix is knowing where to look.

This document is a practical troubleshooting guide covering the most common CI/CD problems and their solutions. Bookmark it. You'll need it at 2 AM when production is down.

---

## Build Failures

### Dependency Resolution Issues

**Symptom:** `npm install` or `pip install` fails with version conflicts or missing packages.

**Common causes:**
- Lock file out of sync with package.json/requirements.txt
- Private registry not configured
- Network issues reaching package registries
- Package was unpublished/yanked

**Solutions:**

```bash
# Regenerate lock file
rm package-lock.json
npm install
git add package-lock.json
git commit -m "fix: regenerate lock file"

# Clear npm cache
npm cache clean --force

# Use exact versions
npm ci  # Instead of npm install
```

```yaml
# Configure private registry
- name: Configure npm registry
  run: |
    echo "//npm.pkg.github.com/:_authToken=${{ secrets.GITHUB_TOKEN }}" >> .npmrc
    echo "@myorg:registry=https://npm.pkg.github.com" >> .npmrc
```

### Out of Disk Space

**Symptom:** Build fails with "no space left on device" or similar.

**Solutions:**

```yaml
# Clean up before build
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    sudo rm -rf /opt/ghc
    docker system prune -af
    df -h

# Use smaller runner images
runs-on: ubuntu-latest  # Instead of ubuntu-22.04 with extra packages
```

### Out of Memory

**Symptom:** Process killed, OOM errors, or build hangs.

**Solutions:**

```bash
# Node.js: Increase memory limit
NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Docker: Limit build memory
docker build --memory=4g .
```

```yaml
# Use larger runner
runs-on: ubuntu-latest-8-cores
```

### Timeout Errors

**Symptom:** Job cancelled due to timeout.

**Solutions:**

```yaml
# Increase timeout
jobs:
  build:
    timeout-minutes: 60  # Default is 360 for GitHub Actions

# Or per-step
- name: Long running task
  timeout-minutes: 30
  run: ./slow-task.sh
```

**But also:** Investigate why it's slow. Timeouts often indicate underlying problems.

---

## Test Failures

### Flaky Tests

**Symptom:** Tests pass sometimes, fail sometimes, with no code change.

**Diagnosis:**

```bash
# Run tests multiple times to identify flaky ones
for i in {1..10}; do npm test; done

# Record failures
npm test 2>&1 | tee test-run-$i.log
```

**Common causes and fixes:**

| Cause | Fix |
|-------|-----|
| Timing/async issues | Add proper waits, don't use `sleep()` |
| Shared state | Isolate tests, reset state in `beforeEach` |
| External dependencies | Mock external services |
| Order dependence | Randomize test order to detect |
| Resource contention | Reduce parallel test workers |

```javascript
// Bad: timing dependent
test('shows result', async () => {
  render(<Component />);
  await sleep(100);
  expect(screen.getByText('Result')).toBeInTheDocument();
});

// Good: wait for condition
test('shows result', async () => {
  render(<Component />);
  await waitFor(() => {
    expect(screen.getByText('Result')).toBeInTheDocument();
  });
});
```

### Environment-Dependent Failures

**Symptom:** Tests pass locally, fail in CI (or vice versa).

**Diagnosis:**

```yaml
# Print environment info
- name: Debug environment
  run: |
    uname -a
    node --version
    npm --version
    env | sort
```

**Common causes:**
- Different OS (Linux vs macOS vs Windows)
- Different versions (Node, Python, etc.)
- Missing environment variables
- Different file system (case sensitivity)
- Different timezone

**Solutions:**

```yaml
# Pin versions
- uses: actions/setup-node@v4
  with:
    node-version: '20.10.0'  # Exact version, not '20'

# Set timezone
env:
  TZ: UTC
```

### Database/Service Connection Failures

**Symptom:** "Connection refused" or timeout connecting to test database.

**Solutions:**

```yaml
# Wait for service to be ready
services:
  postgres:
    image: postgres:15
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

```yaml
# Or use a wait script
- name: Wait for PostgreSQL
  run: |
    until pg_isready -h localhost -p 5432; do
      echo "Waiting for postgres..."
      sleep 2
    done
```

---

## Deployment Failures

### Image Pull Errors

**Symptom:** "ImagePullBackOff" or "ErrImagePull" in Kubernetes.

**Causes and fixes:**

```bash
# Check if image exists
docker pull myregistry.io/myapp:v1.0.0

# Check registry credentials
kubectl get secret regcred -o yaml
kubectl describe pod <pod-name>  # Look for pull errors

# Recreate registry secret
kubectl create secret docker-registry regcred \
  --docker-server=myregistry.io \
  --docker-username=$USER \
  --docker-password=$TOKEN
```

```yaml
# Ensure pod spec uses imagePullSecrets
spec:
  imagePullSecrets:
    - name: regcred
  containers:
    - name: myapp
      image: myregistry.io/myapp:v1.0.0
```

### Health Check Failures

**Symptom:** Pods crash loop, deployment never becomes ready.

**Diagnosis:**

```bash
# Check pod status
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous  # Logs from crashed container

# Check if app starts locally
docker run -p 8080:8080 myapp:v1.0.0
curl http://localhost:8080/health
```

**Common fixes:**

```yaml
# Increase initial delay
readinessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30  # Give app time to start
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

### Rollback Not Working

**Symptom:** `kubectl rollout undo` doesn't restore service.

**Diagnosis:**

```bash
# Check rollout history
kubectl rollout history deployment/myapp

# Check revision details
kubectl rollout history deployment/myapp --revision=2
```

**Common causes:**
- ConfigMap/Secret changes not tracked
- Database migrations can't be undone
- External state changed

---

## Secrets and Authentication

### Secret Not Found

**Symptom:** "Secret 'XYZ' not found" or empty variable.

**Diagnosis:**

```yaml
# Check if secret is set
- name: Debug secrets
  run: |
    if [ -z "${{ secrets.MY_SECRET }}" ]; then
      echo "Secret is empty or not set"
      exit 1
    else
      echo "Secret is set (length: ${#${{ secrets.MY_SECRET }}})"
    fi
```

**Common causes:**
- Secret not configured in settings
- Wrong secret name (case-sensitive)
- Secret scoped to different environment
- Missing permissions to access secrets

### Token Expiration

**Symptom:** Authentication worked before, now fails.

**Solutions:**

```yaml
# Use OIDC instead of long-lived tokens
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789:role/github-actions
    aws-region: us-west-2
    # No secrets needed!
```

```bash
# Refresh tokens
gcloud auth activate-service-account --key-file=key.json
aws sts get-caller-identity
```

### OIDC/Workload Identity Failures

**Symptom:** "AssumeRoleWithWebIdentity" or "Workload Identity" errors.

**Diagnosis:**

```yaml
# Print OIDC token claims
- name: Debug OIDC
  run: |
    TOKEN=$(curl -H "Authorization: bearer $ACTIONS_ID_TOKEN_REQUEST_TOKEN" \
      "$ACTIONS_ID_TOKEN_REQUEST_URL&audience=sts.amazonaws.com" | jq -r '.value')
    echo "$TOKEN" | cut -d '.' -f2 | base64 -d | jq .
```

**Common fixes:**
- Verify trust policy has correct audience
- Check repository/branch conditions
- Ensure `id-token: write` permission is set

---

## Platform-Specific Issues

### GitHub Actions

**Workflow not triggering:**
```yaml
# Check path filters aren't excluding your changes
on:
  push:
    paths-ignore:
      - '**.md'  # This excludes README changes

# Check branch name matches
on:
  push:
    branches:
      - main
      - 'release/**'  # Ensure pattern matches your branch
```

**"Resource not accessible by integration":**
```yaml
# Add required permissions
permissions:
  contents: read
  packages: write
  pull-requests: write
```

**Rate limits:**
```yaml
# Use GitHub token for authenticated requests
- name: API call
  run: |
    curl -H "Authorization: token ${{ secrets.GITHUB_TOKEN }}" \
      https://api.github.com/repos/...
```

### GitLab CI

**Job not running:**
```yaml
# Check rules are correct
rules:
  - if: $CI_PIPELINE_SOURCE == "merge_request_event"  # Only MRs
  - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH      # Only default branch

# Validate syntax
# Settings > CI/CD > Editor > Validate
```

**Runner not available:**
```bash
# Check runner status
gitlab-runner status
gitlab-runner verify

# Check runner tags match job
job:
  tags:
    - docker
    - linux
```

### Jenkins

**"Pipeline script not approved":**
```groovy
// Go to Manage Jenkins > In-process Script Approval
// Or use methods that don't require approval
```

**Agent not connecting:**
```bash
# Check agent logs
java -jar agent.jar -jnlpUrl http://jenkins/computer/agent/jenkins-agent.jnlp

# Verify network connectivity
curl -v http://jenkins-server:8080
```

---

## Docker/Container Issues

### Build Cache Not Working

**Diagnosis:**

```bash
# See which layers are cached
docker build --progress=plain .

# Force no cache to compare
docker build --no-cache .
```

**Common causes:**
- COPY before dependency install
- Using ADD instead of COPY
- File timestamps changing

**Fix layer order:**

```dockerfile
# Bad: cache busted on every code change
COPY . .
RUN npm ci

# Good: dependencies cached separately
COPY package*.json ./
RUN npm ci
COPY . .
```

### Multi-Stage Build Issues

**Symptom:** Files missing from final image.

```dockerfile
# Ensure you copy from correct stage
FROM node:20 AS builder
RUN npm run build

FROM node:20-slim
# Must explicitly copy from builder
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
```

### Container Networking

**Symptom:** Services can't connect to each other.

```yaml
# GitHub Actions: use localhost
services:
  postgres:
    image: postgres:15
    ports:
      - 5432:5432
# Connect via localhost:5432

# Docker Compose: use service names
services:
  app:
    environment:
      DATABASE_URL: postgresql://postgres:5432/db
  postgres:
    image: postgres:15
# Connect via postgres:5432 (service name)
```

---

## General Debugging Techniques

### Enable Debug Logging

```yaml
# GitHub Actions
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true

# GitLab CI
variables:
  CI_DEBUG_TRACE: "true"

# Jenkins
pipeline {
  options {
    timestamps()
  }
}
```

### Reproduce Locally

```bash
# GitHub Actions with act
act -j build

# GitLab CI locally
gitlab-runner exec docker build

# Run same commands locally
docker run -it ubuntu:latest /bin/bash
# Then run your build commands
```

### Bisect to Find Breaking Commit

```bash
git bisect start
git bisect bad  # Current commit is broken
git bisect good abc123  # This commit was working
# Git will checkout commits for you to test
# Mark each as good or bad until it finds the culprit
```

---

## Quick Diagnosis Checklist

When a pipeline fails, check these in order:

1. **[ ] Read the error message** — Often the answer is right there
2. **[ ] Check recent changes** — What changed since it last worked?
3. **[ ] Check if it's flaky** — Does re-running fix it?
4. **[ ] Check environment** — Different from local? Missing variables?
5. **[ ] Check dependencies** — Lock file issues? Network problems?
6. **[ ] Check resources** — Out of memory/disk/time?
7. **[ ] Check permissions** — Secrets configured? Access granted?
8. **[ ] Search error message** — Someone else had this problem

---

## What's Next?

Troubleshooting is reactive—you fix problems after they occur. The next document covers **AI in CI/CD**: how AI tools are transforming pipeline development, intelligent test selection, and automated problem detection.

**Ready to explore AI in CI/CD?** Continue to [AI in CI/CD →](./ai-in-cicd)

---

## Quick Reference

### Error Message Patterns

| Error Contains | Likely Cause |
|----------------|--------------|
| "ENOSPC" | Disk full |
| "ENOMEM" / "OOM" | Out of memory |
| "ETIMEDOUT" | Network/connection timeout |
| "ECONNREFUSED" | Service not running |
| "Permission denied" | File/access permissions |
| "not found" | Missing file/command/secret |
| "401" / "403" | Authentication/authorization |

### First Steps by Failure Type

| Failure | First Check |
|---------|-------------|
| Build fails | Dependency lock files |
| Tests flaky | Async/timing issues |
| Deploy fails | Image exists and is pullable |
| Secret errors | Secret name and scope |
| Timeout | Is something genuinely slow? |

### When to Escalate

- Same error after 3 fix attempts
- Error involves infrastructure you don't control
- Production is down
- Security-related failures

---

**Remember:** The best debugging is systematic. Read the error, form a hypothesis, test it, repeat. Resist the urge to randomly try things—that wastes time and can make things worse.
