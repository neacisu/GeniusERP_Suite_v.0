# 11 · Roadmap iWMS v3 – **versiune upgradată** (workeri + integrare suita)

> **Scop:** să implementăm **iWMS v3** ca modulul responsabil de **Warehouse Management** în suita GeniusERP – cu integrare profundă de **workeri** (forecast, pdf.render, ocr, match.ai) și interoperabilitate **suite & stand‑alone** cu **Mercantiq Sales**, **Procurement**, **CRM (Vettify)** și ecosistemul complet.
> **Stack fix:** React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workers), RMQ 3.14 + Redis 7 (bus), PostgreSQL 17 + pgvector, MinIO SSE‑C, Terraform + Helmfile + ArgoCD (deploy). Respectă convențiile de nume evenimente `module.ctx.event`. Folosește doar căile canonice `standalone/iwms/**`.
> **Gate F2 ➜ F3:** flux **Order‑to‑Cash** și **Procure‑to‑Pay** E2E < 3 min, evenimente confirmate; SLO API p95 < 250 ms, error\_rate < 1 %.

**Bounded‑context iWMS:** warehouse, zone, bin, item, stock, picklist, wave, shipment, adjustment cu automatizare completă și inteligență artificială pentru forecast și optimizări operaționale.

**Workeri integrați (disponibili azi în flotă):**
`forecast` (predicții cerere și ROP/SS), `pdf.render` (etichete și BOL), `ocr` (recepție automată), `email.send` (notificări), `match.ai` (optimizări wave și slotting)
**Date & securitate:** Multi‑tenant PG 17 + pgvector + MinIO per tenant (SSE‑C AES‑256‑GCM), Redis per tenant; JWT RS256 cu claims `tid`,`whid`,`scp`,`role`; RLS strictă pe `tid/whid`.
**Observabilitate:** Prometheus metrics, Tempo traces end‑to‑end (browser→API→RMQ→worker), dashboards dedicați O2C/P2P & alerte.

---

## Cum să folosești această documentație

Această documentație reprezintă un roadmap detaliat pentru dezvoltarea aplicației stand-alone **iWMS v3** (Warehouse Management System). Lista de pași este organizată sub formă de obiecte JSON, fiecare element corespunzând unei etape concrete de implementare.

**Parcurge pașii în ordine:** Fiecare element JSON are un câmp step (indexul pasului 300-399) și descrie o acțiune ce trebuie realizată. Pașii sunt organizați logic de la verificarea gate-ului F1 la implementarea completă.

**Înțelege structura câmpurilor:** Fiecare obiect conține câmpuri esențiale – scope indică sub‑sistemul sau componenta vizată, context oferă detalii despre starea proiectului înainte de acest pas, task descrie în mod imperativ acțiunea de efectuat, dirs precizează directoarele/proiectele afectate, constraints enumeră reguli sau condiții ce trebuie respectate, iar output descrie pe scurt rezultatul așteptat.

**Respectă constraints:** Câmpul constraints include cerințe stricte precum respectarea convențiilor de commit (Conventional Commits), rularea linter‑elor, integrarea cu External Secrets pentru credențiale, și condiții de performanță și securitate.

**Navighează după scope:** Pașii sunt grupați logic prin câmpul scope (ex. "scaffold‑*", "db‑*", "svc‑*", "fe‑*", "security‑*"). Poți prioritiza sau delega anumite sub‑sisteme pe baza acestei clasificări.

## 1) Pre‑condiții & Scope

* **Gate F1 trecut**: Shell vizibil (3 widget‑uri), Admin Core & Worker Registry verzi.
* **Event‑Bus v1** și naming `<module>.<ctx>.<event>` deja stabilite; hook `scripts/lint-rmq.sh` obligatoriu.
* **Multitenancy & date**: PostgreSQL 17 (cluster per tenant, schema per modul), MinIO per tenant, Redis per tenant, **RLS pe `tid/whid/mid`**.
* **Worker Fleet** disponibil: `forecast`, `pdf.render`, `ocr`, `email.send`, `match.ai`.
* **Stack fix**: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workeri), RabbitMQ 3.14 + Redis 7 (bus/queue), PostgreSQL 17 + pgvector, IaC: Terraform + Helmfile + Argo CD.
* **Module paralele**: Mercantiq Sales & Procurement în dezvoltare paralelă pentru integrări evenimente.

## 2) Bounded‑Context & Interfețe

### **Entități principale**
* **Warehouse**: depozite cu zone și configurări operaționale
* **Zone/Bin**: locații ierarhice cu capacități și restricții  
* **Item**: produse cu atribute WMS (dimensiuni, greutate, hazard)
* **Stock**: stocuri pe locații cu rezervări și statusuri (available, allocated, hold)
* **Picklist**: ordine de picking cu optimizare rute și wave planning
* **Wave**: grupare intelligentă comenzi pentru eficiență operațională
* **Shipment**: expediții cu packing, etichetare și tracking
* **Adjustment**: ajustări inventar cu motive și aprobare workflow

### **Evenimente publicate**
* **`wms.picklist.created`**: listă picking nouă generată cu alocare stoc
* **`wms.picklist.completed`**: picking finalizat și expediat
* **`wms.grn.posted`**: recepție marfă confirmată în depozit
* **`wms.inventory.adjusted`**: ajustare stoc cu audit trail complet

### **Evenimente consumate**
* **`sales.order.created`**: nou order pentru alocare picking automată
* **`procurement.po.approved`**: comandă aprobată pentru planificare recepție
* **`pdf.render.done`**: etichetă sau document generat și salvat
* **`forecast.completed`**: predicții ROP/SS actualizate pentru replenishment

### **Workeri integrați**

**Fleet existentă:**
* `forecast` - predicții cerere, calculare ROP/SS și recomandări replenishment
* `pdf.render` - generare etichete bin/item, BOL și packing slips
* `ocr` - procesare automată documente furnizor pentru matching GRN
* `email.send` - notificări pentru devieri, alerte și confirmări
* `match.ai` - optimizări wave planning, slotting și similitudini produse

## 3) Arhitectura Aplicației

### **iWMS v3 Overview**

iWMS v3 devine sistemul central de warehouse management din suita GeniusERP, cu automatizare completă și inteligență artificială integrată. Aplicația acoperă:

- **Operațiuni WMS complete**: recepție, putaway, picking, packing, shipping cu RF support
- **AI‑powered optimization**: wave planning inteligent, slotting recommendations, forecast‑driven replenishment
- **PWA & Offline support**: RF devices cu cache local și sincronizare automată
- **Multi‑warehouse**: suport pentru multiple depozite cu transfer suggestions
- **Advanced analytics**: heatmap slotting, KPI operaționali, performance dashboards

### **Integrarea cu Ecosistemul**

Prin integrările extinse, modulul conectează:
- **Mercantiq Sales**: order allocation automată → picking → shipping cu confirmări
- **Procurement**: PO approved → GRN planning → recepție → three‑way match trigger
- **CRM (Vettify)**: customer priority în wave planning și expedite handling
- **Worker Registry**: orchestrare inteligentă a tuturor serviciilor AI și automatizări

### **Structura Aplicației (stand‑alone)**

```
standalone/iwms/
├── apps/
│   ├── frontend/               # React 19 + Vite 5 Federation + Tailwind 3 + MUI 6
│   │   ├── public/
│   │   └── src/
│   │       ├── pages/{dashboard,receiving,putaway,picking,packing,shipping,inventory,cycle-count}/
│   │       ├── organisms/{rf-receive,rf-pick,rf-putaway,rf-ship}/
│   │       ├── widgets/{health,kpi,stock-heatmap}/
│   │       ├── hooks/, utils/, config/, routers/
│   │       └── tests/ (Vitest/Playwright)
│   ├── api/                    # NestJS 11
│   │   └── src/
│   │       ├── controllers/warehouse/{receiving,putaway,picking,wave,shipment,inventory,adjustment}/
│   │       ├── services/warehouse/{alloc,wave,slotting,stock,doc}/
│   │       ├── dto/, guards/, interceptors/, filters/, entities/, repositories/, migrations/, config/
│   │       └── tests/
│   └── workers/                # wrappere iWMS către workers existenți
│       ├── forecast.adapter/
│       ├── labels.adapter/
│       └── ocr.adapter/
├── infra/
│   ├── terraform/, helm/, helmfile/, grafana/, k8s/, policies/opa/
│   └── scripts/
├── docs/ (api/openapi, domain/wms, handovers, postman)
└── tests/ (k6, contract/event-bus)
```

## 4) Securitate & RBAC

* Scopes Keycloak `wms/*` cu roluri operaționale (operator, supervisor, manager, wms‑admin)
* Guard JWT RS256 + RLS pe toate tabelele pentru izolare multi‑tenant și warehouse
* ABAC la UI cu permisiuni fine pe operațiuni (cycle count, adjustments, wave release)
* Rate limiting și throttling pentru RF devices și bulk operations
* Audit trail pentru toate mișcările de stoc cu hash verification și non‑repudiation

## 5) Observabilitate

* OTel traces end‑to‑end (RF device→API→workers) cu propagare context complet
* Prometheus metrics (HTTP + business: pick rate, dock‑to‑stock, order‑to‑ship times)
* Dashboards dedicați Order‑to‑Cash și Procure‑to‑Pay cu KPI operaționali
* Alerting pentru SLO (p95 latență, error rate), RMQ lag, stockout predictions
* Web Vitals collection pentru performance RF și analytics avansate

## 6) Criterii de Acceptanță F2

* **Flux O2C complet**: Sales Order → Allocation → Pick → Pack → Ship în <3 minute
* **Flux P2P complet**: PO Approved → GRN → Putaway → Stock Available în <3 minute  
* **AI Integration**: forecast working, wave optimization active, OCR processing
* **Performance**: API p95 <250ms, error rate <1%, RF responsiveness optimal
* **PWA support**: offline cache working, background sync functional
* **Multi‑warehouse**: transfer suggestions și cross‑dock capabilities
* **Integrări**: evenimente publicate/consumate conform specificației Event‑Bus

## 7) Structura Implementării

### **Interval F2**: 300‑399 (100 pași)
- **Effort**: 6‑7 săptămâni dezvoltare (incluzând RF UI și AI integrations)
- **Scop**: iWMS v3 complet cu toate fluxurile WMS și AI features
- **Modul**: `iwms‑v3` (frontend + api + workers adapters)
- **Dependențe**: F1 Core Platform + F2 Base Workers + Sales/Procurement integration

## 8) CursorAI Prompts (iWMS v3 300–399)

> **Format obligatoriu:** `step`, `scope`, `context`, `task`, `dirs`, `constraints`, `output` (identic F0/F1/F2). **Nu hard‑coda secrete**, folosește External Secrets. **Căi canonice** `standalone/iwms/**` (lint‑paths blochează vechile `/apps/...`).

```json
[
  {"step":300,"scope":"handover-f1-check","context":"Gate F1 cerut de Roadmap General; Shell+Admin+Workers verzi","task":"Adaugă job CI `handover-check` care fail-uieste dacă Shell nu are 3 widget-uri demo sau Worker Registry nu e verde","dirs":["/core/docs/handovers/","/.github/workflows/"],"constraints":"Respectă lint-paths; fără secrete în logs","output":"F2 unblocked"},
  {"step":301,"scope":"bus-spec-iwms","context":"F2 cere listă topic-uri per modul","task":"Extinde `core/docs/event-bus/v1-spec.md` cu topic-urile iWMS (`wms.*`) și payload schemă JSON","dirs":["/core/docs/event-bus/"],"constraints":"naming `<module>.<ctx>.<event>`; PR semnat","output":"Spec bus iWMS publicată"},
  {"step":302,"scope":"sdk-ts-events","context":"SDK TS există din F1","task":"Adaugă tipuri TS și helpers publish/subscribe pentru `wms.picklist.created|completed`, `wms.grn.posted`, `wms.inventory.adjusted`","dirs":["/core/packages/sdk-ts/src/"],"constraints":"tests ≥90% coverage","output":"SDK-TS bus iWMS"},
  {"step":303,"scope":"sdk-py-events","context":"SDK Py există","task":"Extinde clientul Python cu topics `wms.*` + exemple publish/consume","dirs":["/core/packages/sdk-py/genius_sdk/bus/"],"constraints":"pytest verde","output":"SDK-Py bus iWMS"},
  {"step":304,"scope":"seed-data-wms","context":"Lipsă date demo pentru iWMS","task":"Script `scripts/seed-f2-wms.ts` cu warehouses, zones, bins, items, barcodes, uom","dirs":["/core/scripts/"],"constraints":"nu introduce secrete; CC msg `feat(seed): wms demo`","output":"Seed iWMS"},
  {"step":305,"scope":"module-ci-templates","context":"F2 recomandă pipeline per modul","task":"Generează `.github/workflows/module-ci-iwms.yml` (build/test/scan/sign/publish + Argo sync dev)","dirs":["/.github/workflows/"],"constraints":"paths=`standalone/iwms/**`","output":"CI iWMS"},
  {"step":306,"scope":"scaffold-frontend","context":"Nu există UI iWMS","task":"`core/scripts/create-module.ts --standalone iwms --frontend` → React 19 + Vite Federation + Tailwind + MUI","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"tags Nx `module:iwms,layer:frontend`","output":"Skeleton FE iWMS"},
  {"step":307,"scope":"scaffold-api","context":"Nu există API iWMS","task":"Generează `standalone/iwms/apps/api` (NestJS 11) cu setup TypeORM, OpenAPI, pino logger","dirs":["/standalone/iwms/apps/api/"],"constraints":"tags Nx `module:iwms,layer:api`","output":"Skeleton API iWMS"},
  {"step":308,"scope":"fe-tailwind-theme","context":"UI necesită styling unificat","task":"Configurează Tailwind + tokens MUI în `tailwind.config.ts`; `important:'#root'`","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"commit 'chore(iwms-fe): tailwind tokens'","output":"Tailwind activ"},
  {"step":309,"scope":"fe-federation","context":"Module federation","task":"Activează Vite plugin federation; expune `remoteEntry.js` pentru Shell","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"commit 'feat(iwms-fe): remote-loader'","output":"remoteEntry expus"},
  {"step":310,"scope":"fe-aliases","context":"Imports relative greu de întreținut","task":"Configurează aliasuri `@iwms/*` în tsconfig + vite","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"fără căi absolute","output":"alias-uri FE"},
  {"step":311,"scope":"api-config","context":"API skeleton","task":"Setează config multi-tenant (tid/whid/mid), pgBouncer DSN, MinIO SSE-C, RMQ URL din ExternalSecrets","dirs":["/standalone/iwms/apps/api/src/config/","/standalone/iwms/infra/k8s/external-secrets/"],"constraints":"fără secrete în repo","output":"config securizat"},
  {"step":312,"scope":"db-migrations-core","context":"Schema iWMS necesară","task":"Migrations pentru `warehouses, zones, bins, items` cu PK compuse (tid,whid,code)","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"respectă RLS design","output":"DDL locații"},
  {"step":313,"scope":"db-migrations-stock","context":"Stocuri & mișcări","task":"Migrations `stock, stock_tx, reservations` cu indecși (item_id,bin_id,status)","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"no hard-coded defaults","output":"DDL stocuri"},
  {"step":314,"scope":"db-migrations-flows","context":"Fluxuri operaționale","task":"Migrations `picklists, waves, shipments, grn, adjustments, returns`","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"FK stricte; on delete restrict","output":"DDL fluxuri"},
  {"step":315,"scope":"db-rls","context":"Security by design","task":"Activează RLS pe toate tabelele; politici `tid = current_setting('app.tid') AND (whid = current_setting('app.whid') OR whid IS NULL)`","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"doar RLS; fără view-uri nesecurizate","output":"RLS activ"},
  {"step":316,"scope":"db-vector","context":"Recomandări/slotting ușor","task":"Instalează pgvector; tabele `item_embeddings` pentru similitudini (opțional)","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"nu bloca MVP; feature flag","output":"pgvector ready"},
  {"step":317,"scope":"entities-dto","context":"ORM + validare","task":"Definește entități TypeORM + DTO cu class-validator pentru warehousing domain","dirs":["/standalone/iwms/apps/api/src/entities/","/standalone/iwms/apps/api/src/dto/"],"constraints":"no `any`","output":"entități + DTO"},
  {"step":318,"scope":"guards-interceptors","context":"Auth & observabilitate","task":"JWT guard extins (claims `tid,whid,scp,role`), interceptors OTEL trace-id în headers RMQ","dirs":["/standalone/iwms/apps/api/src/guards/","/standalone/iwms/apps/api/src/interceptors/"],"constraints":"unit tests 80%","output":"securitate API"},
  {"step":319,"scope":"repositories","context":"Acces date performant","task":"Repo-uri custom (stock, reservations, waves) cu query-uri index-friendly","dirs":["/standalone/iwms/apps/api/src/repositories/"],"constraints":"explain analyze în tests","output":"repo-uri optimizate"},
  {"step":320,"scope":"svc-stock-core","context":"Servicii domeniu","task":"`StockService` (get/hold/release/move) cu tranzacții și blocaje conservative","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"idempotent; retries backoff","output":"serviciu stoc"},
  {"step":321,"scope":"svc-alloc","context":"Alocare pick","task":"`AllocService` — rezervă stoc pe SO; suport FEFO/LIFO, lot, serie","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"policy config din Admin Core","output":"serviciu alocare"},
  {"step":322,"scope":"svc-wave","context":"Planificare wave","task":"`WaveService` — grupează picklists, optimizează rute/zone/bins","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"p95<200ms pe 1k linii","output":"serviciu wave"},
  {"step":323,"scope":"svc-putaway","context":"Depozitare","task":"`PutawayService` — loc recomandat (heuristică zone/bin capacity) + execuție","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"fallback simplu dacă lipsesc reguli","output":"serviciu putaway"},
  {"step":324,"scope":"svc-receiving","context":"Recepție (GRN)","task":"`ReceivingService` — recepție PO, validări cant./lot/batch, generare GRN","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"RLS & audit trail","output":"serviciu GRN"},
  {"step":325,"scope":"svc-shipment","context":"Expediții","task":"`ShipmentService` — packing, etichetare, AWB, confirm ship","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"persistă doc în MinIO (SSE-C)","output":"serviciu shipment"},
  {"step":326,"scope":"svc-adjustments","context":"Ajustări inventar","task":"`AdjustmentService` — +/− stoc cu motive și aprobare (RBAC)","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"journal în `stock_tx`","output":"serviciu adjust"},
  {"step":327,"scope":"ctrl-receiving","context":"API recepții","task":"Controller `ReceivingController` (POST /grn) — postează GRN și publică `wms.grn.posted`","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/receiving/"],"constraints":"DTO stricte; e2e tests","output":"endpoint GRN"},
  {"step":328,"scope":"ctrl-putaway","context":"API putaway","task":"`PutawayController` — recomandă bin target + confirmare mutare","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/putaway/"],"constraints":"trace RMQ header","output":"endpoint putaway"},
  {"step":329,"scope":"ctrl-picking","context":"API picking","task":"`PickingController` — create/confirm picklist; publică `wms.picklist.created`","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/picking/"],"constraints":"AbortController timeout 3s","output":"endpoint picking"},
  {"step":330,"scope":"ctrl-wave","context":"API wave","task":"`WaveController` — planifică/lansează wave; calculează KPI pick efficiency","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/wave/"],"constraints":"p95<250ms","output":"endpoint wave"},
  {"step":331,"scope":"ctrl-shipment","context":"API shipping","task":"`ShipmentController` — confirmă packing/ship; publică `wms.picklist.completed`","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/shipment/"],"constraints":"persist docs MinIO","output":"endpoint shipment"},
  {"step":332,"scope":"ctrl-inventory","context":"API inventory","task":"`InventoryController` — status stoc, rezervări, lot/serie, locații","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/inventory/"],"constraints":"cache Redis 30s","output":"endpoint inventar"},
  {"step":333,"scope":"ctrl-adjust","context":"API adjustments","task":"`AdjustmentController` — +/− stoc cu aprobare RBAC","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/adjustment/"],"constraints":"audit + RLS","output":"endpoint adjust"},
  {"step":334,"scope":"ctrl-cycle-count","context":"API numărătoare","task":"`CycleCountController` — plan/execuție numărătoare ciclice, toleranțe","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/inventory/"],"constraints":"eveniment `wms.inventory.adjusted` la final","output":"endpoint cycle-count"},
  {"step":335,"scope":"events-publish","context":"Bus v1","task":"Implementă publisher pentru `wms.*` cu idempotency key și `x-corr-id`","dirs":["/standalone/iwms/apps/api/src/services/bus/"],"constraints":"contract-tests bus","output":"publishers iWMS"},
  {"step":336,"scope":"events-consume-so","context":"Integrare Sales","task":"Consumer `sales.order.created` → `AllocService` + `PickingController` create","dirs":["/standalone/iwms/apps/api/src/services/bus/"],"constraints":"retries/backoff; DLQ","output":"consume SO"},
  {"step":337,"scope":"events-consume-po","context":"Integrare Procurement","task":"Consumer `procurement.po.approved` → `ReceivingService` create GRN plan","dirs":["/standalone/iwms/apps/api/src/services/bus/"],"constraints":"DLQ + alert dacă invalid","output":"consume PO"},
  {"step":338,"scope":"events-contract-tests","context":"Conform F2","task":"Pact/contract tests pentru `wms.*` cu Sales/Procurement","dirs":["/standalone/iwms/tests/contract/event-bus/"],"constraints":"CI gate obligatoriu","output":"contract tests verzi"},
  {"step":339,"scope":"events-lint","context":"Conveții naming","task":"Integrează `scripts/cli/sync-topic-names.ts` și `lint-rmq.sh` pe iWMS","dirs":["/standalone/iwms/scripts/","/core/scripts/"],"constraints":"fail pe abateri","output":"naming validat"},
  {"step":340,"scope":"fe-layout","context":"FE skeleton","task":"AppBar/Drawer/Outlet + navigație dinamică furnizată de Admin Core `/v1/admin/nav`","dirs":["/standalone/iwms/apps/frontend/src/"],"constraints":"fallback static","output":"layout FE"},
  {"step":341,"scope":"fe-pages","context":"Pagini principale","task":"Pagini: Dashboard, Receiving, Putaway, Picking, Packing, Shipping, Inventory, Cycle-Count","dirs":["/standalone/iwms/apps/frontend/src/pages/"],"constraints":"routing lazy; split-chunks","output":"pagini FE"},
  {"step":342,"scope":"fe-rf-organisms","context":"PWA RF","task":"Organisme RF: `rf-receive`, `rf-putaway`, `rf-pick`, `rf-ship` (touch+scanner)","dirs":["/standalone/iwms/apps/frontend/src/organisms/"],"constraints":"a11y; tab order corect","output":"RF UI"},
  {"step":343,"scope":"fe-webvitals","context":"Perf & RUM","task":"Integrează web-vitals; expune LCP/FID/CLS în Prometheus (window.prometheusWebVitals)","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"LCP P75 ≤2.5s","output":"RUM activ"},
  {"step":344,"scope":"fe-offline-cache","context":"RF offline tolerant","task":"Workbox cache pentru rute RF; queue requests `background-sync`","dirs":["/standalone/iwms/apps/frontend/src/"],"constraints":"size SW ≤ 200KB","output":"PWA offline"},
  {"step":345,"scope":"fe-i18n","context":"Globalizare","task":"i18n cu fallback en/ro; dayjs timezone aware","dirs":["/standalone/iwms/apps/frontend/src/"],"constraints":"no dynamic eval","output":"i18n activ"},
  {"step":346,"scope":"fe-a11y-lint","context":"Accesibilitate","task":"eslint-plugin-jsx-a11y high rules + axe tests pe paginile RF","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"CI fail on error","output":"a11y enforced"},
  {"step":347,"scope":"fe-tests-unit","context":"Calitate FE","task":"Vitest unit pentru Layout, RF organisms, Inventory table (≥80% coverage)","dirs":["/standalone/iwms/apps/frontend/"],"constraints":"no flaky","output":"unit FE verde"},
  {"step":348,"scope":"fe-e2e","context":"Calitate E2E","task":"Playwright: recepție→putaway→pick→pack→ship (flow minimal)","dirs":["/standalone/iwms/apps/frontend-e2e/"],"constraints":"headless CI","output":"E2E FE verde"},
  {"step":349,"scope":"fe-health-widget","context":"Observabilitate UI","task":"Widget health status (Gateway, Admin, RMQ) cu poll 30s","dirs":["/standalone/iwms/apps/frontend/src/widgets/health/"],"constraints":"AbortController 3s","output":"health widget"},
  {"step":350,"scope":"pdf-labels","context":"Documente/Etichete","task":"Endpoint API care publică `pdf.render` pentru etichete bin/item și pack list","dirs":["/standalone/iwms/apps/api/src/services/warehouse/doc/"],"constraints":"link MinIO SSE-C","output":"PDF generat"},
  {"step":351,"scope":"pdf-bol","context":"Expediții","task":"Generează BOL/packing slip via `pdf.render`; atașează la shipment","dirs":["/standalone/iwms/apps/api/src/services/warehouse/doc/"],"constraints":"cosign images","output":"BOL/packing slip"},
  {"step":352,"scope":"ocr-grn","context":"Recepție automată","task":"Integrează `ocr` pentru matching GRN cu documente furnizor (număr PO, linii, cantități)","dirs":["/standalone/iwms/apps/workers/ocr.adapter/"],"constraints":"confidențialitate; fără upload extern","output":"OCR recepție"},
  {"step":353,"scope":"labels-ui","context":"UI documente","task":"UI pentru generare/previzualizare etichete + tipar lot/serie","dirs":["/standalone/iwms/apps/frontend/src/pages/shipping/"],"constraints":"MUI DataGrid Pro","output":"UI etichete"},
  {"step":354,"scope":"minio-sse-c","context":"Securitate storage","task":"Config SSE-C (AES-256-GCM) pentru toate documentele iWMS; rotație chei la 90 zile","dirs":["/standalone/iwms/infra/k8s/external-secrets/","/standalone/iwms/apps/api/src/config/"],"constraints":"Vault CMK; fără chei în repo","output":"SSE-C activ"},
  {"step":355,"scope":"doc-audit","context":"Audit trail","task":"Persistă hash doc (BOL/labels) în jurnal `stock_tx`; verificare integritate","dirs":["/standalone/iwms/apps/api/src/services/warehouse/doc/"],"constraints":"sha256","output":"audit doc"},
  {"step":356,"scope":"doc-webhooks","context":"Distribuție","task":"Webhook post-ship către Sales cu URL documente sigure (expirare)","dirs":["/standalone/iwms/apps/api/src/services/warehouse/doc/"],"constraints":"signed URLs","output":"webhook trimis"},
  {"step":357,"scope":"forecast-contract","context":"Integrare worker","task":"Definește contract API ↔ worker `forecast` (input: sales history, lead time; output: ROP, SS)","dirs":["/standalone/iwms/apps/workers/forecast.adapter/"],"constraints":"Ray cluster; timeouts","output":"contract definit"},
  {"step":358,"scope":"forecast-cron","context":"Planificare","task":"Cron zilnic pentru recomput ROP/SS pe iteme active; publish `ai.stock.forecasted`","dirs":["/standalone/iwms/apps/workers/forecast.adapter/","/standalone/iwms/infra/k8s/"],"constraints":"cooldown 24h","output":"forecast zilnic"},
  {"step":359,"scope":"forecast-ui","context":"UI replenishment","task":"Pagină „Replenishment" cu ROP/SS, propuneri PO/transfer între depozite","dirs":["/standalone/iwms/apps/frontend/src/pages/"],"constraints":"export CSV","output":"UI ROP/SS"},
  {"step":360,"scope":"forecast-approve","context":"Execuție","task":"Endpoint POST `/replenishment/approve` → publică evenimente spre Procurement pentru PO draft","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/"],"constraints":"RBAC; idempotent","output":"PO draft events"},
  {"step":361,"scope":"forecast-metrics","context":"Observabilitate AI","task":"OTEL spans + Prom metrics (MAPE, service time) pentru forecast pipeline","dirs":["/standalone/iwms/apps/workers/forecast.adapter/"],"constraints":"grafana labels `tid,mid`","output":"metrici forecast"},
  {"step":362,"scope":"forecast-backfill","context":"Bootstrap","task":"Task backfill istoric 12 luni din Sales pentru inițializare model","dirs":["/standalone/iwms/apps/workers/forecast.adapter/"],"constraints":"rate-limit RMQ","output":"backfill rulat"},
  {"step":363,"scope":"forecast-abtest","context":"Calibrare","task":"AB test 2 politici (ROP clasic vs ROP+SS AI); KPI stockout rate","dirs":["/standalone/iwms/tests/k6/","/infra/grafana/"],"constraints":"experimente etichetate","output":"raport abtest"},
  {"step":364,"scope":"transfer-suggestions","context":"Multi-warehouse","task":"Sugestii transfer cross-warehouse bazat pe surplus/deficit + lead time","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"eveniment `wms.transfer.suggested`","output":"transfer propus"},
  {"step":365,"scope":"putaway-rules","context":"Îmbunătățiri","task":"Reguli putaway configurabile (zone hazard, heavy, fast-movers) din Admin Core","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"config map RBAC","output":"putaway rules"},
  {"step":366,"scope":"wave-heuristics","context":"Optimizare","task":"Heuristici wave: clusterizare pe zone/adâncime bin, batch picking","dirs":["/standalone/iwms/apps/api/src/services/warehouse/wave/"],"constraints":"latency < 200ms","output":"wave optim"},
  {"step":367,"scope":"slotting-report","context":"Vizibilitate","task":"Raport heatmap slotting (turnover×distance); widget Grafana custom","dirs":["/standalone/iwms/infra/grafana/provisioning/dashboards/"],"constraints":"uid `iwms_slotting`","output":"dashboard slotting"},
  {"step":368,"scope":"returns-flow","context":"Reverse logistics","task":"Flow retururi: RMA → recepție → sortare (restock/scrap)","dirs":["/standalone/iwms/apps/api/src/controllers/warehouse/","/standalone/iwms/apps/frontend/src/pages/"],"constraints":"evenimente retur","output":"flow retur"},
  {"step":369,"scope":"quality-hold","context":"Calitate","task":"Statut `quality_hold` pe stoc; blocare alocare până la eliberare","dirs":["/standalone/iwms/apps/api/src/entities/"],"constraints":"RBAC","output":"hold calitate"},
  {"step":370,"scope":"cycle-count-policy","context":"Inventar continuu","task":"Politici ABC pentru numărătoare ciclice; planificator zilnic","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"alert devieri >2%","output":"plan CC"},
  {"step":371,"scope":"fe-kpi-widgets","context":"KPI operaționali","task":"Widgets KPI (pick rate, dock-to-stock, order-to-ship)","dirs":["/standalone/iwms/apps/frontend/src/widgets/kpi/"],"constraints":"Loki/LokiQL pentru logs","output":"widgets KPI"},
  {"step":372,"scope":"k6-scenarios","context":"Perf KPI","task":"k6: 100 RPS pe `/picklists` p95<250ms; 50 RPS `/grn`","dirs":["/standalone/iwms/tests/k6/"],"constraints":"grafana datasource","output":"raport k6"},
  {"step":373,"scope":"rmq-autoscale","context":"Backlog","task":"KEDA ScaledObject pe cozi `wms.*` (queueLength ≥ 100)","dirs":["/standalone/iwms/infra/helm/","/standalone/iwms/infra/k8s/"],"constraints":"cooldown 120s","output":"autoscaling cozi"},
  {"step":374,"scope":"hpa-api","context":"Autoscale API","task":"HPA CPU 50–500m pe iWMS API","dirs":["/standalone/iwms/infra/helm/iwms-api/"],"constraints":"chart semnat cosign","output":"HPA activ"},
  {"step":375,"scope":"observability-metrics","context":"SLO iWMS","task":"Expune `/metrics` Nest + dashboards Grafana (Order-to-Ship, Dock-to-Stock)","dirs":["/standalone/iwms/apps/api/","/standalone/iwms/infra/grafana/"],"constraints":"UID `iwms_o2s`","output":"dashboards SLO"},
  {"step":376,"scope":"observability-traces","context":"OTEL full-chain","task":"Trace frontend→API→RMQ→worker→API; propagate `traceparent`","dirs":["/standalone/iwms/apps/frontend/","/standalone/iwms/apps/api/"],"constraints":"Tempo 2","output":"traces vizibile"},
  {"step":377,"scope":"observability-logs","context":"Logging unificat","task":"Nest pino + structlog; Loki labels `tid,mid,whid,trace_id`","dirs":["/standalone/iwms/apps/api/","/standalone/iwms/apps/workers/"],"constraints":"30 zile hot, 365 cold","output":"logs centralizate"},
  {"step":378,"scope":"alerts-slo","context":"Alerting","task":"Alertmanager reguli: SLO burn, RMQ lag, `wms.*` failure rate ≥1%","dirs":["/standalone/iwms/infra/k8s/alertmanager/"],"constraints":"rute Slack/Email","output":"alerte active"},
  {"step":379,"scope":"synthetic-checks","context":"Nightly","task":"GitHub Actions rulează k6 + blackbox exporter; push metrics","dirs":["/.github/workflows/","/standalone/iwms/tests/k6/"],"constraints":"no secrets leak","output":"synthetic OK"},
  {"step":380,"scope":"security-jwt","context":"API security","task":"Verifică claims `tid,whid,scp,role` pe toate endpoint-urile; deny by default","dirs":["/standalone/iwms/apps/api/src/guards/"],"constraints":"unit tests","output":"JWT enforced"},
  {"step":381,"scope":"security-opa","context":"Admission policies","task":"OPA Gatekeeper templates + constraints pentru imagini fără `latest` și resurse corecte","dirs":["/standalone/iwms/infra/policies/opa/"],"constraints":"mode warn dev","output":"OPA activ"},
  {"step":382,"scope":"security-waf","context":"Perimetru","task":"Traefik WAF + OWASP CRS v4 + rate-limit Redis (10 req/s user)","dirs":["/core/infra/helmfile/","/standalone/iwms/infra/helm/"],"constraints":"fără bypass","output":"WAF activ"},
  {"step":383,"scope":"security-sbom","context":"Supply-chain","task":"SBOM Syft + semnare imagini cosign + verify pe deploy","dirs":["/.github/workflows/","/standalone/iwms/docker/"],"constraints":"fail pe verify","output":"SBOM + sign"},
  {"step":384,"scope":"security-trivy","context":"Container scan","task":"Trivy OS+deps; fail CI pe HIGH","dirs":["/.github/workflows/module-ci-iwms.yml"],"constraints":"exit code 1 HIGH","output":"scan enforced"},
  {"step":385,"scope":"secrets-eso","context":"Secrets mgmt","task":"External Secrets Operator pentru RMQ/PG/MinIO; intergire IRSA","dirs":["/standalone/iwms/infra/k8s/external-secrets/"],"constraints":"least-privilege","output":"secrete injectate"},
  {"step":386,"scope":"data-retention","context":"Compliance","task":"Politici retenție loguri/doc: 30z hot, 365z cold; lifecycle MinIO","dirs":["/standalone/iwms/infra/helm/","/standalone/iwms/infra/k8s/"],"constraints":"no PII leak","output":"retenție aplicată"},
  {"step":387,"scope":"rls-tests","context":"Security tests","task":"Test integrare RLS: acces încrucișat tid/whid respins","dirs":["/standalone/iwms/apps/api/tests/"],"constraints":"e2e verde","output":"RLS validat"},
  {"step":388,"scope":"perf-db","context":"Tuning PG","task":"Indexuri partiale & covering pe `stock_tx`, `picklines`; pool pgBouncer","dirs":["/standalone/iwms/apps/api/src/migrations/"],"constraints":"EXPLAIN validate","output":"DB optimizat"},
  {"step":389,"scope":"cache-redis","context":"TTFB API","task":"Cache Redis pentru `inventory/status` și `bin/availability`","dirs":["/standalone/iwms/apps/api/src/services/warehouse/"],"constraints":"TTL 30s; purge la update","output":"TTFB redus"},
  {"step":390,"scope":"helm-charts","context":"Deploy iWMS","task":"Charts `iwms-frontend`, `iwms-api`, `iwms-workers` + IngressRoute + ServiceMonitor","dirs":["/standalone/iwms/infra/helm/"],"constraints":"OCI push; cosign","output":"charts gata"},
  {"step":391,"scope":"argocd-apps","context":"CD","task":"Argo Application YAML pentru iWMS (dev/stage/prod)","dirs":["/standalone/iwms/infra/k8s/argocd/"],"constraints":"auto-sync off pe prod","output":"Argo sync"},
  {"step":392,"scope":"ci-nx","context":"CI build/test","task":"`nx affected -t lint,test,build` pentru FE/API; upload coverage Codecov","dirs":["/.github/workflows/module-ci-iwms.yml"],"constraints":"fail on warn","output":"CI complet"},
  {"step":393,"scope":"dockerfiles","context":"Containerizare","task":"Dockerfile FE (vite build → Nginx non-root), API (Nest multi-stage)","dirs":["/standalone/iwms/docker/"],"constraints":"user 1000; no root","output":"imagini OK"},
  {"step":394,"scope":"postman","context":"Testare manuală","task":"Exportă colecție Postman iWMS în `docs/postman/iwms.json`","dirs":["/standalone/iwms/docs/postman/"],"constraints":"v2.1","output":"postman colecție"},
  {"step":395,"scope":"handover-doc","context":"Transmitere","task":"`docs/handovers/F2_iwms_handover.md` cu instrucțiuni de runbook","dirs":["/standalone/iwms/docs/handovers/"],"constraints":"actualizat la fiecare release","output":"handover gata"},
  {"step":396,"scope":"e2e-o2c","context":"Gate F2 O2C","task":"Test E2E: Lead→SO (Sales)→Pick→Ship (iWMS)→Invoice→Payment; verifică evenimentele","dirs":["/standalone/iwms/tests/e2e/","/standalone/mercantiq/"],"constraints":"timeout 3 min","output":"O2C reușit"},
  {"step":397,"scope":"e2e-p2p","context":"Gate F2 P2P","task":"Test E2E: RFQ→PO (Procurement)→GRN (iWMS)→3WM→Supplier Invoice","dirs":["/standalone/iwms/tests/e2e/","/standalone/mercantiq/"],"constraints":"deviație ≤2%","output":"P2P reușit"},
  {"step":398,"scope":"gate-slo","context":"Gate SLO","task":"Verifică p95<250ms, error_rate<1% pentru principalele endpoint-uri","dirs":["/standalone/iwms/infra/grafana/"],"constraints":"CI gate obligatoriu","output":"SLO ok"},
  {"step":399,"scope":"release-cut","context":"Release management","task":"Tag semnat, SBOM atașat, imagini semnate, changelog generat; Argo sync stage","dirs":["/.github/workflows/","/standalone/iwms/"],"constraints":"cosign verify on deploy","output":"release F2 iWMS"}
]
```

---

### Note & aliniere la documentația suitei

* **Event‑Bus & convenții v1:** nume evenimente `module.ctx.event` (ex.: `wms.picklist.created`, `wms.grn.posted`, `wms.inventory.adjusted`).
* **Stack & căi canonice:** UI/API pe stack fix, proiecte sub `standalone/iwms/...` (lint‑paths blochează `apps/...`).
* **Workeri disponibili & Registry:** `forecast`, `pdf.render`, `ocr`, `email.send`, `match.ai` cu health & traces vizibile prin Worker Registry/Tempo.
* **Date & securitate:** multitenancy pe PG/MinIO/Redis, RLS pe `tid/whid`, SSE‑C pe MinIO, JWT RS256 cu claims standard.
* **Observabilitate:** Prometheus metrics, Loki logs, Tempo traces, dashboards SLO, alerte queue lag/erroare.
* **Gate F2 ➜ F3:** O2C < 3 min, P2P complet, SLO p95 < 250 ms, erori < 1 %.

> Această versiune implementează **logica stand‑alone** a aplicației iWMS v3 și integrează **bi‑direcțional** cu suita (Sales pentru picking, Procurement pentru GRN), extinzând capabilitățile de automatizare AI (forecast pentru ROP/SS, wave optimization), RF support cu PWA offline și operațiuni WMS complete – aliniat cu principiile și standardele tehnice ale GeniusERP Suite.

## 9) Note de implementare

* **Căi canonice & arbore directoare**: folosește exact structura indicată pentru standalone apps (`standalone/iwms/apps/`); nu devia la `/apps` fără prefix `standalone/`.
* **Evenimente & naming**: menține convențiile v1 și validează în CI cu `lint-rmq.sh`. Format: `wms.picklist.created`, `wms.grn.posted`, `wms.inventory.adjusted`.
* **Workeri**: integrează‑te cu workers existenți (forecast, pdf.render, ocr) fără a schimba stack‑ul lor (Python 3.13 + Ray/Celery).
* **Multitenancy/RLS**: izolare strictă `tid/whid/mid` conform modelului de date Fazei F2.
* **RF Interface**: implementarea PWA trebuie să fie robustă cu cache offline și sincronizare automată.
* **Order‑to‑Cash & Procure‑to‑Pay**: fluxurile complete trebuie validate E2E cu toate evenimentele în succesiune.
* **AI Integration**: integrarea cu worker‑ul `forecast` pentru ROP/SS este obligatorie și trebuie să fie performantă.
* **Wave Optimization**: algoritmi de wave planning cu heuristici de optimizare pentru eficiență operațională.
* **CI/CD**: Trivy HIGH, cosign sign/attest, Argo sync, canary + rollback metric‑based conform umbrele F2.
* **Observabilitate**: traces end‑to‑end, metrics per‑tenant și per‑warehouse, dashboards O2C/P2P, alerte pentru devieri operaționale.

---

## 10) Dependențe externe și API keys

Pentru funcționarea completă a integrărilor, sunt necesare următoarele configurații via ExternalSecrets:

* **Warehouse scanners**: configurări pentru integrare RF devices și barcode scanners
* **Courier APIs**: integrări pentru AWB și tracking (Fan, DHL, UPS)
* **Label printers**: configurații Zebra/Datamax pentru printing workflows
* **SMTP**: configurare server pentru notificări și alerte operaționale
* **Slack/Teams**: webhook URL pentru notificări warehouse și escalări
* **AI Services**: configurări pentru worker‑ul `forecast` și optimizări
* **OCR Services**: configurații pentru procesarea documentelor furnizor
* **Database**: credențiale PostgreSQL + pgvector per tenant pentru RLS și AI

Toate acestea trebuie configurate prin Kubernetes ExternalSecrets, nu hardcodate în aplicație.

---

## 11) KPI & Gate F2 → F3 (iWMS)

### **Criterii de trecere Gate F2:**

* **O2C & P2P E2E reușite** pe 1 tenant demo sub 3 minute, cu evenimente confirmate la fiecare hop
* **SLO API**: p95 < 250 ms, error_rate < 1% pe endpoint‑urile critice (picking, wave, inventory)
* **Observabilitate completă**: dashboards & alerte pentru O2C, P2P, RMQ lag, task failure ≥1%
* **Securitate**: JWT claims & RLS pe toate tabelele; MinIO SSE‑C activ, OPA/Gatekeeper în cluster
* **AI Integration**: forecast working pentru ROP/SS, wave optimization functional
* **RF Support**: PWA offline cache working, background sync operational
* **Multi‑warehouse**: transfer suggestions și cross‑warehouse capabilities demonstrabile

### **Demonstrație finală:**

1. **Flux O2C complet**: Sales Order → Allocation → Wave → Pick → Pack → Ship → Confirmation
2. **Flux P2P complet**: PO Approved → GRN Plan → Receiving → Putaway → Stock Available
3. **AI Capabilities**: Forecast predictions, wave optimization, transfer suggestions working
4. **Performance validation**: toate SLO‑urile respectate sub încărcare normală
5. **Security validation**: RLS working, JWT enforcement, audit trails complete

---

> Această versiune implementează **iWMS v3** ca sistemul central WMS cu capabilități avansate AI, RF support complet, PWA offline și interoperabilitate maximă cu suita GeniusERP, respectând totodată principiile de securitate, observabilitate și scalabilitate ale platformei.
