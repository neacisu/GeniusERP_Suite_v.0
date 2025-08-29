# Roadmap F3 · Operational & Financial Backbone

> **Scop:** să implementăm backbone-ul operațional și financiar al suitei GeniusERP cu modulele **Numeriqo Manufacturing**, **Numeriqo Accounting** și **Numeriqo People & Payroll** pentru o platformă ERP completă.

> **Timeline:** Q1 → Q2 2026 (10 SW total)

---

## Gate F2 → F3

**Pre-condiții obligatorii pentru începerea F3:**
- **F2 Commercial Core completă:** Vettify, Mercantiq (Sales + Procurement), iWMS v3 operaționale
- **Event-Bus v1** funcțional cu toate événementele F2
- **Worker Fleet** disponibil și integrat cu modulele F2
- **Multi-tenancy & Database:** PostgreSQL 17 cluster per tenant funcțional cu RLS

---

## F3 Modules Overview

| Modul | Durată | Obiectiv | Dependințe |
|-------|--------|----------|-------------|
| **Numeriqo Manufacturing** | 4 SW | BOM, MRP II beta, Work Orders | F2-4 iWMS |
| **Numeriqo Accounting** | 3 SW | Plan Conturi RO, Balanțe, SAF-T | F3-1 Manufacturing |
| **Numeriqo People & Payroll** | 3 SW | Motor salarizare RO, REGES | F3-2 Accounting |

---

## Gate F3 → F4

**Criteriile de trecere:**
- Balanță lunară și SAF-T generate din Numeriqo Accounting
- Payroll RO funcțional cu integrarea REGES
- Manufacturing MRP II beta operațional
- Integrare completă cu modulele F2 prin Event-Bus

---

## Roadmaps Derivate

- `14_roadmap_f_3_1_numeriqo_manufacturing.md`
- `15_roadmap_f_3_2_numeriqo_accounting.md`
- `16_roadmap_f_3_3_numeriqo_people_payroll.md`

> Pentru detaliile de implementare, consultați roadmap-urile individuale ale fiecărui modul.
