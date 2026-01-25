---
# Required
sidebar_position: 18
title: "CI/CD Glossary"
description: >-
  Complete glossary of CI/CD terminology. Definitions for continuous integration, 
  continuous delivery, deployment strategies, DevOps practices, and related concepts.

# SEO
keywords:
  - ci/cd glossary
  - ci/cd terms
  - devops terminology
  - continuous integration definition
  - continuous delivery definition
  - deployment terms
  - pipeline terminology

# Social sharing
og_title: "CI/CD Glossary: Complete Terminology Reference"
og_description: "Definitions for all CI/CD and DevOps terminology. From artifacts to zero-downtime deployment."
og_image: "/img/ci-cd-social-card.svg"

# Content management
date_published: 2025-01-24
date_modified: 2025-01-24
author: shivam
reading_time: 10
content_type: reference
---

# CI/CD Glossary

Quick reference for CI/CD and DevOps terminology used throughout this documentation.

---

## A

**Artifact**
A file or set of files produced by a build process. Examples include compiled binaries, Docker images, and deployment packages.

**Artifact Registry**
A storage system for build artifacts. Examples: Docker Hub, GitHub Packages, Artifactory, Nexus.

---

## B

**Blue-Green Deployment**
A deployment strategy using two identical production environments (blue and green). Traffic is switched from one to the other after validating the new deployment.

**Branch Protection**
Rules that enforce requirements before changes can be merged to protected branches. Examples: required reviews, passing tests, up-to-date branches.

**Build**
The process of transforming source code into deployable artifacts. May include compilation, bundling, and packaging.

---

## C

**Canary Deployment**
A deployment strategy that gradually rolls out changes to a small subset of users before full deployment. Named after canaries used in coal mines.

**CD (Continuous Delivery)**
The practice of automatically preparing code changes for release to production. Every change that passes automated tests is ready to deploy.

**CD (Continuous Deployment)**
The practice of automatically deploying every change that passes automated tests to production. No manual approval required.

**Change Failure Rate (CFR)**
The percentage of deployments that cause failures in production. One of the four DORA metrics.

**CI (Continuous Integration)**
The practice of frequently merging code changes to a shared repository, with each merge triggering automated build and test processes.

**Commit**
A snapshot of changes saved to version control. In CI/CD, commits often trigger pipeline runs.

**Container**
A lightweight, standalone executable package that includes everything needed to run software: code, runtime, libraries, and settings.

**Container Registry**
A storage and distribution system for container images. Examples: Docker Hub, Google Container Registry, Amazon ECR.

---

## D

**DAG (Directed Acyclic Graph)**
A graph structure used to define pipeline job dependencies. Jobs can run in parallel when no dependencies exist between them.

**Deployment**
The process of releasing software to an environment (development, staging, production).

**Deployment Frequency**
How often code is deployed to production. One of the four DORA metrics.

**DevOps**
A set of practices combining software development (Dev) and IT operations (Ops) to shorten the development lifecycle.

**Docker**
A platform for developing, shipping, and running applications in containers.

**DORA Metrics**
Four key metrics identified by DevOps Research and Assessment that predict software delivery performance: Deployment Frequency, Lead Time for Changes, Change Failure Rate, and Mean Time to Recovery.

---

## E

**Environment**
A deployment target with specific configuration. Common environments: development, staging, production.

**Environment Variable**
A variable set in the execution environment, often used to configure applications without changing code.

---

## F

**Feature Flag (Feature Toggle)**
A technique that allows features to be enabled or disabled without deploying new code. Enables trunk-based development and progressive rollouts.

**Flaky Test**
A test that produces inconsistent results without code changes. Sometimes passes, sometimes fails.

---

## G

**Gate (Quality Gate)**
A checkpoint in the pipeline that must pass before proceeding. Gates may check test coverage, security scan results, or other quality metrics.

**GitOps**
A practice that uses Git as the single source of truth for declarative infrastructure and applications. Changes are made via pull requests.

**Golden Path**
A recommended, well-supported way to accomplish a task in platform engineering. Makes the right thing the easy thing.

---

## H

**Helm**
A package manager for Kubernetes that uses templates (charts) to define, install, and manage applications.

**Hotfix**
An urgent fix applied directly to production, often bypassing normal release processes.

---

## I

**IaC (Infrastructure as Code)**
The practice of managing infrastructure through machine-readable definition files rather than manual configuration.

**Image**
A read-only template containing instructions for creating a container. Built from a Dockerfile.

**IDP (Internal Developer Platform)**
A self-service platform where developers can provision resources, deploy applications, and manage services.

---

## J

**Job**
A unit of work in a CI/CD pipeline. Jobs may run in parallel or sequentially depending on dependencies.

---

## K

**Kubernetes (K8s)**
An open-source container orchestration platform for automating deployment, scaling, and management of containerized applications.

---

## L

**Lead Time for Changes**
The time from code commit to production deployment. One of the four DORA metrics.

**Lint / Linting**
Static analysis of code to find potential errors, style issues, and suspicious constructs.

---

## M

**Matrix Build**
A build strategy that runs the same job across multiple configurations (operating systems, language versions, etc.) in parallel.

**Mean Time to Recovery (MTTR)**
The average time to recover from a production incident. One of the four DORA metrics.

**Merge Request / Pull Request (MR/PR)**
A request to merge changes from one branch into another, typically including code review.

**Monorepo**
A single repository containing multiple projects or services. Contrast with polyrepo (one repo per project).

---

## N

**Node**
In CI/CD, typically refers to a machine that runs pipeline jobs. Also called runner, agent, or worker.

---

## O

**OPA (Open Policy Agent)**
A general-purpose policy engine used to implement policy-as-code.

**OIDC (OpenID Connect)**
An authentication protocol used for secure, tokenless authentication between CI/CD systems and cloud providers.

---

## P

**Pipeline**
A series of automated steps that build, test, and deploy code. Triggered by events like commits or pull requests.

**Platform Engineering**
The discipline of designing and building toolchains and workflows that enable self-service capabilities for software engineering organizations.

**Pod**
The smallest deployable unit in Kubernetes, containing one or more containers.

**Progressive Delivery**
Deployment strategies that gradually expose changes to users, including canary, blue-green, and feature flags.

**Promotion**
Moving an artifact or deployment from one environment to another (e.g., staging to production).

---

## Q

**Quality Gate**
See Gate.

---

## R

**Registry**
A storage system for artifacts. See Artifact Registry, Container Registry.

**Release**
A versioned, deployable artifact or the act of making software available to users.

**Rollback**
Reverting to a previous version of deployed software after a failed deployment or incident.

**Rolling Deployment**
A deployment strategy that gradually replaces instances of the old version with the new version.

**Runner**
A machine or container that executes CI/CD pipeline jobs. Also called agent, node, or worker.

---

## S

**SARIF (Static Analysis Results Interchange Format)**
A standard format for the output of static analysis tools.

**SBOM (Software Bill of Materials)**
A list of all components, libraries, and dependencies in a software project.

**Secret**
Sensitive information (API keys, passwords, certificates) that must be protected and not stored in code.

**Self-Hosted Runner**
A runner managed by your organization rather than the CI/CD platform provider.

**Semantic Versioning (SemVer)**
A versioning scheme using MAJOR.MINOR.PATCH (e.g., 2.1.0) with specific rules for incrementing each number.

**Service Mesh**
Infrastructure layer that handles service-to-service communication, including features like load balancing, encryption, and observability.

**Shift Left**
Moving activities (testing, security) earlier in the development process to catch issues sooner.

**SSDLC (Secure Software Development Lifecycle)**
Development practices that integrate security at every phase of software creation.

**Stage**
A phase in a CI/CD pipeline grouping related jobs. Stages typically run sequentially while jobs within stages may run in parallel.

---

## T

**Tag**
A marker pointing to a specific commit, typically used for releases. Example: v1.0.0.

**Test Coverage**
The percentage of code executed during testing. Higher coverage generally indicates better testing.

**Trigger**
An event that starts a pipeline run. Common triggers: commits, pull requests, schedules, manual.

**Trunk-Based Development**
A branching strategy where developers frequently merge small changes to a single main branch (trunk).

---

## U

**Unit Test**
Tests that verify individual units of code (functions, methods) in isolation.

---

## V

**VCS (Version Control System)**
Software for tracking changes to files over time. Git is the most common VCS.

---

## W

**Workflow**
In GitHub Actions, a configurable automated process defined in YAML. Similar to pipeline in other systems.

---

## Y

**YAML**
A human-readable data format commonly used for CI/CD configuration files.

---

## Z

**Zero-Downtime Deployment**
A deployment strategy that ensures continuous availability during deployment. Achieved through rolling updates, blue-green, or canary deployments.

---

## Acronym Reference

| Acronym | Full Form |
|---------|-----------|
| CD | Continuous Delivery / Continuous Deployment |
| CFR | Change Failure Rate |
| CI | Continuous Integration |
| DAG | Directed Acyclic Graph |
| DORA | DevOps Research and Assessment |
| IaC | Infrastructure as Code |
| IDP | Internal Developer Platform |
| K8s | Kubernetes |
| MTTR | Mean Time to Recovery |
| OPA | Open Policy Agent |
| OIDC | OpenID Connect |
| PR | Pull Request |
| MR | Merge Request |
| SARIF | Static Analysis Results Interchange Format |
| SBOM | Software Bill of Materials |
| SemVer | Semantic Versioning |
| SSDLC | Secure Software Development Lifecycle |
| VCS | Version Control System |

---

## Related Documentation

- [Introduction to CI/CD](./introduction) — Start here if you're new to CI/CD
- [Core Concepts](./core-concepts) — Deep dive into fundamental CI/CD concepts
- [Troubleshooting](./troubleshooting) — Solutions for common problems

---

**This glossary is a living document.** If you encounter a term not listed here, the concept is likely explained in detail in the relevant section of this documentation.
