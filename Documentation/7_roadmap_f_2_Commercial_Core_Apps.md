### 7 · Roadmap F2 – Commercial Core Apps (CRM, Sales/Billing, Procurement, iWMS)

Scop: coordonează implementarea fazei F2 sub forma unei umbrele peste 4 aplicații: Vettify (CRM+Marketing), Mercantiq Sales & Billing, Mercantiq Procurement, iWMS v3. Faza se pornește doar după trecerea Gate‑ului F1 (Shell vizibil + Admin Core + Base Workers). Criteriul de ieșire din F2 este demonstrarea E2E a fluxurilor Order‑to‑Cash și Procure‑to‑Pay.

### 1) Pre‑condiții & Scope

- Gate F1 trecut: Shell cu 3 widget‑uri demo + Worker Registry verde.
- Event‑Bus v1 disponibil (naming `<module>.<ctx>.<event>` + tags de worker), SDK‑uri TS/Py publicate, contract‑tests. (vezi F1 step 264 „bus-spec”).
- Multitenancy & date: PostgreSQL 17 (cluster per tenant, schema per modul), MinIO per tenant, Redis per tenant, RLS pe `tid/whid/mid`.
- Workers disponibili din flotă: `ai.summary`, `ai.churn`, `tax.vat`, `anaf.taxpayer`, `anaf.efactura`, `anaf.etransport`, `anaf.saft`, `reges`, `forecast`, `match.ai`, `pdf.render`, `ocr`, `email.send` (ș.a.).  
- *Notă:* Au fost integrați workeri comuni pentru conformitate națională – **ANAF** (`anaf.taxpayer` pentru validare CUI, `anaf.efactura` pentru e-Factura, `anaf.etransport` pentru declarații transport, `anaf.saft` pentru SAF-T) și **REGES** (`reges` pentru Revisal online). Mercantiq Sales & Billing folosește deja `anaf.taxpayer` și `anaf.efactura` în F2 (validare automată client și transmitere e-Facturi), iar modulele **Numeriqo** Accounting și People le vor consuma pe `anaf.saft` și `reges` în faza F3 (pentru raportările contabile și de personal obligatorii).
- Stack fix (obligatoriu): React 19 + Vite5 Federation + MUI6 + Tailwind3 (UI), NestJS 11 (API), Python 3.13 Celery/Ray (workeri), RabbitMQ 3.14 + Redis 7 (bus/queue), Terraform + Helmfile + Argo CD (deploy).

### 2) Bounded‑Contexts & interfețe

| App (standalone) | Bounded context   | Principale entități                                                                 | Evenimente cheie (publish)                                                                   | Consumă                                                             |
| --- | --- | --- | --- | --- |
| Vettify | CRM & Marketing | lead, account, contact, opportunity, campaign                                        | `crm.lead.created`, `crm.opportunity.stage_changed`, `crm.campaign.sent`                    | `sales.order.created` (enrichment), `wms.shipment.delivered`         |
| Mercantiq Sales | Sales & Billing | customer, product, price_list, sales_order, invoice, payment                           | `sales.order.created`, `sales.invoice.issued`, `payment.received`                           | `wms.picklist.completed`, `tax.vat.validated`, `pdf.render.done`     |
| Mercantiq Procurement | Procure | supplier, rfq, quote, purchase_order, grn, three_way_match                                 | `procurement.rfq.created`, `procurement.po.approved`, `procurement.grn.posted`, `procurement.3wm.flagged` | `wms.grn.posted`, `match.ai.suggestion`                              |
| iWMS v3 | Warehouse | warehouse, zone, bin, item, stock, picklist, wave, shipment, adjustment                   | `wms.picklist.created`, `wms.picklist.completed`, `wms.grn.posted`, `wms.inventory.adjusted` | `sales.order.created`, `procurement.po.approved`, `forecast.stock`   |

Notă: pentru F2 „mobile RF” este implementat ca PWA React (Scanner Web + API) — suita React Native dedicată rămâne în F6.

### 3) Evenimente & topic‑uri (convenții v1)

- Prefix module urmat de context și verb la past‑tense: `sales.invoice.issued`, `procurement.grn.posted`, `wms.picklist.completed`, `crm.lead.created`.
- Correlation: header `x-corr-id` propagat; Tempo trace‑id `wrk-<uuid>` de la Workers Registry.
- Validare naming prin hook‑ul `scripts/lint-rmq.sh` (activ încă din F1).

### 4) KPI & Gate F2 → F3

- Order‑to‑Cash E2E (Lead→Opportunity→SO→Pick→Ship→Invoice→Payment) reușește pe 1 tenant demo în < 3 min; toate hop‑urile emit evenimente confirmate.
- Procure‑to‑Pay E2E (RFQ→PO→GRN→3WM→Supplier Invoice) reușește end‑to‑end; `three_way_match` produce alertă pentru discrepanțe > 2 %.
- Observability: 2 dashboards Grafana (O2C, P2P) + 8 alerte (RMQ lag, fail rate ≥1 %, task timeout).
- SLO API per modul: `p95 < 250 ms`, `error_rate < 1 %`.
- Security: JWT claims (`tid`,`whid`,`scp`,`role`) verificate la toate endpoint‑urile; RLS activ pe toate tabelele noi.

### 5) Formatul JSON extins – câmpuri obligatorii

- `step` – index consecutiv 300‑399
- `scope` – sub‑sistem vizat (max 3‑4 cuvinte)
- `context` – livrări anterioare relevante
- `task` – instrucțiune imperativă clară
- `dirs` – directoare vizate (prefixe canonice `core/**`, `standalone/**`)
- `constraints` – reguli stricte (commit‑msg, lint‑paths, fără secrete)
- `output` – rezultat așteptat

> Atenție: folosește numai căile canonice (ex.: `standalone/mercantiq/apps/sales/…`) și stack‑ul fix. Commit‑urile pe căi vechi `/apps/...` sunt respinse de lint‑paths.

### 6) Pașii de implementare F2 (CursorAI prompts)

```json
[
  {"step":300,"scope":"handover-f1-check","context":"Gate F1 cerut în Readme 1/roadmap general","task":"Fail pipeline dacă Shell nu afișează 3 widget-uri demo sau Worker Registry nu este verde.","dirs":["/core/docs/handovers/"],"constraints":"GitHub Action handover-check; verde obligatoriu","output":"F2 unblocked"},
  {"step":301,"scope":"bus-topics-f2","context":"Event-Bus v1-spec definit la F1","task":"Extinde `docs/event-bus/v1-spec.md` cu lista topic-urilor F2 pentru crm/sales/procurement/wms.","dirs":["/core/docs/event-bus/"],"constraints":"naming `<module>.<ctx>.<event>`; tabel markdown; PR semnat","output":"Spec F2 publicată"},
  {"step":302,"scope":"sdk-ts-events","context":"SDK TS existent din F1","task":"Adaugă tipuri & helpers publish/subscribe pentru noile topic-uri F2.","dirs":["/core/packages/sdk-ts/"],"constraints":"tests ≥90%","output":"SDK TS bus actualizat"},
  {"step":303,"scope":"sdk-py-events","context":"SDK Py existent","task":"Adaugă client Python pentru noile topic-uri (publish/consume) + exemplu minimal.","dirs":["/core/packages/sdk-py/"],"constraints":"pytest verde","output":"SDK Py bus actualizat"},
  {"step":304,"scope":"seed-data-core","context":"Nu există date demo F2","task":"Script `scripts/seed-f2.ts` cu seed universal: products, price_list, sample customers & suppliers.","dirs":["/core/scripts/"],"constraints":"nu hard-code secrete; commit 'feat(seed): f2 demo'","output":"seed F2"},
  {"step":305,"scope":"ci-templates-f2","context":"module-ci exemplu în readme 2","task":"Generează `module-ci.yml` per modul F2 cu build/test/scan/sign/publish + Argo sync dev.","dirs":["/.github/workflows/"],"constraints":"paths folosesc `standalone/**`","output":"4 pipeline-uri module-ci"},
  {"step":310,"scope":"vettify-scaffold","context":"Modul inexistent","task":"`core/scripts/create-module.ts --standalone vettify --with-ai` → frontend, api, workers stubs.","dirs":["/standalone/vettify/"],"constraints":"tags Nx `module:vettify`","output":"schelet Vettify"},
  {"step":311,"scope":"vettify-db","context":"PG per tenant, schema per modul","task":"Migrations pentru `accounts, contacts, leads, opportunities, campaigns` cu RLS pe tid/whid/mid.","dirs":["/standalone/vettify/apps/api/src/migrations/"],"constraints":"RLS activ; pgvector pregătit","output":"tabele CRM"},
  {"step":312,"scope":"vettify-api","context":"DTO/Controllers lipsă","task":"Controller NestJS pentru CRUD lead/account/contact/opportunity + stage transitions.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"class-validator; p95<250ms","output":"API CRM"},
  {"step":313,"scope":"vettify-events","context":"Bus spec F2 (step 301)","task":"Publică `crm.lead.created`, `crm.opportunity.stage_changed`; consumă `sales.order.created`.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"contract-tests bus","output":"events CRM live"},
  {"step":314,"scope":"vettify-workers","context":"Workers disponibili din flotă","task":"Integrează `ai.summary` pentru note apel, `ai.churn` pentru risc client și `anaf.taxpayer` pentru validare CUI clienți/prospects.","dirs":["/standalone/vettify/apps/workers/"],"constraints":"queue `ai.*`, `anaf.*`; metrics OTel","output":"AI + ANAF CRM online"},
  {"step":315,"scope":"vettify-ui","context":"Frontend gol","task":"Micro-frontend remote Vite Federation: Leads, Opportunities, Campaigns.","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"MUI6 + Tailwind3; vitest 80%","output":"UI CRM"},
  {"step":316,"scope":"vettify-helm","context":"Deploy lipsă","task":"Chart Helm `vettify-{frontend,api,workers}` + IngressRoute + ServiceMonitor.","dirs":["/standalone/vettify/infra/helm/"],"constraints":"OCI push; cosign sign","output":"deploy Vettify"},
  {"step":317,"scope":"vettify-e2e","context":"E2E absent","task":"Playwright: create lead→convert to opportunity + event verificat pe RMQ.","dirs":["/standalone/vettify/tests/e2e/"],"constraints":"headless ci","output":"E2E CRM verde"},
  {"step":320,"scope":"sales-scaffold","context":"Modul inexistent","task":"Creează `standalone/mercantiq/apps/sales` (frontend+api) + seeds produse/prețuri.","dirs":["/standalone/mercantiq/apps/sales/"],"constraints":"tags Nx `module:mercantiq-sales`","output":"schelet Sales"},
  {"step":321,"scope":"sales-db","context":"Schema sales","task":"Migrations: `customers, products, price_lists, so, so_lines, invoices, payments` + RLS.","dirs":["/standalone/mercantiq/apps/sales/api/src/migrations/"],"constraints":"FK stricte; RLS pe tid/whid","output":"tabele Sales"},
  {"step":322,"scope":"sales-anaf-compliance","context":"Conformitate RO","task":"Integrează workeri `anaf.taxpayer` (validare CUI) + `anaf.efactura` (transmitere e-Factura la ANAF) + flux PDF via `pdf.render`.","dirs":["/standalone/mercantiq/apps/sales/api/src/","/standalone/mercantiq/apps/sales/workers/"],"constraints":"fără chei în repo; ExternalSecrets","output":"conformitate ANAF ok"},
  {"step":323,"scope":"sales-pos","context":"UI necesar","task":"UI POS (organism `pos-terminal`) + creare SO + plată cash/card mock.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/"],"constraints":"vitest 80%","output":"POS MVP"},
  {"step":324,"scope":"sales-events","context":"Bus spec F2","task":"Publică `sales.order.created`, `sales.invoice.issued`, `payment.received`; consumă `wms.picklist.completed`.","dirs":["/standalone/mercantiq/apps/sales/api/src/"],"constraints":"contract-tests","output":"events Sales"},
  {"step":325,"scope":"sales-pdf","context":"Worker pdf","task":"Endpoint `POST /invoices/:id/pdf` → publish `pdf.render`; persistă link în MinIO.","dirs":["/standalone/mercantiq/apps/sales/api/src/"],"constraints":"SSE‑C MinIO","output":"PDF factură"},
  {"step":326,"scope":"sales-k6","context":"Perf KPI","task":"k6: 100 RPS pe `POST /sales-orders` p95<250ms.","dirs":["/standalone/mercantiq/tests/k6/"],"constraints":"grafana datasource","output":"raport k6"},
  {"step":327,"scope":"sales-helm","context":"Deploy","task":"Charts Helm sales + ServiceMonitor; Argo app.","dirs":["/standalone/mercantiq/infra/helm/"],"constraints":"OCI push; cosign","output":"deploy Sales"},
  {"step":330,"scope":"proc-scaffold","context":"Modul procurement inexistent","task":"`standalone/mercantiq/apps/procurement` scaffold (frontend+api).","dirs":["/standalone/mercantiq/apps/procurement/"],"constraints":"tags Nx `module:procurement`","output":"schelet Procurement"},
  {"step":331,"scope":"proc-db","context":"Schema procurement","task":"Migrations: `suppliers, rfq, rfq_lines, quotes, po, po_lines, grn, invoices, three_way_match` + RLS.","dirs":["/standalone/mercantiq/apps/procurement/api/src/migrations/"],"constraints":"chei compuse (tid,mid,whid,...)","output":"tabele Procurement"},
  {"step":332,"scope":"proc-match-ai","context":"AI matching","task":"Integrează worker `match.ai` pentru sugestii furnizori (RFQ) și 3WM anomaly detect.","dirs":["/standalone/mercantiq/apps/procurement/workers/"],"constraints":"faiss index per tenant","output":"AI procurement"},
  {"step":333,"scope":"proc-events","context":"Bus spec F2","task":"Publică `procurement.rfq.created`, `procurement.po.approved`, `procurement.grn.posted`, `procurement.3wm.flagged`.","dirs":["/standalone/mercantiq/apps/procurement/api/src/"],"constraints":"contract-tests","output":"events Procurement"},
  {"step":334,"scope":"proc-ui","context":"Frontend","task":"Pagini RFQ, PO, GRN + vizual 3WM (status verde/galben/roșu).","dirs":["/standalone/mercantiq/apps/procurement/frontend/src/"],"constraints":"MUI DataGrid","output":"UI Procurement"},
  {"step":335,"scope":"proc-helm","context":"Deploy","task":"Charts Helm procurement + Argo app.","dirs":["/standalone/mercantiq/infra/helm/"],"constraints":"OCI push; cosign","output":"deploy Procurement"},
  {"step":340,"scope":"iwms-scaffold","context":"iWMS v3 inexistent","task":"`standalone/iwms/apps/frontend` + `standalone/iwms/apps/api` scaffold; PWA RF scanner.","dirs":["/standalone/iwms/apps/"],"constraints":"tags Nx `module:iwms`","output":"schelet iWMS"},
  {"step":341,"scope":"iwms-db","context":"Schema WMS","task":"Migrations: `warehouses, zones, bins, items, stock, picklists, waves, shipments, adjustments` + RLS pe whid.","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"index compus (tid,whid,item)","output":"tabele iWMS"},
  {"step":342,"scope":"iwms-api","context":"Operațional","task":"Endpoints: allocate picklist (SO), confirm pick, post GRN (PO), inventory adjust.","dirs":["/standalone/iwms/apps/api/src/"],"constraints":"guards JWT+RLS; p95<250ms","output":"API iWMS"},
  {"step":343,"scope":"iwms-events","context":"Bus spec F2","task":"Publică `wms.picklist.created|completed`, `wms.grn.posted`, `wms.inventory.adjusted`; consumă SO/PO.","dirs":["/standalone/iwms/apps/api/src/"],"constraints":"contract-tests","output":"events iWMS"},
  {"step":344,"scope":"iwms-forecast","context":"AI forecast","task":"Integrează worker `forecast` pentru propuneri re‑order point (ROP) pe `items`.","dirs":["/standalone/iwms/apps/workers/"],"constraints":"Ray cluster; metrici în Grafana","output":"ROP sugerat"},
  {"step":345,"scope":"iwms-rf-pwa","context":"Mobile RF (browser)","task":"UI PWA: login, pick, putaway, receive; acces scanner camera API.","dirs":["/standalone/iwms/apps/frontend/src/"],"constraints":"CLS<0.1, LCP<2.5s","output":"RF PWA"},
  {"step":346,"scope":"iwms-helm","context":"Deploy","task":"Charts iWMS + ServiceMonitor.","dirs":["/standalone/iwms/infra/helm/"],"constraints":"OCI push; cosign","output":"deploy iWMS"},
  {"step":350,"scope":"o2c-flow","context":"Legătură Sales↔iWMS","task":"SO creat → iWMS generează picklist → completare → Sales emite factură → `payment.received`.","dirs":["/standalone/mercantiq/","/standalone/iwms/"],"constraints":"contract-tests pe fiecare hop","output":"Order-to-Cash E2E"},
  {"step":351,"scope":"p2p-flow","context":"Legătură Procurement↔iWMS","task":"PO aprobat → iWMS postează GRN → 3WM rulează (worker `match.ai`) → status pe UI Procurement.","dirs":["/standalone/mercantiq/","/standalone/iwms/"],"constraints":"alert dacă deviere >2%","output":"Procure-to-Pay E2E"},
  {"step":352,"scope":"observability-dash","context":"Observability stack F0","task":"2 dashboards Grafana: O2C, P2P (RMQ lag, event throughput, error rate, p95).","dirs":["/core/infra/grafana/provisioning/dashboards/"],"constraints":"uid-uri unice","output":"dashboards F2"},
  {"step":353,"scope":"alerts-f2","context":"Alertmanager în F0","task":"Alerte: RMQ lag>1m/queue, `contract-test` fail, error_rate>1%, worker timeout>30s.","dirs":["/core/infra/k8s/alertmanager/rules/"],"constraints":"Slack webhook via `notify.slack`","output":"alerte F2"},
  {"step":354,"scope":"argo-apps","context":"Argo app-of-apps","task":"Definește aplicații Argo per modul F2, dependente de `infra/base`.","dirs":["/core/infra/k8s/argocd/"],"constraints":"syncPolicy automated + selfHeal","output":"Argo apps F2"},
  {"step":355,"scope":"postman-f2","context":"Colecții lipsă","task":"Colecție Postman pentru toate API‑urile noi + exemple events.","dirs":["/core/docs/postman/"],"constraints":"env dev/stage","output":"Postman F2"},
  {"step":356,"scope":"security-rls","context":"RLS cerut în 9.2/9.5","task":"Test automat care eșuează dacă tabele noi nu au RLS și politicile nu aplică `tid`/`whid`.","dirs":["/core/tests/security/"],"constraints":"ci fail hard","output":"guard RLS"},
  {"step":357,"scope":"keycloak-scopes","context":"Identity Keycloak 23","task":"Actualizează realm export: scopes noi `crm/*, sales/*, procurement/*, wms/*`.","dirs":["/core/infra/keycloak/realm-export.json"],"constraints":"OPA Gatekeeper validează","output":"scopes adăugate"},
  {"step":358,"scope":"rate-limit-f2","context":"WAF/Rate-limit F0","task":"Definire rate-limit pe endpoints critice (POS, RFQ, GRN) în Traefik.","dirs":["/core/infra/helm/umbrella/"],"constraints":"token-bucket Redis 10 req/s user","output":"rate-limit activ"},
  {"step":359,"scope":"dr-backup-f2","context":"DR & backup 9.4","task":"Joburi backup PG schema F2 + replicare MinIO verificată.","dirs":["/core/infra/helm/backup/"],"constraints":"RPO≈0, RTO<15m","output":"backup valid"},
  {"step":360,"scope":"ci-contract-tests","context":"Contract tests bus","task":"Pact publisher/consumer între module pe topic-urile F2.","dirs":["/core/tests/contract/event-bus/"],"constraints":"coverage ≥90%","output":"contract-tests F2"},
  {"step":361,"scope":"e2e-o2c-ci","context":"E2E O2C","task":"Job CI rulează O2C end‑to‑end pe dev la fiecare PR pe sales/iwms.","dirs":["/.github/workflows/"],"constraints":"mask secrets; 12 min target","output":"pipeline O2C"},
  {"step":362,"scope":"e2e-p2p-ci","context":"E2E P2P","task":"Job CI rulează P2P end‑to‑end pe dev la PR pe procurement/iwms.","dirs":["/.github/workflows/"],"constraints":"canary 10%","output":"pipeline P2P"},
  {"step":363,"scope":"kpi-sli-slo","context":"KPI CI/CD (12.5)","task":"Expune SLI/SLO F2 în Grafana (p95, error_rate, rollback time).","dirs":["/core/infra/grafana/provisioning/dashboards/"],"constraints":"targets 12.5","output":"SLO dashboards"},
  {"step":364,"scope":"docs-ctx","context":"Arhitectură","task":"Diagrame context pentru cele 4 bounded contexts + relații event-driven.","dirs":["/standalone/*/docs/architecture/ctx-view/diagrams/"],"constraints":"Mermaid + export svg","output":"diagrame F2"},
  {"step":365,"scope":"gate-f2-script","context":"Gate‑uri standard","task":"Script `scripts/gate-f2.sh`: validează E2E O2C/P2P, dashboards prezente, alerte active.","dirs":["/core/scripts/"],"constraints":"exit>0 la orice fail","output":"gate F2"},
  {"step":366,"scope":"shell-integration","context":"Shell remote loader","task":"Publică remotes pentru Vettify/Mercantiq/iWMS în Shell nav dinamic.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"fallback static","output":"module vizibile în Shell"},
  {"step":367,"scope":"rbac-ui-claims","context":"Admin Core","task":"Mapează roluri (sales, procurement, wms, marketing) pe scopes și ascunde meniuri nepermise.","dirs":["/core/apps/admin-core/","/core/apps/shell-gateway/frontend/"],"constraints":"OPA Gatekeeper","output":"RBAC UI corect"},
  {"step":368,"scope":"analytics-feed","context":"F5 ulterior","task":"Evenimentele F2 sunt replicate în lakehouse (DuckDB/Delta) prin worker `etl.sync`.","dirs":["/standalone/*/"],"constraints":"cron orquestrat","output":"feed OLAP"},
  {"step":369,"scope":"audit-trail","context":"Security 10.x","task":"Audit per resursă: cine a emis SO/PO/GRN/Invoice, export CSV semnat.","dirs":["/standalone/*/apps/api/src/"],"constraints":"sigiliu cosign","output":"audit trail"},
  {"step":370,"scope":"handover-f2","context":"Închidere F2","task":"Generează `docs/handovers/F2_handover.md` cu link dashboards, Argo apps, checklist Gate.","dirs":["/core/docs/handovers/"],"constraints":"semnat de owner","output":"hand‑over F2"}
]
```

### 7) Detalii de implementare pe module

#### 7.1 Vettify (CRM + Marketing)
- API NestJS: controllers pentru leads/opportunities/campaigns; conversie lead→opportunity; validări class-validator.
- AI: `ai.summary` (rezumate întâlniri/email), `ai.churn` (risc client).
- Events: `crm.lead.created`, `crm.opportunity.stage_changed`.
- UI: micro‑frontend (Vite Federation) cu pagini Leads/Opportunities/Campaigns.
- RBAC: scopes `crm/*` în Keycloak; ABAC via OPA.

#### 7.2 Mercantiq – Sales & Billing
- Core: produse, liste de preț, comenzi, facturi, plăți.
- Conformitate RO: `anaf.taxpayer` (validare CUI clienți) + `anaf.efactura` (transmitere e-Factură la ANAF); generare PDF factură cu `pdf.render` și stocare semnată (MinIO SSE‑C).
- Events: `sales.order.created`, `sales.invoice.issued`, `payment.received`.
- POS UI: terminal ușor, offline‑friendly (cache + retry).

#### 7.3 Mercantiq – Procurement
- Core: RFQ→Quote→PO→GRN→3‑Way‑Match; anomalii semnalate.
- AI: `match.ai` pentru propuneri furnizori & 3WM flags.
- Events: `procurement.rfq.created`, `procurement.po.approved`, `procurement.grn.posted`, `procurement.3wm.flagged`.

#### 7.4 iWMS v3
- Core: multi‑warehouse, locuri (zone/bins), gestiune stoc, pick/pack/ship, recepții.
- Mobile RF (PWA): scanare coduri (MediaDevices), task‑uri pick/putaway/receive.
- AI: `forecast` pentru ROP/demand.
- Events: `wms.picklist.created`, `wms.picklist.completed`, `wms.grn.posted`, `wms.inventory.adjusted`.

### 8) Securitate, date & multi‑tenant (rezumat aplicat F2)

- Identitate: Keycloak 23 multi‑realm, OIDC+PKCE; JWT RS256 (`tid`, `whid`, `scp`, `role`).
- ABAC/RBAC: Keycloak groups + OPA Gatekeeper; rate‑limit Redis token‑bucket.
- RLS la DB: reguli `tid/whid` setate via `current_setting('app.tid')`.
- Criptare: MinIO SSE‑C AES‑256‑GCM; CMK per tenant în Vault; TLS 1.3 / mTLS intern.

### 9) Observabilitate & CI/CD

- Dashboards: Web‑Vitals pentru PWA RF, throughput events, RMQ lag, Celery queue lag.
- CI: șabloane `module-ci.yml` cu build/test/scan (Trivy HIGH), `cosign sign`, push OCI, Argo sync, canary 10% și rollback metric‑based.
- Supply‑chain: `cosign attest` (SPDX), retenție registry (ultimele 3 minore).

### 10) Livrabile și hand‑over

- Argo apps live pentru cele 4 module.
- Dashboards Grafana (O2C, P2P) + alerte în Alertmanager.
- Colecții Postman pe `docs/postman`.
- `F2_handover.md` semnat cu link‑uri către diagrame, dashboards, Argo, colecții.
- Gate F2 rulat de `scripts/gate-f2.sh`.

### Roadmap‑uri derivate

- `8_roadmap_vettify.md`
- `9_roadmap_mercantiq_sales_billing.md`
- `10_roadmap_mercantiq_procurement.md`
- `11_roadmap_iwms_v3.md`

### Note de conformitate cu convențiile proiectului

- Căi canonice obligatorii: `core/**` pentru Shell/Admin/Workers și `standalone/<app>/**` pentru aplicațiile F2; NU folosi `/apps/...` fără prefix.
- Stack fix: fără Next.js/Angular/Flask/Kafka; respectă tabelul „Stack tehnologic – obligatoriu”.
- Evenimente: respectă `docs/event-bus/v1-spec.md` + hook `lint-rmq.sh` (naming enforcement).