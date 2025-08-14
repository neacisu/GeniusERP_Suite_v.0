# 4 · Roadmap Shell Gateway (30 prompts CursorAI)

## Format JSON extins - câmpuri obligatorii:

- **step** - index original (păstrăm 200-224, 294, 297-298 pentru trasabilitate)
- **scope** - sub-sistem vizat (max 3-4 cuvinte)
- **context** - livrări anterioare relevante
- **task** - instrucțiune imperativă clară
- **dirs** - listează directoarele vizate
- **constraints** - reguli stricte (commit-msg, chmod, etc.)
- **output** - rezultat așteptat

Structura respectă identic convențiile din **F0** și **F1**; nu introduce termene, doar ordinea logică.

## Umbrella - Dependencies & Context F1

| Interval | Effort | Scop/Componente | Layer | Dependințe F0 |
|----------|--------|-----------------|-------|----------------|
| 1‑4 | 1 SW | Event Bus RMQ namespaces & conventions v1 | infra | **0‑20, 33** |

```json
[
  {"step":200,"scope":"shell-ui-bootstrap","context":"Nu există frontend Shell.","task":"Folosește scripts/create-module.ts pentru a genera app React Vite `shell-gateway/frontend` + tags Nx `module:shell,layer:frontend`.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"commit 'feat(shell-ui): scaffold shell frontend'.","output":"skeleton frontend Shell"},
  {"step":201,"scope":"shell-ui-tailwind","context":"Skeleton creat (pas 200).","task":"Configurează Tailwind + preset tokens în `tailwind.config.ts`; importă `@genius/ui/tokens`.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"commit 'chore(shell-ui): add tailwind'.","output":"Tailwind funcțional"},
  {"step":202,"scope":"shell-ui-aliases","context":"Imports relative.","task":"Adaugă path-aliases `@shell/*` în tsconfig base și vite.config federation.","dirs":["/","/core/apps/shell-gateway/frontend/"],"constraints":"No paths absolute.","output":"alias paths"},
  {"step":203,"scope":"shell-ui-loader","context":"Module federation neconfigurat.","task":"Integrează remote-loader (Vite plugin federation) și expune `remoteEntry.js`.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"commit 'feat(shell-ui): remote-loader'.","output":"remoteEntry expus"},
  {"step":204,"scope":"shell-ui-layout","context":"UI gol.","task":"Scaffold Layout (AppBar, Drawer, Outlet) cu MUI Components & slots.","dirs":["/core/apps/shell-gateway/frontend/src/"],"constraints":"fără styled-components.","output":"layout vizibil"},
  {"step":205,"scope":"ui-docs-tailwind","context":"MUI 6 + Tailwind 3 coexistă.","task":"Actualizează `packages/ui/README.md` cu ordinea importurilor + `tailwind.config` { important:'#root' }.","dirs":["/packages/ui/"],"constraints":"","output":"doc styling"},
  {"step":206,"scope":"shell-ui-theme","context":"Tokens importate (pas 201).","task":"Implementează ThemeProvider + switch light/dark salvând în localStorage `theme`.","dirs":["/core/apps/shell-gateway/frontend/src/"],"constraints":"Respectă pregătirea Theme Hub.","output":"theme switch"},
  {"step":207,"scope":"shell-ui-nav","context":"Drawer static.","task":"Generează meniu side-nav din JSON livrat de Admin Core `/v1/admin/nav`.","dirs":["/core/apps/shell-gateway/frontend/src/"],"constraints":"Fallback static când API 404.","output":"navigație dinamică"},
  {"step":208,"scope":"shell-ui-version","context":"Nu afișează versiune.","task":"Adaugă componentă `VersionBadge` care citește `import.meta.env.VITE_COMMIT_SHA`.","dirs":["/core/apps/shell-gateway/frontend/src/components/"],"constraints":"vite define env.","output":"commit hash în UI"},
  {"step":209,"scope":"shell-ui-health-widget","context":"/health doar backend.","task":"Afișează widget status Gateway, Admin Core, RMQ prin fetch periodic 30s.","dirs":["/core/apps/shell-gateway/frontend/src/widgets/"],"constraints":"AbortController timeout 3s.","output":"health widget"},
  {"step":210,"scope":"shell-ui-webvitals","context":"Observabilitate UX lipsă.","task":"Integrează `web-vitals` și trimite metrici la `window.prometheusWebVitals`.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"commit 'feat(shell-ui): web-vitals'.","output":"LCP/FID/CLS colectate"},
  {"step":211,"scope":"shell-ui-storybook","context":"Componente fără catalog.","task":"Adaugă Storybook8 la workspace și configurează pentru `packages/ui` + shell.","dirs":["/","/packages/ui/"],"constraints":"nx run-many storybook.","output":"storybook local"},
  {"step":212,"scope":"shell-ui-stories","context":"Storybook gol.","task":"Creează 3 stories (Button, Card, Modal) folosind tokens.","dirs":["/packages/ui/src/"],"constraints":"CSF 3 format.","output":"stories vizibile"},
  {"step":213,"scope":"shell-ui-unit-test","context":"Zero teste.","task":"Adaugă Vitest + Testing Library, cover Layout + VersionBadge; threshold 80%.","dirs":["/core/apps/shell-gateway/frontend/"],"constraints":"commit 'test(shell-ui): vitest'.","output":"teste unit pass"},
  {"step":214,"scope":"shell-ui-e2e","context":"E2E absent.","task":"Configurează Playwright proiect `shell-e2e` cu test login + nav.","dirs":["/core/apps/shell-gateway/frontend-e2e/"],"constraints":"headless ci.","output":"playwright verde"},
  {"step":215,"scope":"shell-ui-ci","context":"CI generic F0.","task":"Adaugă job `nx affected -t lint,test,build` pt shell-ui + upload storybook artefact.","dirs":["/.github/workflows/ci-template.yml"],"constraints":"lint fail on warn.","output":"CI shell-ui"},
  {"step":216,"scope":"shell-ui-dockerfile","context":"Image lipsă.","task":"Creează `docker/frontend.Dockerfile` multi-stage vite build → Nginx.","dirs":["/docker/"],"constraints":"no root user.","output":"image build ok"},
  {"step":217,"scope":"shell-ui-helm","context":"Deploy lipsă.","task":"Chart `infra/helm/shell-frontend/` values dev|prod incl. IngressRoute.","dirs":["/infra/helm/shell-frontend/"],"constraints":"OCI push.","output":"chart publicat"},
  {"step":218,"scope":"shell-ui-dashboard","context":"Observability UX.","task":"Dashboard Grafana Web-Vitals (LCP P75, CLS P75).","dirs":["/infra/grafana/provisioning/dashboards/"],"constraints":"uid shell_vitals.","output":"dashboard gata"},
  {"step":219,"scope":"shell-ui-gate","context":"Gate F1 criteriu shell.","task":"Script `scripts/gate-f1-shell.sh` verifică 3 widget demo up.","dirs":["/scripts/"],"constraints":"exit>0 dacă fail.","output":"gate script"},
  {"step":220,"scope":"shell-ui-docs","context":"Docs incomplet.","task":"Update `roadmap/shell.md` cu secțiune F1 livrări.","dirs":["/roadmap/"],"constraints":"commit 'docs(shell): f1 roadmap'.","output":"docs actualizate"},
  {"step":221,"scope":"shell-ui-a11y","context":"Accesibilitate need.","task":"Activează eslint-plugin-jsx-a11y rules high.","dirs":["/packages/rules-eslint/"],"constraints":"CI fail on error.","output":"a11y rules"},
  {"step":222,"scope":"shell-ui-lighthouse","context":"Perf budget.","task":"Adaugă job Lighthouse CI: LCP ≤ 2.5s, score≥ 90.","dirs":["/.github/workflows/ci-template.yml"],"constraints":"upload report.","output":"perf gate"},
  {"step":223,"scope":"shell-ui-cdn","context":"remoteEntry publish manual.","task":"Script `scripts/publish-remote.sh` push `remoteEntry.js` în R2 CDN, semnat Cosign.","dirs":["/scripts/"],"constraints":"idempotent.","output":"remote CDN"},
  {"step":224,"scope":"shell-ui-argocd","context":"Argo app lipsă.","task":"Application YAML `infra/k8s/argocd/shell-frontend.yaml`.","dirs":["/infra/k8s/argocd/"],"constraints":"","output":"Argo sync shell"},
  {"step":294,"scope":"obs-servicemon-shell","context":"Prom scrape Shell.","task":"ServiceMonitor shell-frontend added namespace gateway.","dirs":["/infra/k8s/"],"constraints":"","output":"SM shell"},
  {"step":297,"scope":"obs-k6-shell","context":"Synthetic.","task":"k6 script 200 VU 30s / nav; threshold error_rate<0.5%.","dirs":["/tests/k6/"],"constraints":"","output":"k6 report"},
  {"step":298,"scope":"script-module-flag","context":"DX create-module.","task":"Adaugă flag `--with-shell-nav` ce actualizează meniu automat.","dirs":["/scripts/create-module.ts"],"constraints":"","output":"flag nou"}
]
```

**Nota:** acest roadmap individual este sincronizat automat cu `3_roadmap_f_1_Core_Platform.md`; nu modifica manual pașii din alt fișier.