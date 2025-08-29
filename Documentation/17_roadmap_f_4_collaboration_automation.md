# Roadmap F4 · Collaboration & Automation

> **Scop:** să implementăm modulele de colaborare și automatizare **Triggerra Collaboration Hub** și **Triggerra Automation Studio** pentru workflow management și low-code development în suita GeniusERP.

> **Timeline:** Q2 2026 (6 SW total)

---

## Gate F3 → F4

**Pre-condiții obligatorii pentru începerea F4:**
- **F3 Operational & Financial completă:** Manufacturing, Accounting, People & Payroll operaționale
- **Event-Bus v1** funcțional cu evenimente din toate modulele F1-F3
- **Worker Fleet** extins cu workerii business-critical
- **Multi-tenancy & Database:** Schema consolidate pentru toate modulele

---

## F4 Modules Overview

| Modul | Durată | Obiectiv | Dependințe |
|-------|--------|----------|-------------|
| **Triggerra Collaboration Hub** | 3 SW | Kanban, Chat, OKR management | F2-1 Vettify |
| **Triggerra Automation Studio** | 3 SW | Flow-builder, Runtime sandbox | F4-1 Collab Hub |

---

## Architecture Overview

- **Collaboration Hub:** Real-time collaboration tools cu integrare în ecosistemul ERP
- **Automation Studio:** Low-code platform pentru business process automation
- **Event Integration:** Consume și publică evenimente din/către toate modulele
- **Worker Integration:** Utilizează fleet-ul complet de workeri pentru automatizări

---

## Gate F4 → F5

**Criteriile de trecere:**
- Cel puțin 100 workflow-uri active în Automation Studio
- Demonstrare E2E automation pentru Manufacturing→Accounting→HR
- 10+ Kanban boards active în Collaboration Hub
- Integrare completă cu toate modulele existente

---

## Roadmaps Derivate

- `18_roadmap_f_4_1_triggerra_collaboration_hub.md`
- `19_roadmap_f_4_2_triggerra_automation_studio.md`

> Pentru detaliile de implementare, consultați roadmap-urile individuale ale fiecărui modul.
