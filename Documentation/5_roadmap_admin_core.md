# 5 • Roadmap Admin Core (39 prompts CursorAI)

**Format JSON extins** – câmpuri obligatorii:
• `step` – index original (păstrăm 225-263 pentru trasabilitate)
• `scope` – sub-sistem vizat (max 3-4 cuvinte)
• `context` – livrări anterioare relevante
• `task` – instrucțiune imperativă clară
• `dirs` – listează directoarele vizate
• `constraints` – reguli stricte (commit-msg, chmod, etc.)
• `output` – rezultat așteptat

Structura respectă identic convențiile din **F0** și **F1**; nu introduce termene, doar ordinea logică.

## Umbrella - Dependencies & Context F1

| Interval | Effort | Scop/Componente | Layer | Dependințe F0 |
|----------|--------|-----------------|-------|----------------|
| 1‑4 | 1 SW | Event Bus RMQ namespaces & conventions v1 | infra | **0‑20, 33** |

```json
[
  {"step":225,"scope":"admin-core-skel","context":"Admin Core inexistent.","task":"`scripts/create-module.ts` generează `admin-core` (frontend, api, workers).","dirs":["/core/apps/admin-core/{frontend,api}/"],"constraints":"commit 'feat(admin-core): skeleton'.","output":"module skeleton"},
  {"step":226,"scope":"admin-db-migrations","context":"PG schema lipsă.","task":"Creează migrations TypeORM tabele `settings`, `roles`, `themes`.","dirs":["/core/apps/admin-core/api/src/migrations/"],"constraints":"include tid,whid.","output":"migrations SQL"},
  {"step":227,"scope":"admin-rbac-service","context":"Tabele create.","task":"Serviciu NestJS `RbacService` CRUD roluri + scope uri.","dirs":["/core/apps/admin-core/api/src/"],"constraints":"unit tests 80%.","output":"serviciu RBAC"},
  {"step":228,"scope":"admin-settings-api","context":"Settings table există.","task":"Controller `SettingsController` GET/PUT tenant-scoped.","dirs":["/core/apps/admin-core/api/src/controllers/"],"constraints":"Guard tid.","output":"API settings"},
  {"step":229,"scope":"admin-theme-api","context":"Theme Hub table.","task":"Endpoint `/themes` POST → validate JSON tokens.","dirs":["/core/apps/admin-core/api/src/"],"constraints":"payload 50KB max.","output":"API themes"},
  {"step":230,"scope":"admin-dtos","context":"Validare lipsă.","task":"Define DTO cu `class-validator`, pipe global validation.","dirs":["/core/apps/admin-core/api/src/dto/"],"constraints":"no any.","output":"DTO stricte"},
  {"step":231,"scope":"admin-auth-guard","context":"JWT guard generic.","task":"Extinde AuthGuard pentru claims `scp` + `role`.","dirs":["/core/apps/admin-core/api/src/guards/"],"constraints":"unit tested.","output":"guard RBAC"},
  {"step":232,"scope":"admin-configmap","context":"Valori default.","task":"Helm `ConfigMap` `admin-defaults` + `ExternalSecret admin-theme` din SecretsManager","dirs":["/infra/helm/admin-core/","/infra/k8s/"],"constraints":"ESO gata (step 41).","output":"ConfigMap + secret sync"},
  {"step":233,"scope":"admin-unit-tests","context":"Coverage sub 80%.","task":"Adaugă teste servicii Settings & Rbac.","dirs":["/core/apps/admin-core/api/"],"constraints":"","output":"coverage 85%"},
  {"step":234,"scope":"admin-e2e-tests","context":"E2E lipsă.","task":"Supertest `e2e/settings.spec.ts` la /settings.","dirs":["/core/apps/admin-core/api/tests/"],"constraints":"","output":"e2e verde"},
  {"step":235,"scope":"admin-swagger","context":"API doc.","task":"Integrează Swagger module `/docs` protejat basic-auth.","dirs":["/core/apps/admin-core/api/"],"constraints":"info.version from pkg.","output":"Swagger online"},
  {"step":236,"scope":"admin-ui-skel","context":"Frontend gol.","task":"Scaffold MUI pages Settings, RBAC, ThemeHub consumând API.","dirs":["/core/apps/admin-core/frontend/"],"constraints":"Use tanstack-query.","output":"UI pagini"},
  {"step":237,"scope":"admin-ui-settings","context":"Skeleton creat.","task":"Finalizează Settings form cu react-hook-form + zod.","dirs":["/core/apps/admin-core/frontend/"],"constraints":"tests 80%.","output":"page settings"},
  {"step":238,"scope":"admin-ui-rbac","context":"Directory page.","task":"Implementează tabel Users + Roles cu DataGrid Pro.","dirs":["/core/apps/admin-core/frontend/"],"constraints":"","output":"RBAC directory"},
  {"step":239,"scope":"admin-ui-theme","context":"ThemeHub.","task":"Upload JSON theme, preview live în iframe Shell.","dirs":["/core/apps/admin-core/frontend/"],"constraints":"size<25KB.","output":"ThemeHub UI"},
  {"step":240,"scope":"admin-ui-tests","context":"Unit tests page.","task":"Vitest + Jest-dom pentru cele 3 pagini.","dirs":["/core/apps/admin-core/frontend/"],"constraints":"","output":"tests pass"},
  {"step":241,"scope":"admin-ui-e2e","context":"Playwright.","task":"Add `admin-e2e` test create role, edit theme.","dirs":["/core/apps/admin-core/frontend-e2e/"],"constraints":"","output":"e2e verde"},
  {"step":242,"scope":"admin-ci","context":"CI generic.","task":"Nx affected pentru admin-core build/test + upload coverage Codecov.","dirs":["/.github/workflows/ci-template.yml"],"constraints":"Codecov token secret.","output":"CI admin"},
  {"step":243,"scope":"admin-dockerfile","context":"Containerizare.","task":"Dockerfile api (multi-stage Nest build) + Dockerfile ui.","dirs":["/docker/"],"constraints":"non-root 1000.","output":"images ok"},
  {"step":244,"scope":"admin-helm-chart","context":"Deploy admin.","task":"Chart `infra/helm/admin-core/` include api, ui, ingress, HPA.","dirs":["/infra/helm/admin-core/"],"constraints":"cosign sign.","output":"chart OCI"},
  {"step":245,"scope":"admin-otel","context":"Traces lipsă.","task":"Enable OTEL NestJS exporter + resource.service.name admin-api.","dirs":["/core/apps/admin-core/api/"],"constraints":"","output":"traces Tempo"},
  {"step":246,"scope":"admin-prom-metrics","context":"Metrics default.","task":"Add Prometheus metrics middleware Nest (`http_requests_seconds`).","dirs":["/core/apps/admin-core/api/"],"constraints":"","output":"metrics"},
  {"step":247,"scope":"admin-grafana","context":"Dashboard.","task":"Grafana dashboard RBAC ops (role count, fail auth).","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"","output":"dashboard RBAC"},
  {"step":248,"scope":"admin-tenant-script","context":"Bootstrap tenant.","task":"Extinde `scripts/bootstrap-tenant.py` să cheme Admin API `/settings/init`.","dirs":["/scripts/"],"constraints":"","output":"script extins"},
  {"step":249,"scope":"admin-opa-policies","context":"Gatekeeper rule.","task":"Template Constraint `CTThemeValid` + Constraint `ThemeValid` limitează culoare hex.","dirs":["/infra/policies/opa/"],"constraints":"mode warn dev.","output":"OPA policy"},
  {"step":250,"scope":"admin-postman","context":"Colecție lipsă.","task":"Exportă Postman collection v2.1 în `docs/postman/admin-core.json`.","dirs":["/docs/postman/"],"constraints":"","output":"colecție postman"},
  {"step":251,"scope":"admin-hpa","context":"Scalare.","task":"Adaugă HPA CPU 50-300m pentru admin-api în chart.","dirs":["/infra/helm/admin-core/"],"constraints":"","output":"HPA activ"},
  {"step":252,"scope":"admin-jwt-secret","context":"JWT RS256.","task":"K8s Secret `admin-jwt` cu placeholder, montat la pod.","dirs":["/infra/k8s/"],"constraints":"no key leak.","output":"secret creat"},
  {"step":253,"scope":"admin-coverage-badge","context":"Codecov.","task":"Badge codecov în README root.","dirs":["/README.md"],"constraints":"","output":"badge vizibil"},
  {"step":254,"scope":"admin-argocd","context":"Continuous deploy.","task":"Argo Application YAML `admin-core.yaml`.","dirs":["/infra/k8s/argocd/"],"constraints":"","output":"Argo sync admin"},
  {"step":255,"scope":"wrk-registry-model","context":"Worker tabele lipsă.","task":"Entity TypeORM `WorkerStatus` (id,tag,ver,last_seen).","dirs":["/core/apps/admin-core/api/src/entities/"],"constraints":"","output":"model DB"},
  {"step":256,"scope":"wrk-registry-endpoints","context":"Model creat.","task":"Controller `/workers` GET list, PATCH heartbeat.","dirs":["/core/apps/admin-core/api/src/controllers/"],"constraints":"auth scope admin.","output":"API registry"},
  {"step":257,"scope":"wrk-registry-cron","context":"update-worker-registry existent F0.","task":"Adaugă logic scrape Celery /metrics și update status Redis.","dirs":["/scripts/update-worker-registry.py"],"constraints":"","output":"cron actualizat"},
  {"step":258,"scope":"wrk-registry-redis","context":"Redis structura.","task":"Define key-schema `wrk:<tag>:status` TTL 120s.","dirs":["/core/apps/admin-core/api/"],"constraints":"","output":"cache live"},
  {"step":259,"scope":"wrk-registry-tests","context":"No tests.","task":"Unit & e2e Supertest pentru endpoints registry.","dirs":["/core/apps/admin-core/api/tests/"],"constraints":"","output":"tests verde"},
  {"step":260,"scope":"wrk-registry-helm","context":"Cron deploy.","task":"CronJob manifest `worker-reg-health` în chart admin-core.","dirs":["/infra/helm/admin-core/"],"constraints":"","output":"cron job live"},
  {"step":261,"scope":"wrk-registry-dashboard","context":"Observability.","task":"Grafana panel worker count, missing workers.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"","output":"panel workers"},
  {"step":262,"scope":"wrk-registry-alert","context":"Alert slack.","task":"Alertmanager rule alert if missing_workers>0 for 5m.","dirs":["/infra/k8s/alertmanager/"],"constraints":"","output":"alert activ"},
  {"step":263,"scope":"wrk-registry-docs","context":"API doc.","task":"Adaugă secțiune Worker Registry în `docs/api/admin-core.md`.","dirs":["/docs/api/"],"constraints":"","output":"doc actualizat"}
]
```

**Nota:** acest roadmap individual este sincronizat automat cu `3_roadmap_f_1_Core_Platform.md`; nu modifica manual pașii din alt fișier.