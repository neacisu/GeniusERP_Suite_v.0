# Roadmap General – GeniusERP Suite

> **Ghid ierarhic și cronologic** pentru implementarea aplicației-mamă **Genius Shell** împreună cu toate cele 13 aplicații stand-alone. Nu conține estimări calendaristice – doar ordinea logică de execuție.

---

## Structura pe faze

| Fază   | Obiectiv principal                   | Conținut                                                                             | Roadmap-uri derivate                                                                                  |
|--------|--------------------------------------|--------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| **F0** | *Foundation & Infrastructure*        | Repo Nx, CI template, Kubernetes & Traefik, Observability Stack, Gateway & Auth    | —                                                                                                     |
| **F1** | *Core Platform*                      | Genius Shell UI, Admin Core (Setări & RBAC), Worker Registry API, Base Workers     | `roadmap/shell.md`, `roadmap/admin-core.md`                                                          |
| **F2** | *Commercial Core Apps*               | Vettify (CRM+Marketing), Mercantiq Sales & Billing, Mercantiq Procurement, iWMS v3 | `roadmap/vettify.md`, `roadmap/mercantiq.md`, `roadmap/iwms.md`                                      |
| **F3** | *Operational & Financial Backbone*   | Numeriqo Manufacturing, Accounting (RO GAAP), People & Payroll                     | `roadmap/numeriqo-manufacturing.md`, `roadmap/numeriqo-accounting.md`, `roadmap/numeriqo-people.md`  |
| **F4** | *Collaboration & Automation*         | Triggerra Collaboration Hub, Triggerra Automation Studio                           | `roadmap/triggerra-collab.md`, `roadmap/triggerra-automation.md`                                     |
| **F5** | *Knowledge & Analytics*              | Archify (DMS + e-Sign), Cerniq (Cognitive BI)                                      | `roadmap/archify.md`, `roadmap/cerniq.md`                                                            |
| **F6** | *Hardening & Multi-Cloud*            | Multi-cloud DR, ISO 27001 audit, Mobile React Native Suite                         | `roadmap/dr.md`, `roadmap/mobile-suite.md`, `roadmap/iso27001.md`                                    |
| **F7** | *Continuous Improvement*             | AI Config Advisor, AI Vision GA, Edge IoT Gateway, GDPR Portal                     | roadmap-uri viitoare                                                                                 |

> Începerea unei faze este permisă **doar după îndeplinirea livrabilelor fazei anterioare**.

---

## F0 · Foundation & Infrastructure

1. **Repo Bootstrap**
   - Rulează `init.sh`
   - Generează workspace Nx
   - Configurează pnpm, poetry, pre-commit

2. **Cloud Infra** 
   - Terraform: VPC, k8s (dev, stage, prod)
   - Storage Class

3. **Gateway & Auth**
   - Traefik v3
   - Keycloak 23
   - TLS/mTLS, rate-limit

4. **Observability Stack**
   - Prometheus, Loki, Tempo
   - Grafana dashboards provisionate

5. **CI Template**
   - GitHub Actions
   - Nx affected, Trivy
   - Cosign signing, publish OCI

> **Gate F0 → F1**: CI verde, Gateway servește `/health`, Grafana panourile up.

---

## F1 · Core Platform

1. **Genius Shell UI scaffold**
   - Remote-loader
   - Layout, theme tokens

2. **Admin Core v0.9**
   - Setări
   - RBAC Directory
   - Theme Hub

3. **Worker Registry API**
   - Health endpoints
   - Redis status

4. **Event-Bus Conventions**
   - RMQ namespaces
   - Contract-tests

5. **Base Workers**
   - `ocr`
   - `pdf.render`
   - `email.send`

> **Gate F1 → F2**: Shell afișează 3 widget-uri demo, Worker Registry verde.

---

## F2 · Commercial Core Apps

1. **Vettify CRM & Marketing**
   - Micro-frontend, API
   - Workeri AI (`ai.summary`, `ai.churn`)

2. **Mercantiq Sales & Billing**
   - POS, Invoice
   - e-Factură
   - Events `sales.*`

3. **Mercantiq Procurement**
   - RFQ → PO → GRN
   - Events `procurement.*`

4. **iWMS v3**
   - Multi-warehouse
   - Mobile RF
   - Workers `forecast`, `match.ai`

> **Gate F2 → F3**: Flux „Order-to-Cash" și „Procure-to-Pay" demonstrat end-to-end.

---

## F3 · Operational & Financial Backbone

1. **Numeriqo Manufacturing**
   - BOM, MRP II
   - Shop-floor terminals

2. **Numeriqo Accounting (RO GAAP)**
   - Partidă dublă
   - SAF-T, balanțe

3. **Numeriqo People & Payroll**
   - Salarii RO
   - Revisal, time-off

> **Gate F3 → F4**: contabilitate generează balanță din tranzacții Mercantiq; payroll postează jurnal în Accounting.

---

## F4 · Collaboration & Automation

1. **Triggerra Collaboration Hub**
   - Kanban, chat
   - OKR alignment

2. **Triggerra Automation Studio**
   - Flow builder low-code
   - Runtime sandbox

> **Gate F4 → F5**: cel puțin 100 workflow-uri active și 10 board-uri Kanban live.

---

## F5 · Knowledge & Analytics

1. **Archify**
   - DMS, OCR
   - e-Sign
   - Retention policies

2. **Cerniq**
   - Cognitive BI
   - AI2BI, AI4BI
   - Lakehouse Delta-Parquet

> **Gate F5 → F6**: Dashboard Cerniq consumă date din toate modulele, e-Sign calificat funcțional.

---

## F6 · Hardening & Multi‑Cloud

1. **Disaster Recovery Multi-Cloud**
   - AKS ↔ EKS
   - Failover drill

2. **ISO 27001 External Audit**
   - Stage 2
   - 0 non-conformități majore

3. **Mobile React Native Suite**
   - Offline parity cu Shell & iWMS

> **Gate F6 → F7**: Failover ≤ 15 min, audit trecut, mobile‑suite disponibil în store intern.

---

## F7 · Continuous Improvement (rolling)

- **AI Vision GA**
  - Clasificare imagini în producție
  - Defect heat-map

- **Edge IoT Gateway GA**
  - MQTT buffering
  - Sync offline

- **AI Config Advisor**
  - GPT-4o recomandă tuning SLO

- **GDPR Data Subject Portal**
  - Export/erase self-service

- **Marketplace Automation Templates**
  - Fluxuri pregătite community

---

## Milestone-uri principale

| Cod    | Definiție               | Criteriu de trecere                                           |
|--------|-------------------------|---------------------------------------------------------------|
| **M0** | ✔ Infra Ready          | Gateway & Observability online, CI verde                     |
| **M1** | ✔ Shell GA             | Shell + Admin + Workers de bază live                         |
| **M2** | ✔ Commercial Core      | Vânzări + CRM + WMS funcționează cross-module                |
| **M3** | ✔ Financial Backbone   | Accounting & Payroll primesc evenimente și publică rapoarte  |
| **M4** | ✔ Collab & Automation  | 100+ workflow-uri în producție, board-uri Kanban active      |
| **M5** | ✔ BI Launch            | Cerniq dashboards real-time, forecast AI live                |
| **M6** | ✔ DR Certified         | Failover multi-cloud reușit fără downtime perceptibil        |

---

## KPI Umbrelă Proiect (fără dată)

- **Deployment frequency** ≥ 2 release‑uri / săptămână / modul
- **Mean Time to Restore (MTTR)** ≤ 30 min
- **Error Budget Burn global** < 5 % / lună
- **Adopție Shell** – ≥ 90 % utilizatori activi în suite

---

## 11 · Infrastructura de Conformitate Fiscală & HR Națională

Pentru a asigura respectarea cerințelor legale fiscale și de HR, GeniusERP include o **flotă de workeri comuni** integrați cu platformele naționale ANAF și Inspecția Muncii. Acești workeri sunt microservicii Python reutilizabile de toate modulele relevante, oferind un punct unic de conectare la sistemele guvernamentale (evitând duplicarea logicii în fiecare aplicație). Fiecare worker expune contracte JSON bine definite (schema de intrare/ieșire) și operează prin topic-uri RabbitMQ canonice (`anaf.*`, `reges`), similar celorlalți workeri din suită.

- **anaf.taxpayer** – interogare și validare *CUI* (cod fiscal) prin serviciul web ANAF. La cerere, returnează date oficiale despre contribuabil (denumire, stare TVA etc.), inclusiv verificarea validității și a înregistrării în registrul RO e-Factura. *(Ex: utilizat în Vettify la adăugarea clienților/prospects, în Mercantiq la facturare/POS/achiziții/furnizori/avize/chitanțe/încasări/bancă, și în Numeriqo Accounting pentru parteneri contabili.)*

- **anaf.efactura** – preluare, semnare și transmitere *e-Factură* (factură electronică XML conform standardului național) către sistemul ANAF. Worker-ul primește datele facturii (sau XML-ul generat de modulul de vânzări), aplică semnătura electronică unde e cazul și folosește autentificare pe portalul ANAF (OAuth2/token sau certificat digital) pentru a depune factura. Rezultatele (ex: identificatorul GUID al facturii sau erori de validare) sunt trimise înapoi modulului solicitant.

- **anaf.etransport** – generare și transmitere declarații *e-Transport* pentru bunurile cu risc fiscal ridicat. Acest worker compilează datele de transport (expeditor, destinatar, categorii de bunuri, cantități) conform schema ANAF, și le transmite către RO e-Transport folosind certificatul digital al companiei. În urma depunerii, primește codul UIT unic (și documentul PDF cu QR) pe care îl pune la dispoziția modulului logistic (ex: iWMS) pentru conformitate în timpul transportului.

- **anaf.saft** – colectare date contabile și generare fișier *SAF-T D406* conform specificațiilor ANAF. Worker-ul extrage din baza de date contabilă tranzacțiile, conturile și registrele cerute, construiește fișierul XML SAF-T și îl **validează oficial** prin kit-ul ANAF **DUKIntegrator** (inclus în container). Fișierul rezultat (XML + PDF aferent) este returnat gata de depunere, asigurându-se că respectă schema și regulile de validare ANAF. Autentificarea și semnarea electronică pentru depunerea efectivă (dacă se face automat) se realizează tot prin certificate digitale, gestionate securizat.

- **reges** – transmitere automată a registrului de evidență a salariaților (*REGES Online*). Worker-ul primește evenimente din modulul HR (angajare nouă, modificare contract, încetare) și apelează API-ul Inspecției Muncii pentru a trimite datele actualizate în registrul online oficial (în formatul impus, ex. XML conform XSD Revisal). Integrarea folosește protocolul oficial (ex: SOAP Web Service via **zeep**) și certificatul digital calificat al angajatorului pentru autentificare. Rezultatele (confirmarea înregistrării sau erori) sunt captate și pot declanșa notificări în platformă.

Fiecare dintre workeri operează asincron (prin cozi RMQ dedicate) și propagă evenimente de răspuns (exemple: `tax.vat.validated`, `sales.invoice.efactura_sent`, `wms.shipment.etransport_code` sau `accounting.saft.ready`) consumate de modulele de business. Toate credențialele sensibile (token-uri OAuth, certificate PKI, chei API) nu sunt hardcodate, ci sunt gestionate prin **External Secrets** (ex. stocate în HashiCorp Vault și montate la runtime în workeri). De asemenea, workeri precum cei ANAF utilizează validatori oficiali (ex. librăria DUK/Validator ANAF pentru SAF-T și e-Factura) pentru consistență maximă cu cerințele autorităților. 

Acești workeri comuni apar în **Worker Registry** (Admin Core) alături de ceilalți workeri, expunând endpoint-urile de health/status și metricile de performanță. Astfel, platforma GeniusERP este pregătită încă din fazele de bază să gestioneze obligațiile de raportare către autorități (ANAF, Inspecția Muncii) într-un mod unitar și automatizat, oricare ar fi modulul de business care generează acele date.

---

## Următorii pași

1. **Validare roadmap** cu stakeholder-ii principali
2. **Creare backlog** F0 + F1 în Jira, etichetat `scope:foundation`
3. **Generare roadmap-uri** individuale în directorul `roadmap/`
4. **Kick-off F0** → trecere la execuție

> Pentru reguli stricte de proiectare consultați `0_Instructiuni_stricte_de_proiectare.md`.

