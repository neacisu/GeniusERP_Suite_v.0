---
created: 2025-08-29T10:00:23Z
last_updated: 2025-08-29T10:00:23Z
version: 1.0
author: Claude Code PM System
---

# Technology Context

## Technology Stack Overview

**Project Type**: Documentation and Planning Repository for Enterprise ERP Suite  
**Primary Focus**: Project management, roadmap planning, and development coordination

### Core Technologies

#### Documentation & Project Management
- **Markdown**: Primary documentation format (.md files)
- **CCPM (Claude Code PM)**: Advanced project management system
- **Git**: Version control with GitHub integration
- **GitHub Issues**: Task and epic tracking through CCPM

#### Development Tools
- **GitHub CLI (gh)**: Installed version 2.45.0
- **gh-sub-issue extension**: For parent-child issue relationships
- **Tree command**: For directory structure visualization
- **Bash scripting**: Automation and tooling

### Runtime Environment

#### System Environment
- **OS**: Linux Ubuntu 24.04 LTS (6.8.0-58-generic kernel)
- **Architecture**: amd64
- **Shell**: /bin/bash
- **Working Directory**: /var/www/GeniusERP_Suite_v0_1

#### User Environment
- **User**: root
- **Group**: genius-team
- **Permissions**: Full read/write access to project directory

### Planned Technology Stack (From Documentation)

Based on the roadmap documentation, the future implementation will use:

#### Backend Technologies
- **Python 3.13**: Primary backend language
- **FastAPI**: API framework
- **PostgreSQL 17**: Primary database with pgvector extension
- **Redis 7**: Caching and session management
- **RabbitMQ**: Message queue for worker communication
- **Celery**: Distributed task queue

#### Frontend Technologies
- **React 19**: Frontend framework
- **Vite**: Build tool and development server
- **Nx**: Monorepo management
- **TypeScript**: Type-safe JavaScript

#### Infrastructure & DevOps
- **Kubernetes**: Container orchestration
- **Traefik v3**: API Gateway and load balancer
- **Keycloak 23**: Identity and access management
- **Docker**: Containerization
- **Helm**: Kubernetes package manager

#### Observability Stack
- **Prometheus 2.50**: Metrics collection
- **Grafana 10**: Dashboards and visualization
- **Loki 3**: Log aggregation
- **Tempo 2**: Distributed tracing
- **OpenTelemetry**: Telemetry instrumentation

#### AI & ML Technologies
- **GPU Workloads**: PyTorch, TensorFlow for AI workers
- **LLM Integration**: GPT-4o, Claude, local LLM support
- **Computer Vision**: OpenCV, MediaPipe for image processing
- **OCR**: PaddleOCR, Tesseract 5 for document processing

### Development Configurations

#### Port Allocations (NEANELU Application)
- **Frontend (React/Vite)**: Port 5000
- **Backend (FastAPI)**: Port 5001
- **PostgreSQL**: Port 5002 (main), 5433 (gestiune_marfa)

#### Database Configuration
- **Primary DB**: gestiune_marfa
- **User**: gestiune_user
- **Password**: gestiune_pass
- **Port**: 5433

#### Test Credentials
- **Email**: test_admin@iwms.com
- **Password**: Test123456

### Build & Development Tools

#### Package Management
- **pnpm**: Node.js package manager (planned)
- **Poetry**: Python dependency management (planned)
- **pip**: Python package installer

#### Code Quality
- **Pre-commit hooks**: Code quality enforcement (planned)
- **ESLint**: JavaScript/TypeScript linting (planned)
- **Black**: Python code formatting (planned)
- **Pytest**: Python testing framework (planned)

#### CI/CD Pipeline (Planned)
- **GitHub Actions**: Continuous integration
- **Nx Affected**: Incremental builds
- **Trivy**: Security scanning
- **Cosign**: Container signing
- **ArgoCD**: GitOps deployment

### Project Management Tools

#### CCPM System
- **Project Management**: PRD creation, epic planning, task decomposition
- **Parallel Execution**: Multiple Claude agents working simultaneously
- **GitHub Integration**: Seamless issue synchronization
- **Context Management**: Persistent project state

#### Git Workflow
- **Repository**: https://github.com/neacisu/GeniusERP_Suite_v.0.git
- **Branch Strategy**: main branch (current)
- **Authentication**: GitHub CLI with personal access token

### Security & Compliance

#### Planned Security Stack
- **TLS 1.3**: Encryption in transit
- **mTLS**: Service-to-service communication
- **HashiCorp Vault**: Secrets management
- **OPA Gatekeeper**: Policy enforcement
- **RBAC/ABAC**: Role/attribute-based access control

#### Compliance Features
- **GDPR**: Data protection and privacy
- **eIDAS**: Electronic signatures
- **ISO 27001**: Information security management
- **SAF-T RO**: Romanian tax reporting

### Performance & Scalability

#### Scaling Technologies (Planned)
- **Horizontal Pod Autoscaler**: Kubernetes-based scaling
- **pgBouncer**: Database connection pooling
- **Redis Cluster**: Distributed caching
- **MinIO**: Object storage with erasure coding

#### Monitoring & Alerting
- **Alertmanager**: Alert routing and management
- **PagerDuty**: Incident response (planned)
- **Slack Integration**: Team notifications
- **Synthetic Monitoring**: k6 load testing

### Development Dependencies

#### Current Dependencies
- **CCPM System**: Full installation with all commands and agents
- **GitHub CLI**: Authentication and repository management
- **Git**: Version control operations
- **Bash**: Script execution and automation

#### Future Dependencies (From Roadmap)
- **Node.js Ecosystem**: React, Vite, Nx, TypeScript
- **Python Ecosystem**: FastAPI, SQLAlchemy, Pydantic
- **Container Ecosystem**: Docker, Kubernetes, Helm
- **Cloud Services**: Multi-cloud deployment (Azure, AWS)

### Integration Points

#### External Services
- **GitHub**: Repository hosting and issue tracking
- **Container Registries**: ghcr.io for image storage (planned)
- **Cloud Providers**: Azure AKS, AWS EKS (planned)
- **Romanian Government APIs**: ANAF, Inspecția Muncii (planned)

#### Internal Services
- **Worker Fleet**: 30+ specialized Python workers
- **Microservices**: 13 standalone applications in the suite
- **Event Bus**: RabbitMQ-based inter-service communication

### Version Management

#### Current Versions
- **GitHub CLI**: 2.45.0-1ubuntu0.3
- **Git**: System default
- **Ubuntu**: 24.04 LTS
- **Linux Kernel**: 6.8.0-58-generic

#### Planned Version Strategy
- **Semantic Versioning**: For all application components
- **Container Tagging**: SHA-based with semantic tags
- **API Versioning**: v1, v2 strategy for APIs

### Development Workflow

#### Current Workflow
1. Documentation-driven development
2. CCPM-managed project planning
3. GitHub issue-based task tracking
4. Git-based version control

#### Planned Workflow
1. PRD creation with CCPM
2. Epic decomposition and parallel development
3. Continuous integration with GitHub Actions
4. GitOps deployment with ArgoCD
5. Monitoring and observability with full stack
