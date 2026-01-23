# Makefile for Docker Build/Push workflow
# Docusaurus Blog - Docker Deployment

# Load environment variables from .env file
ifneq (,$(wildcard ./.env))
	include .env
	export
endif

# Default values
DOCKER_REGISTRY ?= ghcr.io
DOCKER_USERNAME ?= shivam-g-mishra
IMAGE_TAG ?= latest
IMAGE_BLOG ?= blog
SSH_HOST ?= 134.199.180.26
SSH_USER ?= root

# Full image name
BLOG_IMAGE := $(DOCKER_REGISTRY)/$(DOCKER_USERNAME)/$(IMAGE_BLOG):$(IMAGE_TAG)

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)Docusaurus Blog - Docker Deployment$(NC)"
	@echo ""
	@echo "$(BLUE)Quick Start:$(NC)"
	@echo "  $(GREEN)make release$(NC)          # Complete deployment (recommended)"
	@echo "  $(GREEN)make dev$(NC)              # Start local development"
	@echo ""
	@echo "$(BLUE)Manual Steps:$(NC)"
	@echo "  make login              # Login to GHCR (auto-loads PAT)"
	@echo "  make build              # Build Docker image"
	@echo "  make push               # Push to registry"
	@echo "  make deploy             # Deploy to VPS"
	@echo "  make validate           # Validate deployment"
	@echo ""
	@echo "$(BLUE)Local Development:$(NC)"
	@echo "  make install            # Install dependencies"
	@echo "  make dev                # Start dev server"
	@echo "  make build-local        # Build locally"
	@echo ""
	@echo "$(BLUE)Shortcuts:$(NC)"
	@echo "  make r                  # release"
	@echo "  make v                  # validate"
	@echo ""
	@echo "$(BLUE)VPS Management:$(NC)"
	@echo "  make status             # Check container status"
	@echo "  make logs               # View logs"
	@echo "  make ssh                # SSH into VPS"
	@echo ""
	@echo "$(BLUE)All Targets:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' Makefile | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'
	@echo ""

.PHONY: check-env
check-env: ## Check if .env file exists
	@if [ ! -f .env ]; then \
		echo "$(RED)Error: .env file not found$(NC)"; \
		echo "$(YELLOW)Run: make setup$(NC)"; \
		exit 1; \
	fi

.PHONY: check-docker
check-docker: ## Check if Docker is running
	@if ! docker info > /dev/null 2>&1; then \
		echo "$(RED)Error: Docker is not running$(NC)"; \
		echo "$(YELLOW)Please start Docker and try again$(NC)"; \
		exit 1; \
	fi

.PHONY: setup
setup: ## Initial setup - create .env from template
	@if [ -f .env ]; then \
		echo "$(YELLOW).env file already exists$(NC)"; \
	else \
		cp env.example .env; \
		echo "$(GREEN).env file created from template$(NC)"; \
		echo "$(YELLOW)Please edit .env if needed$(NC)"; \
	fi

.PHONY: install
install: ## Install npm dependencies
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@npm install
	@echo "$(GREEN)✓ Dependencies installed$(NC)"

.PHONY: dev
dev: ## Start local development server
	@echo "$(BLUE)Starting development server...$(NC)"
	@npm start

.PHONY: build-local
build-local: ## Build locally (not Docker)
	@echo "$(BLUE)Building Docusaurus site...$(NC)"
	@npm run build
	@echo "$(GREEN)✓ Build completed$(NC)"

.PHONY: serve
serve: ## Serve the built site locally
	@echo "$(BLUE)Serving built site...$(NC)"
	@npm run serve

.PHONY: login
login: check-env ## Login to Docker registry (auto-loads PAT from secrets file)
	@echo "$(BLUE)Logging in to $(DOCKER_REGISTRY)...$(NC)"
	@if [ "$(DOCKER_REGISTRY)" = "ghcr.io" ]; then \
		if [ -z "$$CR_PAT" ]; then \
			if [ -f ~/Documents/secrets/github-pat.txt ]; then \
				export CR_PAT=$$(cat ~/Documents/secrets/github-pat.txt); \
				echo "$(GREEN)✓ Loaded PAT from ~/Documents/secrets/github-pat.txt$(NC)"; \
				echo "$$CR_PAT" | docker login ghcr.io -u $(DOCKER_USERNAME) --password-stdin; \
			else \
				echo "$(RED)Error: CR_PAT not set and ~/Documents/secrets/github-pat.txt not found$(NC)"; \
				exit 1; \
			fi; \
		else \
			echo "$$CR_PAT" | docker login ghcr.io -u $(DOCKER_USERNAME) --password-stdin; \
		fi; \
	else \
		docker login $(DOCKER_REGISTRY); \
	fi
	@echo "$(GREEN)✓ Logged in successfully$(NC)"

.PHONY: build
build: check-env check-docker ## Build Docker image
	@echo "$(BLUE)Building blog image...$(NC)"
	@echo "$(YELLOW)Image: $(BLOG_IMAGE)$(NC)"
	@docker build \
		-f Dockerfile \
		-t $(BLOG_IMAGE) \
		--platform linux/amd64 \
		.
	@echo "$(GREEN)✓ Blog image built$(NC)"

.PHONY: push
push: check-env ## Push image to registry
	@echo "$(BLUE)Pushing blog image...$(NC)"
	@docker push $(BLOG_IMAGE)
	@echo "$(GREEN)✓ Blog image pushed$(NC)"

.PHONY: publish
publish: build push ## Build and push image

.PHONY: deploy
deploy: check-env ## Deploy to VPS (updates blog container in personal-site stack)
	@echo "$(BLUE)Deploying blog to $(SSH_USER)@$(SSH_HOST)...$(NC)"
	@if [ "$(DOCKER_REGISTRY)" = "ghcr.io" ] && [ -z "$$CR_PAT" ]; then \
		if [ -f ~/Documents/secrets/github-pat.txt ]; then \
			export CR_PAT=$$(cat ~/Documents/secrets/github-pat.txt); \
		fi; \
	fi; \
	./scripts/deploy-blog.sh $(SSH_USER)@$(SSH_HOST)

.PHONY: validate
validate: ## Validate blog deployment
	@echo "$(BLUE)Validating blog deployment...$(NC)"
	@./scripts/validate-blog.sh

.PHONY: status
status: ## Check status of blog container on VPS
	@echo "$(BLUE)Checking blog container status on VPS...$(NC)"
	@ssh $(SSH_USER)@$(SSH_HOST) 'docker ps --filter name=blog'

.PHONY: logs
logs: ## View logs from blog container
	@echo "$(BLUE)Fetching logs from VPS...$(NC)"
	@ssh $(SSH_USER)@$(SSH_HOST) 'docker logs --tail=100 blog 2>&1 || echo "Container not found"'

.PHONY: ssh
ssh: ## SSH into VPS
	@ssh $(SSH_USER)@$(SSH_HOST)

.PHONY: clean
clean: ## Remove local Docker image
	@echo "$(BLUE)Removing local image...$(NC)"
	@docker rmi $(BLOG_IMAGE) 2>/dev/null || true
	@echo "$(GREEN)✓ Local image removed$(NC)"

.PHONY: images
images: check-env ## List built images
	@echo "$(BLUE)Docker images:$(NC)"
	@docker images | grep -E "$(IMAGE_BLOG)" || echo "No images found"

.PHONY: version
version: check-env ## Show current version info
	@echo "$(BLUE)Current Configuration:$(NC)"
	@echo "  Registry:       $(DOCKER_REGISTRY)"
	@echo "  Username:       $(DOCKER_USERNAME)"
	@echo "  Tag:            $(IMAGE_TAG)"
	@echo ""
	@echo "$(BLUE)Image Name:$(NC)"
	@echo "  Blog:           $(BLOG_IMAGE)"
	@echo ""
	@echo "$(BLUE)Deployment Target:$(NC)"
	@echo "  VPS:            $(SSH_USER)@$(SSH_HOST)"

# Full release workflow
.PHONY: release
release: login build push deploy validate ## Complete release: login, build, push, deploy, validate
	@echo ""
	@echo "$(GREEN)========================================$(NC)"
	@echo "$(GREEN)✓ Blog release completed successfully!$(NC)"
	@echo "$(GREEN)========================================$(NC)"
	@echo ""
	@echo "$(BLUE)Blog is live at:$(NC) $(GREEN)https://shivamm.info/blog$(NC)"

# Quick shortcuts
.PHONY: b
b: build ## Shortcut for build

.PHONY: p
p: push ## Shortcut for push

.PHONY: d
d: deploy ## Shortcut for deploy

.PHONY: pub
pub: publish ## Shortcut for publish

.PHONY: v
v: validate ## Shortcut for validate

.PHONY: r
r: release ## Shortcut for release

.DEFAULT_GOAL := help
