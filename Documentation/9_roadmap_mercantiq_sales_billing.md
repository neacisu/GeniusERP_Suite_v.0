# 9 · Roadmap Mercantiq Sales & Billing – **versiune upgradată** (workeri + integrare suita)

> **Scop:** să transformăm **Mercantiq Sales & Billing** în cea mai modernă aplicație de **sales, billing & POS** din suita GeniusERP – cu integrare profundă de **workeri** (tax/vat, e‑Factura, PDF, e‑mail, Slack, Shopify, SAF‑T, Oblio) și interoperabilitate **suite & stand‑alone** cu **CRM (Vettify)**, **iWMS**, **Procurement** și, ulterior, **Accounting**.

> **Stack fix:** React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workers), RMQ 3.14 + Redis 7 (bus), Terraform + Helmfile + ArgoCD (deploy). Respectă convențiile de nume evenimente `module.ctx.event`. Folosește doar căile canonice `standalone/mercantiq/...`.

> **Gate F2 ➜ F3:** flux **Order‑to‑Cash** E2E < 3 min, evenimente confirmate; SLO API p95 < 250 ms, error\_rate < 1 %.

## Cum să folosești această documentație

Această documentație reprezintă un roadmap detaliat și upgradat pentru dezvoltarea aplicației stand-alone Mercantiq Sales & Billing (Order-to-Cash + POS) cu integrări extinse de workeri și interoperabilitate completă cu suita GeniusERP. Lista de pași este organizată sub formă de obiecte JSON, fiecare element corespunzând unei etape concrete de implementare.

**Parcurge pașii în ordine:** Fiecare element JSON are un câmp step (indexul pasului) și descrie o acțiune ce trebuie realizată. Pașii sunt organizați în două secțiuni: **F2 core (320–399)** pentru funcționalitatea de bază și **F2‑EXT (900–939)** pentru funcționalități avansate și scalare.

**Înțelege structura câmpurilor:** Fiecare obiect conține câmpuri esențiale – scope indică sub-sistemul sau componenta vizată, context oferă detalii despre starea proiectului înainte de acest pas, task descrie în mod imperativ acțiunea de efectuat, dirs precizează directoarele/proiectele afectate, constraints enumeră reguli sau condiții ce trebuie respectate, iar output descrie pe scurt rezultatul așteptat.

**Respectă constraints:** Câmpul constraints include cerințe stricte precum respectarea convențiilor de commit (Conventional Commits), rularea linter-elor, integrarea cu External Secrets pentru credențiale, și condiții de performanță și securitate.

**Navighează după scope:** Pașii sunt grupați logic prin câmpul scope (ex. "sales-…", "pos-…", "invoice-…", "efactura-…", "shopify-…"). Poți prioritiza sau delega anumite sub-sisteme pe baza acestei clasificări.

## 1) Pre‑condiții & Scope

* **Gate F1 trecut**: Shell vizibil (3 widget‑uri), Admin Core & Worker Registry verzi.
* **Event‑Bus v1** și naming `<module>.<ctx>.<event>` deja stabilite; hook `scripts/lint-rmq.sh` obligatoriu.
* **Multitenancy & date**: PostgreSQL 17 (cluster per tenant, schema per modul), MinIO per tenant, Redis per tenant, **RLS pe `tid/whid/mid`**.
* **Worker Fleet** disponibil: `pdf.render`, `tax.vat`, `notify.slack`, `email.send`, `match.ai`, `forecast`, `ai.summary`, `ai.classify`.
* **Stack fix**: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workeri), RabbitMQ 3.14 + Redis 7 (bus/queue), IaC: Terraform + Helmfile + Argo CD.

## 2) Bounded‑Context & Interfețe

### **Entități principale**
* **Customers**: clienți pentru comenzi și facturare cu lookup ANAF automat
* **Products**: produse cu prețuri în liste configurabile și coduri EAN
* **SalesOrders**: comenzi de vânzare cu linii detaliate și calcul taxe automat
* **Invoices**: facturi emise cu suport e-Factura ANAF și validare fiscală
* **Payments**: plăți înregistrare cu suport parțial și metode multiple

### **Evenimente publicate**
* **`sales.order.created`**: comandă nouă plasată
* **`sales.invoice.issued`**: factură emisă după livrare cu detalii fiscale
* **`payment.received`**: plată înregistrată pentru factură

### **Evenimente consumate**
* **`wms.picklist.completed`**: trigger pentru generare factură automată
* **`tax.vat.validated`**: confirmare validare ANAF
* **`pdf.render.done`**: PDF factură finalizat
* **`anaf.efactura.status`**: status e-Factura din SPV
* **`crm.opportunity.stage_changed`**: conversie CRM → Sales Order

### **Workeri integrați**

**Fleet existentă:**
* `pdf.render` - generare PDF facturi cu branding per tenant
* `email.send` - trimitere facturi către clienți 
* `notify.slack` - notificări plăți și evenimente critice
* `tax.vat` - validare fiscală și conformitate ANAF
* `match.ai`, `forecast`, `ai.summary`, `ai.classify` - funcționalități AI

**Noi conectori Sales-orientați:**
* `anaf.taxpayer` - lookup client după CUI cu date actualizate
* `anaf.efactura` - submit e-Factura către SPV ANAF
* `anaf.saft` - export SAF‑T pentru raportare fiscală
* `sync.shopify` - sincronizare bidirecțională cu magazin online
* `oblio.fiscal.receipt` - emitere bonuri fiscale prin case de marcat

## 3) Arhitectura Aplicației

### **Mercantiq Sales & Billing Overview**

Mercantiq Sales & Billing devine cea mai avansată aplicație de sales și billing din suita GeniusERP, cu integrări profunde de workeri pentru automatizarea completă a fluxului Order-to-Cash. Aplicația acoperă:

- **Flux O2C complet**: de la oportunitate CRM la încasare cu automatizare maximă
- **Conformitate fiscală**: e-Factura ANAF, SAF-T, validare TVA automată  
- **POS avansat**: offline-first cu sincronizare, periferice hardware, bonuri fiscale
- **E-commerce**: integrare bidirecțională Shopify cu stoc și comenzi
- **Inteligență artificială**: detecție anomalii, scoring fraud, sumarizare automată

### **Integrarea cu Ecosistemul**

Prin integrările extinse, modulul conectează:
- **CRM (Vettify)**: oportunități câștigate → comenzi automate
- **iWMS v3**: livrări → facturare automată + fulfillment e-commerce  
- **Procurement**: stoc insuficient → RFQ automat
- **Worker Registry**: orchestrare inteligentă a tuturor serviciilor

### **Conformitate și Securitate**

- **ANAF e-Factura**: submit automat după 4 zile cu retry
- **SAF-T**: export lunar programat cu validare XSD
- **Audit trail**: Merkle trees pentru non-repudiation
- **GDPR**: export self-service și data masking

## 4) Securitate & RBAC

* Scopes Keycloak `sales/*` cu roluri granulare (cashier, sales-ops, sales-admin)
* Guard JWT RS256 + RLS pe toate tabelele pentru izolare multi-tenant
* ABAC la UI cu permisiuni fine pe funcționalități
* Rate limiting per rol și throttling anti-abuz
* Audit log pentru toate deciziile RBAC

## 5) Observabilitate

* OTel traces end-to-end (browser→API→workers) cu propagare context
* Prometheus metrics (HTTP + business: orders, invoices, payments, efactura)
* Dashboard dedicat Order-to-Cash și per-tenant SLO monitoring  
* Alerting pentru SLO (p95 <250ms, error rate <1%, queue lag)
* Web Vitals collection pentru performance frontend

## 6) Criterii de Acceptanță F2

* **Flux O2C complet**: comandă → factură → plată în <3 minute
* **Conformitate ANAF**: e-Factură validată și emisă automat
* **Performance**: API p95 <250ms, error rate <1%
* **POS offline**: funcțional fără conexiune cu sync automat
* **Integrări**: evenimente publicate/consumate conform specificației
* **Shopify sync**: comenzi, stoc și fulfillment bidirecțional
* **Workeri activi**: PDF, email, tax, Slack, ANAF, Oblio

## 7) Structura Implementării

### **Interval F2**: 2-3 (4 SW)
- **Effort**: 4 săptămâni dezvoltare (extins pentru integrări)
- **Scop**: Mercantiq Sales & Billing complet cu toate integrările
- **Modul**: `mercantiq-sales` (frontend + api + workers integration)
- **Dependențe**: F1 Core Platform + F2 Base Workers + External APIs

## 8) CursorAI Prompts (Mercantiq Sales & Billing 320–399 + 900–939)

> **Format obligatoriu:** `step`, `scope`, `context`, `task`, `dirs`, `constraints`, `output` (identic F0/F1). **Nu hard‑coda secrete**, folosește External Secrets. **Căi canonice** `standalone/mercantiq/**` (lint‑paths blochează vechile `/apps/...`).

```json
[
  {"step":320,"scope":"sales-scaffold","context":"Monorepo Nx & Shell gata (F0/F1); modul inexistent","task":"Generează proiectele Mercantiq Sales (frontend React+Vite remote, API NestJS) sub `standalone/mercantiq/apps/sales/`. Activează Module Federation și remoteEntry.","dirs":["/standalone/mercantiq/apps/sales/frontend/","/standalone/mercantiq/apps/sales/api/"],"constraints":"scripts/create-module.ts --standalone mercantiq; tags Nx `module:mercantiq-sales,layer:frontend|api`; commit 'feat(mercantiq-sales): scaffold'.","output":"skeleton FE+API"},
  {"step":321,"scope":"db-migrations-base","context":"Schema Sales inexistentă","task":"Creează migration init pentru: customers, products, price_lists, price_list_items, sales_orders, sales_order_lines, invoices, payments. Adaugă coloane multi-tenant `tid`,`whid` și audit `created_at`,`updated_at`.","dirs":["/standalone/mercantiq/apps/sales/api/src/migrations/"],"constraints":"UUID PK; numeric(18,4) pentru sume; FK stricte; commit 'feat(sales-db): init schema'.","output":"tabele create"},
  {"step":322,"scope":"db-migrations-tax-efactura","context":"Necesare atribute fiscale","task":"Adaugă câmpuri fiscale pe invoices: `series`,`number`,`currency`,`vat_amount`,`efactura_xml_path`,`efactura_status`(enum draft|queued|submitted|accepted|rejected),`efactura_submitted_at`,`pdf_path`,`validated_vat` boolean, `anaf_errors` jsonb.","dirs":["/standalone/mercantiq/apps/sales/api/src/migrations/"],"constraints":"index pe (tid,efactura_status); commit 'feat(sales-db): tax & eFactura fields'.","output":"coloane fiscale & indexuri"},
  {"step":323,"scope":"db-rls-policies","context":"PG multi-tenant; securitate dată","task":"Activează RLS pe toate tabelele și politici `tid = current_setting('app.tid') AND (whid = current_setting('app.whid') OR whid IS NULL)`; set session vars din JWT.","dirs":["/standalone/mercantiq/apps/sales/api/src/db/"],"constraints":"respectă RLS model din suita; commit 'feat(sales-db): rls policies'.","output":"RLS activ pe schema Sales"},
  {"step":324,"scope":"customers-api","context":"Tabel customers creat","task":"CRUD Customers (GET/POST/PUT/DELETE) cu DTO validate (class-validator). Integrează lookup ANAF la create/update: publică job `client.lookup.anaf` cu CUI; la răspuns, precompletează denumire/adresă/TVA.","dirs":["/standalone/mercantiq/apps/sales/api/src/{controllers,services,dto,events}/"],"constraints":"JWT guard + scopes `sales.read|write`; test unit service ≥85%; commit 'feat(sales-api): customers + anaf lookup'.","output":"API customers + integrare ANAF"},
  {"step":325,"scope":"products-price-api","context":"Produse & prețuri necesare","task":"CRUD Products și PriceLists (+ items). GET /products include preț activ (join la lista implicită). Validări: price>=0; SKU unic per tenant.","dirs":["/standalone/mercantiq/apps/sales/api/src/{controllers,services,dto}/"],"constraints":"transactional la create product+price; commit 'feat(sales-api): products & price lists'.","output":"API products+prices"},
  {"step":326,"scope":"salesorder-api","context":"Tabele SO/lines gata","task":"POST /sales-orders (clientId, lines[{productId,qty,price?}]) → calculează subtotal/taxe/total folosind price list; GET list + GET by id; status inițial NEW.","dirs":["/standalone/mercantiq/apps/sales/api/src/{controllers,services}/"],"constraints":"transacție ACID SO+lines; 400 dacă lipsă preț; commit 'feat(sales-api): sales order create/get'.","output":"API SalesOrders"},
  {"step":327,"scope":"event-publish-so","context":"Bus v1 activ; naming v1","task":"La creare SO emită `sales.order.created` cu payload (orderId, customerId, total, items).","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"un singur publish post-commit; contract-test; commit 'feat(sales-events): sales.order.created'.","output":"event publicat"},
  {"step":328,"scope":"wms-consume-pick-complete","context":"Integrare iWMS","task":"Subscriber pentru `wms.picklist.completed` → găsește SO, marchează delivered și invocă emitere factură.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"idempotent; retry backoff; commit 'feat(sales-events): consume wms.picklist.completed'.","output":"autofacturare on delivery"},
  {"step":329,"scope":"invoice-service","context":"Facturare după livrare","task":"Service & controller Invoice: POST /sales-orders/:id/invoice → creează 1:1 invoice din SO; GET /invoices/:id.","dirs":["/standalone/mercantiq/apps/sales/api/src/{controllers,services}/"],"constraints":"unică factură per SO; 409 dacă există; commit 'feat(sales-api): invoice service'.","output":"emitere factură"},
  {"step":330,"scope":"event-publish-invoice","context":"Eveniment factură","task":"După creare factură emite `sales.invoice.issued` (invoiceId, orderId, total, due_date).","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"nume eveniment conform; contract-test; commit 'feat(sales-events): sales.invoice.issued'.","output":"event publicat"},
  {"step":331,"scope":"tax-vat-validate","context":"Validare fiscală automată","task":"La `sales.invoice.issued` publică task către `tax.vat` (sau consumă direct eveniment dacă workerul ascultă). La răspuns `tax.vat.validated`, setează invoice.validated_vat și/anume erori.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"no secrete; log erori în audit; commit 'feat(sales-tax): vat validation pipeline'.","output":"invoice validat VAT"},
  {"step":332,"scope":"pdf-request","context":"PDF necesar clienți","task":"POST /invoices/:id/pdf → publică task `pdf.render` cu payload templating; setează pdf_status=processing.","dirs":["/standalone/mercantiq/apps/sales/api/src/controllers/"],"constraints":"async 202 Accepted; commit 'feat(sales-pdf): request endpoint'.","output":"cerere PDF trimisă"},
  {"step":333,"scope":"pdf-consume-done","context":"Worker PDF finalizează","task":"Subscriber `pdf.render.done` → salvează fișier în MinIO (SSE‑C), actualizează invoice.pdf_path & pdf_status=ready.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"SSE‑C key via Vault/ESO; commit 'feat(sales-pdf): consume done'.","output":"PDF atașat facturii"},
  {"step":334,"scope":"email-send-invoice","context":"Trimitere factură client","task":"La pdf_status=ready trimite job `email.send` cu atașament PDF către client (șablon HTML).","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"SMTP via ExternalSecret; retry; commit 'feat(sales-email): send invoice pdf'.","output":"factură expediată pe email"},
  {"step":335,"scope":"efactura-scheduler","context":"Politică: submit după 4 zile","task":"Job programat (cron) care selectează facturi `issued` ne-transmise >4 zile → publică task `anaf.efactura.submit`.","dirs":["/standalone/mercantiq/apps/sales/api/src/jobs/"],"constraints":"folosește bull/cron; timezone UTC; commit 'feat(sales-efactura): scheduler 4 days'.","output":"coadă submit ANAF"},
  {"step":336,"scope":"efactura-consume-status","context":"Răspuns SPV/ANAF","task":"Subscriber `anaf.efactura.status` → actualizează `efactura_status` (submitted/accepted/rejected), salvează `efactura_xml_path` & `anaf_errors` la nevoie.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"idempotent; audit trail; commit 'feat(sales-efactura): status consumer'.","output":"status e-Factura urmărit"},
  {"step":337,"scope":"payments-api","context":"Înregistrare plăți","task":"POST /invoices/:id/payments (sumă, metodă) → update invoice.Paid dacă acoperă total; GET /payments recent.","dirs":["/standalone/mercantiq/apps/sales/api/src/{controllers,services}/"],"constraints":"validări sumă>0, invoice existent; commit 'feat(sales-pay): payments api'.","output":"plată înregistrată"},
  {"step":338,"scope":"event-publish-payment","context":"Notificare încasare","task":"Emite `payment.received` la creare plată (paymentId, invoiceId, amount).","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"post-commit; contract-test; commit 'feat(sales-events): payment.received'.","output":"event publicat"},
  {"step":339,"scope":"notify-slack","context":"Vizibilitate cash-flow","task":"La `payment.received` publică job `notify.slack` cu mesaj standardizat (#finance).","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"webhook via secret; commit 'feat(sales-slack): payment notifications'.","output":"notificări Slack trimise"},
  {"step":340,"scope":"frontend-pos","context":"UI POS necesar","task":"Implementează `PosTerminalPage` (scan/alege produs, coș, select client, submit). Integrează cu /sales-orders + /payments.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/{pages,components/pos}/"],"constraints":"UX rapid; vitest cov ≥80%; commit 'feat(sales-ui): POS terminal'.","output":"POS MVP"},
  {"step":341,"scope":"pos-offline-store","context":"Vânzare offline","task":"Implementă `OfflineOrderQueue` (IndexedDB) pentru buffer comenzi când navigator.offline.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/utils/"],"constraints":"persistență; PII minim; commit 'feat(sales-ui): offline queue'.","output":"buffer offline comenzi"},
  {"step":342,"scope":"pos-offline-sync","context":"Reconectare","task":"Listener `online` → re-trimite cozile în ordinea inițială, cu backoff la eșec.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/utils/"],"constraints":"log dev-only; commit 'feat(sales-ui): offline sync'.","output":"auto-sync comenzi"},
  {"step":343,"scope":"oblio-config","context":"Bon fiscal prin Oblio","task":"Adaugă integrare Oblio: config endpoint & chei API prin ExternalSecret; structura payload bon.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/oblio/","/infra/k8s/externalsecrets/"],"constraints":"nu include chei în repo; commit 'feat(sales-oblio): config integration'.","output":"config integrare Oblio"},
  {"step":344,"scope":"oblio-receipt","context":"Tipărire bon la POS","task":"Endpoint /pos/receipt → cheamă Oblio API pentru bon; salvează număr bon & status în DB.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/oblio/"],"constraints":"retry & idempotent; commit 'feat(sales-oblio): fiscal receipt'.","output":"bon fiscal emis"},
  {"step":345,"scope":"shopify-scaffold","context":"Integrare e‑commerce","task":"Creează integrarea `sync.shopify` (service + webhook handlers): structură pentru orders, products, stock sync.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"Admin API keys via ESO; commit 'feat(sales-shopify): scaffold'.","output":"schelet integrare Shopify"},
  {"step":346,"scope":"shopify-webhooks","context":"Import comenzi","task":"Expune endpoint-uri webhook Shopify (orders/create, customers/create). La orders/create → mapare în SalesOrder.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"verifică HMAC; 202 Accepted; commit 'feat(sales-shopify): webhook orders'.","output":"SO create din Shopify"},
  {"step":347,"scope":"shopify-products-stock","context":"Catalog & stoc","task":"Job periodic push stock către Shopify; opțional sync produse & prețuri (ERP master).","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"respectă rate limits; commit 'feat(sales-shopify): stock & products sync'.","output":"stoc sincronizat"},
  {"step":348,"scope":"shopify-fulfillment","context":"Status livrare","task":"La livrare (WMS) → publish fulfillment către Shopify (tracking/AWB) + mark as fulfilled.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"retry; idempotent; commit 'feat(sales-shopify): fulfillment update'.","output":"status Shopify actualizat"},
  {"step":349,"scope":"shopify-invoice-link","context":"Transparență client","task":"După PDF ready → adaugă link factură în timeline Shopify (order note/attachment).","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"link presigned scurt; commit 'feat(sales-shopify): attach invoice link'.","output":"link factură în Shopify"},
  {"step":350,"scope":"awb-courier-bridge","context":"AWB auto","task":"Adapter generic curieri (Fan/DHL/etc.) sau via Oblio dacă disponibil → creează AWB la expediție, salvează nr.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/courier/"],"constraints":"secrete via ESO; commit 'feat(sales-courier): awb adapter'.","output":"AWB generat & salvat"},
  {"step":351,"scope":"api-security-guards","context":"JWT RS256; RBAC suite","task":"Extinde guards pentru claims `tid,whid,scp,role` + scope `sales.*`. Set session vars PG pentru RLS.","dirs":["/standalone/mercantiq/apps/sales/api/src/guards/"],"constraints":"unit tests; commit 'feat(sales-auth): rbac+rls guard'.","output":"endpoints securizate"},
  {"step":352,"scope":"otel-tracing","context":"Observabilitate E2E","task":"Activează OTEL în Sales API (HTTP, TypeORM, RMQ publish/consume). Propagă traceparent pe evenimente.","dirs":["/standalone/mercantiq/apps/sales/api/src/config/"],"constraints":"service.name=mercantiq-sales-api; commit 'feat(sales-otel): tracing'.","output":"traces în Tempo"},
  {"step":353,"scope":"prom-metrics","context":"KPI O2C","task":"Expune /metrics (http standard + counters business: sales_orders_total, invoices_issued_total, payments_total).","dirs":["/standalone/mercantiq/apps/sales/api/src/config/"],"constraints":"prefix mercantiq_sales_*; commit 'feat(sales-metrics): prometheus'.","output":"metrici Prometheus"},
  {"step":354,"scope":"grafana-dashboard-o2c","context":"Vizibilitate management","task":"Dashboard Grafana O2C (SO vs Invoices vs Payments), latente p95, 5xx rate, RMQ lag pdf/tax.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"UID unic; commit 'feat(obs): dashboard sales o2c'.","output":"dashboard O2C live"},
  {"step":355,"scope":"alerts-slo","context":"SLO F2","task":"Reguli Alertmanager: HighErrorRateSales (>1%/5m), SlowResponseSales (p95>250ms/5m), QueueBacklog (>50).","dirs":["/infra/prometheus/rules/","/infra/k8s/alertmanager/"],"constraints":"route → Slack/email; commit 'feat(obs): sales SLO alerts'.","output":"alerte active"},
  {"step":356,"scope":"helm-secrets","context":"Credențiale integrare","task":"ExternalSecret pentru: ANAF (SPV), Oblio, Shopify, SMTP; montează în pods API.","dirs":["/infra/k8s/externalsecrets/","/standalone/mercantiq/infra/helm/mercantiq-sales/"],"constraints":"niciun secret în repo; commit 'feat(infra): externalsecrets sales'.","output":"secrete montate"},
  {"step":357,"scope":"helm-chart","context":"Deploy K8s","task":"Chart Helm Mercantiq Sales (api, ui, ingress, HPA, ServiceMonitor).","dirs":["/standalone/mercantiq/infra/helm/mercantiq-sales/"],"constraints":"OCI push + cosign; commit 'feat(helm): mercantiq-sales chart'.","output":"chart publicat"},
  {"step":358,"scope":"argocd-app","context":"CD automat","task":"Definiție ArgoCD app mercantiq-sales (namespace dedicat, sync auto).","dirs":["/infra/k8s/argocd/apps/"],"constraints":"health checks; commit 'feat(argocd): mercantiq-sales app'.","output":"Argo sync ok"},
  {"step":359,"scope":"ci-pipeline","context":".github workflows existente","task":"CI pentru Sales: build FE/API, test, Trivy HIGH, Syft SBOM, cosign sign, push images & Helm; Argo sync dev.","dirs":["/.github/workflows/"],"constraints":"paths `standalone/**`; commit 'ci(sales): add pipeline'.","output":"CI verde"},
  {"step":360,"scope":"contract-tests-bus","context":"Conveții evenimente v1","task":"Teste contract pentru publish/subscribe: sales.order.created, sales.invoice.issued, payment.received, wms.picklist.completed.","dirs":["/standalone/mercantiq/apps/sales/api/tests/contracts/"],"constraints":"naming `<module>.<ctx>.<event>`; commit 'test(bus): sales contracts'.","output":"contracte verzi"},
  {"step":361,"scope":"k6-perf","context":"SLO latency","task":"k6 100 RPS pe POST /sales-orders (p95<250ms); raportează în Grafana.","dirs":["/standalone/mercantiq/tests/k6/"],"constraints":"datasource prom; commit 'perf(sales): k6 o2c'.","output":"raport k6"},
  {"step":362,"scope":"swagger-docs","context":"Dev UX","task":"Activează Swagger `/docs` cu basic-auth; include DTO, examples.","dirs":["/standalone/mercantiq/apps/sales/api/src/"],"constraints":"version din package; commit 'feat(api-docs): swagger'.","output":"API docs online"},
  {"step":363,"scope":"postman-collection","context":"QA & demo","task":"Exportă colecție Postman pentru Sales (customers, products, SO, invoices, payments).","dirs":["/docs/postman/"],"constraints":"v2.1; commit 'docs(postman): sales collection'.","output":"postman JSON"},
  {"step":364,"scope":"frontend-orders-page","context":"UI management comenzi","task":"`SalesOrdersPage` (list, filter status, download invoice).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/{pages,components/orders}/"],"constraints":"DataGrid; commit 'feat(sales-ui): orders page'.","output":"listare comenzi"},
  {"step":365,"scope":"frontend-invoice-download","context":"PDF ready","task":"Buton Download Invoice consumând GET /invoices/:id/pdf (sau presigned URL).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/components/orders/"],"constraints":"loader + errors; commit 'feat(sales-ui): invoice download'.","output":"descărcare PDF"},
  {"step":366,"scope":"returns-credit-notes","context":"Operațiuni post‑vânzare","task":"Model & API pentru retururi și storno (credit notes) legate de facturi.","dirs":["/standalone/mercantiq/apps/sales/api/src/{entities,controllers,services}/"],"constraints":"consistență stoc cu iWMS; commit 'feat(sales): returns & credit notes'.","output":"retururi suportate"},
  {"step":367,"scope":"partial-payments","context":"Cazuri reale plăți","task":"Suport plăți parțiale + alocare sumă pe factură, calcul sold.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"precizie numerică; commit 'feat(sales): partial payments'.","output":"sold corect"},
  {"step":368,"scope":"aging-report","context":"Contabilitate light stand‑alone","task":"Raport Aging (30/60/90) din plăți/facturi.","dirs":["/standalone/mercantiq/apps/sales/api/src/reports/"],"constraints":"export CSV/XLSX; commit 'feat(sales-reports): aging'.","output":"raport aging"},
  {"step":369,"scope":"ai-anomaly-vat","context":"Conformitate proactivă","task":"Integrează `ai.classify/ai.anomaly` pe facturi pentru pattern-uri suspecte (TVA zero anormal etc.).","dirs":["/standalone/mercantiq/apps/sales/api/src/services/ai/"],"constraints":"no PII în prompt; commit 'feat(sales-ai): anomaly detection'.","output":"flag anomalii TVA"},
  {"step":370,"scope":"saft-export","context":"Stand‑alone legal","task":"Endpoint `POST /saft/export?period=YYYY-MM` → publică `anaf.saft.generate`; la done atașează fișier XML în MinIO.","dirs":["/standalone/mercantiq/apps/sales/api/src/controllers/","/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"SSE‑C; commit 'feat(sales-saft): export'.","output":"SAF‑T generat"},
  {"step":371,"scope":"crm-consume-opportunity","context":"Integrare Vettify","task":"Subscriber `crm.opportunity.stage_changed` (won) → creează SO din opportunity.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"idempotent; commit 'feat(sales-crm): consume won'.","output":"SO din CRM"},
  {"step":372,"scope":"crm-publish-sales","context":"Îmbogățire CRM","task":"La `sales.order.created` trimite event către CRM pentru timeline & scoring.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"payload minim; commit 'feat(sales-crm): publish sales'.","output":"CRM enrichment"},
  {"step":373,"scope":"procurement-low-stock","context":"Legătură cu achiziții","task":"La SO cu stoc insuficient → publică event pentru Procurement (ex: `procurement.rfq.created` draft).","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"nu crea PO automat în producție; commit 'feat(sales-proc): low stock rfq'.","output":"RFQ draft creat"},
  {"step":374,"scope":"pos-close-shift","context":"Operațiuni retail","task":"EOD POS: sumar Z (total vânzări, cash/card), export CSV, optional push Slack.","dirs":["/standalone/mercantiq/apps/sales/api/src/reports/"],"constraints":"rotunjiri corecte; commit 'feat(sales-pos): end of day'.","output":"raport închidere zi"},
  {"step":375,"scope":"minio-lifecycle","context":"Retention documente","task":"Policy lifecycle MinIO pentru facturi PDF/XML (ex: 5 ani) + object lock.","dirs":["/infra/storage/minio/"],"constraints":"conform local; commit 'feat(infra): minio lifecycle invoices'.","output":"retention aplicat"},
  {"step":376,"scope":"opa-policies","context":"Supply chain & sec","task":"OPA Gatekeeper: interzice imagini `:latest`, cere cosign verify pentru imagini Sales.","dirs":["/infra/policies/opa/"],"constraints":"mode warn dev; enforce prod; commit 'feat(sec): opa container policies'.","output":"policy activă"},
  {"step":377,"scope":"rate-limit-waf","context":"Protecție API","task":"Rate‑limit Redis token-bucket (10 req/s user, 1000 req/min IP) la gateway pentru rutele Sales.","dirs":["/infra/gateway/traefik/"],"constraints":"OWASP CRS on; commit 'feat(sec): rate limit sales'.","output":"abuz limitat"},
  {"step":378,"scope":"frontend-a11y-perf","context":"UX calitate","task":"eslint jsx-a11y + Lighthouse CI (score ≥90; LCP ≤2.5s).","dirs":["/standalone/mercantiq/apps/sales/frontend/","/.github/workflows/"],"constraints":"fail pipeline la score < target; commit 'chore(ui): a11y+perf gates'.","output":"gărzi UX active"},
  {"step":379,"scope":"frontend-storybook","context":"Catalog UI","task":"Storybook pentru componente POS/Orders; trei stories minime; upload artefact în CI.","dirs":["/standalone/mercantiq/apps/sales/frontend/"],"constraints":"CSF3; commit 'docs(ui): storybook sales'.","output":"storybook live"},
  {"step":380,"scope":"unit-tests-backend","context":"Acoperire logică","task":"Jest unit tests pentru Services critice (SO create, Invoice issue, Payment).","dirs":["/standalone/mercantiq/apps/sales/api/src/services/__tests__/"],"constraints":"cov≥85%; commit 'test(sales-api): units'.","output":"unit tests verzi"},
  {"step":381,"scope":"e2e-tests-backend","context":"Scenariu O2C","task":"Supertest E2E: customer+products → SO → WMS event → invoice → pdf → payment → eFactura queued.","dirs":["/standalone/mercantiq/apps/sales/api/test/e2e/"],"constraints":"DB sqlite mem; commit 'test(sales-api): e2e o2c'.","output":"e2e backend verde"},
  {"step":382,"scope":"e2e-tests-frontend","context":"Flux UI complet","task":"Playwright: login→POS vânzare→Orders vede factura→download PDF.","dirs":["/standalone/mercantiq/apps/sales/frontend-e2e/"],"constraints":"headless CI; data-test-id; commit 'test(sales-ui): e2e'.","output":"e2e frontend verde"},
  {"step":383,"scope":"shopify-e2e","context":"Integrare e‑comm","task":"Test E2E: webhook order→SO→WMS simulate→invoice→fulfillment update Shopify.","dirs":["/standalone/mercantiq/apps/sales/api/test/e2e/"],"constraints":"mocks Shopify HMAC; commit 'test(sales-shopify): e2e'.","output":"e2e shopify verde"},
  {"step":384,"scope":"efactura-e2e","context":"Conformitate ANAF","task":"Test E2E programat: emite 1 factură demo, rulează cron 4 zile simulate, verifică submit & status acceptat (mock).","dirs":["/standalone/mercantiq/apps/sales/api/test/e2e/"],"constraints":"no live ANAF; commit 'test(sales-efactura): e2e'.","output":"pipelines ANAF verzi"},
  {"step":385,"scope":"report-kpi-daily","context":"Management reporting","task":"Integrează worker `report.kpi` → PDF zilnic cu KPI vânzări în Slack.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/reports/"],"constraints":"program 08:00; commit 'feat(sales-report): daily kpi'.","output":"raport KPI zilnic"},
  {"step":386,"scope":"discounts-promotions","context":"Comercial","task":"Rule engine discounturi (cupoane, volume) aplicate la SO.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"test business rules; commit 'feat(sales): discounts engine'.","output":"discounturi suportate"},
  {"step":387,"scope":"multi-currency","context":"Piețe multiple","task":"Suport valute cu rate FX zilnice; calcul total în currency factură.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"surse FX via secret; commit 'feat(sales): multi-currency'.","output":"FX on invoices"},
  {"step":388,"scope":"roles-rbac-fine","context":"Securitate fină","task":"Roluri: cashier, sales-ops, sales-admin; mapare scopes pe rute.","dirs":["/standalone/mercantiq/apps/sales/api/src/guards/"],"constraints":"documentează; commit 'feat(sales-auth): roles'.","output":"RBAC granular"},
  {"step":389,"scope":"data-retention-logs","context":"Forensic & GDPR","task":"Loki labels `tid,mid,whid,trace_id`; retenție 30/365 zile; redaction PII.","dirs":["/infra/logging/loki/"],"constraints":"conform GDPR; commit 'feat(obs): loki tuning sales'.","output":"logging conform"},
  {"step":390,"scope":"theme-admin-nav","context":"Integrare Shell/Admin","task":"Adaugă în Admin Core nav entry 'Sales & Billing' (remote federation) + ThemeHub compat.","dirs":["/core/apps/admin-core/api/src/controllers/","/standalone/mercantiq/apps/sales/frontend/"],"constraints":"format JSON nav; commit 'feat(admin-nav): sales entry'.","output":"meniu în Shell"},
  {"step":391,"scope":"seed-f2-data","context":"Demo/Try‑out","task":"Script `scripts/seed-f2.ts` (customers, products, price list, demo orders).","dirs":["/core/scripts/"],"constraints":"nu include secrete; commit 'feat(seed): sales demo'.","output":"seed F2"},
  {"step":392,"scope":"tenants-onboarding","context":"Multi‑tenant","task":"Script bootstrap tenant cheamă Admin `/tenants` → creează cluster PG/bucket MinIO/realm; setări default Sales.","dirs":["/scripts/","/standalone/mercantiq/apps/sales/api/src/config/"],"constraints":"<60s target; commit 'feat(tenants): bootstrap sales'.","output":"onboarding rapid"},
  {"step":393,"scope":"waf-owasp-crs","context":"Perimetru","task":"Activează/afinare OWASP CRS pentru rutele Sales la Traefik.","dirs":["/infra/gateway/traefik/"],"constraints":"exclude false positives; commit 'chore(sec): owasp crs sales'.","output":"WAF activ"},
  {"step":394,"scope":"gdpr-export","context":"Legal","task":"Endpoint export date client (facturi proprii) la cerere (CSV/ZIP).","dirs":["/standalone/mercantiq/apps/sales/api/src/controllers/"],"constraints":"scop client; commit 'feat(sales-gdpr): export portal'.","output":"export self‑service"},
  {"step":395,"scope":"pos-card-integration","context":"Plăți card","task":"Adaptor gateway plăți (ex. Stripe/Netopia) pentru POS; marchează payment dacă succeeded.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/payments/"],"constraints":"PCI safe via provider; commit 'feat(sales-pos): card adapter'.","output":"card payments POS"},
  {"step":396,"scope":"shopify-returns","context":"RMA online","task":"Consumă webhook returns/refunds; creează credit note & update Shopify.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"policy retur; commit 'feat(sales-shopify): returns flow'.","output":"retururi sincronizate"},
  {"step":397,"scope":"gate-f2-script","context":"Predare F2","task":"Script gate F2: rulează O2C demo automat & verifică evenimentele și SLO; fail pipeline dacă nu trece.","dirs":["/scripts/"],"constraints":"CI only; commit 'ci(gate-f2): checker'.","output":"gate validat"},
  {"step":398,"scope":"handover-docs","context":"Documentație predare","task":"`docs/handovers/F2_handover.md` cu diagrame ERD, sequence O2C, link dashboard & alerte.","dirs":["/docs/handovers/"],"constraints":"semnat; commit 'docs(handover): F2 sales'.","output":"handover complet"},
  {"step":399,"scope":"release-tag","context":"Stabilizare","task":"Tag release `mercantiq-sales@vX.Y.0` + release notes (features, breaking).","dirs":["/"],"constraints":"semnat; commit 'chore(release): tag mercantiq-sales'.","output":"release publicat"},

  /* -------- F2-EXT (integrare extinsă / scalare) -------- */

  {"step":900,"scope":"sync-shopify-bulk","context":"Volum mare comenzi","task":"Implementă import bulk periodic (GraphQL) cu cursor pagination pentru order backlog.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"respect rate limit; commit 'feat(shopify): bulk orders sync'.","output":"backlog sincronizat"},
  {"step":901,"scope":"sync-shopify-inventory-pull","context":"ERP follower","task":"Pull periodic inventory din Shopify în modul stand-alone (dacă ERP nu e master).","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"conflict policy; commit 'feat(shopify): inventory pull'.","output":"inventar sincron"},
  {"step":902,"scope":"sync-shopify-price-rules","context":"Promo online","task":"Sincronizează price rules Shopify ↔ discount engine ERP.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"mapare reguli; commit 'feat(shopify): price rules sync'.","output":"promo aliniate"},
  {"step":903,"scope":"oblio-fallback-queue","context":"Case de marcat indisponibile","task":"Coadă locală pentru bonuri eșuate; retry cu backoff; alertă Slack dacă >N în coadă.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/oblio/"],"constraints":"persistență sigură; commit 'feat(oblio): fallback queue'.","output":"reziliență bonuri"},
  {"step":904,"scope":"efactura-xml-preview","context":"Transparență","task":"Previzualizare XML e‑Factura în UI (read‑only) înainte de submit.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/pages/"],"constraints":"sanitize; commit 'feat(ui): efactura preview'.","output":"preview e‑Factura"},
  {"step":905,"scope":"efactura-resubmit","context":"Erori workflow","task":"Buton re‑submit la erori ANAF; log motiv; păstrează versiuni XML.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/pages/","/standalone/mercantiq/apps/sales/api/src/controllers/"],"constraints":"audit; commit 'feat(efactura): resubmit'.","output":"resubmit control"},
  {"step":906,"scope":"ai-summary-order","context":"UX vânzare","task":"Invocă `ai.summary` pentru notițe autom. de conversație POS (opțional).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/services/ai/"],"constraints":"consimțământ; commit 'feat(ai): pos summary'.","output":"notițe auto"},
  {"step":907,"scope":"pdf-branding-templates","context":"Brand multi-tenant","task":"Suport template-uri PDF per tenant (logo, culori) cu ThemeHub.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/pdf/","/core/apps/admin-core/"],"constraints":"size<1MB; commit 'feat(pdf): branded templates'.","output":"PDF branduit"},
  {"step":908,"scope":"pricing-tiered","context":"B2B complex","task":"Liste de preț pe segmente client (tiered) + contract pricing.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"precedență clară; commit 'feat(pricing): tiers & contracts'.","output":"prețuri avansate"},
  {"step":909,"scope":"wms-multi-warehouse","context":"Logistică scalată","task":"SO split pe depozite; consumă `wms.picklist.completed` pe whid multiple.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"agregare facturi; commit 'feat(wms): multi-warehouse'.","output":"livrare multi‑WH"},
  {"step":910,"scope":"accounting-events-v2","context":"F3 pregătire","task":"Enrich `sales.invoice.issued` cu mapping conturi (meta) pentru Accounting.","dirs":["/standalone/mercantiq/apps/sales/api/src/events/"],"constraints":"opt-in; commit 'feat(acc): enrich events'.","output":"events ready for ACC"},
  {"step":911,"scope":"saft-validate","context":"Calitate export","task":"Validare XSD SAF‑T înainte de livrare; rapoarte erori UI.","dirs":["/standalone/mercantiq/apps/sales/api/src/reports/"],"constraints":"no external post; commit 'feat(saft): xsd validation'.","output":"SAF‑T valid"},
  {"step":912,"scope":"tenants-metrics-slo","context":"SLA by tenant","task":"Dashboards per tenant (UID=tid) pentru KPI Sales.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"templating tid; commit 'feat(obs): per-tenant dashboards'.","output":"SLO by tenant"},
  {"step":913,"scope":"audit-merkle","context":"Forensic","task":"Hash facturi (PDF/XML) în merkle-tree zilnic, publish checksum IPFS (via worker).","dirs":["/standalone/mercantiq/apps/sales/api/src/jobs/"],"constraints":"privacy; commit 'feat(audit): merkle anchors'.","output":"non‑repudiation"},
  {"step":914,"scope":"pos-hardware-bridge","context":"Periferice POS","task":"Abstracție pentru scanner/barcode & cash drawer (WebUSB/WebSerial).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/hw/"],"constraints":"permisiuni user; commit 'feat(pos): hardware bridge'.","output":"periferice POS"},
  {"step":915,"scope":"notify-teams","context":"Alternative Slack","task":"Extinde worker notificări pentru MS Teams canal.","dirs":["/core/apps/workers-core/notify-slack/"],"constraints":"toggle; commit 'feat(notify): teams channel'.","output":"notificări Teams"},
  {"step":916,"scope":"shopify-giftcards","context":"Retail avansat","task":"Consumă/sincronizează gift cards (dacă merchant folosește).","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"security; commit 'feat(shopify): gift cards'.","output":"giftcards sync"},
  {"step":917,"scope":"shopify-partial-shipments","context":"Livrări parțiale","task":"Mapare fulfillment parțial ↔ facturi parțiale; update Shopify per item.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"no duplicate invoicing; commit 'feat(shopify): partial fulfillment'.","output":"partial flow ok"},
  {"step":918,"scope":"fraud-check","context":"Risc","task":"Scor fraud (ai.classify) la comenzi online high-risk; hold până la review.","dirs":["/standalone/mercantiq/apps/sales/api/src/services/ai/"],"constraints":"explainable; commit 'feat(risk): fraud scoring'.","output":"flag fraude"},
  {"step":919,"scope":"event-replay-dlq","context":"Reziliență bus","task":"DLQ & replay pentru evenimente Sales (rmq policies + tool admin).","dirs":["/infra/rmq/","/standalone/mercantiq/apps/sales/api/src/tools/"],"constraints":"audit; commit 'feat(bus): dlq+replay'.","output":"recuperare mesaje"},
  {"step":920,"scope":"api-rate-tiers","context":"Planuri clienți","task":"Rate-limit per rol/plan (cashier vs admin) pe API Sales.","dirs":["/standalone/mercantiq/apps/sales/api/src/middleware/"],"constraints":"config via Admin; commit 'feat(api): role rate tiers'.","output":"rate tiers"},
  {"step":921,"scope":"catalog-barcodes","context":"UX scan","task":"Generator/validator coduri de bare pentru produse (EAN‑13).","dirs":["/standalone/mercantiq/apps/sales/api/src/services/"],"constraints":"checksum; commit 'feat(catalog): barcode utils'.","output":"EAN suportat"},
  {"step":922,"scope":"data-mask-demo","context":"Demo public","task":"Worker `data.mask` pe dump demo înainte de share.","dirs":["/core/apps/workers-core/"],"constraints":"fără PII; commit 'chore(data): mask demo'.","output":"dataset anonim"},
  {"step":923,"scope":"load-testing-pos","context":"Scalare retail","task":"k6 scenarii POS (peak de Black Friday) cu grafice comparate.","dirs":["/standalone/mercantiq/tests/k6/"],"constraints":"artefacte CI; commit 'perf(pos): k6 bf'.","output":"profilare POS"},
  {"step":924,"scope":"slo-burn-down","context":"SRE","task":"Grafana SLO error-budget burn pentru Sales API.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"targets defin.; commit 'feat(obs): slo burn panel'.","output":"panel SLO"},
  {"step":925,"scope":"doc-architecture","context":"Knowledge","task":"Diagrama C4 L2/L3 pentru Mercantiq (integrări & bus).","dirs":["/docs/architecture/"],"constraints":"update la fiecare release; commit 'docs(arch): mercantiq c4'.","output":"diagrame C4"},
  {"step":926,"scope":"tenants-cost-metrics","context":"FinOps","task":"Metrics cost per tenant (requests, pdf count, efactura submits) pentru facturare internă.","dirs":["/standalone/mercantiq/apps/sales/api/src/metrics/"],"constraints":"nu PII; commit 'feat(finops): tenant metrics'.","output":"showback metrici"},
  {"step":927,"scope":"saft-schedule","context":"Operare lunar","task":"Cron lunar auto‑export SAF‑T + notificare Slack & link download.","dirs":["/standalone/mercantiq/apps/sales/api/src/jobs/"],"constraints":"fereastră în afara orelor; commit 'feat(saft): monthly cron'.","output":"SAF‑T lunar"},
  {"step":928,"scope":"web-vitals-ui","context":"Perf FE","task":"Colectează Web‑Vitals și trimite la Prometheus (prometheus‑web‑vitals).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/"],"constraints":"no PII; commit 'feat(ui): web vitals'.","output":"LCP/FID/CLS colectate"},
  {"step":929,"scope":"ui-accessibility","context":"Incluziune","task":"A11y audit + remedieri (aria‑labels, focus, contrast).","dirs":["/standalone/mercantiq/apps/sales/frontend/"],"constraints":"jsx-a11y rules high; commit 'chore(ui): a11y fixes'.","output":"A11y îmbunătățit"},
  {"step":930,"scope":"efactura-queue-monitor","context":"Operare","task":"Panou operare cozi e‑Factura/PDF (nr. în coadă, timpi).","dirs":["/standalone/mercantiq/apps/sales/frontend/src/pages/ops/"],"constraints":"read-only; commit 'feat(ops-ui): queues monitor'.","output":"UI ops cozi"},
  {"step":931,"scope":"oblio-healthcheck","context":"Stabilitate POS","task":"Health‑check periodic la Oblio; failover rule (fallback queue).","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/oblio/"],"constraints":"alerte dacă down; commit 'feat(oblio): health'.","output":"monitorizare Oblio"},
  {"step":932,"scope":"shopify-webhook-rotate","context":"Securitate","task":"Rotire periodică secret webhook Shopify; update automat config.","dirs":["/standalone/mercantiq/apps/sales/api/src/integrations/shopify/"],"constraints":"CI job secure; commit 'chore(shopify): rotate webhook secret'.","output":"securitate întărită"},
  {"step":933,"scope":"tenant-theme-sync","context":"Brand unitar","task":"Sync ThemeHub (Admin Core) → temi UI Sales per tenant.","dirs":["/standalone/mercantiq/apps/sales/frontend/src/theme/"],"constraints":"size<25KB; commit 'feat(ui): theme sync'.","output":"teme per tenant"},
  {"step":934,"scope":"api-paginated-lists","context":"Scalare date","task":"Paginare server pentru /customers,/products,/orders (cursor based).","dirs":["/standalone/mercantiq/apps/sales/api/src/controllers/"],"constraints":"indexuri adecvate; commit 'feat(api): pagination'.","output":"liste scalabile"},
  {"step":935,"scope":"rbac-audit-log","context":"Audit","task":"Log RBAC decisions (allow/deny) cu labels Loki `uid,role,scp`.","dirs":["/standalone/mercantiq/apps/sales/api/src/middleware/"],"constraints":"sampling; commit 'feat(sec): rbac audit'.","output":"audit RBAC"},
  {"step":936,"scope":"api-throttling-payments","context":"Abuz prevenit","task":"Throttle per invoice la POST /payments (no duplicate spam).","dirs":["/standalone/mercantiq/apps/sales/api/src/middleware/"],"constraints":"lock per invoice; commit 'feat(pay): throttle'.","output":"duplicate evitated"},
  {"step":937,"scope":"error-catalog","context":"DX & support","task":"Catalog coduri eroare Sales (range dedicat) + mapping HTTP.","dirs":["/standalone/mercantiq/apps/sales/api/src/errors/"],"constraints":"documentează; commit 'docs(api): error catalog'.","output":"erori standardizate"},
  {"step":938,"scope":"changelog-automation","context":"Release hygiene","task":"Generează CHANGELOG din Conventional Commits pentru modul Sales.","dirs":["/"],"constraints":"semantic-release; commit 'chore(release): changelog'.","output":"changelog automat"},
  {"step":939,"scope":"training-runbooks","context":"Adopție","task":"Runbook-uri pentru operare: e‑Factura, POS offline, Shopify sync.","dirs":["/docs/runbooks/"],"constraints":"format standard; commit 'docs(runbooks): sales ops'.","output":"runbooks publicate"},
  
  // 🚀 DEPLOYMENT & SUPPLY CHAIN SECURITY (940-943)
  {"step":940,"scope":"sales-dockerfiles","context":"Containerizare pentru deployment necesară","task":"Creează Dockerfile pentru API Sales (NestJS multi-stage build) și Dockerfile pentru frontend (React Vite build + nginx non-root).","dirs":["/standalone/mercantiq/apps/sales/docker/"],"constraints":"user non-root 1000; optimizează dimensiunea imaginii; stage build separate","output":"Dockerfiles Sales create"},
  {"step":941,"scope":"sales-helm-chart","context":"Charts Helm pentru deployment","task":"Adaugă chart Helm pentru modul Sales: Deployment-uri Kubernetes pentru api și frontend, Service pentru API, IngressRoute Traefik cu host/path dedicat, și ServiceMonitor pentru metrici.","dirs":["/standalone/mercantiq/apps/sales/infra/helm/"],"constraints":"Include valori separate dev/prod; imagini semnate (cosign); testează upgrade chart local","output":"chart Helm Sales cu cosign"},
  {"step":942,"scope":"sales-ci-pipeline","context":"CI/CD pipeline pentru securitate","task":"Implementează CI/CD complet pentru Sales folosind template F0: Trivy scans cu praguri standardizate CRITICAL=0, HIGH≤3, MEDIUM≤15, SAST analysis pentru financial code, PCI DSS compliance scanning, e-Factura security validation, SBOM generation, Cosign signing.","dirs":["/.github/workflows/"],"constraints":"financial security critical; PCI DSS compliance; e-Factura security; fail on CRITICAL; codecov 85%; conform standard global","output":"CI/CD Sales securizat cu praguri standardizate"},
  {"step":943,"scope":"sales-argocd","context":"Chart Helm disponibil cu cosign","task":"Configurează Argo CD cu canary deployment pentru Sales: Argo Rollouts pentru financial APIs, traffic split 5%→25%→100%, analysis cu financial metrics (payment success rate > 99%, invoice generation < 30s), automated rollback pe financial errors.","dirs":["/core/infra/k8s/argocd/","/standalone/mercantiq/apps/sales/infra/k8s/argo-rollouts/"],"constraints":"financial stability critical; conservative canary; payment protection; automated rollback; cosign verify","output":"Sales canary deployment financial-grade"},
  
  // 📊 OBSERVABILITATE MERCANTIQ SALES (944-950)
  {"step":944,"scope":"sales-dashboard-o2c-metrics","context":"Order-to-Cash metrics dashboard lipsește.","task":"Creează dashboard Grafana pentru fluxul O2C în Sales: order processing time, invoice generation latency, payment collection rate, e-Factura submission success, POS transaction volumes.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"UID mercantiq_o2c_metrics; business KPIs focus; per tenant breakdown","output":"dashboard Sales O2C"},
  {"step":945,"scope":"sales-dashboard-anaf-compliance","context":"ANAF compliance monitoring dashboard lipsește.","task":"Creează dashboard pentru ANAF compliance în Sales: e-Factura submission rates, SAF-T export status, tax calculation accuracy, ANAF API response times, compliance violations.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"UID sales_anaf_compliance; regulatory focus; alert integration","output":"dashboard Sales ANAF Compliance"},
  {"step":946,"scope":"sales-alerts-e-factura","context":"Alerte e-Factura pentru Sales lipsesc.","task":"Configurează alerte e-Factura pentru Sales: alert dacă submission failure rate > 2%, alert dacă ANAF API timeout > 15s, alert pentru rejected invoices > 5%, alert pentru queue backlog > 100.","dirs":["/infra/k8s/alertmanager/rules/"],"constraints":"regulatory compliance critical; immediate escalation; include retry logic","output":"alerte Sales e-Factura"},
  {"step":947,"scope":"sales-alerts-payment-processing","context":"Payment processing alerts lipsesc.","task":"Configurează alerte payment processing: alert dacă payment failure rate > 3%, alert dacă POS offline > 5min, alert pentru suspicious transaction patterns, alert pentru payment gateway timeout.","dirs":["/infra/k8s/alertmanager/rules/"],"constraints":"financial critical; fraud detection; real-time monitoring","output":"alerte Sales Payment Processing"},
  {"step":948,"scope":"sales-metrics-revenue-tracking","context":"Revenue tracking metrics detaliate lipsesc.","task":"Adaugă metrici revenue pentru Sales: revenue per tenant, payment method distribution, invoice aging analysis, discount usage patterns, refund rates per product.","dirs":["/standalone/mercantiq/apps/sales/api/src/metrics/"],"constraints":"financial accuracy; audit trail; privacy compliant","output":"metrici Sales Revenue Tracking"},
  {"step":949,"scope":"sales-slo-financial","context":"SLO financiare pentru Sales lipsesc.","task":"Definește SLO financiare pentru Sales: invoice generation < 30s (SLO 99%), payment processing < 10s (SLO 95%), e-Factura submission < 2min (SLO 98%), POS uptime > 99.9%.","dirs":["/infra/grafana/provisioning/dashboards/","/infra/k8s/alertmanager/rules/"],"constraints":"financial SLOs critical; error budget tracking; escalation procedures","output":"SLO Sales Financial definite"},
  {"step":950,"scope":"sales-dashboard-shopify-integration","context":"Shopify integration monitoring lipsește.","task":"Creează dashboard pentru integrarea Shopify: sync success rates, webhook processing latency, inventory updates accuracy, order fulfillment status, API quota usage.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"UID sales_shopify_integration; e-commerce focus; real-time status","output":"dashboard Sales Shopify Integration"},
  
  // 🔐 CI/CD SALES SECURITATE FINANCIARĂ (951-955)
  {"step":951,"scope":"sales-vulnerability-scanning-financial","context":"Financial-grade vulnerability scanning lipsește.","task":"Implementează scanning financiar pentru Sales: PCI DSS compliance scanning, payment processing vulnerability analysis, e-Factura security validation, financial libraries CVE monitoring.","dirs":["/standalone/mercantiq/apps/sales/","/infra/k8s/trivy/"],"constraints":"PCI DSS compliance critical; payment security focus; regulatory compliance; zero tolerance","output":"Sales financial vulnerability scanning"},
  {"step":952,"scope":"sales-canary-financial-metrics","context":"Canary deployment cu financial metrics lipsește.","task":"Configurează canary analysis pentru Sales cu financial metrics: payment success rate monitoring, invoice generation performance, e-Factura submission tracking, financial data integrity validation.","dirs":["/standalone/mercantiq/apps/sales/infra/k8s/argo-rollouts/"],"constraints":"financial metrics critical; payment integrity; regulatory compliance; conservative approach","output":"Sales canary financial metrics"},
  {"step":953,"scope":"sales-rollback-financial-protection","context":"Rollback protection pentru financial data lipsește.","task":"Implementează rollback protection pentru financial data: payment transaction integrity, invoice data consistency, e-Factura compliance preservation, financial audit trail protection.","dirs":["/standalone/mercantiq/apps/sales/infra/k8s/","/standalone/mercantiq/apps/sales/scripts/"],"constraints":"financial data integrity critical; zero transaction loss; audit compliance; regulatory requirements","output":"Sales financial rollback protection"},
  {"step":954,"scope":"sales-health-checks-financial","context":"Health checks financiare specifice lipsesc.","task":"Implementează health checks financiare pentru Sales: payment gateway connectivity, e-Factura ANAF API health, POS system status, financial data consistency validation.","dirs":["/standalone/mercantiq/apps/sales/api/src/health/","/infra/k8s/health-checks/"],"constraints":"financial health validation; payment system dependency; regulatory API connectivity","output":"Sales financial health checks"},
  {"step":955,"scope":"sales-deployment-financial-validation","context":"Deployment validation pentru financial business logic lipsește.","task":"Adaugă deployment validation pentru financial logic: payment processing verification, invoice calculation validation, e-Factura compliance testing, financial reporting accuracy checks.","dirs":["/standalone/mercantiq/apps/sales/tests/deployment/","/standalone/mercantiq/apps/sales/scripts/validation/"],"constraints":"financial accuracy critical; regulatory compliance validation; automated testing; audit trail","output":"Sales financial deployment validation"}
]
```

---

### Note & aliniere la documentația suitei

* **Event‑Bus & convenții v1:** nume evenimente `module.ctx.event` (ex.: `sales.invoice.issued`, `wms.picklist.completed`, `payment.received`).
* **Stack & căi canonice:** UI/API pe stack fix, proiecte sub `standalone/mercantiq/...` (lint‑paths blochează `apps/...`).
* **Workeri disponibili & Registry:** `pdf.render`, `email.send`, `tax.vat`, `notify.slack`, `match.ai`, etc., cu health & traces vizibile prin Worker Registry/Tempo.
* **Date & securitate:** multitenancy pe PG/MinIO/Redis, RLS pe `tid/whid`, SSE‑C pe MinIO, JWT RS256 cu claims standard.
* **Observabilitate:** Prometheus metrics, Loki logs, Tempo traces, dashboards SLO, alerte queue lag/erroare.
* **Gate F2 ➜ F3:** O2C < 3 min, P2P complet, SLO p95 < 250 ms, erori < 1 %.

> Această versiune upgradată păstrează **logica stand‑alone** a aplicației Mercantiq și integrează **bi‑direcțional** cu suita (Vettify CRM, iWMS, Procurement), extinzând capabilitățile de automatizare fiscală (ANAF e‑Factura, SAF‑T), POS fiscal (Oblio) și e‑commerce (Shopify) – aliniat cu principiile și standardele tehnice ale GeniusERP Suite.

## 9) Note de implementare

* **Căi canonice & arbore directoare**: folosește exact structura indicată pentru standalone apps (`standalone/mercantiq/apps/sales/`); nu devia la `/apps` fără prefix `standalone/`.
* **Evenimente & naming**: menține convențiile v1 și validează în CI cu `lint-rmq.sh`. Format: `sales.order.created`, `sales.invoice.issued`, `payment.received`.
* **Workeri**: integrează-te cu workers existenți și noi conectori fără a schimba stack-ul lor (Python 3.13 + Celery/Ray).
* **Multitenancy/RLS**: izolare strictă `tid/whid/mid` conform modelului de date Fazei F2.
* **POS Offline**: implementarea offline trebuie să fie robustă cu IndexedDB și sync automat la reconectare.
* **Order-to-Cash**: fluxul complet trebuie validat E2E cu toate evenimentele în succesiune.
* **Conformitate ANAF**: integrarea cu workeri `tax.vat`, `anaf.efactura`, `anaf.saft` este obligatorie.
* **Integrări e-commerce**: Shopify sync bidirecțional pentru comenzi, stoc, fulfillment.
* **CI/CD**: Trivy HIGH, cosign sign/attest, Argo sync, canary + rollback metric-based conform umbrele F2.
* **Observabilitate**: traces end-to-end, metrics per-tenant, dashboards SLO, alerte queue lag.

---

## 10) Dependențe externe și API keys

Pentru funcționarea completă a integrărilor, sunt necesare următoarele credențiale via ExternalSecrets:

* **ANAF SPV**: certificat și parola pentru e-Factura
* **Oblio**: API key pentru case de marcat și bonuri fiscale  
* **Shopify**: Admin API key, webhook secret, store domain
* **SMTP**: configurare server pentru trimitere facturi
* **Slack/Teams**: webhook URL pentru notificări
* **Curieri**: API keys Fan/DHL/UPS pentru AWB
* **Payment gateways**: Stripe/Netopia pentru POS card

Toate acestea trebuie configurate prin Kubernetes ExternalSecrets, nu hardcodate în aplicație.

---

> Această versiune upgradată transformă **Mercantiq Sales & Billing** într-o aplicație enterprise-ready cu integrări profunde de workeri, conformitate fiscală completă și interoperabilitate maximă cu suita GeniusERP, respectând totodată principiile de securitate, observabilitate și scalabilitate ale platformei.

