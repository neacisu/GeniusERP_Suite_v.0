---
created: 2025-08-29T10:00:23Z
last_updated: 2025-08-29T10:00:23Z
version: 1.0
author: Claude Code PM System
---

# System Patterns

## Architectural Patterns

### Project Management Pattern
**CCPM (Claude Code PM) System** - Advanced project management with parallel agent execution

#### Pattern Implementation
- **PRD-Driven Development**: All features start with Product Requirements Documents
- **Epic Decomposition**: Large features broken into manageable tasks
- **Parallel Agent Execution**: Multiple Claude instances working simultaneously
- **GitHub Integration**: Issues as the single source of truth

#### Benefits
- Context preservation across sessions
- Parallel development without conflicts
- Full traceability from idea to production
- Transparent progress tracking

### Documentation-First Architecture

#### Structure Pattern
```
Documentation/
├── 0_instructiuni_stricte_de_proiectare.md  # Design principles
├── 1_roadmap_general_suita_genius_erp.md    # Master roadmap
├── 2-11_roadmap_*.md                        # Phase-specific roadmaps
└── readme_genius_erp_suite.md               # Extended documentation
```

#### Design Principles
- **Sequential Numbering**: Clear dependency order (0-11)
- **Phase-Based Organization**: F0-F7 development phases
- **Hierarchical Structure**: General → Specific → Implementation
- **Cross-Reference Links**: Inter-document connectivity

### Microservices Architecture (Planned)

#### Service Organization
- **13 Standalone Applications**: Independent deployable units
- **Worker Fleet**: 30+ specialized Python workers
- **Event-Driven Communication**: RabbitMQ message bus
- **API Gateway**: Traefik for request routing

#### Worker Pattern
```yaml
Worker Types:
  - Core Workers: ocr, pdf.render, email.send
  - ANAF Workers: taxpayer, efactura, etransport, saft
  - AI Workers: llm, forecast, match.ai, summary
  - Business Workers: fraud.scoring, route.optimization
  - GDPR Workers: consent.ai, rtbf, audit.ai
```

### Multi-Tenancy Pattern

#### Isolation Strategy
- **Database**: Cluster per tenant, schema per module
- **Storage**: Bucket per tenant, prefix per module  
- **Kubernetes**: Namespace per tenant
- **Identity**: Keycloak realm per tenant

#### Resource Pattern
```
Tenant Isolation:
├── PostgreSQL: {tenant}_core database
├── MinIO: {tenant}-bucket storage
├── K8s: {tenant}-namespace
└── Redis: logical-db per tenant
```

### Event-Driven Architecture

#### Message Patterns
- **Command Events**: Direct action requests (`worker.request.<tag>`)
- **Domain Events**: Business state changes (`sales.*`, `procurement.*`)
- **Integration Events**: Cross-module communication
- **Audit Events**: Compliance and tracking

#### Event Flow
```
Frontend → API → RabbitMQ → Worker → Response Queue → API → Frontend
```

### Security Patterns

#### Zero Trust Architecture
- **mTLS Everywhere**: Service-to-service encryption
- **JWT Authentication**: Stateless token-based auth
- **RBAC/ABAC**: Role and attribute-based access
- **Secrets Management**: HashiCorp Vault integration

#### Data Protection Pattern
```yaml
Encryption Layers:
  - Transit: TLS 1.3 + mTLS
  - Rest: AES-256-GCM per tenant
  - Application: Field-level encryption
  - Backup: Encrypted snapshots
```

### Observability Patterns

#### Three Pillars Implementation
- **Metrics**: Prometheus with Grafana dashboards
- **Logs**: Structured logging with Loki aggregation
- **Traces**: OpenTelemetry with Tempo backend

#### Monitoring Pattern
```yaml
Observability Stack:
  - Collection: OTEL auto-instrumentation
  - Storage: Prometheus + Loki + Tempo
  - Visualization: Grafana unified dashboards
  - Alerting: Alertmanager + PagerDuty
```

### Development Patterns

#### Nx Monorepo Structure (Planned)
```
workspace/
├── apps/
│   ├── shell-ui/           # Main shell application
│   ├── admin-core/         # Admin interface
│   └── {module}-api/       # Module-specific APIs
├── libs/
│   ├── shared/             # Common utilities
│   ├── ui-components/      # Reusable UI components
│   └── api-clients/        # Generated API clients
└── tools/
    ├── generators/         # Code generators
    └── executors/          # Build tools
```

#### Code Generation Patterns
- **API Client Generation**: OpenAPI spec → TypeScript clients
- **Database Migrations**: Declarative schema evolution
- **Helm Chart Templates**: Kubernetes deployment consistency

### Data Flow Patterns

#### CQRS (Command Query Responsibility Segregation)
- **Write Side**: FastAPI + PostgreSQL for commands
- **Read Side**: DuckDB + Delta Lake for analytics
- **Event Sourcing**: RabbitMQ for state changes
- **Materialized Views**: Real-time aggregations

#### Data Pipeline Pattern
```
OLTP (PostgreSQL) → Events (RMQ) → ETL (DuckDB) → Analytics (Cerniq)
```

### Testing Patterns

#### Test Pyramid Implementation
- **Unit Tests**: Individual function testing
- **Integration Tests**: Service interaction testing
- **Contract Tests**: API compatibility testing
- **E2E Tests**: Full workflow validation

#### Test Strategy
```yaml
Testing Levels:
  - Unit: Jest/Vitest (Frontend), Pytest (Backend)
  - Integration: Testcontainers for databases
  - Contract: Pact.js for API contracts
  - E2E: Playwright for user workflows
```

### Deployment Patterns

#### GitOps Workflow
```
Code → GitHub → Actions → Artifacts → ArgoCD → Kubernetes
```

#### Canary Deployment Pattern
- **Blue-Green Staging**: Safe production deployments
- **Traffic Splitting**: Gradual rollout (10% → 100%)
- **Automated Rollback**: SLO-based failure detection
- **Observability Integration**: Real-time monitoring

### Configuration Patterns

#### Environment Management
```yaml
Configuration Layers:
  - Base: Default values in code
  - Environment: Environment-specific overrides
  - Runtime: Dynamic configuration updates
  - Secrets: Vault-managed sensitive data
```

#### Feature Flags Pattern
- **Progressive Rollout**: Feature enablement control
- **A/B Testing**: Experimental feature validation
- **Emergency Switches**: Rapid feature disabling
- **User Segmentation**: Targeted feature access

### Integration Patterns

#### API Gateway Pattern
- **Traefik v3**: Request routing and load balancing
- **Rate Limiting**: Token bucket algorithm
- **Authentication**: JWT validation middleware
- **Circuit Breaker**: Failure resilience

#### External Service Integration
```yaml
Government APIs:
  - ANAF: Tax and e-Invoice integration
  - Inspecția Muncii: REGES employment data
  - Pattern: Circuit breaker + retry + fallback
```

### Performance Patterns

#### Caching Strategy
- **L1 Cache**: Application-level (in-memory)
- **L2 Cache**: Redis distributed cache
- **L3 Cache**: CDN for static assets
- **Database Cache**: pgBouncer connection pooling

#### Scaling Patterns
```yaml
Horizontal Scaling:
  - Stateless Services: HPA with CPU/memory metrics
  - Stateful Services: Cluster-aware scaling
  - Workers: Queue-length based scaling
  - Databases: Read replicas + sharding
```

### Error Handling Patterns

#### Resilience Patterns
- **Circuit Breaker**: Prevent cascade failures
- **Retry with Backoff**: Transient error recovery
- **Bulkhead**: Failure isolation
- **Timeout**: Resource exhaustion prevention

#### Error Response Pattern
```yaml
Error Structure:
  - HTTP Status: Standard codes
  - Error Code: Application-specific
  - Message: User-friendly description
  - Details: Technical debugging info
  - Trace ID: Distributed tracing correlation
```

### Compliance Patterns

#### GDPR Implementation
- **Data Minimization**: Collect only necessary data
- **Right to be Forgotten**: Automated data deletion
- **Consent Management**: Granular permission tracking
- **Data Portability**: Export capabilities

#### Audit Trail Pattern
```yaml
Audit Events:
  - Who: User identification
  - What: Action performed
  - When: Timestamp (UTC)
  - Where: Source system/IP
  - Why: Business context
  - Result: Success/failure + details
```

These patterns form the foundation for building scalable, maintainable, and secure enterprise software that meets both technical and regulatory requirements.
