# Roadmap F5 · Knowledge & Analytics

> **Scop:** să implementăm modulele de knowledge management și business intelligence **Archify DMS** și **Cerniq Cognitive BI** pentru o platformă ERP completă cu capabilities avansate de analiză.

> **Timeline:** Q3 2026 (6 SW total)

---

## Gate F4 → F5

**Pre-condiții obligatorii pentru începerea F5:**
- **F4 Collaboration & Automation completă:** Triggerra Hub + Studio operaționale
- **Event-Bus v1** cu evenimente comprehensive din toate modulele F1-F4
- **Worker Fleet** complet cu AI workers avansați
- **Data Accumulation:** Suficiente date business în sistem pentru analytics

---

## F5 Modules Overview

| Modul | Durată | Obiectiv | Dependințe |
|-------|--------|----------|-------------|
| **Archify DMS** | 2 SW | Document Management + e-Sign calificat | F2-4 iWMS |
| **Cerniq Cognitive BI** | 4 SW | AI-powered BI, Lakehouse, AI2BI queries | F3-2 Accounting + F5-1 Archify |

---

## Architecture Overview

**F5-1 Archify DMS:**
- Document lifecycle management
- Qualified e-signature integration
- OCR și content analysis
- Integration cu toate modulele pentru document workflow

**F5-2 Cerniq Cognitive BI:**
- Delta-Parquet Lakehouse pentru comprehensive data analytics
- AI-powered query generation (AI2BI)
- Cognitive dashboards cu ML insights
- Data consumption din TOATE modulele suite

---

## Gate F5 → F6

**Criteriile de trecere:**
- DMS operațional cu 1000+ documente procesate
- e-Sign calificat funcțional cu certificate management
- Dashboard Cerniq consumă date din TOATE modulele suite
- AI2BI query response time < 1s
- 10+ dashboards active cu insights actionable

---

## Roadmaps Derivate

- `20_roadmap_f_5_1_archify_dms.md`
- `21_roadmap_f_5_2_cerniq_cognitive_bi.md`

> Pentru detaliile de implementare, consultați roadmap-urile individuale ale fiecărui modul.
