---
created: 2025-08-29T10:00:23Z
last_updated: 2025-08-29T10:00:23Z
version: 1.0
author: Claude Code PM System
---

# Project Structure

## Directory Organization

**Root Directory**: `/var/www/GeniusERP_Suite_v0_1`

### Core Structure

```
GeniusERP_Suite_v0_1/
├── .claude/                    # CCPM System Files
│   ├── agents/                 # Agent definitions
│   ├── commands/               # PM command definitions
│   │   ├── context/            # Context management commands
│   │   ├── pm/                 # Project management commands
│   │   └── testing/            # Testing commands
│   ├── context/               # Project context documentation
│   ├── epics/                 # Epic documentation (empty, for future use)
│   ├── prds/                  # PRD documentation (empty, for future use)
│   ├── rules/                 # System behavior rules
│   ├── scripts/               # Automation scripts
│   ├── CLAUDE.md              # Core system configuration
│   └── settings.local.json    # Local settings
├── Documentation/             # Project Documentation
│   ├── 0_instructiuni_stricte_de_proiectare.md
│   ├── 1_roadmap_general_suita_genius_erp.md
│   ├── 2_roadmap_f_0_foundation_infrastructure.md
│   ├── 3_roadmap_f_1_Core_Platform.md
│   ├── 4_roadmap_shell_gateway.md
│   ├── 5_roadmap_admin_core.md
│   ├── 6_roadmap_base_workers.md
│   ├── 7_roadmap_f_2_Commercial_Core_Apps.md
│   ├── 8_roadmap_vettify.md
│   ├── 9_roadmap_mercantiq_sales_billing.md
│   ├── 10_roadmap_mercantiq_procurement.md
│   ├── 11_roadmap_iwms_v3.md
│   └── readme_genius_erp_suite.md
├── scripts/                   # Project automation scripts
├── AGENTS.md                  # CCPM agents documentation
├── CLAUDE.md                  # Project-specific Claude instructions
└── COMMANDS.md                # CCPM commands reference
```

### Key Directories

#### `.claude/` - CCPM System
- **Purpose**: Claude Code Project Management system files
- **Contents**: Commands, agents, rules, context, and automation
- **Usage**: Manages project workflow, PRDs, epics, and parallel agent execution

#### `Documentation/` - Project Specification
- **Purpose**: Comprehensive project documentation and roadmaps
- **Organization**: Numbered roadmap files for different phases and modules
- **Key Files**:
  - `0_instructiuni_stricte_de_proiectare.md` - Strict design instructions
  - `1_roadmap_general_suita_genius_erp.md` - General roadmap overview
  - `readme_genius_erp_suite.md` - Extended project documentation

#### `scripts/` - Automation
- **Purpose**: Project-specific automation and utility scripts
- **Usage**: Deployment, testing, and maintenance automation

### File Naming Patterns

#### Documentation Files
- **Format**: `{number}_{category}_{specific_name}.md`
- **Examples**: 
  - `0_instructiuni_stricte_de_proiectare.md`
  - `2_roadmap_f_0_foundation_infrastructure.md`
  - `7_roadmap_f_2_Commercial_Core_Apps.md`

#### CCPM Files
- **Commands**: Located in `.claude/commands/{category}/{command}.md`
- **Context**: Located in `.claude/context/{context_type}.md`
- **Rules**: Located in `.claude/rules/{rule_name}.md`

### Module Organization

The project follows a phase-based structure:

#### Phase Structure
- **F0**: Foundation & Infrastructure
- **F1**: Core Platform
- **F2**: Commercial Core Apps
- **F3-F7**: Advanced modules (Manufacturing, Accounting, etc.)

#### Documentation Mapping
- Each phase has dedicated roadmap files
- Module-specific documentation in numbered sequence
- Cross-references between related modules

### Development Workspace

#### Working Directories
- **Development**: `/var/www/GeniusERP_Suite_v0_1` (current)
- **Git Repository**: Tracked with GitHub
- **CCPM Integration**: Seamless with `.claude/` directory

#### File Management
- **Version Control**: Git-based with GitHub integration
- **Documentation**: Markdown-based with clear hierarchy
- **Project Management**: CCPM-based with issue tracking

### Integration Points

#### CCPM Integration
- **PRDs**: Will be stored in `.claude/prds/`
- **Epics**: Will be stored in `.claude/epics/`
- **Context**: Active project context in `.claude/context/`

#### GitHub Integration
- **Issues**: Synced through CCPM system
- **Projects**: Managed through GitHub Issues
- **Workflow**: CCPM commands interact directly with GitHub

### Access Patterns

#### Documentation Access
- Sequential reading of roadmap files (0-11)
- Cross-reference between phases
- Central readme for overview

#### Development Access
- CCPM commands for project management
- Scripts for automation
- Context files for session continuity

### Future Growth

#### Scalability Considerations
- Modular structure supports new phases
- CCPM system handles parallel development
- Clear separation between documentation and active development

#### Extension Points
- Additional roadmap files can be added
- New modules follow existing naming patterns
- CCPM system grows with project complexity
