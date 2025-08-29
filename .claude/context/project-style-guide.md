---
created: 2025-08-29T10:00:23Z
last_updated: 2025-08-29T10:00:23Z
version: 1.0
author: Claude Code PM System
---

# Project Style Guide

## Development Standards

### Language and Framework Conventions

#### Python Development
**Version**: Python 3.13 (always use `python3`, never `python`)

**Code Style:**
```python
# File naming: snake_case
user_manager.py
data_validator.py

# Class naming: PascalCase
class UserManager:
    pass

class DataValidator:
    pass

# Function naming: snake_case
def process_user_data():
    pass

def validate_email_format():
    pass

# Constant naming: UPPER_SNAKE_CASE
MAX_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 30
```

**Import Organization:**
```python
# Standard library imports
import os
import sys
from datetime import datetime

# Third-party imports
import fastapi
import sqlalchemy
from pydantic import BaseModel

# Local application imports
from app.models import User
from app.utils import validators
```

#### TypeScript/JavaScript Development
**Framework**: React 19 with TypeScript

**Naming Conventions:**
```typescript
// File naming: kebab-case for components, camelCase for utilities
user-profile.component.tsx
user-manager.service.ts
dataValidators.ts

// Component naming: PascalCase
interface UserProfileProps {
  userId: string;
}

const UserProfile: React.FC<UserProfileProps> = ({ userId }) => {
  return <div>User Profile</div>;
};

// Function naming: camelCase
const processUserData = () => {};
const validateEmailFormat = () => {};

// Type naming: PascalCase
type UserData = {
  id: string;
  email: string;
};

interface ApiResponse<T> {
  data: T;
  status: 'success' | 'error';
}
```

### Database Conventions

#### Table Naming
```sql
-- Table names: snake_case, plural
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE user_roles (
    user_id UUID REFERENCES users(id),
    role_name VARCHAR(100)
);

-- Column names: snake_case
-- Foreign keys: {table}_id
user_id, tenant_id, warehouse_id
```

#### Multi-tenancy Patterns
```sql
-- Tenant isolation prefix
{tenant_id}_core  -- Database name
{module_name}     -- Schema name

-- Example: tenant_123_core.users.user_profiles
```

### API Design Standards

#### REST API Conventions
```http
# URL structure: /api/v{version}/{resource}
GET    /api/v1/users
POST   /api/v1/users
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}

# Nested resources
GET    /api/v1/tenants/{tenant_id}/users
POST   /api/v1/tenants/{tenant_id}/users/{user_id}/roles
```

#### Response Format
```json
{
  "status": "success",
  "data": {
    "id": "uuid",
    "email": "user@example.com"
  },
  "meta": {
    "timestamp": "2025-08-29T10:00:23Z",
    "request_id": "req_abc123"
  }
}
```

#### Error Response Format
```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  },
  "meta": {
    "timestamp": "2025-08-29T10:00:23Z",
    "request_id": "req_abc123",
    "trace_id": "trace_xyz789"
  }
}
```

### File Structure Conventions

#### Documentation Files
```
Documentation/
├── 0_instructiuni_stricte_de_proiectare.md  # Design principles
├── 1_roadmap_general_suita_genius_erp.md    # Master roadmap
├── 2_roadmap_f_0_foundation_infrastructure.md
├── ...
└── readme_genius_erp_suite.md               # Extended documentation
```

**Naming Pattern**: `{number}_{category}_{specific_name}.md`

#### Source Code Organization
```
app/
├── api/           # API endpoints
├── core/          # Core business logic
├── models/        # Data models
├── services/      # Business services
├── utils/         # Utility functions
└── workers/       # Background workers
```

#### CCPM Project Files
```
.claude/
├── epics/         # Epic documentation
├── prds/          # Product requirements
├── context/       # Project context
└── commands/      # CCPM commands
```

### Configuration Management

#### Environment Variables
```bash
# Naming: UPPER_SNAKE_CASE with module prefix
GENIUS_DB_HOST=localhost
GENIUS_DB_PORT=5432
GENIUS_REDIS_URL=redis://localhost:6379

# Test credentials (as specified in requirements)
TEST_EMAIL=test_admin@iwms.com
TEST_PASSWORD=Test123456

# Database configuration
DB_USER=gestiune_user
DB_PASSWORD=gestiune_pass
DB_NAME=gestiune_marfa
DB_PORT=5433
```

#### Application Management
```bash
# Control applications with specified script
sudo -u dev ./manage-app.sh start
sudo -u dev ./manage-app.sh stop
sudo -u dev ./manage-app.sh restart
sudo -u dev ./manage-app.sh status
```

### Port Allocation Standards

#### NEANELU Application Ports
```yaml
Frontend (React/Vite): 5000
Backend (FastAPI): 5001
PostgreSQL: 5002
```

#### Standard Port Ranges
```yaml
Frontend Services: 5000-5099
Backend APIs: 5100-5199
Databases: 5200-5299
Cache/Queue: 5300-5399
Monitoring: 5400-5499
```

### Git Workflow Standards

#### Branch Naming
```bash
# Feature branches
feature/user-authentication
feature/anaf-integration

# Bug fixes
bugfix/login-validation
hotfix/security-patch

# Epic branches (CCPM managed)
epic/foundation-infrastructure
epic/commercial-core-apps
```

#### Commit Message Format
```
type(scope): short description

Longer description explaining the change if needed.

Closes #123
```

**Types**: feat, fix, docs, style, refactor, test, chore

### Testing Conventions

#### Test File Naming
```python
# Python tests
test_user_manager.py
test_data_validator.py

# TypeScript tests
user-profile.test.tsx
data-validators.test.ts
```

#### Test Organization
```
tests/
├── unit/          # Unit tests
├── integration/   # Integration tests
├── e2e/          # End-to-end tests
└── fixtures/     # Test data
```

### Documentation Standards

#### Code Comments
```python
def process_user_data(user_id: str, tenant_id: str) -> UserData:
    """
    Process user data for the specified tenant.
    
    Args:
        user_id: Unique identifier for the user
        tenant_id: Tenant context for data isolation
        
    Returns:
        UserData: Processed user information
        
    Raises:
        ValidationError: If user_id or tenant_id is invalid
        DatabaseError: If data retrieval fails
    """
    pass
```

#### README Structure
```markdown
# Project Name

## Overview
Brief description of the project

## Installation
Step-by-step installation guide

## Usage
Basic usage examples

## Configuration
Configuration options and environment variables

## API Reference
API endpoints and usage

## Contributing
Development setup and contribution guidelines

## License
License information
```

### Security Standards

#### Authentication Headers
```http
Authorization: Bearer <jwt_token>
X-Tenant-ID: <tenant_uuid>
X-Warehouse-ID: <warehouse_uuid>
```

#### Secrets Management
```bash
# Never hardcode secrets
❌ API_KEY = "abc123"

# Use environment variables
✅ API_KEY = os.getenv("GENIUS_API_KEY")

# Use proper secret management
✅ vault.get_secret("genius/api_key")
```

### Performance Standards

#### Database Queries
```python
# Use proper indexing hints
SELECT /*+ INDEX(users, idx_users_email) */ 
FROM users 
WHERE email = %s;

# Limit result sets
SELECT * FROM users LIMIT 100 OFFSET 0;

# Use appropriate joins
SELECT u.name, r.role_name 
FROM users u 
JOIN user_roles r ON u.id = r.user_id;
```

#### Caching Patterns
```python
# Cache key naming: {service}:{resource}:{identifier}
cache_key = f"users:profile:{user_id}"
redis.setex(cache_key, 3600, user_data)  # 1 hour TTL
```

### Internationalization

#### Message Keys
```typescript
// Message key naming: {module}.{context}.{specific}
'users.validation.email_required'
'auth.login.invalid_credentials'
'anaf.integration.connection_failed'
```

#### Date/Time Formatting
```python
# Always use UTC for storage
from datetime import datetime, timezone
timestamp = datetime.now(timezone.utc)

# Format according to ISO 8601
iso_format = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
```

### Monitoring and Logging

#### Log Message Format
```json
{
  "timestamp": "2025-08-29T10:00:23Z",
  "level": "INFO",
  "service": "user-service",
  "tenant_id": "tenant_123",
  "user_id": "user_456",
  "message": "User profile updated successfully",
  "trace_id": "trace_xyz789",
  "span_id": "span_abc123"
}
```

#### Metric Naming
```prometheus
# Format: {service}_{metric_type}_{unit}
genius_api_requests_total
genius_db_connections_active
genius_worker_processing_duration_seconds
```

### Language and Communication

#### Primary Language
**Romanian** - All user-facing content, documentation, and communication must be in Romanian as specified in project requirements.

#### Technical Documentation
- Code comments: English (for international developer collaboration)
- API documentation: English (for technical integration)
- User documentation: Romanian (for end-user consumption)
- Business documentation: Romanian (for stakeholder communication)

These style guidelines ensure consistency across the entire GeniusERP Suite project, facilitating collaboration, maintenance, and scalability.
