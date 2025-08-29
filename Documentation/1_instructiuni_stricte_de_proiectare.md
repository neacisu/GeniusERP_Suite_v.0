# Instrucțiuni STRICTE de Proiectare – GeniusERP Suite

> **Utilizare:** copiază acest fișier în *"Project → Instructions"* din ChatGPT Projects. ChatGPT trebuie **să respecte literal** aceste reguli la orice prompt viitor.

---

## Limbaj & Ton

1. Răspunsurile vor fi **în limba română** tehnică.  
2. Evită glume, metafore, „hollywood" – stil concis, orientat la acțiune.  
3. Fără filler‑words: „super", „incredibil", „magic".  
4. Citează secțiuni din Readme 1/2 doar când se solicită explicit.  
5. Folosește Markdown (`###`, liste, tabele) fără HTML.

## Domeniul de aplicare (Scope)

- **NU** discuta subiecte în afara GeniusERP Suite.  
- Module permise: Shell, Vettify, Mercantiq (Sales/Procurement), iWMS, Numeriqo (Manufacturing/Accounting/People), Archify, Cerniq, Triggerra (Collab/Automation).  
- Nu inventa module noi; extinde doar prin `core/scripts/create-module.ts` sau `standalone/<app>/scripts/` logic.

## Stack tehnologic – **obligatoriu**

| Layer | Tech fix | Comentariu |
| ----- | -------- | ---------- |
| UI    | React 19, Vite 5 Federation, Tailwind 3, MUI 6 | fără Next.js/Angular. |
| API   | NestJS 11 (Node 20 LTS, TS 5) | fără Express/Koa. |
| Workeri | Python 3.13 (FastAPI tasks, Celery 6, Ray 2) | fără Flask/Django. |
| Storage | PostgreSQL 17 (+pgvector >= 0.5.0), MinIO (REPL, SSE‑C) | nu MySQL/Mongo. |
| Bus   | RabbitMQ 3.14, Redis 7 (BullMQ) | nu Kafka/NATS. |
| IaC   | Terraform 1.9, Helmfile, Argo CD | nu Pulumi/Ansible roles directe. |
| Observability | Prometheus 2.50, Loki 3, Tempo 2, Grafana 10 | invariabil. |
| Security | Trivy scanner, Cosign signing | praguri standard. |

### **Standardul de Securitate – Obligatoriu pentru toate modulele**

**Trivy Scanner Praguri Standard:**
- **CRITICAL = 0** (toleranță zero pentru vulnerabilități critice)
- **HIGH ≤ 3** (maxim 3 vulnerabilități înalte acceptabile în production)  
- **MEDIUM ≤ 15** (maxim 15 vulnerabilități medii acceptabile în development)

**Cosign Integration Standard:**
- Dockerfile creation cu multi-stage builds
- Helm charts cu imagini semnate Cosign
- CI/CD cu SBOM generation și Cosign signing
- ArgoCD cu cosign verify obligatoriu la deployment

**Aceste praguri sunt OBLIGATORII pentru toate modulele și nu pot fi modificate fără aprobare arhitect.**

### **Workers AI Avansați – Validați Oficial pentru Stack**

**Social Media AI Workers (Next-Generation CRM):**
- `facebook.pixel.ai` - Facebook/Instagram pixel analysis cu GPT-4 + pgvector pentru audience intelligence
- `linkedin.sales.ai` - LinkedIn Sales Navigator cu Anthropic Claude pentru B2B lead generation
- `twitter.sentiment.ai` - Real-time sentiment analysis cu VADER + Transformers pentru brand monitoring
- `tiktok.analytics.ai` - TikTok Business API cu Computer Vision pentru content marketing

**Customer Intelligence AI Workers (Advanced CRM):**
- `vision.call.analysis` - Computer vision pentru video calls cu OpenCV + MediaPipe + emotion detection
- `voice.sentiment.ai` - Voice-to-text + sentiment cu Whisper + AssemblyAI pentru conversation intelligence
- `behavior.pattern.ai` - Behavioral pattern recognition cu TensorFlow + PyTorch pentru predictive analytics
- `content.personalization.ai` - AI-driven content recommendations cu GPT-4 pentru marketing automation

**Marketing AI Modern Workers (HubSpot/Salesforce Killer):**
- `ab.testing.ml` - Automated A/B testing cu scipy.stats + MLlib pentru campaign optimization
- `dynamic.pricing.ai` - Real-time pricing cu XGBoost + time series pentru revenue optimization
- `attribution.modeling.ai` - Cross-channel attribution cu Markov chains pentru attribution intelligence
- `campaign.optimization.ai` - Campaign automation cu Reinforcement Learning pentru intelligent campaigns

**Acești 12 workeri AI sunt OFICIALMENTE VALIDAȚI pentru stackul GeniusERP și vor fi implementați în `/core/apps/workers-core/` cu suport GPU enterprise-grade.**

**Business Critical Workers (Operations & Security):**
- `risk.fraud.scoring` - ML fraud detection pentru Mercantiq Sales cu scikit-learn + XGBoost pentru transaction scoring
- `route.optimization.ai` - TSP/VRP route optimization pentru iWMS cu OR-Tools + NetworkX pentru picking efficiency
- `slotting.optimization.ai` - ABC analysis + velocity-based slotting pentru iWMS cu pandas + scikit-learn pentru inventory optimization

**Acești 3 workeri business critical sunt ESENȚIALI pentru operațiunile de zi cu zi și vor fi implementați în `/core/apps/workers-core/` cu performanțe garantate.**

## Structură directoare – **întocmai**

- Răspunsurile care includ calea fișierelor trebuie să respecte piramida revizuită:

### Arbore principal revizuit (root ► ≥ 6 niveluri)

```
/                                   # repo‑root
├── core/                         # rădăcina aplicației‑mamă GeniusERP
│   ├── apps/
│   │   ├── shell-gateway/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   └── src/
│   │   │   │       ├── assets/
│   │   │   │       ├── components/
│   │   │   │       │   ├── common/
│   │   │   │       │   │   └── __tests__/                     # lvl‑8
│   │   │   │       │   ├── layout/
│   │   │   │       │   ├── navigation/
│   │   │   │       │   └── widgets/health/
│   │   │   │       ├── hooks/
│   │   │   │       ├── pages/
│   │   │   │       ├── styles/
│   │   │   │       └── utils/
│   │   │   ├── frontend-e2e/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/health/dto/validators/     # lvl‑8
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── interceptors/
│   │   │   │       ├── middlewares/
│   │   │   │       ├── services/
│   │   │   │       ├── filters/
│   │   │   │       ├── entities/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       └── health-check/src/tasks/__tests__/          # lvl‑8
│   │   ├── admin-core/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   └── src/
│   │   │   │       ├── components/
│   │   │   │       │   ├── settings/__tests__/                # lvl‑8
│   │   │   │       │   ├── rbac/
│   │   │   │       │   └── themehub/
│   │   │   │       ├── pages/
│   │   │   │       ├── hooks/
│   │   │   │       ├── styles/
│   │   │   │       └── utils/
│   │   │   ├── frontend-e2e/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/{settings,themes,workers}/
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── services/
│   │   │   │       ├── entities/
│   │   │   │       ├── migrations/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       └── registry/src/tasks/__tests__/             # lvl‑8
│   │   └── workers-core/
│   │       ├── ocr/src/tasks/__tests__/                      # lvl‑8
│   │       ├── pdf-render/src/tasks/__tests__/
│   │       ├── email-send/src/tasks/__tests__/
│   │       ├── anaf-taxpayer/src/tasks/__tests__/
│   │       ├── anaf-efactura/src/tasks/__tests__/
│   │       ├── anaf-etransport/src/tasks/__tests__/
│   │       ├── anaf-saft/src/tasks/__tests__/
│   │       ├── reges/src/tasks/__tests__/
│   │       ├── shared/libs/
│   │       └── celery/celeryconfig/
│   ├── packages/
│   │   ├── ui/src/
│   │   │   ├── components/atoms/button/__stories__/         # lvl‑8
│   │   │   └── tokens/
│   │   ├── auth/src/
│   │   ├── sdk-ts/src/lib/bus/{client,tests}/
│   │   ├── sdk-py/src/genius_sdk/bus/{client,tests}/
│   │   ├── proto/v1/{admin,common}/
│   │   └── rules-eslint/src/{rules,configs}/tests/
│   ├── infra/
│   │   ├── terraform/
│   │   │   ├── envs/
│   │   │   │   ├── dev/backend/state/lock/                   # lvl‑8
│   │   │   │   ├── stage/backend/state/lock/
│   │   │   │   └── prod/backend/state/lock/
│   │   │   ├── base/
│   │   │   │   ├── backend.tf
│   │   │   │   ├── providers.tf
│   │   │   │   └── s3-backend-policy.json
│   │   │   └── modules/
│   │   │       ├── vpc/{main,variables,outputs,tests}/
│   │   │       ├── k8s-cluster/{main,variables,outputs,tests}/
│   │   │       ├── dns/route53-dev/{main,variables,outputs,tests}/
│   │   │       └── iam-irsa-eso/{main,variables,outputs,tests}/
│   │   ├── helm/
│   │   │   ├── umbrella/{Chart.yaml,charts/,values-dev.yaml}
│   │   │   ├── shell-frontend/charts/templates/_helpers/
│   │   │   ├── admin-core/templates/api-deployment.yaml
│   │   │   ├── workers-core/templates/deployment-ocr.yaml
│   │   │   └── rmq-exporter/templates/
│   │   ├── helmfile/
│   │   │   ├── defaults.yaml
│   │   │   ├── releases/{base,apps}.yaml
│   │   │   └── values-{traefik,cert-manager,prom,tempo,gatekeeper,argo}.yaml
│   │   ├── kustomize/overlays/prod/patches/strategic/         # lvl‑8
│   │   ├── grafana/provisioning/
│   │   │   ├── dashboards/{shell_vitals,http_requests,worker_lag}.json
│   │   │   └── datasources/{prometheus,loki,tempo}.yaml
│   │   ├── k8s/
│   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   ├── argocd/{shell-frontend,admin-core,workers-core}.yaml
│   │   │   ├── alertmanager/rules/{missing_workers,task_failed}.yaml
│   │   │   ├── service-monitors/{traefik,shell-frontend}.yaml
│   │   │   ├── external-secrets/{grafana-admin,rmq-creds-dev}.yaml
│   │   │   ├── tempo/span_metrics/config.yaml
│   │   │   └── secrets/admin-jwt.yaml
│   │   ├── policies/opa/
│   │   │   ├── templates/{CTNotLatestTag,CTThemeValid}.yaml
│   │   │   └── constraints/{NotLatestTag,ThemeValid}.yaml
│   │   ├── keycloak/realm-export.json
│   │   └── tempo/agent/configs/
│   ├── ops/
│   │   ├── dev/docker-compose/overrides/env/                 # lvl‑8
│   │   ├── stage/compose/secrets/
│   │   └── prod/compose/secrets/
│   ├── docs/
│   │   ├── F0_foundation.md
│   │   ├── F1_core_platform.md
│   │   ├── graph.svg
│   │   ├── api/admin-core.md
│   │   ├── event-bus/v1/spec/examples/                       # lvl‑8
│   │   ├── handovers/F0_handover.md
│   │   ├── postman/admin-core.json
│   │   └── sdk/event-bus.md
│   └── scripts/
│       ├── init.sh
│       ├── manage-app.sh/lib/helpers/__tests__/              # lvl‑8
│       ├── create-module.ts/templates/frontend/pages/
│       ├── create-worker.py/templates/worker/src/
│       ├── publish-remote.sh
│       ├── backup-s3.sh
│       ├── blue-green-deploy.sh
│       ├── migrate-tenant.py
│       ├── rotate-keys.sh
│       ├── update-worker-registry.py
│       ├── bootstrap-tenant.py
│       ├── lint-rmq.sh
│       ├── notify_slack.sh
│       ├── gate-f0.sh
│       └── gate-f1-shell.sh
│
├── standalone/
│   ├── vettify/
│   │   ├── apps/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   │   ├── favicons/
│   │   │   │   │   └── assets/
│   │   │   │   └── src/
│   │   │   │       ├── assets/
│   │   │   │       │   ├── images/
│   │   │   │       │   └── svg/
│   │   │   │       ├── components/
│   │   │   │       │   ├── atoms/
│   │   │   │       │   │   ├── button/
│   │   │   │       │   │   │   └── __tests__/                    # lvl‑8
│   │   │   │       │   │   ├── input/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── icon/
│   │   │   │       │   ├── molecules/
│   │   │   │       │   │   ├── card/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── modal/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── organisms/
│   │   │   │       │   │   ├── lead-table/
│   │   │   │       │   │   │   └── __tests__/                   # lvl‑8
│   │   │   │       │   │   └── contact-form/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── common/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── layout/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── hooks/
│   │   │   │       ├── pages/
│   │   │   │       │   ├── dashboard/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── leads/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── campaigns/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── auth/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── routers/
│   │   │   │       ├── styles/
│   │   │   │       ├── utils/
│   │   │   │       ├── widgets/
│   │   │   │       │   ├── health/
│   │   │   │       │   │   └── __tests__/                       # lvl‑8
│   │   │   │       │   └── kpi/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/
│   │   │   │       │   ├── crm/
│   │   │   │       │   │   ├── accounts/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   ├── leads/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   └── campaigns/
│   │   │   │       │   │       ├── dto/
│   │   │   │       │   │       └── validators/
│   │   │   │       │   └── health/
│   │   │   │       │       └── dto/
│   │   │   │       ├── services/
│   │   │   │       │   ├── crm/
│   │   │   │       │   └── auth/
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── interceptors/
│   │   │   │       ├── filters/
│   │   │   │       ├── entities/
│   │   │   │       ├── repositories/
│   │   │   │       ├── migrations/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       ├── ai.summary/
│   │   │       │   └── src/
│   │   │       │       ├── tasks/
│   │   │       │       │   └── __tests__/                       # lvl‑8
│   │   │       │       ├── models/
│   │   │       │       ├── services/
│   │   │       │       └── utils/
│   │   │       └── ai.churn/
│   │   │           └── src/
│   │   │               ├── tasks/
│   │   │               │   └── __tests__/                       # lvl‑8
│   │   │               ├── models/
│   │   │               ├── services/
│   │   │               └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/
│   │   │   │   ├── base/
│   │   │   │   │   ├── dev/
│   │   │   │   │   ├── stage/
│   │   │   │   │   └── prod/
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   └── iam-irsa-eso/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── vettify-frontend/templates/
│   │   │   │   ├── vettify-api/templates/
│   │   │   │   ├── vettify-workers/templates/
│   │   │   │   └── umbrella/charts/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/{dashboards,datasources}/
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── issuers/
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   └── argocd/vettify.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── architecture/ctx-view/diagrams/
│   │   │   ├── architecture/deployment/
│   │   │   ├── domain/crm/
│   │   │   ├── api/vettify/openapi/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/               # lvl‑8
│   │   │   ├── seed-data.js
│   │   │   ├── migrate-db.sh
│   │   │   └── cli/sync-topic-names.ts
│   │   └── tests/
│   │       ├── k6/
│   │       └── contract/event-bus/
│   ├── mercantiq/
│   │   ├── apps/
│   │   │   ├── sales/
│   │   │   │   ├── frontend/
│   │   │   │   │   ├── public/
│   │   │   │   │   │   ├── favicons/
│   │   │   │   │   │   └── assets/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── assets/
│   │   │   │   │       │   ├── images/
│   │   │   │   │       │   └── svg/
│   │   │   │   │       ├── components/
│   │   │   │   │       │   ├── atoms/
│   │   │   │   │       │   │   ├── button/                      # lvl‑8
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   ├── input/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── icon/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── molecules/
│   │   │   │   │       │   │   ├── card/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── modal/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── organisms/
│   │   │   │   │       │   │   ├── pos-terminal/
│   │   │   │   │       │   │   │   └── __tests__/              # lvl‑8
│   │   │   │   │       │   │   ├── invoice-table/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── customer-dashboard/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── layout/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── common/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── pages/
│   │   │   │   │       │   ├── pos/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── invoices/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── customers/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── dashboard/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── hooks/
│   │   │   │   │       ├── routers/
│   │   │   │   │       ├── styles/
│   │   │   │   │       ├── utils/
│   │   │   │   │       ├── widgets/
│   │   │   │   │       │   ├── kpi/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── health/
│   │   │   │   │       │       └── __tests__/                  # lvl‑8
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   │   ├── api/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── controllers/
│   │   │   │   │       │   ├── sales/
│   │   │   │   │       │   │   ├── pos/
│   │   │   │   │       │   │   │   ├── dto/
│   │   │   │   │       │   │   │   └── validators/
│   │   │   │   │       │   │   ├── invoices/
│   │   │   │   │       │   │   │   ├── dto/
│   │   │   │   │       │   │   │   └── validators/
│   │   │   │   │       │   │   └── customers/
│   │   │   │   │       │   │       ├── dto/
│   │   │   │   │       │   │       └── validators/
│   │   │   │   │       │   └── health/
│   │   │   │   │       │       └── dto/
│   │   │   │   │       ├── services/
│   │   │   │   │       │   ├── sales/
│   │   │   │   │       │   └── auth/
│   │   │   │   │       ├── dto/
│   │   │   │   │       ├── guards/
│   │   │   │   │       ├── interceptors/
│   │   │   │   │       ├── filters/
│   │   │   │   │       ├── entities/
│   │   │   │   │       ├── repositories/
│   │   │   │   │       ├── migrations/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   │   └── workers/
│   │   │   │       ├── pdf.render/
│   │   │   │       │   └── src/
│   │   │   │       │       ├── tasks/
│   │   │   │       │       │   └── __tests__/                  # lvl‑8
│   │   │   │       │       ├── models/
│   │   │   │       │       ├── services/
│   │   │   │       │       └── utils/
│   │   │   │       └── notify.slack/
│   │   │   │           └── src/
│   │   │   │               ├── tasks/
│   │   │   │               │   └── __tests__/                  # lvl‑8
│   │   │   │               ├── models/
│   │   │   │               ├── services/
│   │   │   │               └── utils/
│   │   │   └── procurement/
│   │   │       ├── frontend/
│   │   │       │   ├── public/
│   │   │       │   │   ├── favicons/
│   │   │       │   │   └── assets/
│   │   │       │   └── src/
│   │   │       │       ├── assets/
│   │   │       │       │   ├── images/
│   │   │       │       │   └── svg/
│   │   │       │       ├── components/
│   │   │       │       │   ├── atoms/
│   │   │       │       │   │   ├── button/
│   │   │       │       │   │   │   └── __tests__/             # lvl‑8
│   │   │       │       │   │   ├── input/
│   │   │       │       │   │   │   └── __tests__/
│   │   │       │       │   │   └── icon/
│   │   │       │       │   │       └── __tests__/
│   │   │       │       │   ├── molecules/
│   │   │       │       │   │   ├── card/
│   │   │       │       │   │   │   └── __tests__/
│   │   │       │       │   │   └── modal/
│   │   │       │       │   │       └── __tests__/
│   │   │       │       │   ├── organisms/
│   │   │       │       │   │   ├── rfq-table/
│   │   │       │       │   │   │   └── __tests__/             # lvl‑8
│   │   │       │       │   │   ├── po-tracker/
│   │   │       │       │   │   │   └── __tests__/
│   │   │       │       │   │   └── grn-board/
│   │   │       │       │   │       └── __tests__/
│   │   │       │       │   ├── layout/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── common/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── pages/
│   │   │       │       │   ├── rfq/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── purchase-orders/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── grn/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── dashboard/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── hooks/
│   │   │       │       ├── routers/
│   │   │       │       ├── styles/
│   │   │       │       ├── utils/
│   │   │       │       ├── widgets/
│   │   │       │       │   ├── kpi/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── health/
│   │   │       │       │       └── __tests__/                # lvl‑8
│   │   │       │       ├── config/
│   │   │       │       └── tests/
│   │   │       ├── api/
│   │   │       │   └── src/
│   │   │       │       ├── controllers/
│   │   │       │       │   ├── procurement/
│   │   │       │       │   │   ├── rfq/
│   │   │       │       │   │   │   ├── dto/
│   │   │       │       │   │   │   └── validators/
│   │   │       │       │   │   ├── purchase-orders/
│   │   │       │       │   │   │   ├── dto/
│   │   │       │       │   │   │   └── validators/
│   │   │       │       │   │   └── grn/
│   │   │       │       │   │       ├── dto/
│   │   │       │       │   │       └── validators/
│   │   │       │       │   └── health/
│   │   │       │       │       └── dto/
│   │   │       │       ├── services/
│   │   │       │       │   ├── procurement/
│   │   │       │       │   └── auth/
│   │   │       │       ├── dto/
│   │   │       │       ├── guards/
│   │   │       │       ├── interceptors/
│   │   │       │       ├── filters/
│   │   │       │       ├── entities/
│   │   │       │       ├── repositories/
│   │   │       │       ├── migrations/
│   │   │       │       ├── config/
│   │   │       │       └── tests/
│   │   │       └── workers/
│   │   │           ├── match.ai/
│   │   │           │   └── src/
│   │   │           │       ├── tasks/
│   │   │           │       │   └── __tests__/                 # lvl‑8
│   │   │           │       ├── models/
│   │   │           │       ├── services/
│   │   │           │       └── utils/
│   │   │           └── notify.slack/
│   │   │               └── src/
│   │   │                   ├── tasks/
│   │   │                   │   └── __tests__/                 # lvl‑8
│   │   │                   ├── models/
│   │   │                   ├── services/
│   │   │                   └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/          # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   └── iam-irsa-eso/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── mercantiq-frontend/templates/
│   │   │   │   ├── mercantiq-api/templates/
│   │   │   │   ├── mercantiq-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{pos_metrics.json,procurement_metrics.json,order_to_cash.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/mercantiq.yaml
│   │   │   │   └── alertmanager/rules/order_to_cash_alerts.yaml
│   │   │   └── policies/opa/
│   │   │       ├── templates/{CTNoLatestTag.yaml,CTPurchaseLimit.yaml}
│   │   │       └── constraints/{NoLatestTag.yaml,PurchaseLimit.yaml}
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── domain/
│   │   │   │   ├── order-to-cash/{flows,diagrams}/
│   │   │   │   └── procure-to-pay/{flows,diagrams}/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/{sales/openapi,procurement/openapi}/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/              # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,billing-reconcile.ts}
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{pos_load_test.js,procure_to_pay.js,dashboards/}
│   │       └── contract/event-bus/
│   │           ├── sales/pact/
│   │           └── procurement/pact/
│   ├── numeriqo/
│   │   ├── apps/
│   │   │   ├── manufacturing/
│   │   │   │   ├── frontend/
│   │   │   │   │   ├── public/
│   │   │   │   │   │   ├── favicons/
│   │   │   │   │   │   └── assets/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── assets/
│   │   │   │   │       │   ├── images/
│   │   │   │   │       │   └── svg/
│   │   │   │   │       ├── components/
│   │   │   │   │       │   ├── atoms/
│   │   │   │   │       │   │   ├── button/
│   │   │   │   │       │   │   │   └── __tests__/                        # lvl‑8
│   │   │   │   │       │   │   ├── input/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── icon/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── molecules/
│   │   │   │   │       │   │   ├── card/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── modal/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── organisms/
│   │   │   │   │       │   │   ├── shopfloor‑terminal/
│   │   │   │   │       │   │   │   └── __tests__/                        # lvl‑8
│   │   │   │   │       │   │   └── mrp‑board/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── layout/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── common/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── pages/
│   │   │   │   │       │   ├── bom/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── mrp/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── workorders/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── dashboard/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── hooks/
│   │   │   │   │       ├── routers/
│   │   │   │   │       ├── styles/
│   │   │   │   │       ├── utils/
│   │   │   │   │       ├── widgets/
│   │   │   │   │       │   ├── kpi/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── health/
│   │   │   │   │       │       └── __tests__/                          # lvl‑8
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   │   ├── api/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── controllers/
│   │   │   │   │       │   └── manufacturing/
│   │   │   │   │       │       ├── bom/
│   │   │   │   │       │       │   ├── dto/
│   │   │   │   │       │       │   └── validators/
│   │   │   │   │       │       ├── workorders/
│   │   │   │   │       │       │   ├── dto/
│   │   │   │   │       │       │   └── validators/
│   │   │   │   │       │       └── mrp/
│   │   │   │   │       │           ├── dto/
│   │   │   │   │       │           └── validators/
│   │   │   │   │       ├── services/
│   │   │   │   │       │   ├── bom/
│   │   │   │   │       │   ├── mrp/
│   │   │   │   │       │   └── auth/
│   │   │   │   │       ├── dto/
│   │   │   │   │       ├── guards/
│   │   │   │   │       ├── interceptors/
│   │   │   │   │       ├── filters/
│   │   │   │   │       ├── entities/
│   │   │   │   │       ├── repositories/
│   │   │   │   │       ├── migrations/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   ├── accounting/
│   │   │   │   ├── frontend/
│   │   │   │   │   ├── public/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── assets/{images,svg}/
│   │   │   │   │       ├── components/
│   │   │   │   │       │   ├── atoms/
│   │   │   │   │       │   │   └── __tests__/                         # lvl‑8
│   │   │   │   │       │   ├── reports/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── layout/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── common/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── pages/
│   │   │   │   │       │   ├── ledger/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── trial‑balance/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── saft/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── dashboard/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── hooks/
│   │   │   │   │       ├── routers/
│   │   │   │   │       ├── styles/
│   │   │   │   │       ├── utils/
│   │   │   │   │       └── widgets/health/__tests__/                 # lvl‑8
│   │   │   │   ├── api/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── controllers/
│   │   │   │   │       │   └── accounting/
│   │   │   │   │       │       ├── ledger/
│   │   │   │   │       │       │   ├── dto/
│   │   │   │   │       │       │   └── validators/
│   │   │   │   │       │       ├── journal/
│   │   │   │   │       │       │   ├── dto/
│   │   │   │   │       │       │   └── validators/
│   │   │   │   │       │       └── saft/
│   │   │   │   │       │           ├── dto/
│   │   │   │   │       │           └── validators/
│   │   │   │   │       ├── services/{ledger,journal,auth}/
│   │   │   │   │       ├── dto/
│   │   │   │   │       ├── guards/
│   │   │   │   │       ├── interceptors/
│   │   │   │   │       ├── filters/
│   │   │   │   │       ├── entities/
│   │   │   │   │       ├── repositories/
│   │   │   │   │       ├── migrations/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   └── people/
│   │   │       ├── frontend/
│   │   │       │   ├── public/
│   │   │       │   └── src/
│   │   │       │       ├── assets/{images,svg}/
│   │   │       │       ├── components/
│   │   │       │       │   ├── atoms/
│   │   │       │       │   │   └── __tests__/                       # lvl‑8
│   │   │       │       │   ├── payroll‑sheet/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── layout/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── common/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── pages/
│   │   │       │       │   ├── employees/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── payroll/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── timeoff/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── dashboard/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── hooks/
│   │   │       │       ├── routers/
│   │   │       │       ├── styles/
│   │   │       │       ├── utils/
│   │   │       │       └── widgets/health/__tests__/                # lvl‑8
│   │   │       ├── api/
│   │   │       │   └── src/
│   │   │       │       ├── controllers/
│   │   │       │       │   └── hr/
│   │   │       │       │       ├── employees/
│   │   │       │       │       │   ├── dto/
│   │   │       │       │       │   └── validators/
│   │   │       │       │       ├── payroll/
│   │   │       │       │       │   ├── dto/
│   │   │       │       │       │   └── validators/
│   │   │       │       │       └── timeoff/
│   │   │       │       │           ├── dto/
│   │   │       │       │           └── validators/
│   │   │       │       ├── services/{payroll,auth}/
│   │   │       │       ├── dto/
│   │   │       │       ├── guards/
│   │   │       │       ├── interceptors/
│   │   │       │       ├── filters/
│   │   │       │       ├── entities/
│   │   │       │       ├── repositories/
│   │   │       │       ├── migrations/
│   │   │       │       ├── config/
│   │   │       │       └── tests/
│   │   ├── workers/
│   │   │   └── hr.payroll/
│   │   │       └── src/
│   │   │           ├── tasks/
│   │   │           │   └── __tests__/                               # lvl‑8
│   │   │           ├── models/
│   │   │           ├── services/
│   │   │           └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/                # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   └── iam-irsa-eso/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── numeriqo-frontend/templates/
│   │   │   │   ├── numeriqo-api/templates/
│   │   │   │   ├── numeriqo-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{mrp_metrics.json,ledger_metrics.json,payroll_metrics.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/numeriqo.yaml
│   │   │   │   └── alertmanager/rules/backbone_alerts.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── bounded-context/
│   │   │   │   ├── manufacturing/{sequence,diagrams}/
│   │   │   │   ├── accounting/{ledger,saft}/
│   │   │   │   └── people/{payroll,timeoff}/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/{manufacturing/openapi,accounting/openapi,people/openapi}/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/                    # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,ledger-close.ts}
│   │   │   ├── payroll-runner.py
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{mrp_load.js,ledger_perf.js,payroll_bench.js}
│   │       └── contract/event-bus/
│   │           ├── manufacturing/pact/
│   │           ├── accounting/pact/
│   │           └── people/pact/
│   ├── triggerra/
│   │   ├── apps/
│   │   │   ├── collab/
│   │   │   │   ├── frontend/
│   │   │   │   │   ├── public/
│   │   │   │   │   │   ├── favicons/
│   │   │   │   │   │   └── assets/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── assets/
│   │   │   │   │       │   ├── images/
│   │   │   │   │       │   └── svg/
│   │   │   │   │       ├── components/
│   │   │   │   │       │   ├── atoms/
│   │   │   │   │       │   │   ├── button/
│   │   │   │   │       │   │   │   └── __tests__/                         # lvl‑8
│   │   │   │   │       │   │   ├── input/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── icon/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── molecules/
│   │   │   │   │       │   │   ├── card/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── modal/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── organisms/
│   │   │   │   │       │   │   ├── kanban-board/
│   │   │   │   │       │   │   │   └── __tests__/                         # lvl‑8
│   │   │   │   │       │   │   ├── chat-panel/
│   │   │   │   │       │   │   │   └── __tests__/
│   │   │   │   │       │   │   └── okr-dashboard/
│   │   │   │   │       │   │       └── __tests__/
│   │   │   │   │       │   ├── layout/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── common/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── pages/
│   │   │   │   │       │   ├── boards/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── chat/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   ├── okr/
│   │   │   │   │       │   │   └── __tests__/
│   │   │   │   │       │   └── dashboard/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── hooks/
│   │   │   │   │       ├── routers/
│   │   │   │   │       ├── styles/
│   │   │   │   │       ├── utils/
│   │   │   │   │       ├── widgets/
│   │   │   │   │       │   ├── notifications/
│   │   │   │   │       │   │   └── __tests__/                             # lvl‑8
│   │   │   │   │       │   └── kpi/
│   │   │   │   │       │       └── __tests__/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   │   ├── api/
│   │   │   │   │   └── src/
│   │   │   │   │       ├── controllers/
│   │   │   │   │       │   ├── chat/
│   │   │   │   │       │   │   ├── messages/
│   │   │   │   │       │   │   │   ├── dto/
│   │   │   │   │       │   │   │   └── validators/
│   │   │   │   │       │   │   └── channels/
│   │   │   │   │       │   │       ├── dto/
│   │   │   │   │       │   │       └── validators/
│   │   │   │   │       │   ├── kanban/
│   │   │   │   │       │   │   ├── boards/
│   │   │   │   │       │   │   │   ├── dto/
│   │   │   │   │       │   │   │   └── validators/
│   │   │   │   │       │   │   └── cards/
│   │   │   │   │       │   │       ├── dto/
│   │   │   │   │       │   │       └── validators/
│   │   │   │   │       │   ├── okr/
│   │   │   │   │       │   │   ├── objectives/
│   │   │   │   │       │   │   │   ├── dto/
│   │   │   │   │       │   │   │   └── validators/
│   │   │   │   │       │   │   └── key‑results/
│   │   │   │   │       │   │       ├── dto/
│   │   │   │   │       │   │       └── validators/
│   │   │   │   │       │   └── health/
│   │   │   │   │       │       └── dto/
│   │   │   │   │       ├── services/
│   │   │   │   │       │   ├── chat/
│   │   │   │   │       │   ├── kanban/
│   │   │   │   │       │   ├── okr/
│   │   │   │   │       │   └── auth/
│   │   │   │   │       ├── dto/
│   │   │   │   │       ├── guards/
│   │   │   │   │       ├── interceptors/
│   │   │   │   │       ├── filters/
│   │   │   │   │       ├── entities/
│   │   │   │   │       ├── repositories/
│   │   │   │   │       ├── migrations/
│   │   │   │   │       ├── config/
│   │   │   │   │       └── tests/
│   │   │   └── automation/
│   │   │       ├── frontend/
│   │   │       │   ├── public/
│   │   │       │   └── src/
│   │   │       │       ├── assets/{images,svg}/
│   │   │       │       ├── components/
│   │   │       │       │   ├── atoms/
│   │   │       │       │   │   └── __tests__/                             # lvl‑8
│   │   │       │       │   ├── flow‑builder/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── runtime‑monitor/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── layout/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── common/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── pages/
│   │   │       │       │   ├── flows/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── executions/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   ├── templates/
│   │   │       │       │   │   └── __tests__/
│   │   │       │       │   └── dashboard/
│   │   │       │       │       └── __tests__/
│   │   │       │       ├── hooks/
│   │   │       │       ├── routers/
│   │   │       │       ├── styles/
│   │   │       │       ├── utils/
│   │   │       │       ├── widgets/health/__tests__/                      # lvl‑8
│   │   │       │       ├── config/
│   │   │       │       └── tests/
│   │   │       ├── api/
│   │   │       │   └── src/
│   │   │       │       ├── controllers/
│   │   │       │       │   └── runtime/
│   │   │       │       │       ├── executions/
│   │   │       │       │       │   ├── dto/
│   │   │       │       │       │   └── validators/
│   │   │       │       │       ├── templates/
│   │   │       │       │       │   ├── dto/
│   │   │       │       │       │   └── validators/
│   │   │       │       │       └── health/
│   │   │       │       │           └── dto/
│   │   │       │       ├── services/{runtime,auth}/
│   │   │       │       ├── dto/
│   │   │       │       ├── guards/
│   │   │       │       ├── interceptors/
│   │   │       │       ├── filters/
│   │   │       │       ├── entities/
│   │   │       │       ├── repositories/
│   │   │       │       ├── migrations/
│   │   │       │       ├── config/
│   │   │       │       └── tests/
│   │   ├── workers/
│   │   │   ├── notify.slack/
│   │   │   │   └── src/
│   │   │   │       ├── tasks/
│   │   │   │       │   └── __tests__/                                     # lvl‑8
│   │   │   │       ├── models/
│   │   │   │       ├── services/
│   │   │   │       └── utils/
│   │   │   └── flow.runtime/
│   │   │       └── src/
│   │   │           ├── tasks/
│   │   │           │   └── __tests__/                                     # lvl‑8
│   │   │           ├── models/
│   │   │           ├── services/
│   │   │           └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/                      # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── keda-autoscale/{examples,tests}/
│   │   │   │   │   └── iam-irsa-eso/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── triggerra-frontend/templates/
│   │   │   │   ├── triggerra-api/templates/
│   │   │   │   ├── triggerra-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{collab_metrics.json,automation_metrics.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/triggerra.yaml
│   │   │   │   └── alertmanager/rules/collab_auto_alerts.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── collaboration/{flows,diagrams}/
│   │   │   ├── automation/{patterns,examples}/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/{collab/openapi,automation/openapi}/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/                          # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,workflow-export.ts}
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{chat_load.js,flow_perf.js}
│   │       └── contract/event-bus/
│   │           ├── collab/pact/
│   │           └── automation/pact/
│   ├── iwms/
│   │   ├── apps/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   │   ├── favicons/
│   │   │   │   │   └── assets/
│   │   │   │   └── src/
│   │   │   │       ├── assets/
│   │   │   │       │   ├── images/
│   │   │   │       │   └── svg/
│   │   │   │       ├── components/
│   │   │   │       │   ├── atoms/
│   │   │   │       │   │   ├── button/
│   │   │   │       │   │   │   └── __tests__/                                 # lvl‑8
│   │   │   │       │   │   ├── input/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── icon/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── molecules/
│   │   │   │       │   │   ├── card/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── modal/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── organisms/
│   │   │   │       │   │   ├── rf-handheld/
│   │   │   │       │   │   │   └── __tests__/                               # lvl‑8
│   │   │   │       │   │   ├── pallet-tracker/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── dock-scheduler/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── mobile/
│   │   │   │       │   │   ├── inventory/
│   │   │   │       │   │   │   └── __tests__/                               # lvl‑8
│   │   │   │       │   │   ├── inbound/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── outbound/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── layout/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── common/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── pages/
│   │   │   │       │   ├── inbound/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── outbound/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── inventory/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── dashboard/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── hooks/
│   │   │   │       ├── routers/
│   │   │   │       ├── styles/
│   │   │   │       ├── utils/
│   │   │   │       ├── widgets/
│   │   │   │       │   ├── kpi/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── health/
│   │   │   │       │       └── __tests__/                                # lvl‑8
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/
│   │   │   │       │   └── warehouse/
│   │   │   │       │       ├── inbound/
│   │   │   │       │       │   ├── dto/
│   │   │   │       │       │   └── validators/
│   │   │   │       │       ├── outbound/
│   │   │   │       │       │   ├── dto/
│   │   │   │       │       │   └── validators/
│   │   │   │       │       ├── inventory/
│   │   │   │       │       │   ├── dto/
│   │   │   │       │       │   └── validators/
│   │   │   │       │       └── health/
│   │   │   │       │           └── dto/
│   │   │   │       ├── services/
│   │   │   │       │   ├── inbound/
│   │   │   │       │   ├── outbound/
│   │   │   │       │   ├── inventory/
│   │   │   │       │   └── auth/
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── interceptors/
│   │   │   │       ├── filters/
│   │   │   │       ├── entities/
│   │   │   │       ├── repositories/
│   │   │   │       ├── migrations/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       ├── forecast/
│   │   │       │   └── src/
│   │   │       │       ├── tasks/
│   │   │       │       │   └── __tests__/                               # lvl‑8
│   │   │       │       ├── models/
│   │   │       │       ├── services/
│   │   │       │       └── utils/
│   │   │       └── notify.slack/
│   │   │           └── src/
│   │   │               ├── tasks/
│   │   │               │   └── __tests__/                               # lvl‑8
│   │   │               ├── models/
│   │   │               ├── services/
│   │   │               └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/                    # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   ├── iam-irsa-eso/{examples,tests}/
│   │   │   │   │   └── iot-gateway/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── iwms-frontend/templates/
│   │   │   │   ├── iwms-api/templates/
│   │   │   │   ├── iwms-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{rfid_metrics.json,warehouse_kpi.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/iwms.yaml
│   │   │   │   └── alertmanager/rules/warehouse_alerts.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── domain/warehouse/{flows,diagrams}/
│   │   │   ├── mobile/rf-handheld/flows/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/iwms/openapi/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/                        # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,rfid-importer.ts}
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{inbound_load.js,outbound_perf.js,inventory_bench.js}
│   │       └── contract/event-bus/
│   │           └── warehouse/pact/
│   ├── archify/
│   │   ├── apps/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   │   ├── favicons/
│   │   │   │   │   └── assets/
│   │   │   │   └── src/
│   │   │   │       ├── assets/
│   │   │   │       │   ├── images/
│   │   │   │       │   └── svg/
│   │   │   │       ├── components/
│   │   │   │       │   ├── atoms/
│   │   │   │       │   │   ├── button/
│   │   │   │       │   │   │   └── __tests__/                               # lvl‑8
│   │   │   │       │   │   ├── input/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── icon/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── molecules/
│   │   │   │       │   │   ├── card/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── modal/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── organisms/
│   │   │   │       │   │   ├── document-viewer/
│   │   │   │       │   │   │   └── __tests__/                              # lvl‑8
│   │   │   │       │   │   ├── retention-board/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── esign-panel/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── dms/
│   │   │   │       │   │   ├── folder-tree/
│   │   │   │       │   │   │   └── __tests__/                              # lvl‑8
│   │   │   │       │   │   ├── document-table/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── sign-queue/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── layout/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── common/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── pages/
│   │   │   │       │   ├── documents/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── esign/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── retention/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── dashboard/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── hooks/
│   │   │   │       ├── routers/
│   │   │   │       ├── styles/
│   │   │   │       ├── utils/
│   │   │   │       ├── widgets/
│   │   │   │       │   ├── kpi/
│   │   │   │       │   │   └── __tests__/                                 # lvl‑8
│   │   │   │       │   └── health/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/
│   │   │   │       │   ├── documents/
│   │   │   │       │   │   ├── upload/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   ├── search/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   └── retention/
│   │   │   │       │   │       ├── dto/
│   │   │   │       │   │       └── validators/
│   │   │   │       │   └── esign/
│   │   │   │       │       ├── request/
│   │   │   │       │       │   ├── dto/
│   │   │   │       │       │   └── validators/
│   │   │   │       │       ├── callback/
│   │   │   │       │       │   ├── dto/
│   │   │   │       │       │   └── validators/
│   │   │   │       │       └── health/
│   │   │   │       │           └── dto/
│   │   │   │       ├── services/
│   │   │   │       │   ├── documents/
│   │   │   │       │   ├── esign/
│   │   │   │       │   └── auth/
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── interceptors/
│   │   │   │       ├── filters/
│   │   │   │       ├── entities/
│   │   │   │       ├── repositories/
│   │   │   │       ├── migrations/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       ├── ocr/
│   │   │       │   └── src/
│   │   │       │       ├── tasks/
│   │   │       │       │   └── __tests__/                                 # lvl‑8
│   │   │       │       ├── models/
│   │   │       │       ├── services/
│   │   │       │       └── utils/
│   │   │       └── image.resize/
│   │   │           └── src/
│   │   │               ├── tasks/
│   │   │               │   └── __tests__/                                 # lvl‑8
│   │   │               ├── models/
│   │   │               ├── services/
│   │   │               └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/                      # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   ├── iam-irsa-eso/{examples,tests}/
│   │   │   │   │   └── s3-retention-bucket/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── archify-frontend/templates/
│   │   │   │   ├── archify-api/templates/
│   │   │   │   ├── archify-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{dms_metrics.json,esign_metrics.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/archify.yaml
│   │   │   │   └── alertmanager/rules/archify_alerts.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── compliance/eidas/{workflows,certs}/
│   │   │   ├── domain/dms/{flows,diagrams}/
│   │   │   ├── esign/{sequence,diagrams}/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/archify/openapi/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/                          # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,retention-cleanup.ts}
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{upload_load.js,esign_perf.js,retention_bench.js}
│   │       └── contract/event-bus/
│   │           └── archify/pact/
│   ├── cerniq/
│   │   ├── apps/
│   │   │   ├── frontend/
│   │   │   │   ├── public/
│   │   │   │   │   ├── favicons/
│   │   │   │   │   └── assets/
│   │   │   │   └── src/
│   │   │   │       ├── assets/
│   │   │   │       │   ├── images/
│   │   │   │       │   └── svg/
│   │   │   │       ├── components/
│   │   │   │       │   ├── atoms/
│   │   │   │       │   │   ├── button/
│   │   │   │       │   │   │   └── __tests__/                             # lvl‑8
│   │   │   │       │   │   ├── input/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── icon/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── molecules/
│   │   │   │       │   │   ├── card/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── modal/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── organisms/
│   │   │   │       │   │   ├── bi-dashboard/
│   │   │   │       │   │   │   └── __tests__/                             # lvl‑8
│   │   │   │       │   │   ├── chart-panel/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── dataset-browser/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── bi/
│   │   │   │       │   │   ├── sql-editor/
│   │   │   │       │   │   │   └── __tests__/                             # lvl‑8
│   │   │   │       │   │   ├── notebook-viewer/
│   │   │   │       │   │   │   └── __tests__/
│   │   │   │       │   │   └── insight-feed/
│   │   │   │       │   │       └── __tests__/
│   │   │   │       │   ├── layout/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── common/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── pages/
│   │   │   │       │   ├── dashboards/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── datasets/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── notebooks/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   ├── ai‑insights/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── landing/
│   │   │   │       │       └── __tests__/
│   │   │   │       ├── hooks/
│   │   │   │       ├── routers/
│   │   │   │       ├── styles/
│   │   │   │       ├── utils/
│   │   │   │       ├── widgets/
│   │   │   │       │   ├── kpi/
│   │   │   │       │   │   └── __tests__/
│   │   │   │       │   └── health/
│   │   │   │       │       └── __tests__/                                 # lvl‑8
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   ├── api/
│   │   │   │   └── src/
│   │   │   │       ├── controllers/
│   │   │   │       │   ├── analytics/
│   │   │   │       │   │   ├── dashboards/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   ├── datasets/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   ├── notebooks/
│   │   │   │       │   │   │   ├── dto/
│   │   │   │       │   │   │   └── validators/
│   │   │   │       │   │   └── insights/
│   │   │   │       │   │       ├── dto/
│   │   │   │       │   │       └── validators/
│   │   │   │       │   └── health/
│   │   │   │       │       └── dto/
│   │   │   │       ├── services/
│   │   │   │       │   ├── analytics/
│   │   │   │       │   ├── lakehouse/
│   │   │   │       │   └── auth/
│   │   │   │       ├── dto/
│   │   │   │       ├── guards/
│   │   │   │       ├── interceptors/
│   │   │   │       ├── filters/
│   │   │   │       ├── entities/
│   │   │   │       ├── repositories/
│   │   │   │       ├── migrations/
│   │   │   │       ├── config/
│   │   │   │       └── tests/
│   │   │   └── workers/
│   │   │       ├── ai.classify/
│   │   │       │   └── src/
│   │   │       │       ├── tasks/
│   │   │       │       │   └── __tests__/                                 # lvl‑8
│   │   │       │       ├── models/
│   │   │       │       ├── services/
│   │   │       │       └── utils/
│   │   │       └── ai.anomaly/
│   │   │           └── src/
│   │   │               ├── tasks/
│   │   │               │   └── __tests__/                                 # lvl‑8
│   │   │               ├── models/
│   │   │               ├── services/
│   │   │               └── utils/
│   │   ├── infra/
│   │   │   ├── terraform/
│   │   │   │   ├── envs/{dev,stage,prod}/state/lock/                      # lvl‑8
│   │   │   │   ├── modules/
│   │   │   │   │   ├── vpc/{examples,tests}/
│   │   │   │   │   ├── k8s-cluster/{examples,tests}/
│   │   │   │   │   ├── rds-pg/{examples,tests}/
│   │   │   │   │   ├── lakehouse-delta/{examples,tests}/
│   │   │   │   │   ├── route53/{tests}/
│   │   │   │   │   └── iam-irsa-eso/{examples,tests}/
│   │   │   │   └── base/{backend,providers}/
│   │   │   ├── helm/
│   │   │   │   ├── cerniq-frontend/templates/
│   │   │   │   ├── cerniq-api/templates/
│   │   │   │   ├── cerniq-workers/templates/
│   │   │   │   ├── umbrella/charts/
│   │   │   │   └── rmq-exporter/templates/
│   │   │   ├── helmfile/{defaults.yaml,releases.yaml}
│   │   │   ├── grafana/provisioning/
│   │   │   │   ├── dashboards/{bi_metrics.json,lakehouse_metrics.json}
│   │   │   │   └── datasources/{prometheus.yaml,loki.yaml}
│   │   │   ├── k8s/
│   │   │   │   ├── namespaces-{dev,stage,prod}.yaml
│   │   │   │   ├── ingress/
│   │   │   │   ├── service-monitors/
│   │   │   │   ├── external-secrets/
│   │   │   │   ├── argocd/cerniq.yaml
│   │   │   │   └── alertmanager/rules/lakehouse_alerts.yaml
│   │   │   └── policies/opa/{templates,constraints}/
│   │   ├── ops/
│   │   │   ├── dev/docker-compose/overrides/caddy/
│   │   │   ├── stage/docker-compose/
│   │   │   └── prod/docker-compose/secrets/
│   │   ├── docs/
│   │   │   ├── lakehouse/delta/diagrams/
│   │   │   ├── ai2bi/{guides,examples}/
│   │   │   ├── domain/bi/{flows,sql-patterns}/
│   │   │   ├── architecture/{ctx-view/diagrams,deployment}/
│   │   │   ├── api/cerniq/openapi/
│   │   │   ├── handovers/
│   │   │   └── postman/
│   │   ├── scripts/
│   │   │   ├── deploy.sh/lib/rollback/__tests__/                          # lvl‑8
│   │   │   ├── migrate-db.sh
│   │   │   ├── seed-data.js
│   │   │   ├── cli/{sync-topic-names.ts,lakehouse-refresh.ts}
│   │   │   └── ci/kpi-check.ts
│   │   └── tests/
│   │       ├── k6/{dashboard_load.js,delta_refresh.js}
│   │       └── contract/event-bus/
│   │           └── cerniq/pact/
│   └── … (alte app‑uri stand‑alone)
│
└── tools/
    ├── ci-templates/                                   # workflow & action templates reutilizate în tot monorepo‑ul
    │   ├── github/
    │   │   ├── workflows/
    │   │   │   ├── module-ci.yml
    │   │   │   ├── nightly-backup.yml
    │   │   │   └── renovate.yml
    │   │   └── actions/
    │   │       ├── build-test-scan/
    │   │       │   ├── action.yaml
    │   │       │   └── steps/
    │   │       │       ├── install-pnpm/
    │   │       │       │   ├── entrypoint.sh
    │   │       │       │   └── __tests__/                      # lvl‑8
    │   │       │       ├── nx-affected/
    │   │       │       │   ├── entrypoint.sh
    │   │       │       │   └── __tests__/
    │   │       │       ├── trivy-scan/
    │   │       │       │   ├── entrypoint.sh
    │   │       │       │   └── __tests__/
    │   │       │       └── cosign-sign/
    │   │       │           ├── entrypoint.sh
    │   │       │           └── __tests__/
    │   │       ├── deploy/
    │   │       │   ├── action.yaml
    │   │       │   └── steps/
    │   │       │       ├── helm-package/
    │   │       │       │   ├── entrypoint.sh
    │   │       │       │   └── __tests__/                      # lvl‑8
    │   │       │       └── argocd-sync/
    │   │       │           ├── entrypoint.sh
    │   │       │           └── __tests__/
    │   │       └── lint-paths/
    │   │           └── action.yaml
    │   └── templates/
    │       └── README.md
    │
    ├── lint-rules/                                      # reguli ESLint / Stylelint / Commitlint comune
    │   ├── eslint/
    │   │   ├── configs/
    │   │   │   ├── base.js
    │   │   │   ├── react.js
    │   │   │   └── typescript.js
    │   │   ├── plugins/
    │   │   │   ├── no-internal-imports/
    │   │   │   │   ├── index.js
    │   │   │   │   └── tests/
    │   │   │   │       └── no-internal-imports.test.js       # lvl‑8
    │   │   │   ├── naming-convention/
    │   │   │   │   ├── index.js
    │   │   │   │   └── tests/
    │   │   │   │       └── naming-convention.test.js
    │   │   │   └── hooks-deps/
    │   │   │       ├── index.js
    │   │   │       └── tests/
    │   │   │           └── hooks-deps.test.js
    │   │   └── README.md
    │   ├── stylelint/
    │   │   ├── configs/
    │   │   │   └── base.js
    │   │   └── plugins/
    │   │       └── no-ignored-properties/
    │   │           ├── index.js
    │   │           └── tests/
    │   │               └── no-ignored-properties.test.js     # lvl‑8
    │   └── commitlint/
    │       ├── configs/
    │       │   └── conventional.js
    │       └── README.md
    │
    └── dev-container/                                   # configurări VS Code Dev Container & features adiţionale
        ├── devcontainer.json
        ├── docker-compose.yml
        └── features/
            ├── linux/
            │   ├── docker/
            │   │   ├── install.sh
            │   │   └── files/
            │   │       ├── docker-daemon.json
            │   │       └── __tests__/                       # lvl‑8
            │   ├── kubectl/
            │   │   ├── install.sh
            │   │   └── files/
            │   │       └── __tests__/
            │   ├── minio/
            │   │   ├── install.sh
            │   │   └── files/
            │   │       └── __tests__/
            │   └── helm/
            │       ├── install.sh
            │       └── files/
            │           └── __tests__/                       # lvl‑8
            └── windows/
                └── wsl2/
                    └── files/
                        └── README.md
│
├── .github/                    # workflow‑uri & action‑uri partajate
│   └── workflows/
│       ├── ci-template.yml
│       ├── module-ci.yml
│       ├── nightly-backup.yml
│       └── renovate.yml
│
├── docker/                     # Dockerfile‑uri partajate (vite, Nest, workers…)
│   ├── frontend.Dockerfile
│   ├── api.Dockerfile
│   └── worker.Dockerfile
│
├── scripts/                    # CLI & automations cross‑suite
│   ├── init.sh
│   ├── manage-app.sh
│   ├── create-module.ts
│   ├── create-worker.py
│   ├── blue-green-deploy.sh
│   ├── bootstrap-tenant.py
│   ├── rotate-keys.sh
│   ├── update-worker-registry.py
│   ├── publish-remote.sh
│   └── lint-rmq.sh
│
├── docs/                       # documentație transversală (roadmap recap, KPI, etc.)
│   ├── F0_foundation.md
│   ├── F1_core_platform.md
│   └── event-bus/
│       └── v1-spec.md
│
├── roadmap/                    # toate roadmap‑urile .md generate automat
│   ├── shell.md
│   ├── admin-core.md
│   ├── vettify.md
│   └── … (one per app/fază)
│
├── tests/                      # suite generice (k6, contract‑tests globale)
│   ├── k6/
│   └── contract/
│
├── .editorconfig
├── .gitignore
├── .dockerignore
├── .pre-commit-config.yaml
├── .commitlintrc.js
├── .eslintrc.json
├── .prettierrc.js
├── nx.json
├── workspace.json              # (sau project.json dacă Nx ≥ 18)
├── tsconfig.base.json
├── package.json
├── pnpm-workspace.yaml
├── pnpm-lock.yaml
├── README.md                   # badge CI, Codecov, link diagramă Nx
├── LICENSE
└── .env.example                # variabile non‑sensibile; `.env` real ignorat
```

**Cel mai adânc traseu exemplificat:**  
`/core/apps/shell-gateway/frontend/src/components/common/__tests__/` → **8 niveluri** (cerința ≥ 6 îndeplinită).

**Prin această actualizare, toate modulele, IaC, script‑uri și documentația devin perfect aliniate unui singur arbore‑sursă, facilitând automat validările CI și regulile `enforceModuleBoundaries` definite în Nx.**

- **Arhitectura completă** cuprinde aplicația-mamă (core), aplicațiile standalone, tools și fișierele de configurare monorepo.

## Reguli Nx & CI Paths

### Nx Tags & enforceModuleBoundaries

- Tag-uri obligatorii: `tier:core`, `tier:standalone-vettify`, `tier:standalone-mercantiq`, etc.
- Regula `enforceModuleBoundaries` interzice imports cross-tier între aplicații standalone.
- Aplicația core poate importa din packages, dar standalone apps sunt izolate.

### CI/CD Paths

- **Toate paths din GitHub Actions** trebuie să folosească prefixele canonice:
  - `core/**` pentru aplicația-mamă
  - `standalone/**` pentru aplicații standalone  
  - `tools/**` pentru utilitare partajate
- **Interzise**: paths vechi `apps/**`, `packages/**`, `infra/**` fără prefix
- **Hook lint-paths** validează automat conformitatea la commit

**Exemple corecte de paths CI:**
```yaml
# CORECT
on:
  push:
    paths:
      - 'core/apps/shell-gateway/**'
      - 'standalone/mercantiq/apps/sales/**'
      - 'tools/ci-templates/**'

# GREȘIT - va fi respins de lint-paths
on:
  push:
    paths:
      - 'apps/shell-gateway/**'      # INTERZIS
      - 'apps/mercantiq-sales/**'    # INTERZIS
```

### Directoare admise la rădăcină

Directoarele permise la rădăcină sunt **exact** cele enumerate în structura canonică:
- `core/`, `standalone/`, `tools/` - structura principală
- `.github/`, `docker/`, `scripts/`, `docs/`, `roadmap/`, `tests/` - utilitare
- Fișiere de configurare: `.editorconfig`, `nx.json`, `package.json`, etc.

## Worker & Event Naming

- Worker tags **din tabelul din Readme 2**; nu crea tag nou fără aprobare.  
- Topic‑uri RMQ: `<worker.tag>` pentru solicitare, `<module>.<boundedContext>.<event>` pentru business.  
- Versiune eveniment prin sufix `.v1` doar când schema se schimbă.

## Multi‑tenant, Multi‑warehouse

- Orice exemple de SQL **trebuie** să includă coloanele `tid` și `whid`.  
- DSN exemplu: `postgresql+asyncpg://user:pass@host:5432/tenant_core` + `search_path=iWMS`.

## Securitate & Compliance

- Token JWT RS256, claims minime: `tid`, `whid`, `scp`, `sub`, `iat`, `exp`.  
- TLS 1.3, mTLS intern – nu sugera HTTP simplu.  
- Orice script sau container **semnat Cosign**.  
- Respectă GDPR/eIDAS/ISO 27001 mapping din cap. 10.

## Observability & KPI

- Include trace‑id (`x-trace-id`) în ex. de cod.  
- KPI trebuie să urmărească țintele din capitole. Nu inventa altele.  
- Dashboard latență: folosim Prometheus metric `http_request_duration_seconds_bucket`.

## CI/CD

- Pipeline = GitHub Actions → Cosign → OCI → Argo CD; nu GitLab CI.  
- Canary 10 % → 100 % analiză Prometheus (< 1 h).  
- Fail‑safe: rollback automat, event `deploy.rollback`.

## Răspunsuri la "cum fac X?"

1. Mapează întrebarea la modul + layer (frontend/api/worker).  
2. Propune modificări doar prin:  
   - `core/scripts/create-module.ts` sau `standalone/<app>/scripts/create-worker.py`  
   - configurări Helm (`core/infra/helm/<module>` sau `standalone/<app>/infra/helm/`).  
3. **Folosește OBLIGATORIU prefixele canonice în toate căile**:
   - `core/apps/shell-gateway/` (NU `/apps/shell-gateway/`)
   - `standalone/mercantiq/apps/sales/` (NU `/apps/mercantiq-sales/`)
   - `standalone/numeriqo/apps/manufacturing/` (NU `/apps/numeriqo-manufacturing/`)
4. În exemplele CI/CD, folosește paths cu `core/**`, `standalone/**`, `tools/**`.
5. Actualizează README doar prin instructarea canmore.update_textdoc.  
6. Include snippet YAML/Bash/TS strict necesar; evită tutoriale lungi.

## Prohibiții

- Fără schimbare de stack (ex.: GraphQL → REST plain).  
- Fără rearanjare directoare.  
- **INTERZIS**: folosirea căilor vechi `/apps/`, `/packages/`, `/infra/` fără prefix canonice.
- **INTERZIS**: referințe la module separate `mercantiq-sales`, `numeriqo-manufacturing` etc.
- Nu posta chei secrete dummy (`SECRET_KEY=xyz`). Folosește `<placeholder>`.  
- Nu discuta prețuri/comercial.

## Format Răspuns

- Titlu opțional `###` + conținut la subiect.  
- Cod în blocuri triple back‑tick cu limbaj (`ts`).  
- Liste numerotate pentru pași, tabele când e nevoie (max 8 coloane).  
- Concluzie scurtă („Gata! Spune‑mi dacă…") doar când cere utilizatorul.

---

## Migrarea fișierelor existente

**ATENȚIE**: Fișierele de roadmap și README existente conțin încă referințe la căile vechi și trebuie actualizate:

### Roadmap-uri de actualizat:
- ✅ `5_roadmap_admin_core.md` - actualizat cu `"/core/apps/admin-core/"`
- ✅ `4_roadmap_shell_gateway.md` - actualizat cu `"/core/apps/shell-gateway/"`  
- ✅ `6_roadmap_base_workers.md` - actualizat cu `"/core/apps/workers-core/"`
- ✅ `8_roadmap_vettify.md` - actualizat cu numerotare F2 sincronizată
- `3_roadmap_f_1_Core_Platform.md` - idem pentru toate căile core

### README-uri de actualizat:
- `readme_1_genius_erp_suite.md` - `numeriqo-manufacturing` → aplicația unificată `numeriqo`
- `1_roadmap_general_suita_genius_erp.md` - referințe la module separate

**Până la actualizare, hook-ul lint-paths va respinge commit-urile care încalcă structura canonică.**

---

**Încălcarea oricărei reguli = ChatGPT trebuie să se autocorecteze imediat sau să ceară clarificare.**