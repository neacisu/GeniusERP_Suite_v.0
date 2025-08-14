# 8 · Roadmap Vettify (F2) — CRM + Marketing

**Scop:** livrarea aplicației stand‑alone **`vettify.app`** (CRM + Marketing) ca micro‑frontend cu API NestJS și integrare cu workerii `ai.summary` și `ai.churn`. Vettify acoperă **Leads, Accounts, Contacts, Opportunities, Campaigns** + automatizări ușoare (email sequences) și se integrează cu Order‑to‑Cash prin consumul evenimentelor `sales.order.created`.

## Cum să folosești această documentație

Această documentație reprezintă un roadmap detaliat pentru dezvoltarea aplicației stand-alone Vettify.app (CRM + Marketing). Lista de pași este organizată sub formă de obiecte JSON, fiecare element corespunzând unei etape concrete de implementare. Iată câteva sfaturi pentru a utiliza eficient această documentație:

**Parcurge pașii în ordine:** Fiecare element JSON are un câmp step (indexul pasului) și descrie o acțiune ce trebuie realizată. Este recomandat să se abordeze aceste task-uri sequential, deoarece unele depind de livrările anterioare (indicate în câmpul context).

**Înțelege structura câmpurilor:** Fiecare obiect conține câmpuri esențiale – scope indică sub-sistemul sau componenta vizată, context oferă detalii despre starea proiectului înainte de acest pas, task descrie în mod imperativ acțiunea de efectuat, dirs precizează directoarele/proiectele afectate, constraints enumeră reguli sau condiții ce trebuie respectate (ex.: convenții de commit, limite de performanță, stil de cod), iar output descrie pe scurt rezultatul așteptat în urma implementării.

**Respectă constraints:** Câmpul constraints include cerințe stricte precum respectarea convențiilor de commit (ex. Conventional Commits), rularea linter-elor, evitarea includerii secretelor în cod, sau condiții de performanță și securitate. Asigură-te că la finalul fiecărui pas aceste condiții sunt îndeplinite (pipeline-urile CI/CD vor verifica multe dintre ele automat).

**Verifică output-ul așteptat:** După ce implementezi un pas, compară rezultatul cu descrierea din output. Acesta oferă un indiciu dacă implementarea ta a atins obiectivul (de ex. un test care trece, un modul generat, o funcționalitate vizibilă în UI sau metrici expuse în sistemul de monitorizare).

**Navighează după scope:** Pașii sunt grupați logic prin câmpul scope (ex. „frontend-…", „api-…", „ui-…", „security-…"). Poți prioritiza sau delega anumite sub-sisteme pe baza acestei clasificări, dacă lucrează mai mulți dezvoltatori în paralel. De asemenea, dacă întâmpini dificultăți într-un anumit domeniu (ex. configurarea bus-ului de evenimente), poți identifica toți pașii relaționați (ex. cei cu scope care conține „bus").

**Precondiții și context:** Documentația presupune că Gate-ul F1 (faza anterioară) a fost trecut cu succes (ex. shell-ul aplicației este funcțional, modulul Admin-Core și Worker Registry sunt în starea dorită). Astfel, pașii de față (F2) se concentrează pe modulul Vettify și integrarea sa cu restul platformei. Înainte de a începe, asigură-te că ai setat corect mediul (baza de date, cluster MinIO, chei JWT, etc.), conform contextului menționat la începutul listei.

După ce ai parcurs întregul roadmap, modulul Vettify ar trebui să fie complet implementat, integrat (inclusiv cu serviciile ANAF/REGES pentru verificarea companiilor) și gata de testare end-to-end în ecosistemul Genius ERP. Folosește această listă ca ghid de implementare, dar și ca listă de verificare (checklist) pentru a te asigura că nu scapă nimic neimplementat.

## 1) Pre‑condiții & Scope

* **Gate F1 trecut**: Shell vizibil (3 widget‑uri), Admin Core & Worker Registry verzi.
* **Event‑Bus v1** și naming `<module>.<ctx>.<event>` deja stabilite; hook `scripts/lint-rmq.sh` obligatoriu.
* **Multitenancy & date**: PostgreSQL 17 (cluster per tenant, schema per modul), MinIO per tenant, Redis per tenant, **RLS pe `tid/whid/mid`**.
* **CRITICAL DEPENDENCY - Worker Fleet ANAF/REGES** disponibil și TESTAT (F1 steps 287-292 COMPLETE):
  - `anaf.taxpayer` (step 288) - validare CUI clienți/prospects
  - `anaf.efactura` (step 289) - transmitere e-Factură
  - `anaf.etransport` (step 290) - declarații transport
  - `anaf.saft` (step 291) - SAF-T D406
  - `reges` (step 292) - Revisal Online
* **Worker Fleet AI** disponibil: `ai.summary`, `ai.churn`, `email.send`, `pdf.render`, `etl.sync`.
* **Stack fix**: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workeri), RabbitMQ 3.14 + Redis 7 (bus/queue), IaC: Terraform + Helmfile + Argo CD.

## 2) Bounded‑Context & Interfețe

* **Entități principale**: `account`, `contact`, `lead`, `opportunity`, `campaign` (email).
* **Publish**: `crm.lead.created`, `crm.opportunity.stage_changed`, `crm.campaign.sent`.
* **Consume**: `sales.order.created` (enrichment CRM), eventual `wms.shipment.delivered` pentru timeline account.&#x20;

## 3) Securitate & RBAC

* Scopes Keycloak `crm/*` adăugate în realm export (F2 step 357). Guard JWT + RLS pe toate tabelele.&#x20;
* ABAC la UI (ascunde meniuri pentru roluri nepermise) sincronizat cu Shell nav dinamic (F2 step 366/367).&#x20;

## 4) Observabilitate

* OTel traces frontend→API→worker; Prometheus HTTP metrics pe API; dashboard dedicat *Vettify CRM* în Grafana.

## 5) CI/CD & Gating

* Pipeline `module-ci.yml` cu build/test/scan (Trivy HIGH), cosign sign/attest, publish OCI, Argo sync dev; integrat în E2E O2C pipeline (F2 steps 361–366).&#x20;

## 6) Structură directoare (canonice)

* `standalone/vettify/apps/frontend/**` (Vite Federation remote)
* `standalone/vettify/apps/api/**` (NestJS 11)
* `standalone/vettify/apps/workers/ai.summary/**`, `ai.churn/**` (task wrappers + clients)
* se aliniază arborelui din **Instrucțiuni STRICTE** (nu folosi `/apps` la root fără `standalone/`).

## 7) Format JSON extins – câmpuri obligatorii (prompts CursorAI)

* `step` – index consecutiv **310–399 (sincronizat cu umbrela F2)** pentru consistență cu roadmap-ul general F2.
* `scope` – sub‑sistem vizat (max 3–4 cuvinte)
* `context` – livrări anterioare relevante
* `task` – instrucțiune imperativă clară
* `dirs` – directoare vizate (prefixe canonice `standalone/**`, `core/**`)
* `constraints` – reguli stricte (commit‑msg, lint‑paths, fără secrete)
* `output` – rezultat așteptat

> Nota de conformitate: păstrează **stack‑ul fix**, naming events v1 și lint‑paths; commit‑uri cu Conventional Commits; **nu** introduce tehnologii neaprobate.

---

## 8) CursorAI Prompts (Vettify 310–399 - Sincronizat F2)

```json
[
  {"step":310,"scope":"scaffold-module","context":"F2 umbrella aprobat; create-module.ts disponibil","task":"Generează scheletul stand-alone `vettify` (frontend, api, workers) cu flagurile Nx/tags.","dirs":["/standalone/vettify/"],"constraints":"folosește scripts/create-module.ts --standalone vettify --with-ai; tags Nx module:vettify,layer:*; commit 'feat(vettify): scaffold module'.","output":"schelet module generat"},
  {"step":311,"scope":"frontend-bootstrap","context":"Module creat (310)","task":"Init UI React 19 + Vite 5 Federation + MUI 6 + Tailwind 3.","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"respectă tokens UI; fără Next.js; commit 'chore(vettify-ui): init vite federation'.","output":"frontend bootstrap"},
  {"step":312,"scope":"frontend-structure","context":"UI init (311)","task":"Creează maparea de directoare conform arborelui din Instrucțiuni STRICTE (assets, components, pages, widgets, etc.).","dirs":["/standalone/vettify/apps/frontend/src/"],"constraints":"păstrează subfolderele __tests__; lint‑paths canonical; commit 'refactor(vettify-ui): folders'.","output":"structură UI conformă"},
  {"step":313,"scope":"frontend-remote-entry","context":"Vite federation activă","task":"Expune `remoteEntry.js` și modulele `LeadsPage`, `OpportunitiesPage`, `CampaignsPage`.","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"nume expuneri stabile; commit 'feat(vettify-ui): expose remotes'.","output":"remotes exportate"},
  {"step":314,"scope":"frontend-theme","context":"UI tokens disponibili","task":"Integrează ThemeProvider, switch light/dark, persist în localStorage `theme`.","dirs":["/standalone/vettify/apps/frontend/src/"],"constraints":"conform ThemeHub; commit 'feat(vettify-ui): theme switch'.","output":"teme funcționale"},
  {"step":315,"scope":"frontend-nav","context":"Shell nav dinamic F2 (366/367)","task":"Adaugă manifest JSON pentru meniuri (Leads, Accounts, Campaigns) consumat de Shell.","dirs":["/standalone/vettify/apps/frontend/public/"],"constraints":"fallback static dacă `/v1/admin/nav` 404; commit 'feat(vettify-ui): nav manifest'.","output":"nav integrat"},
  {"step":316,"scope":"frontend-pages","context":"UI schelet","task":"Generează paginile `dashboard/`, `leads/`, `opportunities/`, `campaigns/`, `auth/` cu routing.","dirs":["/standalone/vettify/apps/frontend/src/pages/"],"constraints":"tanstack-router sau react-router; commit 'feat(vettify-ui): pages scaffold'.","output":"pagini create"},
  {"step":317,"scope":"frontend-data-layer","context":"Paginile create","task":"Configurează TanStack Query + axios client cu interceptoare JWT.","dirs":["/standalone/vettify/apps/frontend/src/"],"constraints":"timeout 5s, retry 1, p95 UI <2.5s; commit 'feat(vettify-ui): data layer'.","output":"data‑layer funcțional"},
  {"step":318,"scope":"frontend-forms","context":"UI forms necesare","task":"Integrează react-hook-form + zod pentru validări lead/opportunity.","dirs":["/standalone/vettify/apps/frontend/src/components/"],"constraints":"fără any; commit 'feat(vettify-ui): forms + validation'.","output":"formuri validate"},
  {"step":319,"scope":"frontend-widgets","context":"Observabilitate UX","task":"Adaugă widget health (API/Bus) + web-vitals colectate local.","dirs":["/standalone/vettify/apps/frontend/src/widgets/"],"constraints":"30s refresh; AbortController 3s; commit 'feat(vettify-ui): health + webvitals'.","output":"widget health + vitals"},

  {"step":320,"scope":"api-bootstrap","context":"Module creat (310)","task":"Inițializează NestJS 11 (Node 20, TS5) cu config, DTO pipes, Swagger protejat basic-auth.","dirs":["/standalone/vettify/apps/api/"],"constraints":"disable any; `npm run lint` green; commit 'chore(vettify-api): init nest'.","output":"API bootstrap"},
  {"step":321,"scope":"api-orm-config","context":"DB PG17 per tenant","task":"Configurează TypeORM data-source multi‑schema (schema `crm`).","dirs":["/standalone/vettify/apps/api/src/config/"],"constraints":"DSN din env; fără secrete hard‑code; commit 'feat(vettify-api): typeorm config'.","output":"TypeORM configurat"},
  {"step":322,"scope":"db-migrations-1","context":"ORM configurat (321)","task":"Creează migrations pentru `accounts`, `contacts` cu chei compuse (tid,mid,id) + RLS.","dirs":["/standalone/vettify/apps/api/src/migrations/"],"constraints":"RLS activ; index composite; extensia pgvector activă; commit 'feat(vettify-db): accounts+contacts'.","output":"tabele accounts/contacts"},
  {"step":323,"scope":"db-migrations-2","context":"Migrations 1 ok (322)","task":"Adaugă `leads`, `opportunities` (pipeline/stage), `campaigns` (email).","dirs":["/standalone/vettify/apps/api/src/migrations/"],"constraints":"enum stage; fk către accounts/contacts; commit 'feat(vettify-db): leads+opps+campaigns'.","output":"tabele leads/opps/campaigns"},
  {"step":324,"scope":"db-rls-tests","context":"RLS definit","task":"Teste Jest pentru politici RLS (select/insert/update izolate pe tid).","dirs":["/standalone/vettify/apps/api/tests/"],"constraints":"CI fail hard; commit 'test(vettify-db): rls policies'.","output":"RLS testat"},
  {"step":325,"scope":"entities-repos","context":"Migrations gata","task":"Definește entități TypeORM + repositories per entitate.","dirs":["/standalone/vettify/apps/api/src/entities/","/standalone/vettify/apps/api/src/repositories/"],"constraints":"no business in repo; commit 'feat(vettify-api): entities+repos'.","output":"layer repo stabil"},
  {"step":326,"scope":"services-core","context":"Repos create","task":"Implementează servicii `AccountsService`, `ContactsService`, `LeadsService`, `OpportunitiesService`, `CampaignsService`.","dirs":["/standalone/vettify/apps/api/src/services/crm/"],"constraints":"unit tests ≥80%; commit 'feat(vettify-api): core services'.","output":"servicii CRUD"},
  {"step":327,"scope":"dtos-validators","context":"Services gata","task":"DTO cu class-validator pentru create/update + custom validators (email, stage).","dirs":["/standalone/vettify/apps/api/src/dto/"],"constraints":"strict; commit 'feat(vettify-api): dtos + validators'.","output":"DTO complete"},
  {"step":328,"scope":"controllers-acc-contact","context":"DTO/Services OK","task":"Controllers `crm/accounts`, `crm/contacts` (CRUD, search, pagination).","dirs":["/standalone/vettify/apps/api/src/controllers/crm/accounts/","/standalone/vettify/apps/api/src/controllers/crm/contacts/"],"constraints":"p95 < 250ms; commit 'feat(vettify-api): accounts+contacts ctrl'.","output":"API accounts/contacts"},
  {"step":329,"scope":"account-verify","context":"DTO/Services OK","task":"Integrează verificarea companiilor cu serviciile ANAF și REGES la crearea/actualizarea Account: apelează `anaf.taxpayer` pentru validarea CUI și denumirea oficială, și (opțional) `reges.company` pentru numărul de angajați. Actualizează entitatea Account cu datele obținute.","dirs":["/standalone/vettify/apps/api/src/services/"],"constraints":"fără secrete expuse; tratează erorile serviciilor externe","output":"CUI verificat"},
  {"step":330,"scope":"controllers-leads","context":"DTO/Services OK","task":"Controller `crm/leads` (CRUD + qualify → convert).","dirs":["/standalone/vettify/apps/api/src/controllers/crm/leads/"],"constraints":"events on create; commit 'feat(vettify-api): leads ctrl'.","output":"API leads"},
  {"step":331,"scope":"controllers-opps","context":"Leads convert necesar","task":"Controller `crm/opportunities` (CRUD + stage transitions).","dirs":["/standalone/vettify/apps/api/src/controllers/crm/opportunities/"],"constraints":"emit stage_changed; commit 'feat(vettify-api): opportunities ctrl'.","output":"API opportunities"},
  {"step":332,"scope":"controllers-campaigns","context":"Campanii email","task":"Controller `crm/campaigns` (create/send/metrics).","dirs":["/standalone/vettify/apps/api/src/controllers/crm/campaigns/"],"constraints":"rate-limit 10 req/s; commit 'feat(vettify-api): campaigns ctrl'.","output":"API campaigns"},
  {"step":333,"scope":"auth-guards","context":"Scopes Keycloak crm/*","task":"Guard RBAC `crm:*` + mapare roluri la scope; interceptor tenant `tid`.","dirs":["/standalone/vettify/apps/api/src/guards/","/standalone/vettify/apps/api/src/middlewares/"],"constraints":"unit tested; commit 'feat(vettify-api): rbac guards'.","output":"autorizare activă"},
  {"step":334,"scope":"api-metrics","context":"Observability standard","task":"Prometheus Nest middleware (http_requests_seconds) + labels `tid`/`route`.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"no PII; commit 'feat(vettify-api): prom metrics'.","output":"metrics export"},
  {"step":335,"scope":"api-otel","context":"Traces end-to-end","task":"OTel SDK pentru Nest; propagare trace‑id către workers.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"Tempo integrat; commit 'feat(vettify-api): otel traces'.","output":"traces vizibile"},
  {"step":336,"scope":"bus-client","context":"SDK TS/Py bus gata F2 (302/303)","task":"Integrează client Event‑Bus (publish/consume) conform spec F2.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"naming v1; contract tests; commit 'feat(vettify-api): bus client'.","output":"bus integrat"},
  {"step":337,"scope":"events-publish","context":"Leads/Opportunities controllers","task":"Publică `crm.lead.created`, `crm.opportunity.stage_changed` la acțiunile relevante.","dirs":["/standalone/vettify/apps/api/src/controllers/"],"constraints":"include x-corr-id; commit 'feat(vettify-api): publish events'.","output":"events publish OK"},
  {"step":338,"scope":"events-consume","context":"O2C integrare","task":"Consumă `sales.order.created` pentru enrichment (link opportunity→SO); eventual `wms.shipment.delivered` pentru timeline Account; de asemenea, procesează evenimente de conformitate (ex. verificare ANAF finalizată) pentru a actualiza statusul Account-ului.","dirs":["/standalone/vettify/apps/api/src/subscribers/"],"constraints":"ack on success; commit 'feat(vettify-api): consume sales.order.created'.","output":"consumer activ"},
  {"step":339,"scope":"contracts-tests","context":"Bus spec & events","task":"Pact tests publisher/consumer pentru topic‑urile CRM.","dirs":["/core/tests/contract/event-bus/"],"constraints":"coverage ≥90%; commit 'test(vettify-bus): contracts'.","output":"contract tests verzi"},
  {"step":340,"scope":"lint-rmq-hook","context":"Naming enforcement","task":"Activează `scripts/lint-rmq.sh` în CI pentru PR‑uri Vettify.","dirs":["/.github/workflows/module-ci.yml","/core/scripts/lint-rmq.sh"],"constraints":"ci fail on error; commit 'ci(vettify): enforce rmq naming'.","output":"lint events activ"},

  {"step":341,"scope":"worker-ai-summary","context":"Worker Fleet disponibil","task":"Wrapper pentru invocarea `ai.summary` (rezumat întâlniri) + topic request/response.","dirs":["/standalone/vettify/apps/workers/ai.summary/src/"],"constraints":"OTel + metrics; commit 'feat(vettify-workers): ai.summary client'.","output":"ai.summary integrat"},
  {"step":342,"scope":"worker-ai-churn","context":"Risk scoring CRM","task":"Wrapper `ai.churn` (CatBoost/XGBoost) + mapare account→score.","dirs":["/standalone/vettify/apps/workers/ai.churn/src/"],"constraints":"feature store simplu în Redis; commit 'feat(vettify-workers): ai.churn client'.","output":"ai.churn integrat"},
  {"step":343,"scope":"email-send-worker","context":"Campanii email","task":"Invocă `email.send` pentru batch send + webhook status.","dirs":["/standalone/vettify/apps/api/src/services/crm/"],"constraints":"batch=100; retry backoff; commit 'feat(vettify-api): email send integration'.","output":"trimitere email funcțională"},
  {"step":344,"scope":"etl-sync-import","context":"Import leads CSV","task":"Integrează `etl.sync` pentru import CSV→PG (leads).","dirs":["/standalone/vettify/apps/api/src/services/etl/"],"constraints":"validări; commit 'feat(vettify-api): import leads etl'.","output":"import CSV functional"},
  {"step":345,"scope":"pdf-render-export","context":"Export campanie","task":"Invocă `pdf.render` pentru raport campanie (open/click).","dirs":["/standalone/vettify/apps/api/src/services/reporting/"],"constraints":"storare în MinIO SSE‑C; commit 'feat(vettify-api): campaign pdf export'.","output":"PDF campanie"},
  {"step":346,"scope":"minio-attachments","context":"Fișiere CRM","task":"Endpoint upload atașamente (contact/account) în MinIO per tenant.","dirs":["/standalone/vettify/apps/api/src/controllers/crm/"],"constraints":"SSE‑C; size<10MB; commit 'feat(vettify-api): attachments minio'.","output":"upload securizat"},
  {"step":347,"scope":"rate-limit-api","context":"Abuz endpoint send","task":"Rate-limit Traefik pentru `/campaigns/send` (10 req/s/user).","dirs":["/core/infra/helm/umbrella/"],"constraints":"token bucket Redis; commit 'feat(infra): vettify rate-limit'.","output":"rate-limit activ"},
  {"step":348,"scope":"audit-trail","context":"Security & audit","task":"Audit emitere campanii și conversie lead→opportunity; export CSV semnat.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"cosign sign; commit 'feat(vettify-api): audit trail'.","output":"audit trail"},
  {"step":349,"scope":"seed-data","context":"Demo necesar","task":"Seed F2 pentru CRM: 10 accounts, 30 contacts, 40 leads, 5 opportunities, 2 campaigns.","dirs":["/core/scripts/"],"constraints":"nu include PII real; commit 'feat(seed): vettify demo data'.","output":"seed demo CRM"},
  {"step":350,"scope":"api-e2e","context":"API stabil","task":"Teste Supertest pentru rutele CRM (CRUD + flow convert).","dirs":["/standalone/vettify/apps/api/tests/"],"constraints":"coverage ≥85%; commit 'test(vettify-api): e2e'.","output":"e2e API verde"},

  {"step":351,"scope":"ui-leads-table","context":"Frontend pages","task":"Tabel Leads cu DataGrid (sort/filter/paginate) + bulk actions.","dirs":["/standalone/vettify/apps/frontend/src/pages/leads/"],"constraints":"a11y on; commit 'feat(vettify-ui): leads table'.","output":"leads table"},
  {"step":352,"scope":"ui-lead-form","context":"Create/Update lead","task":"Form lead cu RHF+zod; submit către API.","dirs":["/standalone/vettify/apps/frontend/src/pages/leads/"],"constraints":"error states; commit 'feat(vettify-ui): lead form'.","output":"form lead"},
  {"step":353,"scope":"ui-opps-board","context":"Opportunities UX","task":"Kanban board pe stages cu drag&drop; change → publish stage_changed.","dirs":["/standalone/vettify/apps/frontend/src/pages/opportunities/"],"constraints":"optimistic update; commit 'feat(vettify-ui): opps board'.","output":"kanban opps"},
  {"step":354,"scope":"ui-accounts-view","context":"Accounts 360","task":"Pagina Account 360 (timeline evenimente și tab *Compliance* cu status ANAF/REGES).","dirs":["/standalone/vettify/apps/frontend/src/pages/accounts/"],"constraints":"consume sales.order.created; include status ANAF; commit 'feat(vettify-ui): account 360'.","output":"view account"},
  {"step":355,"scope":"ui-campaigns","context":"Campanii email","task":"Listă campanii + wizard creare + send ghidat.","dirs":["/standalone/vettify/apps/frontend/src/pages/campaigns/"],"constraints":"confirm modal; commit 'feat(vettify-ui): campaigns'.","output":"campanii UI"},
  {"step":356,"scope":"ui-churn-badge","context":"ai.churn integrat","task":"Afișează `ChurnRiskBadge` pe account (score buckets).","dirs":["/standalone/vettify/apps/frontend/src/components/"],"constraints":"no PII; commit 'feat(vettify-ui): churn badge'.","output":"riscuri vizibile"},
  {"step":357,"scope":"ui-summary-panel","context":"ai.summary integrat","task":"Panel rezumat meeting/email pe lead/opportunity.","dirs":["/standalone/vettify/apps/frontend/src/components/"],"constraints":"loaders și retries; commit 'feat(vettify-ui): summary panel'.","output":"rezumate afișate"},
  {"step":358,"scope":"ui-health-widget","context":"Widget health (319)","task":"Extinde health: RMQ lag + Celery lag (graf mini‑sparklines).","dirs":["/standalone/vettify/apps/frontend/src/widgets/health/"],"constraints":"fetch la 30s; commit 'feat(vettify-ui): health metrics'.","output":"health extins"},
  {"step":359,"scope":"ui-a11y-perf","context":"Accesibilitate/Perf","task":"JSX a11y rules + Lighthouse CI (LCP ≤ 2.5s).","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"CI fail pe sub 90; commit 'ci(vettify-ui): a11y+lhci'.","output":"gates UI"},
  {"step":360,"scope":"ui-e2e","context":"UX stabil","task":"Teste Playwright pentru fluxurile Leads→Opportunities→Campaign send.","dirs":["/standalone/vettify/apps/frontend-e2e/"],"constraints":"headless; commit 'test(vettify-ui): e2e'.","output":"e2e UI verde"},

  {"step":361,"scope":"helm-frontend","context":"Deploy UI","task":"Helm chart `vettify-frontend` (Deployment+Service+Ingress+HPA).","dirs":["/core/infra/helm/vettify-frontend/"],"constraints":"cosign sign; commit 'feat(infra): helm vettify-frontend'.","output":"chart UI OCI"},
  {"step":362,"scope":"helm-api","context":"Deploy API","task":"Helm chart `vettify-api` (Deployment+Service+Ingress+HPA).","dirs":["/core/infra/helm/vettify-api/"],"constraints":"cosign sign; commit 'feat(infra): helm vettify-api'.","output":"chart API OCI"},
  {"step":363,"scope":"argocd-apps","context":"CD Argo","task":"Argo Application YAML `vettify-frontend.yaml`, `vettify-api.yaml`.","dirs":["/core/infra/k8s/argocd/"],"constraints":"auto‑sync; commit 'feat(infra): argocd vettify'.","output":"Argo apps"},
  {"step":364,"scope":"k8s-secrets","context":"JWT/DSN","task":"ExternalSecrets pentru JWT public key și DSN PG/MinIO/Redis.","dirs":["/core/infra/k8s/external-secrets/"],"constraints":"fără secrete în git; commit 'feat(infra): vettify secrets'.","output":"secrete sincronizate"},
  {"step":365,"scope":"service-monitors","context":"Scrape metrics","task":"ServiceMonitor pentru API și UI.","dirs":["/core/infra/k8s/service-monitors/"],"constraints":"namespace core‑apps; commit 'feat(obs): sm vettify'.","output":"SM create"},
  {"step":366,"scope":"grafana-dashboard","context":"Observability","task":"Dashboard Grafana `vettify_crm.json` (p95, error_rate, RMQ lag, Celery lag).","dirs":["/core/infra/grafana/provisioning/dashboards/"],"constraints":"uid stabil; commit 'feat(obs): dashboard vettify'.","output":"dashboard live"},
  {"step":367,"scope":"alert-rules","context":"SLO","task":"Alertmanager rules pentru error_rate>1% și lag>60s.","dirs":["/core/infra/k8s/alertmanager/rules/"],"constraints":"route slack; commit 'feat(obs): alerts vettify'.","output":"alerte live"},
  {"step":368,"scope":"opa-policies","context":"Gatekeeper","task":"Constrainte OPA pt imagini fără `:latest` și tokens theme valide.","dirs":["/core/infra/policies/opa/"],"constraints":"mode warn dev; commit 'feat(sec): opa vettify'.","output":"OPA activ"},
  {"step":369,"scope":"keycloak-scopes","context":"Realm export F2 (357)","task":"Adaugă scope‑urile `crm/*` și maparea roluri (marketing, sales).","dirs":["/core/infra/keycloak/realm-export.json"],"constraints":"validate la CI; commit 'feat(sec): keycloak crm scopes'.","output":"scopes adăugate"},
  {"step":370,"scope":"rate-limit-ingress","context":"API send","task":"Traefik rate‑limit pentru `POST /campaigns/send`.","dirs":["/core/infra/helm/umbrella/"],"constraints":"token bucket; commit 'feat(infra): rate-limit vettify'.","output":"throttle activ"},

  {"step":371,"scope":"ci-workflow","context":"module-ci model F2 (305)","task":"`module-ci.yml` pentru Vettify (build/test/scan/sign/publish + Argo sync dev).","dirs":["/.github/workflows/"],"constraints":"Trivy HIGH; cosign attest SPDX; commit 'ci(vettify): module-ci'.","output":"pipeline CI"},
  {"step":372,"scope":"coverage-badge","context":"Codecov","task":"Publică coverage badge în README root + status check.","dirs":["/README.md",".github/workflows/"],"constraints":"Codecov token secret; commit 'ci(vettify): codecov badge'.","output":"badge coverage"},
  {"step":373,"scope":"dockerfiles","context":"Containerizare","task":"Dockerfile multi‑stage pentru API și UI (user non‑root 1000).","dirs":["/standalone/vettify/docker/"],"constraints":"scan Trivy; commit 'build(vettify): dockerfiles'.","output":"imagini ok"},
  {"step":374,"scope":"supply-chain","context":"Sigiliu imagini","task":"cosign sign & attest pentru imaginile Vettify.","dirs":["/.github/workflows/"],"constraints":"KMS key; commit 'ci(vettify): cosign'.","output":"imagini semnate"},
  {"step":375,"scope":"postman-collection","context":"DX QA","task":"Exportă colecție Postman Vettify în `docs/postman/vettify.json`.","dirs":["/core/docs/postman/"],"constraints":"v2.1 schema; commit 'docs(vettify): postman'.","output":"colecție postman"},
  {"step":376,"scope":"seed-script","context":"Demo e2e","task":"Script `scripts/seed-vettify.ts` (folosește SDK TS).","dirs":["/core/scripts/"],"constraints":"fără PII; commit 'feat(seed): script vettify'.","output":"seed script"},
  {"step":377,"scope":"shell-integration","context":"F2 step 366","task":"Publică remotes Vettify în Shell nav dinamic.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"fallback static; commit 'feat(shell): add vettify remote'.","output":"vizibil în Shell"},
  {"step":378,"scope":"rbac-ui-hide","context":"F2 step 367","task":"Ascunde meniuri UI Vettify pentru roluri fără scope `crm/*`.","dirs":["/core/apps/shell-gateway/frontend/","/standalone/vettify/apps/frontend/"],"constraints":"OPA validate; commit 'feat(rbac): hide menus'.","output":"RBAC UI corect"},
  {"step":379,"scope":"analytics-feed","context":"F2 step 368","task":"Replică evenimente CRM în lakehouse prin `etl.sync`.","dirs":["/standalone/vettify/apps/api/src/subscribers/"],"constraints":"cron orchestrat; commit 'feat(vettify): analytics feed'.","output":"feed OLAP"},
  {"step":380,"scope":"audit-export","context":"F2 step 369","task":"Export audit trail semnat Cosign pentru acțiuni CRM.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"hash verificabil; commit 'feat(vettify): audit export'.","output":"audit export"},

  {"step":381,"scope":"ui-kpis","context":"Dashboard","task":"Carduri KPI: leads today, conv rate, opps in stage, churn risky accounts.","dirs":["/standalone/vettify/apps/frontend/src/pages/dashboard/"],"constraints":"query cached; commit 'feat(vettify-ui): KPI cards'.","output":"dashboard KPI"},
  {"step":382,"scope":"ui-filters","context":"UX listări","task":"Filtre salvabile (URL‑driven) pentru Leads/Opportunities.","dirs":["/standalone/vettify/apps/frontend/src/pages/{leads,opportunities}/"],"constraints":"debounce 300ms; commit 'feat(vettify-ui): filters'.","output":"filtre salvabile"},
  {"step":383,"scope":"ui-bulk-import","context":"Import CSV (343)","task":"UI wizard import leads (.csv) cu preview și mapare coloane.","dirs":["/standalone/vettify/apps/frontend/src/pages/leads/"],"constraints":"validări; commit 'feat(vettify-ui): import wizard'.","output":"import UI"},
  {"step":384,"scope":"ui-email-templates","context":"Campanii","task":"Editor simple email template (MJML/HTML simplu) + preview.","dirs":["/standalone/vettify/apps/frontend/src/pages/campaigns/"],"constraints":"sanitizare HTML; commit 'feat(vettify-ui): email templates'.","output":"editor template"},
  {"step":385,"scope":"ui-attachments","context":"MinIO attachments (345)","task":"Uploader drag‑and‑drop pe account/contact cu progres.","dirs":["/standalone/vettify/apps/frontend/src/components/"],"constraints":"size<10MB; commit 'feat(vettify-ui): uploader'.","output":"uploader"},
  {"step":386,"scope":"ui-activity-timeline","context":"360 view","task":"Timeline activități combinat (events CRM + sales.order.created).","dirs":["/standalone/vettify/apps/frontend/src/components/"],"constraints":"virtualize list; commit 'feat(vettify-ui): activity timeline'.","output":"timeline unificat"},
  {"step":387,"scope":"ui-notifications","context":"UX feedback","task":"Toasts unificate pentru succes/eroare cu retry.","dirs":["/standalone/vettify/apps/frontend/src/components/common/"],"constraints":"a11y roles; commit 'feat(vettify-ui): notifications'.","output":"notificări"},
  {"step":388,"scope":"ui-accessibility","context":"Conformitate","task":"Rulare eslint-plugin-jsx-a11y și corectarea problemelor.","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"CI fail on error; commit 'chore(vettify-ui): a11y rules'.","output":"a11y conform"},
  {"step":389,"scope":"ui-performance","context":"Budget perf","task":"Lighthouse CI integrat în pipeline pentru Vettify UI.","dirs":["/.github/workflows/module-ci.yml"],"constraints":"LCP ≤ 2.5s; commit 'ci(vettify-ui): lhci'.","output":"perf gate"},
  {"step":390,"scope":"ui-stories","context":"Catalog UI","task":"Storybook pentru componente cheie (Button/Card/Modal/LeadForm).","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"CSF3; commit 'docs(vettify-ui): storybook'.","output":"stories UI"},

  {"step":391,"scope":"tests-unit-api","context":"Stabilitate","task":"Unit tests servicii CRM (≥80%).","dirs":["/standalone/vettify/apps/api/"],"constraints":"jest; commit 'test(vettify-api): unit services'.","output":"coverage 80%"},
  {"step":392,"scope":"tests-unit-ui","context":"Stabilitate","task":"Vitest + React Testing Library pentru componente cheie.","dirs":["/standalone/vettify/apps/frontend/"],"constraints":"coverage ≥80%; commit 'test(vettify-ui): unit'.","output":"coverage UI"},
  {"step":393,"scope":"tests-e2e-bus","context":"Evenimente","task":"E2E evenimente publish/consume pe bus pentru CRM.","dirs":["/standalone/vettify/apps/api/tests/"],"constraints":"Pact verify; commit 'test(vettify-bus): e2e'.","output":"e2e bus"},
  {"step":394,"scope":"security-trivy","context":"Supply-chain","task":"Trivy FS + image scan în CI, prag HIGH.","dirs":["/.github/workflows/module-ci.yml"],"constraints":"--severity HIGH --exit-code 1; commit 'ci(vettify): trivy high'.","output":"scan securitate"},
  {"step":395,"scope":"security-deps","context":"NPM/PNPM","task":"Audit dependențe și fix pentru UI/API.","dirs":["/standalone/vettify/"],"constraints":"pnpm audit fix; commit 'chore(vettify): deps audit'.","output":"deps curate"},
  {"step":396,"scope":"docs-api","context":"DX","task":"Documentează API în `docs/api/vettify.md` + exemple curl.","dirs":["/core/docs/api/"],"constraints":"updatat la CI; commit 'docs(vettify): api'.","output":"doc API"},
  {"step":397,"scope":"docs-architecture","context":"Context view","task":"Diagrame Mermaid pt entități și events (ctx view).","dirs":["/standalone/vettify/docs/architecture/"],"constraints":"export svg; commit 'docs(vettify): diagrams'.","output":"diagrame ctx"},
  {"step":398,"scope":"docs-onboarding","context":"Handover","task":"Ghid onboarding dev pentru Vettify (run local/dev).","dirs":["/standalone/vettify/README.md"],"constraints":"clar, succint; commit 'docs(vettify): onboarding'.","output":"onboarding doc"},
  {"step":399,"scope":"perf-k6","context":"Synthetic tests","task":"Script k6 100 VU / flux CRM; thresholds error_rate<1%.","dirs":["/standalone/vettify/tests/k6/"],"constraints":"report CI; commit 'test(vettify): k6'.","output":"raport k6"},
  {"step":400,"scope":"smoke-tests","context":"CD canary","task":"Smoke tests post‑deploy (health checks, /metrics).","dirs":["/.github/workflows/module-ci.yml"],"constraints":"stop rollout la fail; commit 'ci(vettify): smoke'.","output":"smoke verde"},

  {"step":401,"scope":"rls-guard-tests","context":"RLS critic","task":"Test end‑to‑end că datele tenant A nu sunt vizibile în tenant B.","dirs":["/core/tests/security/","/standalone/vettify/apps/api/tests/"],"constraints":"ci fail hard; commit 'test(vettify): rls guard'.","output":"RLS OK"},
  {"step":402,"scope":"error-budget","context":"SLO","task":"Definește SLI/SLO pentru Vettify (p95<250ms, error_rate<1%).","dirs":["/core/infra/grafana/provisioning/dashboards/"],"constraints":"publică în dashboard; commit 'docs(vettify): SLO'.","output":"SLO vizibile"},
  {"step":403,"scope":"opa-ci-policy","context":"Gatekeeper","task":"Rule CI pentru interzicerea imaginilor `:latest` și validarea theme tokens.","dirs":["/.github/workflows/module-ci.yml"],"constraints":"deny on error; commit 'ci(vettify): opa gate'.","output":"OPA enforce"},
  {"step":404,"scope":"release-notes","context":"Relese mgmt","task":"Generează release notes automat din Conventional Commits.","dirs":["/.github/workflows/"],"constraints":"semantic‑release; commit 'ci(vettify): release notes'.","output":"notes generate"},
  {"step":405,"scope":"bug-report-template","context":"DX QA","task":"Adaugă GitHub Issue Template pentru bug‑uri Vettify.","dirs":["/.github/ISSUE_TEMPLATE/"],"constraints":"labels default; commit 'docs(vettify): issue template'.","output":"template issues"},
  {"step":406,"scope":"security-headers","context":"API hardening","task":"Adaugă Helmet + rate‑limit generic pe API.","dirs":["/standalone/vettify/apps/api/src/"],"constraints":"nu dubla Traefik rate‑limit; commit 'feat(vettify-api): helmet + rate-limit'.","output":"headers + throttle"},
  {"step":407,"scope":"feature-flags","context":"Rollouts","task":"Feature flag `campaign_send_v2` (env‑driven).","dirs":["/standalone/vettify/apps/frontend/src/","/standalone/vettify/apps/api/src/"],"constraints":"default off; commit 'feat(vettify): flag campaign_send_v2'.","output":"flag introdus"},
  {"step":408,"scope":"telemetry-ui","context":"UX metrics","task":"Trimite web‑vitals către endpoint metrics UI→Prometheus.","dirs":["/standalone/vettify/apps/frontend/src/"],"constraints":"no PII; commit 'feat(vettify-ui): webvitals exporter'.","output":"vitals colectate"},
  {"step":409,"scope":"handover-doc","context":"Închidere modul","task":"Document `F2_handover.md` (secțiunea Vettify) cu link la dashboards, Argo apps, Postman.","dirs":["/core/docs/handovers/"],"constraints":"semnat; commit 'docs(vettify): handover F2'.","output":"handover pregătit"},
  {"step":410,"scope":"gate-f2-check","context":"Gate F2 umbrela","task":"Rulează `scripts/gate-f2.sh` și remediază orice neconformitate înainte de merge.","dirs":["/core/scripts/"],"constraints":"exit>0 la eroare; commit 'ci(vettify): gate-f2 pass'.","output":"Gate F2 trecut"}
]
```

---

## 9) Note de implementare

* **Căi canonice & arbore directoare**: folosește exact structura indicată pentru standalone apps; nu devia la `/apps` fără prefix `standalone/`.
* **Evenimente & naming**: menține convențiile v1 și validează în CI cu `lint-rmq.sh`.&#x20;
* **Workers**: `ai.summary` și `ai.churn` sunt deja parte din Worker Fleet — integrează doar clienții și queue‑urile; nu schimba stack‑ul (Python 3.13 + Celery/Ray).
* **Multitenancy/RLS**: izolare strictă `tid/whid/mid` conform modelului de date Fasei F2.
* **CI/CD**: Trivy HIGH, cosign sign/attest, Argo sync, canary + rollback metric‑based conform umbrelei F2.&#x20;