# CLAUDE.md - GeniusERP Suite v0.1

> Think carefully and implement the most concise solution that changes as little code as possible.

## Project Overview

**GeniusERP Suite v0.1** este o suită complexă de aplicații enterprise care urmează un roadmap structurat pe faze (F0-F7):

- **F0**: Foundation & Infrastructure - Kubernetes, Traefik, Observability
- **F1**: Core Platform - Genius Shell UI, Admin Core, Worker Registry
- **F2**: Commercial Core Apps - Vettify CRM, Mercantiq Sales/Billing/Procurement, iWMS v3
- **F3-F7**: Module avansate pentru Manufacturing, Accounting, Collaboration, etc.

## Repository Information

- **Repository**: https://github.com/neacisu/GeniusERP_Suite_v.0.git
- **Main Branch**: main
- **Workspace**: /var/www/GeniusERP_Suite_v0_1
- **Owner**: neacisu

## Project-Specific Instructions

### Stack Tehnologic
- **Python**: întotdeauna folosește `python3` (nu python)
- **Credențiale Test**: 
  - Email: `test_admin@iwms.com`
  - Parolă: `Test123456`
- **Database**: 
  - User: `gestiune_user`
  - Password: `gestiune_pass`
  - DB: `gestiune_marfa`
  - Port: `5433` (PostgreSQL)

### Management Aplicație
Controlează aplicația cu: `sudo -u dev ./manage-app.sh`

### Structura Porturi (Aplicația NEANELU)
- Frontend (React/Vite): port `5000`
- Backend (FastAPI): port `5001`
- PostgreSQL: port `5002`

### Configurări Importante
- **Proxy Config**: În `vite.config.ts`, folosește proxy-uri specifice (ex: `'^/produse/(?!$)'`) pentru a evita conflictele cu rutele SPA React Router
- **Tree Command**: Folosește `tree` pentru structura directoarelor cu exclude: `tree /path -I 'node_modules|venv|__pycache__|*.log|.git|dist' -L 3`

## Testing

Întotdeauna rulează teste înainte de commit:
- Pentru Python: `python3 -m pytest`
- Pentru Node.js: `npm test`
- Pentru aplicațiile principale: folosește `./manage-app.sh test`

## Code Style

- Urmează pattern-urile existente în codebase
- Folosește documentația din `/Documentation/` pentru instrucțiuni specifice
- Respectă convenția de naming pentru module și componente
- Păstrează consistența cu roadmap-urile definite

## Workflow Management

Acest proiect folosește acum **CCPM (Claude Code PM)** pentru:
- Crearea și gestionarea PRD-urilor
- Planificarea epic-urilor și task-urilor
- Execuția paralelă cu mai mulți agenți
- Sincronizarea cu GitHub Issues
- Trasabilitate completă de la idee la producție

### Comenzi Principale CCPM
- `/pm:prd-new <feature>` - Creează un PRD nou
- `/pm:epic-start <name>` - Începe lucrul la un epic
- `/pm:issue-start <id>` - Lucrează la un issue specific
- `/pm:status` - Vezi statusul general al proiectului
- `/pm:help` - Lista completă de comenzi

## Language

**Întotdeauna răspunde în română** conform preferințelor utilizatorului.
