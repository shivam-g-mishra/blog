---
# Required
sidebar_position: 17
title: "CI/CD Case Studies — Real-World Deployment Scenarios"
description: >-
  Real-world CI/CD deployment examples: VPS, Kubernetes, Docker Swarm, serverless, 
  mobile apps, static sites, and data center fleets. Complete pipelines for different 
  deployment targets.

# SEO
keywords:
  - ci/cd examples
  - deployment case studies
  - kubernetes deployment
  - vps deployment
  - serverless ci/cd
  - mobile app ci/cd
  - docker deployment
  - real-world ci/cd
  - deployment patterns

# Social sharing
og_title: "CI/CD Case Studies: Real-World Deployment Scenarios"
og_description: "Complete deployment examples from VPS to Kubernetes to mobile apps. See how CI/CD works in practice."
og_image: "/img/ci-cd-social-card.png"

# Content management
date_published: 2025-01-24
date_modified: 2025-01-24
author: shivam
reading_time: 25
content_type: reference
---

# Case Studies: Real-World Deployments

Theory is useful. Practice is better. This document provides real-world CI/CD deployment examples across different scenarios, from simple VPS deployments to complex multi-region Kubernetes clusters.

Each case study includes:
- When to use this approach
- Complete pipeline configuration
- Key considerations
- Common pitfalls

---

## Case Study 1: Single VPS Deployment

**Scenario:** Small application deployed to a single virtual private server via SSH.

**When to use:**
- Simple applications
- Budget constraints
- Learning projects
- Single-server workloads

### Pipeline

```yaml
name: Deploy to VPS

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup SSH
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.SSH_PRIVATE_KEY }}" > ~/.ssh/id_rsa
          chmod 600 ~/.ssh/id_rsa
          ssh-keyscan ${{ secrets.VPS_HOST }} >> ~/.ssh/known_hosts

      - name: Deploy
        run: |
          rsync -avz --delete \
            --exclude='.git' \
            --exclude='node_modules' \
            ./ ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }}:/var/www/myapp/
          
          ssh ${{ secrets.VPS_USER }}@${{ secrets.VPS_HOST }} << 'EOF'
            cd /var/www/myapp
            npm ci --production
            pm2 restart myapp || pm2 start npm --name myapp -- start
          EOF

      - name: Health check
        run: |
          sleep 10
          curl -f https://myapp.example.com/health || exit 1
```

### Key Considerations

- **SSH key management:** Use deploy keys, not personal keys
- **Zero-downtime:** Consider using PM2 cluster mode
- **Rollback:** Keep previous version for quick rollback
- **Monitoring:** Add health checks and alerting

---

## Case Study 2: Kubernetes Deployment

**Scenario:** Microservice deployed to managed Kubernetes cluster.

**When to use:**
- Scalable applications
- Team needs container orchestration
- Multi-service architectures
- Production workloads

### Pipeline

```yaml
name: Deploy to Kubernetes

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      
      - uses: docker/setup-buildx-action@v3
      
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: type=sha
      
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: azure/setup-kubectl@v3
      
      - uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}
      
      - name: Deploy
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:sha-${{ github.sha }} \
            -n production
          kubectl rollout status deployment/myapp -n production --timeout=300s

      - name: Verify deployment
        run: |
          kubectl get pods -n production -l app=myapp
          curl -f https://myapp.example.com/health
```

### Key Considerations

- **Rolling updates:** Configure proper update strategy
- **Health checks:** Readiness and liveness probes
- **Resource limits:** Set appropriate CPU/memory limits
- **Secrets:** Use External Secrets or Sealed Secrets

---

## Case Study 3: Serverless Deployment

**Scenario:** API deployed to AWS Lambda.

**When to use:**
- Event-driven workloads
- Variable traffic
- Cost optimization
- Simple APIs

### Pipeline

```yaml
name: Deploy Lambda

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      
      - run: npm ci
      - run: npm test
      - run: npm run build
      
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions
          aws-region: us-west-2
      
      - name: Deploy with SAM
        run: |
          sam build
          sam deploy \
            --stack-name myapp-prod \
            --s3-bucket my-sam-bucket \
            --capabilities CAPABILITY_IAM \
            --no-confirm-changeset \
            --no-fail-on-empty-changeset

      - name: Smoke test
        run: |
          API_URL=$(aws cloudformation describe-stacks \
            --stack-name myapp-prod \
            --query 'Stacks[0].Outputs[?OutputKey==`ApiUrl`].OutputValue' \
            --output text)
          curl -f "$API_URL/health"
```

### Key Considerations

- **Cold starts:** Consider provisioned concurrency
- **Versioning:** Use aliases for traffic shifting
- **Monitoring:** CloudWatch Logs and X-Ray
- **Limits:** Be aware of Lambda execution limits

---

## Case Study 4: Static Site / JAMstack

**Scenario:** Marketing site deployed to CDN.

**When to use:**
- Static content
- Maximum performance
- Global distribution
- Low cost

### Pipeline

```yaml
name: Deploy Static Site

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
      - run: npm run build
      
      - uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/

  preview:
    needs: build
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      
      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: mysite
          directory: dist
          gitHubToken: ${{ secrets.GITHUB_TOKEN }}

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: dist
          path: dist/
      
      - uses: cloudflare/pages-action@v1
        with:
          apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
          accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
          projectName: mysite
          directory: dist
          branch: main

      - name: Purge cache
        run: |
          curl -X POST "https://api.cloudflare.com/client/v4/zones/${{ secrets.CLOUDFLARE_ZONE_ID }}/purge_cache" \
            -H "Authorization: Bearer ${{ secrets.CLOUDFLARE_API_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"purge_everything":true}'
```

### Key Considerations

- **Preview deployments:** PR-based previews for review
- **Cache invalidation:** Purge CDN after deploy
- **Asset optimization:** Compress images, minify code
- **Analytics:** Track Core Web Vitals

---

## Case Study 5: Mobile Application

**Scenario:** iOS and Android app deployed to app stores.

**When to use:**
- Native mobile apps
- App store distribution
- Beta testing programs

### Pipeline (iOS)

```yaml
name: iOS Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Xcode
        uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: latest-stable
      
      - name: Install CocoaPods
        run: pod install
      
      - name: Build and test
        run: |
          xcodebuild test \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -destination 'platform=iOS Simulator,name=iPhone 15'
      
      - name: Install certificates
        uses: apple-actions/import-codesign-certs@v2
        with:
          p12-file-base64: ${{ secrets.IOS_P12_BASE64 }}
          p12-password: ${{ secrets.IOS_P12_PASSWORD }}
      
      - name: Install provisioning profile
        uses: apple-actions/download-provisioning-profiles@v2
        with:
          bundle-id: com.example.myapp
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_API_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_API_PRIVATE_KEY }}
      
      - name: Build for distribution
        run: |
          xcodebuild archive \
            -workspace MyApp.xcworkspace \
            -scheme MyApp \
            -archivePath build/MyApp.xcarchive \
            -destination 'generic/platform=iOS'
          
          xcodebuild -exportArchive \
            -archivePath build/MyApp.xcarchive \
            -exportPath build/export \
            -exportOptionsPlist ExportOptions.plist
      
      - name: Upload to TestFlight
        if: github.ref == 'refs/heads/main'
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: build/export/MyApp.ipa
          issuer-id: ${{ secrets.APPSTORE_ISSUER_ID }}
          api-key-id: ${{ secrets.APPSTORE_API_KEY_ID }}
          api-private-key: ${{ secrets.APPSTORE_API_PRIVATE_KEY }}
```

### Key Considerations

- **Code signing:** Certificate and profile management
- **Beta distribution:** TestFlight, Firebase App Distribution
- **App Store review:** Build time for review process
- **Version management:** Automatic version bumping

---

## Case Study 6: Docker Swarm

**Scenario:** Multi-container application on Docker Swarm.

**When to use:**
- Simpler than Kubernetes
- Existing Docker expertise
- Medium-scale deployments

### Pipeline

```yaml
name: Deploy to Docker Swarm

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build images
        run: docker-compose build
      
      - name: Login to registry
        run: echo "${{ secrets.REGISTRY_PASSWORD }}" | docker login registry.example.com -u ${{ secrets.REGISTRY_USER }} --password-stdin
      
      - name: Push images
        run: |
          docker-compose push
      
      - name: Deploy to Swarm
        run: |
          echo "${{ secrets.SWARM_SSH_KEY }}" > /tmp/swarm_key
          chmod 600 /tmp/swarm_key
          
          ssh -i /tmp/swarm_key ${{ secrets.SWARM_MANAGER }} << 'EOF'
            docker stack deploy -c docker-compose.prod.yml myapp --with-registry-auth
          EOF
      
      - name: Verify deployment
        run: |
          ssh -i /tmp/swarm_key ${{ secrets.SWARM_MANAGER }} "docker service ls"
```

---

## Case Study 7: Data Center Fleet Deployment

**Scenario:** Service deployed to thousands of on-premise nodes.

**When to use:**
- Large infrastructure
- On-premise data centers
- Controlled rollouts across fleet

### Pipeline

```yaml
name: Fleet Deployment

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build package
        run: make package
      - uses: actions/upload-artifact@v4
        with:
          name: myservice.tar.gz
          path: dist/myservice.tar.gz

  deploy-canary:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: myservice.tar.gz
      
      - name: Deploy to canary nodes (1%)
        run: |
          ansible-playbook deploy.yml \
            -i inventory/canary.ini \
            -e "package_path=./myservice.tar.gz" \
            -e "version=${{ github.sha }}"
      
      - name: Wait and monitor
        run: |
          sleep 300  # 5 minutes
          ./scripts/check-metrics.sh canary

  deploy-full:
    needs: deploy-canary
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: myservice.tar.gz
      
      - name: Deploy to all nodes (rolling 10%)
        run: |
          ansible-playbook deploy.yml \
            -i inventory/production.ini \
            -e "package_path=./myservice.tar.gz" \
            -e "version=${{ github.sha }}" \
            -e "serial_percentage=10"
```

### Key Considerations

- **Canary deployments:** Test on subset first
- **Rolling updates:** Don't update all nodes simultaneously
- **Rollback capability:** Keep previous package version
- **Health monitoring:** Automated health checks across fleet

---

## Decision Guide

| Scenario | Recommended Approach |
|----------|---------------------|
| Learning/hobby | VPS + SSH |
| Startup MVP | PaaS (Heroku, Railway) |
| Growing team | Kubernetes |
| Static site | CDN (Cloudflare, Vercel) |
| Mobile app | Fastlane + TestFlight/Play Console |
| Enterprise | Kubernetes + GitOps |
| Data center | Ansible + Canary |
| Serverless | Cloud Functions + IaC |

---

## What's Next?

These case studies show CI/CD in action across different deployment targets. The patterns can be combined and adapted for your specific needs.

The final document in this series is the **Glossary**: a quick reference for CI/CD terminology.

**Need a term reference?** Continue to [Glossary →](./glossary)

---

## Quick Reference

### Deployment Target Matrix

| Target | Complexity | Scalability | Cost |
|--------|------------|-------------|------|
| VPS | Low | Low | Low |
| PaaS | Low | Medium | Medium |
| Kubernetes | High | High | Variable |
| Serverless | Medium | High | Low-Medium |
| Static/CDN | Low | High | Low |
| Docker Swarm | Medium | Medium | Low |

### Common Patterns

- **All scenarios:** Build → Test → Deploy → Verify
- **VPS:** rsync/SSH for file transfer
- **Kubernetes:** kubectl/Helm for deployment
- **Serverless:** IaC tools (SAM, Terraform)
- **Static:** CDN upload + cache invalidation
- **Mobile:** Code signing + store upload

---

**Remember:** Start simple. Add complexity when you feel pain, not in anticipation of it. The best deployment is the one that works reliably for your current scale.
