# 6 · Roadmap Base Workers (28 prompts CursorAI)

## Format JSON extins – câmpuri obligatorii
- `step` – index original **274‑301**
- `scope` – sub‑sistem vizat
- `context` – livrări anterioare relevante
- `task` – instrucțiune imperativă clară
- `dirs` – directoare vizate
- `constraints` – reguli stricte (commit‑msg, chmod, etc.)
- `output` – rezultat așteptat

## Umbrella – Dependencies & Context F1
| Interval | Effort | Componente | Layer | Dependințe |
|----------|--------|------------|-------|------------|
| 1‑5 | 2 SW | `ocr`, `pdf.render`, `email.send`, `notify.slack` | workers | **0‑20, 33**, 225‑257 |

```json
[
  {"step":274,"scope":"workers-core-skel","context":"Workers module inexistent.","task":"Creează mono-repo `workers-core` în `/core/apps/workers-core/`.","dirs":["/core/apps/workers-core/"],"constraints":"poetry init.","output":"skeleton workers"},
  {"step":275,"scope":"workers-poetry-deps","context":"Deps Python.","task":"poetry add `paddleocr` `aiosmtplib` `pyppeteer` `slack-sdk` `structlog>=24` `opentelemetry-exporter-prometheus`.","dirs":["/core/apps/workers-core/"],"constraints":"","output":"deps actualizate"},
  {"step":276,"scope":"workers-celery-conf","context":"Queue map.","task":"Creează `celeryconfig.py` cu queue‑uri `ocr`, `pdf.render`, `email.send`, `notify.slack`.","dirs":["/core/apps/workers-core/"],"constraints":"","output":"celery conf"},
  {"step":277,"scope":"workers-env","context":"Vars.","task":"Actualizează `.env.example` worker vars (`SMTP_HOST`, `RMQ_URL`, `SLACK_WEBHOOK_URL`).","dirs":["/"],"constraints":"","output":".env.example upd"},
  {"step":278,"scope":"worker-ocr","context":"Worker OCR absent.","task":"`scripts/create-worker.py --tag ocr` → FastAPI health + Celery task `ocr.extract`.","dirs":["/core/apps/workers-core/ocr/"],"constraints":"GPU=false.","output":"worker ocr"},
  {"step":279,"scope":"worker-pdf-render","context":"`pdf.render` absent.","task":"Scaffold worker **Python** Pyppeteer pentru randare PDF (înlocuiește Node).","dirs":["/core/apps/workers-core/pdf-render/"],"constraints":"Chromium via apt.","output":"worker pdf"},
  {"step":280,"scope":"worker-email-send","context":"`email.send` absent.","task":"Scaffold worker Python aiosmtplib.","dirs":["/core/apps/workers-core/email-send/"],"constraints":"","output":"worker email"},
  {"step":281,"scope":"worker-notify-slack","context":"`notify.slack` absent.","task":"Scaffold worker **Python** slack-sdk pentru notificări (înlocuiește Node).","dirs":["/core/apps/workers-core/notify-slack/"],"constraints":"webhook + channel vars.","output":"worker slack"},
  {"step":282,"scope":"workers-unit-tests","context":"No tests.","task":"Pytest pentru `ocr`, `email` & `notify.slack` (mock).","dirs":["/core/apps/workers-core/"],"constraints":"","output":"pytest verde"},
  {"step":283,"scope":"workers-int-tests","context":"Integration.","task":"Pipeline test Celery → RMQ → worker → Redis result.","dirs":["/tests/integration/workers/"],"constraints":"","output":"tests pass"},
  {"step":284,"scope":"workers-dockerfiles","context":"Images.","task":"Dockerfile slim per worker, etichete SLSA.","dirs":["/docker/"],"constraints":"","output":"images build"},
  {"step":285,"scope":"workers-ci","context":"CI pipeline.","task":"Job matrix build/test/scan workers; push ghcr.","dirs":["/.github/workflows/ci-template.yml"],"constraints":"","output":"CI workers"},
  {"step":286,"scope":"workers-compliance-deps","context":"Noi integrări ANAF/REGES necesită pachete Python suplimentare.","task":"poetry add `zeep>=4` `signxml` (dependințe ANAF & Revisal).","dirs":["/core/apps/workers-core/"],"constraints":"","output":"dependințe ANAF/REGES adăugate"},
  {"step":287,"scope":"workers-celery-queues","context":"Queue-uri noi neconfigurate.","task":"Actualizează `celeryconfig.py` cu noile queue-uri: `anaf.taxpayer`, `anaf.efactura`, `anaf.etransport`, `anaf.saft`, `reges`. Adaugă variabile relevante în `.env.example` (ex.: token ANAF, path certificat).","dirs":["/core/apps/workers-core/celery/"],"constraints":"","output":"config Celery & ENV actualizat"},
  {"step":288,"scope":"worker-anaf-taxpayer","context":"Worker `anaf.taxpayer` inexistent.","task":"Scaffold worker (FastAPI + Celery task) pentru validarea CUI (ANAF) – ex. `taxpayer.validate` care interoghează API ANAF și răspunde cu date firmă.","dirs":["/core/apps/workers-core/anaf-taxpayer/"],"constraints":"fără chei în repo; ExternalSecrets pentru token ANAF","output":"worker `anaf.taxpayer` creat"},
  {"step":289,"scope":"worker-anaf-efactura","context":"Worker `anaf.efactura` inexistent.","task":"Scaffold worker Python pentru transmiterea facturilor electronice (e-Factura) – ex. task `efactura.submit` ce trimite XML la ANAF (cu semnătură) și confirmă status.","dirs":["/core/apps/workers-core/anaf-efactura/"],"constraints":"fără chei în repo; ExternalSecrets (credențiale OAuth/certificat)","output":"worker `anaf.efactura` creat"},
  {"step":290,"scope":"worker-anaf-etransport","context":"Worker `anaf.etransport` inexistent.","task":"Scaffold worker Python pentru declarațiile e-Transport – ex. task `etransport.submit` ce transmite detaliile livrării și obține codul UIT.","dirs":["/core/apps/workers-core/anaf-etransport/"],"constraints":"fără chei în repo; ExternalSecrets (certificat digital)","output":"worker `anaf.etransport` creat"},
  {"step":291,"scope":"worker-anaf-saft","context":"Worker SAF-T inexistent.","task":"Scaffold worker Python pentru generare & validare SAF-T (D406) – ex. task `saft.generate` ce compilează date contabile și rulează validarea DUK.","dirs":["/core/apps/workers-core/anaf-saft/"],"constraints":"include kit ANAF DUK; fără chei în repo (certificat via Vault)","output":"worker `anaf.saft` creat"},
  {"step":292,"scope":"worker-reges","context":"Worker Revisal inexistent.","task":"Scaffold worker Python pentru integrarea REGES (Revisal Online) – ex. task `reges.submit` care transmite XML-ul registrului prin API Inspecției Muncii.","dirs":["/core/apps/workers-core/reges/"],"constraints":"fără chei în repo; ExternalSecrets (autentificare cu certificat)","output":"worker `reges` creat"},
  {"step":293,"scope":"workers-helm-chart","context":"Deploy.","task":"Chart `infra/helm/workers-core/` cu Deployment per tag + Celery ConfigMap.","dirs":["/infra/helm/workers-core/"],"constraints":"cosign sign.","output":"chart OCI"},
  {"step":294,"scope":"workers-otel","context":"Tracing.","task":"Configurează `opentelemetry-exporter-prometheus`; elimină `celery-signalfx`.","dirs":["/core/apps/workers-core/"],"constraints":"","output":"OTEL Prom metrics"},
  {"step":295,"scope":"workers-prom","context":"Metrics.","task":"Expose `/metrics` via `prometheus_fastapi_instrumentator`.","dirs":["/core/apps/workers-core/"],"constraints":"","output":"metrics worker"},
  {"step":296,"scope":"workers-dashboard","context":"Grafana.","task":"Dashboard lag Celery & task success rate.","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"","output":"dashboard workers"},
  {"step":297,"scope":"workers-alerting","context":"Alerting.","task":"Alertmanager rule `task_failed_rate>5%`.","dirs":["/infra/k8s/alertmanager/"],"constraints":"","output":"alert rules"},
  {"step":298,"scope":"workers-hpa","context":"Autoscale.","task":"HPA CPU 70% min1 max10 per worker.","dirs":["/infra/helm/workers-core/"],"constraints":"","output":"HPA rules"},
  {"step":299,"scope":"workers-keda-autoscale","context":"Queue autoscale.","task":"`ScaledObject` per worker (`queueLength ≥ 100`) + `ScaledJob` backlog drain pentru `pdf.render`.","dirs":["/infra/helm/workers-core/"],"constraints":"cooldownPeriod=120s.","output":"autoscaling backlog activ"},
  {"step":300,"scope":"workers-opa-image","context":"Policy.","task":"ConstraintTemplate `CTNoLatest` + Constraint `NoLatestWorkers`.","dirs":["/infra/policies/opa/"],"constraints":"","output":"policy activ"},
  {"step":301,"scope":"workers-docs","context":"Docs.","task":"README `workers-core` (usage & queues).","dirs":["/core/apps/workers-core/"],"constraints":"","output":"doc worker"}
]
```

**Notă**: acest roadmap individual este sincronizat automat cu `3_roadmap_f_1_Core_Platform.md`; nu modificați manual pașii din alte fișiere.