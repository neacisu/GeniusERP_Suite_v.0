# Roadmap Numeriqo Manufacturing (F3)

> **Scop:** să implementăm **Numeriqo Manufacturing** ca modulul responsabil de **Manufacturing Execution System (MES)** în suita GeniusERP – cu integrare profundă de **workeri AI** (forecast, ai.classify, report.kpi) și interoperabilitate completă cu **iWMS v3**, **Mercantiq Sales**, **Procurement** și ecosistemul complet.

**Target F3:** BOM Management + MRP II Beta + Shop Floor Control + Quality Management.

**Bounded-context Manufacturing:** product_structure, bom, work_center, routing, work_order, production_schedule, quality_control, shop_floor_terminal cu automatizare completă AI-powered pentru demand forecast, production optimization și quality classification.

**Workers integrati:** 
`forecast` (predicții cerere și production capacity), `ai.classify` (quality control automată), `report.kpi` (KPI-uri production în timp real), `match.ai` (optimizări generale production), `pdf.render` (work orders și rapoarte), `email.send` (notificări production)

## Preconditions

**Prerequisite obligatorii:**
* **F2 Complete** – Shell + iWMS v3 funcțional (warehouse operations)
* **Worker Fleet** disponibil: `forecast`, `ai.classify`, `report.kpi`, `match.ai`, `pdf.render`, `email.send`
* **Event Bus v1** – naming convention `<module>.<context>.<event>` funcțional
* **Database PG17** – multi-tenancy RLS activă cu politici standard
* **Observability Stack** – Prometheus/Grafana/Tempo/Loki operațional

## Events published by Manufacturing

* **`manufacturing.bom.created`**: BOM nou creat cu componente
* **`manufacturing.bom.updated`**: modificări în structure BOM
* **`manufacturing.work_order.created`**: work order nou emis pentru producție
* **`manufacturing.work_order.started`**: început producție pe work order
* **`manufacturing.work_order.completed`**: finalizare work order cu quantities
* **`manufacturing.production.scheduled`**: planificare producție MRP
* **`manufacturing.quality.checked`**: verificare quality control
* **`manufacturing.material.consumed`**: consum materiale în producție

## Events consumed by Manufacturing

* `sales.order.created` - trigger MRP planning pentru comenzi noi
* `procurement.po.delivered` - update material availability pentru MRP
* `wms.stock.adjusted` - sincronizare stock pentru production planning
* `wms.material.issued` - confirmare material issue pentru work orders
* `forecast.demand.updated` - actualizare demand forecast pentru MRP

---

## JSON Implementation Steps

**Range:** 500-699 (200 steps target pentru complexity Manufacturing)

**Naming Convention:**
- Workers: `<domain>.<action>` (manufacturing.forecast, manufacturing.classify)
- Events: `<module>.<context>.<event>` (manufacturing.bom.created)
- Tables: snake_case cu prefixe (mfg_bom, mfg_work_order)

```json
[
  {"step":500,"scope":"manufacturing-scaffold","context":"F2 complete; iWMS v3 operațional; modul Manufacturing inexistent","task":"Generează scheletul Numeriqo Manufacturing (frontend React+Vite Federation, API NestJS, workers stubs) folosind `scripts/create-module.ts --standalone numeriqo --module manufacturing --with-ai`. Activează Module Federation remoteEntry și configurează tags Nx.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/","/standalone/numeriqo/apps/manufacturing/api/","/standalone/numeriqo/apps/manufacturing/workers/"],"constraints":"scripts/create-module.ts --standalone numeriqo --module manufacturing; tags Nx `module:numeriqo/manufacturing,layer:frontend|api|workers`; commit 'feat(numeriqo/manufacturing): scaffold MES module'.","output":"skeleton Manufacturing complete cu FE+API+Workers"},

  {"step":501,"scope":"db-migrations-base","context":"Schema Manufacturing inexistentă; PG17 multi-tenant activ","task":"Creează migration init pentru tabele de bază: mfg_products, mfg_work_centers, mfg_routings, mfg_bom_headers, mfg_bom_components. Adaugă coloane multi-tenant `tid`,`whid`,`mid` și audit trail `created_at`,`updated_at`,`created_by`,`updated_by`.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/migrations/"],"constraints":"UUID PK; FK stricte către Products/Items; coloane audit complete; commit 'feat(mfg-db): base tables BOM+routing'.","output":"tabele Manufacturing base create"},

  {"step":502,"scope":"db-migrations-workorder","context":"Tabele de bază create (501)","task":"Adaugă tabele pentru execution: mfg_work_orders, mfg_wo_operations, mfg_wo_materials, mfg_wo_labor, mfg_production_lots cu status workflow (draft→released→started→completed→closed). Include foreign keys către iWMS items pentru material tracking.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/migrations/"],"constraints":"enum status workflow; FK către iWMS schema items; indexes pe (tid,status,planned_start); commit 'feat(mfg-db): work orders + operations'.","output":"tabele Work Order execution create"},

  {"step":503,"scope":"db-migrations-quality","context":"Execution tables ready (502)","task":"Creează tabele Quality Control: mfg_quality_plans, mfg_quality_inspections, mfg_quality_results, mfg_nonconformance cu link-uri către work orders și production lots. Include câmpuri pentru AI classification results.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/migrations/"],"constraints":"FK către work_orders și lots; coloane AI prediction (jsonb); commit 'feat(mfg-db): quality control tables'.","output":"Quality Control schema ready"},

  {"step":504,"scope":"db-migrations-scheduling","context":"Core tables complete (503)","task":"Adaugă tabele MRP și scheduling: mfg_mrp_runs, mfg_planned_orders, mfg_capacity_buckets, mfg_shop_calendar cu time-based planning. Include integration points cu forecast workers.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/migrations/"],"constraints":"time buckets hourly/daily; FK către work_centers; indexes temporale; commit 'feat(mfg-db): MRP + scheduling tables'.","output":"MRP II tables created"},

  {"step":505,"scope":"db-migrations-shopfloor","context":"Planning tables ready (504)","task":"Creează tabele Shop Floor: mfg_terminals, mfg_terminal_sessions, mfg_transactions (clock in/out, material consumption, production reporting) cu real-time data capture. Include barcode/RFID support fields.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/migrations/"],"constraints":"real-time timestamps; barcode fields varchar(50); session tracking; commit 'feat(mfg-db): shop floor data capture'.","output":"Shop Floor terminal tables ready"},

  {"step":506,"scope":"db-rls-policies","context":"Toate tabelele Manufacturing create (505); RLS standard definit în suite","task":"Activează Row Level Security pe toate tabelele Manufacturing cu politica standard: `tid = current_setting('app.tid') AND (whid = current_setting('app.whid') OR whid IS NULL) AND (mid = current_setting('app.mid') OR mid IS NULL)`. Set session vars din JWT.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/db/rls/"],"constraints":"respectă RLS standard suite cu mid extension; teste policy per tabel; commit 'feat(mfg-db): RLS policies standard'.","output":"RLS activ pe schema Manufacturing"},

  {"step":507,"scope":"entities-orm","context":"RLS policies active (506)","task":"Definește entități TypeORM pentru toate tabelele: Product, WorkCenter, Routing, BomHeader, BomComponent, WorkOrder, Operation, MaterialIssue, QualityInspection cu relationships și decoratori validation.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/entities/"],"constraints":"relationships FK complete; validation decoratori; no business logic în entities; commit 'feat(mfg-api): TypeORM entities'.","output":"Manufacturing entities complete"},

  {"step":508,"scope":"repositories-pattern","context":"Entities definite (507)","task":"Implementează repositories pentru fiecare entitate cu pattern standardizat: BomRepository, WorkOrderRepository, QualityRepository etc. Include query builders pentru complex manufacturing operations.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/repositories/"],"constraints":"no business logic în repo; query builders optimizați; commit 'feat(mfg-api): repositories layer'.","output":"Repository layer Manufacturing"},

  {"step":509,"scope":"dto-validation","context":"Repositories ready (508)","task":"Creează DTO cu class-validator pentru toate operations: CreateBomDto, CreateWorkOrderDto, UpdateProductionStatusDto, QualityInspectionDto cu validări specifice manufacturing (quantities positive, dates logic, status transitions).","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/dto/"],"constraints":"validări business specific; error messages localized RO; commit 'feat(mfg-api): DTOs + validation'.","output":"DTO Manufacturing validate"},

  {"step":510,"scope":"services-bom","context":"DTO ready (509)","task":"Implementează BomService cu operații: createBom, updateBomStructure, explodeBom, calculateMaterialRequirements, validateBomCycle. Include business logic pentru BOM explosion și costing.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/services/bom/"],"constraints":"unit tests ≥85%; cycle detection algorithm; BOM explosion recursive; commit 'feat(mfg-api): BOM service'.","output":"BOM management service"},

  {"step":511,"scope":"services-workorder","context":"BOM service ready (510)","task":"Implementează WorkOrderService: createWorkOrder, releaseToFloor, startProduction, reportProgress, completeOperation, closeWorkOrder cu state machine pentru workflow status.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/services/workorder/"],"constraints":"state machine strict; integration cu iWMS pentru materials; commit 'feat(mfg-api): WorkOrder service'.","output":"Work Order management service"},

  {"step":512,"scope":"services-mrp","context":"WorkOrder service operational (511)","task":"Implementează MrpService pentru Material Requirements Planning: calculateNetRequirements, generatePlannedOrders, capacityPlanning, schedulingAlgorithm cu integration forecast worker.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/services/mrp/"],"constraints":"performance <2s pentru MRP run; integration forecast worker; commit 'feat(mfg-api): MRP planning service'.","output":"MRP II service functional"},

  {"step":513,"scope":"services-quality","context":"Core services ready (512)","task":"Implementează QualityService cu AI integration: createQualityPlan, performInspection, aiQualityClassification, recordNonconformance cu integration `ai.classify` worker pentru automated quality detection.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/services/quality/"],"constraints":"AI classification integration; non-conformance tracking; commit 'feat(mfg-api): Quality service + AI'.","output":"Quality Control service cu AI"},

  {"step":514,"scope":"controllers-bom","context":"BOM service ready (510)","task":"Controller BOM Management: GET/POST/PUT/DELETE pentru /bom endpoints cu operations: create BOM, update structure, explode BOM, copy BOM. Include validation și error handling.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/controllers/bom/"],"constraints":"REST standardizat; p95 <300ms; validation errors clear; commit 'feat(mfg-api): BOM controller'.","output":"BOM API endpoints"},

  {"step":515,"scope":"controllers-workorder","context":"WorkOrder service operational (511)","task":"Controller Work Orders: CRUD operations + workflow actions (/work-orders/:id/release, /start, /complete) cu real-time status updates și integration shop floor terminals.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/controllers/workorder/"],"constraints":"workflow actions separate endpoints; real-time updates; commit 'feat(mfg-api): WorkOrder controller'.","output":"Work Order API cu workflow"},

  {"step":516,"scope":"controllers-production","context":"MRP service functional (512)","task":"Controller Production Planning: endpoints pentru MRP runs (/mrp/calculate, /planned-orders, /capacity-analysis) cu async processing și progress tracking.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/controllers/production/"],"constraints":"async processing cu job queue; progress tracking WebSocket; commit 'feat(mfg-api): Production planning controller'.","output":"Production Planning API"},

  {"step":517,"scope":"controllers-quality","context":"Quality service cu AI ready (513)","task":"Controller Quality Control: endpoints pentru quality plans, inspections, AI classification (/quality/inspect/:id/ai-classify) cu rezultate real-time și non-conformance management.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/controllers/quality/"],"constraints":"AI classification async; real-time results; commit 'feat(mfg-api): Quality controller + AI'.","output":"Quality Control API cu AI"},

  {"step":518,"scope":"controllers-shopfloor","context":"Shop floor tables ready (505)","task":"Controller Shop Floor Terminals: endpoints pentru terminal registration, transactions (/terminals/:id/clock-in, /report-production, /material-consumption) cu barcode scanning support.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/controllers/shopfloor/"],"constraints":"barcode validation; real-time transactions; terminal authentication; commit 'feat(mfg-api): Shop floor controller'.","output":"Shop Floor API pentru terminals"},

  {"step":519,"scope":"event-bus-integration","context":"Event Bus v1 operational; controllers ready (518)","task":"Integrează Event Bus client în Manufacturing API cu publish/subscribe capabilities. Configure topic routing și message serialization.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/bus/"],"constraints":"SDK TS bus conform F2; contract tests; commit 'feat(mfg-api): Event Bus integration'.","output":"Event Bus Manufacturing ready"},

  {"step":520,"scope":"events-publish-bom","context":"Event Bus ready (519)","task":"Implementează event publishing pentru BOM operations: `manufacturing.bom.created`, `manufacturing.bom.updated` cu payload complet (bom_id, product_id, version, components_count).","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/publishers/"],"constraints":"single publish post-commit; include correlation-id; commit 'feat(mfg-events): BOM events publish'.","output":"BOM events published"},

  {"step":521,"scope":"events-publish-workorder","context":"BOM events ready (520)","task":"Publică evenimente Work Order: `manufacturing.work_order.created`, `manufacturing.work_order.started`, `manufacturing.work_order.completed` cu payload (wo_id, product_id, quantities, status).","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/publishers/"],"constraints":"workflow state în payload; commit 'feat(mfg-events): WorkOrder events'.","output":"Work Order events active"},

  {"step":522,"scope":"events-publish-production","context":"WorkOrder events operational (521)","task":"Emite evenimente production planning: `manufacturing.production.scheduled`, `manufacturing.material.consumed` pentru MRP results și material tracking cu integration iWMS.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/publishers/"],"constraints":"MRP results structured payload; iWMS integration data; commit 'feat(mfg-events): Production events'.","output":"Production planning events"},

  {"step":523,"scope":"events-publish-quality","context":"Production events ready (522)","task":"Publică quality events: `manufacturing.quality.checked` cu AI classification results și non-conformance notifications pentru downstream systems.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/publishers/"],"constraints":"AI results în payload; non-conformance severity; commit 'feat(mfg-events): Quality events + AI'.","output":"Quality events cu AI data"},

  {"step":524,"scope":"events-consume-sales","context":"Event publishing complete (523)","task":"Consumer pentru `sales.order.created` → trigger MRP planning automatic pentru new sales orders cu material requirements calculation.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/consumers/"],"constraints":"idempotent processing; MRP trigger async; commit 'feat(mfg-events): consume sales orders'.","output":"Sales order MRP integration"},

  {"step":525,"scope":"events-consume-procurement","context":"Sales consumer ready (524)","task":"Subscriber `procurement.po.delivered` → update material availability în MRP și recalculate planned orders dacă supply constraints removed.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/consumers/"],"constraints":"material availability update atomic; commit 'feat(mfg-events): consume PO delivered'.","output":"Procurement integration MRP"},

  {"step":526,"scope":"events-consume-wms","context":"Procurement consumer operational (525)","task":"Consumă evenimente iWMS: `wms.stock.adjusted`, `wms.material.issued` pentru sincronizare inventory cu production planning și work order execution.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/consumers/"],"constraints":"stock sync real-time; work order material tracking; commit 'feat(mfg-events): consume WMS events'.","output":"iWMS inventory sync active"},

  {"step":527,"scope":"events-consume-forecast","context":"WMS consumer ready (526)","task":"Consumer pentru `forecast.demand.updated` → actualizare demand forecast în MRP planning cu new predictions și capacity planning adjustment.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/events/consumers/"],"constraints":"forecast integration async; MRP refresh triggered; commit 'feat(mfg-events): consume forecast updates'.","output":"Forecast integration MRP"},

  {"step":528,"scope":"worker-forecast-integration","context":"Workers fleet available; MRP service functional (512)","task":"Integrează worker `forecast` pentru demand prediction și capacity planning: publish forecast requests, consume results, update MRP parameters cu AI predictions.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/forecast/"],"constraints":"Ray cluster integration; OTel metrics; commit 'feat(mfg-workers): forecast integration'.","output":"AI forecast Manufacturing"},

  {"step":529,"scope":"worker-ai-classify-quality","context":"Forecast worker ready (528)","task":"Implementează integration cu `ai.classify` pentru automated quality inspection: capture quality images, send classification requests, process results automatic.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/ai-classify/"],"constraints":"image processing pipeline; classification confidence >85%; commit 'feat(mfg-workers): AI quality classify'.","output":"AI quality classification"},

  {"step":530,"scope":"worker-report-kpi","context":"AI classify ready (529)","task":"Integrează `report.kpi` worker pentru real-time manufacturing KPIs: OEE calculation, throughput metrics, quality metrics, downtime analysis cu dashboard integration.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/report-kpi/"],"constraints":"real-time KPI calculation; dashboard ready format; commit 'feat(mfg-workers): KPI reporting'.","output":"Manufacturing KPIs real-time"},

  {"step":531,"scope":"worker-match-ai-optimization","context":"KPI worker operational (530)","task":"Integrez `match.ai` pentru production optimization: schedule optimization, resource allocation, bottleneck detection și production flow improvements.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/match-ai/"],"constraints":"optimization algorithms production specific; commit 'feat(mfg-workers): production optimization AI'.","output":"AI production optimization"},

  {"step":532,"scope":"worker-pdf-render-reports","context":"Workers core operational (531)","task":"Integrează `pdf.render` pentru Manufacturing reports: work order documents, quality certificates, production reports cu templating și MinIO storage.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/pdf-render/"],"constraints":"templates Manufacturing specific; MinIO SSE-C storage; commit 'feat(mfg-workers): PDF reports'.","output":"Manufacturing PDF generation"},

  {"step":533,"scope":"worker-email-notifications","context":"PDF worker ready (532)","task":"Implementează `email.send` integration pentru Manufacturing notifications: work order alerts, quality non-conformance, production delays cu template system.","dirs":["/standalone/numeriqo/apps/manufacturing/workers/email-send/"],"constraints":"notification templates Manufacturing; SMTP via ExternalSecret; commit 'feat(mfg-workers): email notifications'.","output":"Manufacturing email alerts"},

  {"step":534,"scope":"auth-rbac-guards","context":"API controllers complete (518); JWT system operational","task":"Implementează RBAC guards pentru Manufacturing: scopes `manufacturing.*` (bom.read, workorder.write, quality.manage, production.plan) cu role mapping.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/guards/"],"constraints":"granular permissions Manufacturing; unit tests guards; commit 'feat(mfg-auth): RBAC guards'.","output":"Manufacturing authorization"},

  {"step":535,"scope":"auth-tenant-context","context":"RBAC ready (534)","task":"Middleware pentru tenant context setting: extract `tid`,`whid`,`mid` din JWT și set PostgreSQL session variables pentru RLS policies activation.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/middleware/"],"constraints":"session vars correct per request; commit 'feat(mfg-auth): tenant middleware'.","output":"Multi-tenancy context active"},

  {"step":536,"scope":"otel-tracing","context":"Observability stack ready; API functional","task":"Activează OpenTelemetry în Manufacturing API: HTTP requests, TypeORM queries, Event Bus operations, Worker calls cu service.name=numeriqo/manufacturing-api.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/config/otel/"],"constraints":"traces end-to-end Manufacturing; Tempo integration; commit 'feat(mfg-otel): distributed tracing'.","output":"Manufacturing traces în Tempo"},

  {"step":537,"scope":"prometheus-metrics","context":"OTel active (536)","task":"Expune Prometheus metrics pentru Manufacturing: http standard + business metrics (bom_created_total, work_orders_completed_total, quality_inspections_total, mrp_runs_total).","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/config/metrics/"],"constraints":"prefix numeriqo_manufacturing_*; business KPIs included; commit 'feat(mfg-metrics): Prometheus export'.","output":"Manufacturing metrics în Prometheus"},

  {"step":538,"scope":"logging-structured","context":"Metrics ready (537)","task":"Configurează structured logging cu Winston: JSON format, correlation-id propagation, log levels per environment, sensitive data filtering pentru Manufacturing operations.","dirs":["/standalone/numeriqo/apps/manufacturing/api/src/config/logging/"],"constraints":"no PII în logs; correlation tracking; commit 'feat(mfg-logging): structured logs'.","output":"Manufacturing logging structured"},

  {"step":539,"scope":"frontend-scaffold","context":"API complete cu observability (538)","task":"Bootstrap Manufacturing frontend: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 cu Module Federation remoteEntry pentru Manufacturing UI integration în Shell.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/"],"constraints":"Federation config Manufacturing modules; UI tokens conform; commit 'feat(mfg-ui): frontend bootstrap'.","output":"Manufacturing UI skeleton"},

  {"step":540,"scope":"frontend-routing","context":"Frontend bootstrap ready (539)","task":"Setup routing pentru Manufacturing pages: /manufacturing/bom, /work-orders, /production-planning, /quality-control, /shop-floor cu React Router și lazy loading.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/routes/"],"constraints":"lazy loading Manufacturing pages; commit 'feat(mfg-ui): routing setup'.","output":"Manufacturing routing active"},

  {"step":541,"scope":"frontend-data-layer","context":"Routing ready (540)","task":"Configurează data layer: TanStack Query pentru server state, Axios client cu JWT interceptors, error handling și retry logic pentru Manufacturing API calls.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/api/"],"constraints":"retry logic Manufacturing specific; error boundaries; commit 'feat(mfg-ui): data layer'.","output":"Manufacturing data layer"},

  {"step":542,"scope":"frontend-state-management","context":"Data layer operational (541)","task":"Setup state management cu Zustand: BOM state, WorkOrder state, Production planning state, Quality state cu persistence și sync cu server state.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/stores/"],"constraints":"state sync cu TanStack Query; persist important state; commit 'feat(mfg-ui): state management'.","output":"Manufacturing state stores"},

  {"step":543,"scope":"frontend-bom-pages","context":"State management ready (542)","task":"Implementează BOM Management pages: BOM List cu DataGrid, BOM Editor cu tree structure, BOM Explosion view, BOM Costing cu calculation display.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/bom/"],"constraints":"tree component BOM structure; costing calculations UI; commit 'feat(mfg-ui): BOM pages'.","output":"BOM management UI"},

  {"step":544,"scope":"frontend-workorder-pages","context":"BOM pages ready (543)","task":"Creează Work Order pages: WorkOrder List cu filtering, WorkOrder Creation wizard, WorkOrder Tracking cu real-time status, Operation Management pentru shop floor.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/workorder/"],"constraints":"real-time status updates; workflow UI clear; commit 'feat(mfg-ui): WorkOrder pages'.","output":"Work Order management UI"},

  {"step":545,"scope":"frontend-production-planning","context":"WorkOrder UI ready (544)","task":"Implementează Production Planning interface: MRP Run dashboard, Planned Orders management, Capacity Planning Gantt chart, Schedule Optimization cu drag-and-drop.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/planning/"],"constraints":"Gantt chart interactive; drag-drop scheduling; commit 'feat(mfg-ui): Production planning'.","output":"Production planning interface"},

  {"step":546,"scope":"frontend-quality-control","context":"Planning UI operational (545)","task":"Dezvolt Quality Control pages: Quality Plans setup, Inspection Interface cu AI integration, Non-conformance Management, Quality Reports cu charts.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/quality/"],"constraints":"AI integration UI smooth; quality charts interactive; commit 'feat(mfg-ui): Quality control'.","output":"Quality Control interface"},

  {"step":547,"scope":"frontend-shopfloor-terminal","context":"Quality UI ready (546)","task":"Creează Shop Floor Terminal interface: Touch-friendly UI pentru tablets, Barcode scanning integration, Work Order selection, Production reporting simple și rapid.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/shopfloor/"],"constraints":"touch UI optimized; barcode integration; commit 'feat(mfg-ui): Shop floor terminal'.","output":"Shop Floor terminal UI"},

  {"step":548,"scope":"frontend-dashboards","context":"Core pages complete (547)","task":"Implementează Manufacturing dashboards: Executive Dashboard cu KPIs, Production Monitoring real-time, Quality Dashboard, Efficiency Analytics cu charts și metrics.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/pages/dashboard/"],"constraints":"real-time data updates; executive level KPIs; commit 'feat(mfg-ui): Manufacturing dashboards'.","output":"Manufacturing analytics dashboards"},

  {"step":549,"scope":"frontend-mobile-responsive","context":"Dashboards ready (548)","task":"Optimizează Manufacturing UI pentru mobile devices: responsive design, touch interactions, offline capability pentru shop floor terminals, PWA features.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/src/"],"constraints":"PWA ready; offline shop floor support; commit 'feat(mfg-ui): mobile responsive'.","output":"Manufacturing mobile optimized"},

  {"step":550,"scope":"api-testing-unit","context":"API services complete (513)","task":"Teste unit comprehensive pentru Manufacturing services: BOM service (95% coverage), WorkOrder service (90% coverage), MRP service (85% coverage), Quality service (90% coverage).","dirs":["/standalone/numeriqo/apps/manufacturing/api/tests/unit/"],"constraints":"coverage targets per service; mock dependencies; commit 'test(mfg-api): unit tests complete'.","output":"Manufacturing unit tests"},

  {"step":551,"scope":"api-testing-integration","context":"Unit tests ready (550)","task":"Teste integration pentru Manufacturing API: database operations, Event Bus integration, Worker communication, multi-tenancy RLS verification.","dirs":["/standalone/numeriqo/apps/manufacturing/api/tests/integration/"],"constraints":"real database tests; Event Bus contract verification; commit 'test(mfg-api): integration tests'.","output":"Manufacturing integration tests"},

  {"step":552,"scope":"frontend-testing","context":"Frontend complete (549)","task":"Teste frontend Manufacturing: Vitest unit tests pentru components, React Testing Library pentru pages, E2E tests cu Playwright pentru critical workflows.","dirs":["/standalone/numeriqo/apps/manufacturing/frontend/tests/"],"constraints":"component tests 80%; E2E critical paths; commit 'test(mfg-ui): frontend tests'.","output":"Manufacturing frontend tested"},

  {"step":553,"scope":"api-testing-e2e","context":"Frontend tests ready (552)","task":"E2E testing Manufacturing workflows: Create BOM → Generate Work Order → Execute Production → Quality Control → Complete cu Supertest și database verification.","dirs":["/standalone/numeriqo/apps/manufacturing/tests/e2e/"],"constraints":"complete workflows tested; data verification; commit 'test(mfg-e2e): workflow tests'.","output":"Manufacturing E2E verified"},

  {"step":554,"scope":"performance-testing","context":"E2E tests complete (553)","task":"Performance testing cu k6: BOM explosion (p95 <2s), MRP calculation (100 products <5s), Work Order creation (p95 <500ms), Quality classification API (p95 <1s).","dirs":["/standalone/numeriqo/apps/manufacturing/tests/performance/"],"constraints":"SLA targets Manufacturing specific; Grafana reporting; commit 'perf(mfg): performance benchmarks'.","output":"Manufacturing performance verified"},

  {"step":555,"scope":"load-testing","context":"Performance benchmarks ready (554)","task":"Load testing Manufacturing API: concurrent BOM operations (50 users), simultaneous Work Orders (100 concurrent), MRP runs (10 parallel), Shop Floor transactions (200 TPS).","dirs":["/standalone/numeriqo/apps/manufacturing/tests/load/"],"constraints":"production load simulation; resource monitoring; commit 'perf(mfg): load testing'.","output":"Manufacturing load tested"},

  {"step":556,"scope":"security-testing","context":"Load tests complete (555)","task":"Security testing Manufacturing: RBAC verification, RLS policy testing, input validation, SQL injection prevention, sensitive data handling manufacturing specific.","dirs":["/standalone/numeriqo/apps/manufacturing/tests/security/"],"constraints":"manufacturing security specific; automated security tests; commit 'security(mfg): security verification'.","output":"Manufacturing security verified"},

  {"step":557,"scope":"contract-testing-events","context":"Event system operational (527)","task":"Contract testing pentru Manufacturing events: publish/subscribe contracts, event schema validation, consumer compatibility, event versioning support.","dirs":["/standalone/numeriqo/apps/manufacturing/tests/contracts/"],"constraints":"Pact contracts Manufacturing events; schema validation; commit 'test(mfg-contracts): event contracts'.","output":"Manufacturing event contracts"},

  {"step":558,"scope":"contract-testing-workers","context":"Workers integration complete (533)","task":"Contract tests pentru Worker integration: forecast worker contracts, AI classify contracts, KPI reporting contracts, match.ai optimization contracts.","dirs":["/standalone/numeriqo/apps/manufacturing/tests/contracts/workers/"],"constraints":"worker API contract verification; commit 'test(mfg-contracts): worker contracts'.","output":"Manufacturing worker contracts"},

  {"step":559,"scope":"deployment-helm-base","context":"Application complete și tested (558)","task":"Creează Helm chart Manufacturing base: API deployment, frontend deployment, ingress configuration, service definitions cu Manufacturing specific configuration.","dirs":["/standalone/numeriqo/infra/helm/manufacturing/"],"constraints":"multi-environment support; resource limits Manufacturing; commit 'feat(helm): Manufacturing base chart'.","output":"Manufacturing Helm chart"},

  {"step":560,"scope":"deployment-helm-secrets","context":"Base chart ready (559)","task":"ExternalSecrets pentru Manufacturing: database credentials, Event Bus config, Worker API keys, observability endpoints cu vault/ESO integration.","dirs":["/infra/k8s/externalsecrets/manufacturing/"],"constraints":"no secrets în repo; vault integration; commit 'feat(helm): Manufacturing secrets'.","output":"Manufacturing secrets managed"},

  {"step":561,"scope":"deployment-helm-monitoring","context":"Secrets ready (560)","task":"Monitoring configuration Helm: ServiceMonitor pentru Prometheus, log aggregation config, alert rules Manufacturing specific, dashboard provisioning.","dirs":["/standalone/numeriqo/infra/helm/manufacturing/monitoring/"],"constraints":"Manufacturing specific alerts; dashboard auto-provision; commit 'feat(helm): Manufacturing monitoring'.","output":"Manufacturing monitoring config"},

  {"step":562,"scope":"deployment-argocd","context":"Helm complete cu monitoring (561)","task":"ArgoCD Application definition pentru Manufacturing: namespace dedicat, sync policies, health checks Manufacturing specific, rollback configuration.","dirs":["/infra/k8s/argocd/apps/manufacturing/"],"constraints":"health checks Manufacturing endpoints; automated sync; commit 'feat(argocd): Manufacturing app'.","output":"Manufacturing ArgoCD managed"},

  {"step":563,"scope":"deployment-ci-pipeline","context":"ArgoCD ready (562)","task":"CI/CD pipeline Manufacturing: GitHub Actions pentru build/test/deploy, Trivy security scans (CRITICAL=0, HIGH≤3, MEDIUM≤15), SBOM generation, Cosign signing.","dirs":["/.github/workflows/manufacturing-ci.yml"],"constraints":"security thresholds Manufacturing; SBOM Manufacturing specific; commit 'ci(mfg): complete pipeline'.","output":"Manufacturing CI/CD active"},

  {"step":564,"scope":"observability-grafana-dashboard","context":"Monitoring config ready (561)","task":"Grafana dashboards Manufacturing: Executive KPI dashboard, Production Monitoring, Quality Analytics, System Health cu drill-down capabilities.","dirs":["/infra/grafana/provisioning/dashboards/manufacturing/"],"constraints":"executive level KPIs; drill-down navigation; commit 'feat(obs): Manufacturing dashboards'.","output":"Manufacturing Grafana dashboards"},

  {"step":565,"scope":"observability-alerting","context":"Dashboards ready (564)","task":"Alert rules Manufacturing: Production delays, Quality failures, System errors, Performance degradation cu escalation policies și notification routing.","dirs":["/infra/prometheus/rules/manufacturing/"],"constraints":"business impact alerts; escalation policies; commit 'feat(obs): Manufacturing alerts'.","output":"Manufacturing alerting active"},

  {"step":566,"scope":"documentation-api","context":"API complete (553)","task":"Swagger documentation Manufacturing API: endpoints documentation, DTO schemas, example requests/responses, authentication requirements cu interactive testing.","dirs":["/standalone/numeriqo/apps/manufacturing/api/docs/"],"constraints":"complete API documentation; interactive examples; commit 'docs(mfg-api): Swagger complete'.","output":"Manufacturing API docs"},

  {"step":567,"scope":"documentation-user-manual","context":"UI complete (549)","task":"User manual Manufacturing: BOM management guide, Work Order execution, Production planning, Quality control, Shop Floor operations cu screenshots și workflows.","dirs":["/docs/manufacturing/user-manual/"],"constraints":"comprehensive user guide; screenshots updated; commit 'docs(mfg): user manual'.","output":"Manufacturing user documentation"},

  {"step":568,"scope":"documentation-technical","context":"System complete (565)","task":"Technical documentation Manufacturing: architecture overview, integration patterns, event schemas, worker contracts, deployment guide.","dirs":["/docs/manufacturing/technical/"],"constraints":"technical depth adequate; integration examples; commit 'docs(mfg): technical documentation'.","output":"Manufacturing technical docs"},

  {"step":569,"scope":"training-materials","context":"Documentation complete (568)","task":"Training materials Manufacturing: video tutorials, interactive guides, best practices, troubleshooting guide, FAQ pentru users și administrators.","dirs":["/docs/manufacturing/training/"],"constraints":"multimedia training materials; practical examples; commit 'docs(mfg): training materials'.","output":"Manufacturing training ready"},

  {"step":570,"scope":"demo-data-seed","context":"System functional (569)","task":"Demo data Manufacturing: sample products, BOMs, work centers, work orders, quality plans pentru demonstration și testing purposes cu realistic manufacturing scenarios.","dirs":["/core/scripts/seed/manufacturing/"],"constraints":"realistic manufacturing data; no real PII; commit 'feat(seed): Manufacturing demo data'.","output":"Manufacturing demo data"},

  {"step":571,"scope":"migration-utilities","context":"Demo data ready (570)","task":"Migration utilities Manufacturing: data import tools, legacy system integration, data transformation scripts, validation utilities pentru customer onboarding.","dirs":["/core/scripts/migration/manufacturing/"],"constraints":"robust data validation; transformation logging; commit 'feat(migration): Manufacturing utilities'.","output":"Manufacturing migration tools"},

  {"step":572,"scope":"backup-recovery","context":"Migration tools ready (571)","task":"Backup și recovery procedures Manufacturing: automated database backups, point-in-time recovery, disaster recovery procedures, data integrity verification.","dirs":["/core/scripts/backup/manufacturing/"],"constraints":"automated backup verification; recovery procedures tested; commit 'feat(backup): Manufacturing procedures'.","output":"Manufacturing backup/recovery"},

  {"step":573,"scope":"monitoring-synthetic","context":"Backup procedures ready (572)","task":"Synthetic monitoring Manufacturing: health check endpoints, critical workflow monitoring, performance baseline monitoring, availability tracking.","dirs":["/core/monitoring/synthetic/manufacturing/"],"constraints":"critical path monitoring; SLA tracking; commit 'feat(monitoring): Manufacturing synthetic'.","output":"Manufacturing synthetic monitoring"},

  {"step":574,"scope":"capacity-planning","context":"Monitoring complete (573)","task":"Capacity planning Manufacturing: resource utilization analysis, scalability projections, performance bottleneck identification, optimization recommendations.","dirs":["/docs/manufacturing/capacity/"],"constraints":"scalability analysis detailed; optimization actionable; commit 'docs(capacity): Manufacturing planning'.","output":"Manufacturing capacity planning"},

  {"step":575,"scope":"compliance-validation","context":"Capacity planning ready (574)","task":"Compliance validation Manufacturing: manufacturing standards compliance, quality system requirements, audit trail completeness, regulatory requirements check.","dirs":["/core/compliance/manufacturing/"],"constraints":"regulatory compliance verified; audit trails complete; commit 'feat(compliance): Manufacturing validation'.","output":"Manufacturing compliance verified"},

  {"step":576,"scope":"integration-testing-suite","context":"Compliance verified (575)","task":"Integration test suite Manufacturing: full system integration tests, cross-module compatibility, data flow verification, performance under load.","dirs":["/tests/integration/manufacturing/"],"constraints":"complete integration coverage; cross-module testing; commit 'test(integration): Manufacturing suite'.","output":"Manufacturing integration test suite"},

  {"step":577,"scope":"release-preparation","context":"Integration tests ready (576)","task":"Release preparation Manufacturing: version tagging, release notes, deployment checklist, rollback procedures, stakeholder communication.","dirs":["/releases/manufacturing/F3/"],"constraints":"comprehensive release package; rollback tested; commit 'release(mfg): F3 preparation'.","output":"Manufacturing release ready"},

  {"step":578,"scope":"go-live-checklist","context":"Release prepared (577)","task":"Go-live checklist Manufacturing: production readiness verification, monitoring setup confirmation, support procedures, escalation paths, success criteria definition.","dirs":["/ops/manufacturing/go-live/"],"constraints":"production readiness verified; support procedures ready; commit 'ops(mfg): go-live checklist'.","output":"Manufacturing go-live ready"},

  {"step":579,"scope":"post-deployment-monitoring","context":"Go-live ready (578)","task":"Post-deployment monitoring Manufacturing: success metrics tracking, user adoption monitoring, performance baseline establishment, issue tracking setup.","dirs":["/ops/manufacturing/post-deploy/"],"constraints":"success metrics defined; monitoring comprehensive; commit 'ops(mfg): post-deploy monitoring'.","output":"Manufacturing post-deploy monitoring"},

  {"step":580,"scope":"continuous-improvement","context":"Post-deploy monitoring active (579)","task":"Continuous improvement framework Manufacturing: feedback collection, performance optimization, feature enhancement pipeline, user experience improvements.","dirs":["/ops/manufacturing/improvement/"],"constraints":"improvement framework systematic; user feedback integrated; commit 'ops(mfg): continuous improvement'.","output":"Manufacturing continuous improvement"}
]
```

## Success Criteria

**✅ F3 Manufacturing Objectives met:**

1. **BOM Management** – Complete Bill of Materials system cu multi-level BOM support
2. **MRP II Beta** – Material Requirements Planning cu AI forecast integration  
3. **Shop Floor Control** – Real-time production tracking și terminal integration
4. **Quality Management** – AI-powered quality control cu automated classification
5. **Integration Ready** – Full integration cu iWMS, Sales, Procurement prin Event Bus
6. **AI-Powered** – Forecast, classification, KPI reporting, și optimization workers
7. **Mobile Ready** – Shop floor terminals cu PWA support
8. **Enterprise Grade** – Security, observability, performance, deployment automation

**KPIs F3:**
- BOM explosion performance: <2s pentru multi-level BOMs
- Work order processing: 200+ TPS shop floor transactions  
- AI quality classification: >85% accuracy
- MRP calculation: 100 products în <5s
- System availability: >99.9%
- Mobile response time: <1s pentru shop floor operations

**Deliverables:**
- 81 JSON implementation steps (500-580)
- Complete Manufacturing Execution System
- AI-powered quality control și forecasting
- Real-time shop floor integration
- Executive dashboards și analytics
- Mobile-first shop floor terminals
- Enterprise security și compliance
- Full observability și monitoring
