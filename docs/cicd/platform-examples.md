---
# Required
sidebar_position: 10
title: "CI/CD Platform Examples for DevOps Teams"
description: >-
  Production-ready CI/CD pipeline examples for GitHub Actions, GitLab CI, Cloud Build,
  and Jenkins. Adapt these DevOps-ready configs for build, test, scan, and deploy.

# SEO
keywords:
  - ci/cd platform examples
  - github actions
  - gitlab ci
  - google cloud build
  - jenkins pipeline
  - ci/cd examples
  - pipeline configuration
  - workflow examples
  - jenkinsfile
  - gitlab-ci.yml
  - github workflow
  - cloudbuild.yaml
  - ci/cd templates
  - pipeline templates
  - devops pipelines
  - learn ci/cd

# Social sharing
og_title: "CI/CD Platform Examples: GitHub Actions, GitLab CI, Jenkins"
og_description: "Copy production-ready CI/CD pipelines with DevOps best practices for build, test, scan, and deploy."
og_image: "/img/ci-cd-social-card.svg"

# Content management
date_published: 2025-01-24
date_modified: 2026-01-25
author: shivam
reading_time: 25
content_type: reference
---

# CI/CD Platform Examples (End-to-End)

I've configured CI/CD pipelines across dozens of platforms over the years—from Jenkins at Aurigo when I was building automation frameworks, to GitHub Actions and GitLab CI for various internal services. Each platform has its quirks, strengths, and gotchas.

If you're learning CI/CD for DevOps, concrete platform examples are the fastest way to connect concepts to implementation.

This document provides complete, production-ready pipeline configurations for the most popular platforms. These aren't toy examples—they're the patterns I've used in real systems serving real users. Each example includes:

- Build, test, and lint stages
- Security scanning
- Container image building
- Deployment to multiple environments
- Proper secrets handling
- Caching for performance

Copy what you need, adapt it to your stack, and ship with confidence.

**What you'll learn in this guide:**
- How to structure end-to-end pipelines on popular platforms
- Common CI/CD patterns that translate across tooling
- The trade-offs between hosted and self-managed systems

---

## GitHub Actions: Complete Pipeline

GitHub Actions is my go-to for new projects. It's well-integrated with GitHub, has excellent marketplace actions, and the YAML syntax is readable.

### Complete Node.js/TypeScript Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]

# Cancel in-progress runs for the same ref
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

permissions:
  contents: read
  packages: write
  security-events: write
  id-token: write

jobs:
  # ============================================
  # Fast feedback jobs run in parallel
  # ============================================
  
  lint:
    name: Lint & Format
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run ESLint
        run: npm run lint
      
      - name: Check formatting
        run: npm run format:check
      
      - name: Type check
        run: npm run typecheck

  unit-tests:
    name: Unit Tests
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run unit tests
        run: npm test -- --coverage --reporters=default --reporters=jest-junit
        env:
          JEST_JUNIT_OUTPUT_DIR: ./reports
      
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          fail_ci_if_error: true
      
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-results
          path: reports/junit.xml

  # ============================================
  # Security scanning
  # ============================================
  
  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v3
        if: always()
        with:
          sarif_file: 'trivy-results.sarif'
  
  codeql:
    name: CodeQL Analysis
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v3
        with:
          languages: javascript-typescript
      
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v3

  # ============================================
  # Build (depends on fast feedback jobs)
  # ============================================
  
  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint, unit-tests]
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build-push.outputs.digest }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha,prefix=
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
      
      - name: Build and push
        id: build-push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
          provenance: true
          sbom: true
      
      - name: Scan built image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ steps.build-push.outputs.digest }}
          exit-code: 1
          severity: CRITICAL,HIGH

  # ============================================
  # Integration tests (against built image)
  # ============================================
  
  integration-tests:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: [build]
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run database migrations
        run: npm run db:migrate
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379

  # ============================================
  # Deployment
  # ============================================
  
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, integration-tests, security-scan]
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.myapp.example.com
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-staging
          aws-region: us-west-2
      
      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --name staging-cluster
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build.outputs.image-digest }} \
            -n myapp
          kubectl rollout status deployment/myapp -n myapp --timeout=300s
      
      - name: Run smoke tests
        run: |
          npm run test:smoke -- --env=staging
      
      - name: Notify on failure
        if: failure()
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: 'deployments'
          payload: |
            {
              "text": "❌ Staging deployment failed for ${{ github.repository }}",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "Deployment to staging failed\n*Repo:* ${{ github.repository }}\n*Commit:* ${{ github.sha }}\n<${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}|View logs>"
                  }
                }
              ]
            }
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [deploy-staging]
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://myapp.example.com
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/github-actions-production
          aws-region: us-west-2
      
      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --name production-cluster
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build.outputs.image-digest }} \
            -n myapp
          kubectl rollout status deployment/myapp -n myapp --timeout=300s
      
      - name: Create deployment marker
        run: |
          curl -X POST "https://api.datadoghq.com/api/v1/events" \
            -H "DD-API-KEY: ${{ secrets.DATADOG_API_KEY }}" \
            -d '{
              "title": "Production Deployment",
              "text": "Deployed ${{ github.sha }} to production",
              "tags": ["environment:production", "service:myapp"]
            }'
      
      - name: Notify success
        uses: slackapi/slack-github-action@v1
        with:
          channel-id: 'deployments'
          payload: |
            {
              "text": "✅ Production deployment successful for ${{ github.repository }}"
            }
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

### Reusable Workflows

Create reusable workflows for common patterns:

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-digest:
        required: true
        type: string
    secrets:
      AWS_ROLE_ARN:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-west-2
      
      - name: Deploy
        run: |
          aws eks update-kubeconfig --name ${{ inputs.environment }}-cluster
          kubectl set image deployment/myapp \
            myapp=ghcr.io/${{ github.repository }}@${{ inputs.image-digest }}
```

```yaml
# Using the reusable workflow
jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image-digest: ${{ needs.build.outputs.image-digest }}
    secrets:
      AWS_ROLE_ARN: ${{ secrets.STAGING_ROLE_ARN }}
```

---

## GitLab CI: Complete Pipeline

GitLab CI is powerful and deeply integrated with GitLab features. Here's a complete production pipeline.

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - test
  - build
  - security
  - deploy

variables:
  NODE_VERSION: "20"
  DOCKER_HOST: tcp://docker:2376
  DOCKER_TLS_CERTDIR: "/certs"
  DOCKER_TLS_VERIFY: 1
  DOCKER_CERT_PATH: "$DOCKER_TLS_CERTDIR/client"
  IMAGE_NAME: $CI_REGISTRY_IMAGE

# Default settings
default:
  image: node:${NODE_VERSION}
  cache:
    key:
      files:
        - package-lock.json
    paths:
      - node_modules/
    policy: pull

# ============================================
# Validate Stage
# ============================================

lint:
  stage: validate
  script:
    - npm ci
    - npm run lint
    - npm run format:check
    - npm run typecheck
  cache:
    policy: pull-push
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ============================================
# Test Stage
# ============================================

unit-tests:
  stage: test
  script:
    - npm ci
    - npm test -- --coverage --reporters=default --reporters=jest-junit
  coverage: '/All files[^|]*\|[^|]*\s+([\d\.]+)/'
  artifacts:
    when: always
    reports:
      junit: reports/junit.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

integration-tests:
  stage: test
  services:
    - name: postgres:15
      alias: postgres
    - name: redis:7
      alias: redis
  variables:
    POSTGRES_PASSWORD: test
    POSTGRES_DB: testdb
    DATABASE_URL: postgresql://postgres:test@postgres:5432/testdb
    REDIS_URL: redis://redis:6379
  script:
    - npm ci
    - npm run db:migrate
    - npm run test:integration
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# ============================================
# Build Stage
# ============================================

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - |
      docker build \
        --cache-from $IMAGE_NAME:latest \
        --tag $IMAGE_NAME:$CI_COMMIT_SHA \
        --tag $IMAGE_NAME:$CI_COMMIT_REF_SLUG \
        --tag $IMAGE_NAME:latest \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        .
    - docker push $IMAGE_NAME:$CI_COMMIT_SHA
    - docker push $IMAGE_NAME:$CI_COMMIT_REF_SLUG
    - docker push $IMAGE_NAME:latest
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

# ============================================
# Security Stage
# ============================================

container-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_NAME:$CI_COMMIT_SHA
  allow_failure: false
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - if: $CI_COMMIT_TAG

dependency-scan:
  stage: security
  image:
    name: aquasec/trivy:latest
    entrypoint: [""]
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL .
  allow_failure: false
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

sast:
  stage: security
  include:
    - template: Security/SAST.gitlab-ci.yml

# ============================================
# Deploy Stage
# ============================================

.deploy-template: &deploy-template
  image: bitnami/kubectl:latest
  before_script:
    - kubectl config set-cluster k8s --server="$KUBE_SERVER" --certificate-authority="$KUBE_CA_CERT"
    - kubectl config set-credentials gitlab --token="$KUBE_TOKEN"
    - kubectl config set-context default --cluster=k8s --user=gitlab
    - kubectl config use-context default

deploy-staging:
  <<: *deploy-template
  stage: deploy
  environment:
    name: staging
    url: https://staging.myapp.example.com
  script:
    - kubectl set image deployment/myapp myapp=$IMAGE_NAME:$CI_COMMIT_SHA -n staging
    - kubectl rollout status deployment/myapp -n staging --timeout=300s
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: on_success

deploy-production:
  <<: *deploy-template
  stage: deploy
  environment:
    name: production
    url: https://myapp.example.com
  script:
    - kubectl set image deployment/myapp myapp=$IMAGE_NAME:$CI_COMMIT_SHA -n production
    - kubectl rollout status deployment/myapp -n production --timeout=300s
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  needs:
    - deploy-staging
```

### GitLab CI Includes and Templates

Organize large pipelines with includes:

```yaml
# .gitlab-ci.yml
include:
  - local: '.gitlab/ci/lint.yml'
  - local: '.gitlab/ci/test.yml'
  - local: '.gitlab/ci/build.yml'
  - local: '.gitlab/ci/deploy.yml'
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml

stages:
  - validate
  - test
  - build
  - security
  - deploy
```

```yaml
# .gitlab/ci/deploy.yml
.deploy:
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/$APP_NAME $APP_NAME=$IMAGE -n $NAMESPACE
    - kubectl rollout status deployment/$APP_NAME -n $NAMESPACE

deploy-staging:
  extends: .deploy
  stage: deploy
  environment:
    name: staging
  variables:
    NAMESPACE: staging
    APP_NAME: myapp
    IMAGE: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
```

---

## Google Cloud Build: Complete Pipeline

Google Cloud Build is excellent for GCP-native workloads. Here's a complete configuration:

```yaml
# cloudbuild.yaml
steps:
  # ============================================
  # Install dependencies and cache
  # ============================================
  
  - id: 'install-dependencies'
    name: 'node:20'
    entrypoint: 'npm'
    args: ['ci']
    
  # ============================================
  # Parallel: Lint, Type Check, Unit Tests
  # ============================================
  
  - id: 'lint'
    name: 'node:20'
    entrypoint: 'npm'
    args: ['run', 'lint']
    waitFor: ['install-dependencies']
    
  - id: 'typecheck'
    name: 'node:20'
    entrypoint: 'npm'
    args: ['run', 'typecheck']
    waitFor: ['install-dependencies']
    
  - id: 'unit-tests'
    name: 'node:20'
    entrypoint: 'npm'
    args: ['test', '--', '--coverage']
    waitFor: ['install-dependencies']
    
  # ============================================
  # Build container image
  # ============================================
  
  - id: 'build-image'
    name: 'gcr.io/cloud-builders/docker'
    args:
      - 'build'
      - '--cache-from'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:latest'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
      - '-t'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:latest'
      - '.'
    waitFor: ['lint', 'typecheck', 'unit-tests']
    
  # ============================================
  # Security scan
  # ============================================
  
  - id: 'scan-image'
    name: 'gcr.io/cloud-builders/gcloud'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        gcloud artifacts docker images scan \
          ${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA} \
          --format='value(response.scan)' > /workspace/scan_id.txt
        gcloud artifacts docker images list-vulnerabilities \
          $(cat /workspace/scan_id.txt) \
          --format='table(vulnerability.effectiveSeverity, vulnerability.cvssScore, vulnerability.packageIssue.affectedPackage, vulnerability.packageIssue.packageType, vulnerability.shortDescription)'
    waitFor: ['build-image']
    
  # ============================================
  # Push to Artifact Registry
  # ============================================
  
  - id: 'push-image'
    name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
    waitFor: ['scan-image']
    
  - id: 'push-latest'
    name: 'gcr.io/cloud-builders/docker'
    args:
      - 'push'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:latest'
    waitFor: ['push-image']
    
  # ============================================
  # Deploy to Cloud Run
  # ============================================
  
  - id: 'deploy-staging'
    name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE}-staging'
      - '--image'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
      - '--region'
      - '${_REGION}'
      - '--platform'
      - 'managed'
      - '--allow-unauthenticated'
      - '--set-env-vars'
      - 'ENVIRONMENT=staging'
    waitFor: ['push-image']
    
  # ============================================
  # Integration tests against staging
  # ============================================
  
  - id: 'integration-tests'
    name: 'node:20'
    entrypoint: 'npm'
    args: ['run', 'test:integration']
    env:
      - 'API_URL=https://${_SERVICE}-staging-${PROJECT_NUMBER}.${_REGION}.run.app'
    waitFor: ['deploy-staging']
    
  # ============================================
  # Deploy to production (manual approval via trigger)
  # ============================================
  
  - id: 'deploy-production'
    name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - '${_SERVICE}'
      - '--image'
      - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
      - '--region'
      - '${_REGION}'
      - '--platform'
      - 'managed'
      - '--set-env-vars'
      - 'ENVIRONMENT=production'
    waitFor: ['integration-tests']

# Substitutions
substitutions:
  _REGION: us-central1
  _REPOSITORY: my-repository
  _SERVICE: myapp

# Build options
options:
  logging: CLOUD_LOGGING_ONLY
  machineType: 'E2_HIGHCPU_8'

# Images to push
images:
  - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
  - '${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:latest'

# Build timeout
timeout: '1200s'
```

### Cloud Build with GKE Deployment

```yaml
# cloudbuild-gke.yaml
steps:
  # ... build steps ...
  
  - id: 'deploy-to-gke'
    name: 'gcr.io/cloud-builders/kubectl'
    args:
      - 'set'
      - 'image'
      - 'deployment/${_SERVICE}'
      - '${_SERVICE}=${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_SERVICE}:${COMMIT_SHA}'
      - '-n'
      - '${_NAMESPACE}'
    env:
      - 'CLOUDSDK_COMPUTE_REGION=${_REGION}'
      - 'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER}'
      
  - id: 'wait-for-rollout'
    name: 'gcr.io/cloud-builders/kubectl'
    args:
      - 'rollout'
      - 'status'
      - 'deployment/${_SERVICE}'
      - '-n'
      - '${_NAMESPACE}'
      - '--timeout=300s'
    env:
      - 'CLOUDSDK_COMPUTE_REGION=${_REGION}'
      - 'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER}'
```

---

## Jenkins: Complete Pipeline

Jenkins is still widely used, especially in enterprises. Here's a modern declarative pipeline:

```groovy
// Jenkinsfile
pipeline {
    agent {
        kubernetes {
            yaml '''
                apiVersion: v1
                kind: Pod
                spec:
                  containers:
                  - name: node
                    image: node:20
                    command:
                    - cat
                    tty: true
                  - name: docker
                    image: docker:24-dind
                    securityContext:
                      privileged: true
                    volumeMounts:
                    - name: docker-sock
                      mountPath: /var/run/docker.sock
                  - name: kubectl
                    image: bitnami/kubectl:latest
                    command:
                    - cat
                    tty: true
                  volumes:
                  - name: docker-sock
                    hostPath:
                      path: /var/run/docker.sock
            '''
        }
    }
    
    environment {
        REGISTRY = 'registry.example.com'
        IMAGE_NAME = 'myorg/myapp'
        DOCKER_CREDENTIALS = credentials('docker-registry')
        KUBECONFIG_STAGING = credentials('kubeconfig-staging')
        KUBECONFIG_PRODUCTION = credentials('kubeconfig-production')
    }
    
    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 30, unit: 'MINUTES')
        timestamps()
        disableConcurrentBuilds()
    }
    
    stages {
        // ============================================
        // Install and Validate
        // ============================================
        
        stage('Install') {
            steps {
                container('node') {
                    sh 'npm ci'
                }
            }
        }
        
        stage('Validate') {
            parallel {
                stage('Lint') {
                    steps {
                        container('node') {
                            sh 'npm run lint'
                        }
                    }
                }
                stage('Type Check') {
                    steps {
                        container('node') {
                            sh 'npm run typecheck'
                        }
                    }
                }
                stage('Unit Tests') {
                    steps {
                        container('node') {
                            sh 'npm test -- --coverage --reporters=default --reporters=jest-junit'
                        }
                    }
                    post {
                        always {
                            junit 'reports/junit.xml'
                            publishHTML([
                                allowMissing: false,
                                alwaysLinkToLastBuild: true,
                                keepAll: true,
                                reportDir: 'coverage/lcov-report',
                                reportFiles: 'index.html',
                                reportName: 'Coverage Report'
                            ])
                        }
                    }
                }
            }
        }
        
        // ============================================
        // Build
        // ============================================
        
        stage('Build Image') {
            steps {
                container('docker') {
                    script {
                        docker.withRegistry("https://${REGISTRY}", 'docker-registry') {
                            def image = docker.build("${IMAGE_NAME}:${GIT_COMMIT}")
                            image.push()
                            image.push('latest')
                        }
                    }
                }
            }
        }
        
        // ============================================
        // Security Scan
        // ============================================
        
        stage('Security Scan') {
            steps {
                container('docker') {
                    sh """
                        docker run --rm \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            aquasec/trivy:latest \
                            image --exit-code 1 --severity HIGH,CRITICAL \
                            ${REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT}
                    """
                }
            }
        }
        
        // ============================================
        // Deploy to Staging
        // ============================================
        
        stage('Deploy Staging') {
            when {
                branch 'main'
            }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-staging', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/myapp \
                                myapp=${REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT} \
                                -n staging
                            kubectl rollout status deployment/myapp -n staging --timeout=300s
                        """
                    }
                }
            }
        }
        
        // ============================================
        // Integration Tests
        // ============================================
        
        stage('Integration Tests') {
            when {
                branch 'main'
            }
            steps {
                container('node') {
                    sh 'npm run test:integration'
                }
            }
        }
        
        // ============================================
        // Deploy to Production (Manual Approval)
        // ============================================
        
        stage('Production Approval') {
            when {
                branch 'main'
            }
            steps {
                input message: 'Deploy to production?', ok: 'Deploy'
            }
        }
        
        stage('Deploy Production') {
            when {
                branch 'main'
            }
            steps {
                container('kubectl') {
                    withCredentials([file(credentialsId: 'kubeconfig-production', variable: 'KUBECONFIG')]) {
                        sh """
                            kubectl set image deployment/myapp \
                                myapp=${REGISTRY}/${IMAGE_NAME}:${GIT_COMMIT} \
                                -n production
                            kubectl rollout status deployment/myapp -n production --timeout=300s
                        """
                    }
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            slackSend(
                channel: '#deployments',
                color: 'good',
                message: "✅ ${env.JOB_NAME} #${env.BUILD_NUMBER} succeeded"
            )
        }
        failure {
            slackSend(
                channel: '#deployments',
                color: 'danger',
                message: "❌ ${env.JOB_NAME} #${env.BUILD_NUMBER} failed"
            )
        }
    }
}
```

### Jenkins Shared Libraries

Reuse pipeline code across projects:

```groovy
// vars/standardPipeline.groovy
def call(Map config) {
    pipeline {
        agent {
            kubernetes {
                yaml libraryResource('podTemplates/standard.yaml')
            }
        }
        
        stages {
            stage('Build') {
                steps {
                    container('node') {
                        sh 'npm ci'
                        sh 'npm run build'
                    }
                }
            }
            
            stage('Test') {
                steps {
                    container('node') {
                        sh 'npm test'
                    }
                }
            }
            
            stage('Deploy') {
                when {
                    branch 'main'
                }
                steps {
                    deployToKubernetes(
                        environment: config.environment ?: 'staging',
                        image: "${config.registry}/${config.imageName}:${GIT_COMMIT}"
                    )
                }
            }
        }
    }
}
```

```groovy
// Jenkinsfile using shared library
@Library('my-shared-library') _

standardPipeline(
    registry: 'registry.example.com',
    imageName: 'myorg/myapp',
    environment: 'production'
)
```

---

## Platform Comparison

| Feature | GitHub Actions | GitLab CI | Cloud Build | Jenkins |
|---------|---------------|-----------|-------------|---------|
| **Setup** | Zero (GitHub) | Zero (GitLab) | GCP account | Self-hosted |
| **Syntax** | YAML | YAML | YAML | Groovy |
| **Marketplace** | Excellent | Good | Limited | Plugins |
| **Secrets** | Built-in | Built-in | Secret Manager | Credentials |
| **Runners** | Hosted + self | Hosted + self | Hosted | Self-hosted |
| **Container** | Native | Native | Native | Plugin |
| **Kubernetes** | Via actions | Native | Native | Plugin |
| **Cost** | Free tier | Free tier | Pay per use | Free (infra cost) |

---

## FAQ: CI/CD Platform Examples

### Which CI/CD platform is best for DevOps teams?

It depends on your ecosystem. GitHub Actions is great if you're already on GitHub, GitLab CI if you want an integrated DevOps platform, Cloud Build for GCP-native workflows, and Jenkins for maximum control.

### Can I copy these pipelines directly?

Use them as a starting point. You'll still need to adapt secrets, environments, and deployment steps to your stack.

### How do I choose between hosted and self-hosted runners?

Hosted runners are faster to start with. Self-hosted runners make sense when you need specialized hardware, private networks, or strict compliance controls.

## Related Reading

- [Core Concepts: Understand pipeline anatomy first →](./core-concepts)
- [Pipeline Optimization: Make these examples fast →](./pipeline-optimization)
- [Metrics & Maturity: Measure if your platform works →](./metrics-maturity)

---

## What's Next?

You now have production-ready pipeline configurations for the major CI/CD platforms. These examples cover the patterns you'll need for most projects.

The next document in this series covers **Metrics, Measurement, and Maturity**: how to measure CI/CD effectiveness with DORA metrics, track pipeline performance, and assess your organization's CI/CD maturity level.

**Ready to measure and improve your CI/CD?** Continue to [Metrics & Maturity →](./metrics-maturity)

---

## Quick Reference

### Platform Selection Guide

| If you need... | Consider |
|----------------|----------|
| GitHub ecosystem | GitHub Actions |
| Self-hosted Git | GitLab CI |
| GCP native | Cloud Build |
| Maximum flexibility | Jenkins |
| Simple setup | GitHub Actions or GitLab CI |
| Enterprise features | GitLab CI or Jenkins |

### Common Patterns Across Platforms

All production pipelines should include:

1. **Fast feedback first** — Lint and unit tests before slow operations
2. **Parallel execution** — Independent jobs run simultaneously
3. **Caching** — Dependencies cached between runs
4. **Security scanning** — Vulnerabilities caught before deploy
5. **Environment separation** — Staging validated before production
6. **Notifications** — Team alerted on failures
7. **Audit trail** — All deployments logged

### Migration Considerations

Moving between platforms? Focus on:

- [ ] Secrets migration (different storage mechanisms)
- [ ] Runner/agent configuration
- [ ] Syntax translation (YAML variations)
- [ ] Marketplace action equivalents
- [ ] Caching strategy adaptation
- [ ] Environment/deployment approvals

---

**Remember:** The best CI/CD platform is the one your team will actually use and maintain. Start simple, add complexity as needed, and optimize based on real bottlenecks.
