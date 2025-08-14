# Roadmap General – GeniusERP Suite

> **Scop** – ghid cronologic & logic pentru a implementa întreaga suită (aplicația‑mamă *Genius Shell* + 13 aplicații stand‑alone). Detaliile de execuție fină vor fi elaborate în roadmap‑urile individuale (`roadmap/<module>.md`).

---

## Legenda

- **✔︎** livrat · **⚙︎** în lucru · **○** planificat
- Timp estimat ⇒ săptămâni lucrătoare (SW), asumând echipă core 6 dev FE, 4 dev BE, 4 data/ML, 3 SRE, 2 DevOps.

---

## Phase 0 · Foundation & Infra ( 6 SW ) — _Q3 2025_
| Pas | Durată | Output cheie | Modul(e) | Status |
|-----|-------|--------------|----------|--------|
| 0‑1 | 1 SW | Repo Nx 18 + `init.sh` + `manage-app.sh` | n/a | ✔︎ |
| 0‑2 | 1 SW | Terraform VPC + k8s (dev, stage, prod) | infra | ✔︎ |
| 0‑3 | 1 SW | Traefik v3 ingress, Keycloak 23 realm‑template **(PoC; înlocuit definitiv la step 34 F0)** | shell‑gateway | ✔︎ |
| 0‑4 | 2 SW | Observability stack (Prom 2.50, Loki 3, Tempo 2, Grafana 10) | infra | ⚙︎ |
| 0‑5 | 1 SW | CI template GitHub Actions (build/test/scan/sign/publish) | ci‑templates | ⚙︎ |

---

## Phase 1 · Core Platform ( 8 SW ) — _Q3 → Q4 2025_
| Pas | Durată | Output cheie | Modul(e) | Dependințe |
|-----|-------|--------------|----------|------------|
| 1‑1 | 2 SW | Genius Shell UI scaffold + remote loader | shell‑gateway, packages/ui | 0‑* |
| 1‑2 | 2 SW  | Admin Core (Setări + RBAC Directory + Theme Hub) v0.9 | admin‑core | 1‑1 |
| 1‑3 | 1 SW  | Worker Registry API & health cron | admin‑core | 1‑2 |
| 1‑4 | 1 SW  | Event Bus RMQ namespaces & conventions v1 | infra | 0‑3 |
| 1‑5 | 2 SW  | Base Workers (`ocr`, `email.send`, `pdf.render`) + Celery queues | workers‑core | 1‑3 |

**Roadmap individual lansat:**

- `roadmap/shell.md`
- `roadmap/admin-core.md`

---

## Phase 2 · Commercial Core Apps ( 12 SW ) — _Q4 2025 → Q1 2026_
| Pas | Durată | Output cheie | Modul(e) | Dependințe |
|-----|-------|--------------|----------|------------|
| 2‑1 | 4 SW  | **vettify.app** (CRM + Marketing Suite) – MVP remote‑frontend, NestJS API, workers `ai.summary`, `ai.churn` | vettify | 1‑* |
| 2‑2 | 3 SW  | **Mercantiq Sales & Billing** – POS, Invoice, e‑Factură ANAF | mercantiq‑sales | 2‑1 |
| 2‑3 | 2 SW  | **Mercantiq Procurement** – RFQ → PO → GRN | mercantiq‑procurement | 2‑2 |
| 2‑4 | 3 SW  | **iWMS v3.0** – multi‑warehouse, mobile, worker `forecast` | iwms | 2‑2 |

**Roadmaps individuale:** `roadmap/vettify.md`, `roadmap/mercantiq.md`, `roadmap/iwms.md`

---

## Phase 3 · Operational & Financial Backbone ( 10 SW ) — _Q1 → Q2 2026_
| Pas | Durată | Output cheie | Modul | Dependințe |
|-----|-------|--------------|-------|------------|
| 3‑1 | 4 SW  | **Numeriqo Manufacturing** – BOM, MRP II beta | numeriqo‑manufacturing | 2‑4 |
| 3‑2 | 3 SW  | **Numeriqo Accounting** – Plan Conturi RO, balanțe, SAF‑T | numeriqo‑accounting | 3‑1 |
| 3‑3 | 3 SW  | **Numeriqo People & Payroll** – motor salarizare RO | numeriqo‑people | 3‑2 |

**Roadmaps:** `roadmap/numeriqo-manufacturing.md`, `roadmap/numeriqo-accounting.md`, `roadmap/numeriqo-people.md`

---

## Phase 4 · Collaboration & Automation ( 6 SW ) — _Q2 2026_
| Pas | Durată | Output cheie | Modul | Dependințe |
|-----|-------|--------------|-------|------------|
| 4‑1 | 3 SW  | **triggerra Collaboration Hub** – Kanban, chat, OKR | triggerra‑collab | 2‑1 |
| 4‑2 | 3 SW  | **triggerra Automation Studio** – flow‑builder, runtime sandbox | triggerra‑automation | 4‑1 |

**Roadmaps:** `roadmap/triggerra-collab.md`, `roadmap/triggerra-automation.md`

---

## Phase 5 · Knowledge & Analytics ( 6 SW ) — _Q3 2026_
| Pas | Durată | Output cheie | Modul | Dependințe |
|-----|-------|--------------|-------|------------|
| 5‑1 | 2 SW  | **Archify.app** – DMS + e‑Sign calificat v1 | archify | 2‑4 |
| 5‑2 | 4 SW  | **cerniq.app** – Cognitive BI (AI2BI, AI4BI, Lakehouse) | cerniq | 3‑2, 5‑1 |

**Roadmaps:** `roadmap/archify.md`, `roadmap/cerniq.md`

---

## Phase 6 · Hardening & Multi‑Cloud ( 4 SW ) — _Q4 2026_
| Pas | Durată | Output | Dependințe |
|-----|-------|--------|------------|
| 6‑1 | 2 SW  | Multi‑cloud DR (AKS ↔ EKS) pilot, RTO 15 min | infra | all core |
| 6‑2 | 1 SW  | ISO 27001 external audit – stage 2 | security | 6‑1 |
| 6‑3 | 1 SW  | Mobile React Native suite (offline parity) | shell‑mobile, iwms‑mobile, mercantiq‑mobile | 2‑4 |

---

## Phase 7 · Continuous Improvement (2027+)

- AI Config Advisor, AI Vision GA, Edge IoT Gateway GA, Marketplace de template‑uri Automation Studio, GDPR Portal GA.

Roadmaps viitoare vor fi adăugate sub `roadmap/`:

- `roadmap/ai-config-advisor.md`
- `roadmap/iot-gateway.md`
- `roadmap/gdpr-portal.md`

---

## Milestones & Gates
| Milestone | Fază | Criteriu de trecere |
| --------- | ---- | ------------------- |
| **M0** – Infra Ready | Phase 0 | CI verde, Observability online, Gateway TLS OK |
| **M1** – Shell GA    | Phase 1 | 3 module active, SLO gateway ≥ 99.9 % |
| **M2** – Commercial Core | Phase 2 | Vânzări + CRM + WMS live, Order‑to‑Cash E2E demo |
| **M3** – Financial Close | Phase 3 | Balanță lunară și SAF‑T generate din numeriqo |
| **M4** – Collab & Automation | Phase 4 | > 500 workflow‑uri active în Automation Studio |
| **M5** – BI Launch | Phase 5 | AI2BI query < 1 s, 10 dashboards active |
| **M6** – DR Certified | Phase 6 | Drill failover ≤ 15 min, no data loss |

---

## KPI Umbrelă Proiect
* **Time‑to‑Market** (Q3‑2025 → M1) ≤ 4 luni
* **Team deployment frequency**: ≥ 2 releases/săpt/app
* **Mean Time to Restore (MTTR)** ≤ 30 min (prod)
* **Error Budget Burn** < 5 % pe lună (la nivel suite)

---

## Next Steps
1. Validare roadmap cu stakeholders (product, finance, ops).
2. Detaliere backlog Phase 0 + Phase 1 în Jira.
3. Creare sub‑roadmap‑uri în directorul `roadmap/` conform tabelului.
4. Kick‑off Phase 0 – **14 Aug 2025**.

> _Pentru clarificări suplimentare, consultați `0_Instructiuni_stricte_de_proiectare.md` și ambele README‑uri._

