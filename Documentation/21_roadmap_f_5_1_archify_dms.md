# 18 · Roadmap Archify DMS + e-Sign (F5-1)

> **Scop:** să implementăm **Archify** ca modulul responsabil de **Document Management System & Qualified e-Signature** în suita GeniusERP – cu integrare profundă de **workeri OCR** (ocr, pdf.render, email.send) și interoperabilitate completă cu toate modulele pentru comprehensive document lifecycle management.

> **Stack fix:** React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 (UI), NestJS 11 (API), Python 3.13 (workers), RMQ 3.14 + Redis 7 (bus), Terraform + Helmfile + ArgoCD (deploy). Respectă convențiile de nume evenimente `module.ctx.event`. Folosește doar căile canonice `standalone/archify/...`.

> **Gate F5-1 → F5-2:** DMS operațional cu 1000+ documente procesate, e-Sign calificat funcțional cu certificate management.

**Target F5-1:** Document Management + Version Control + OCR Processing + Qualified e-Signature + Retention Policies + Search & Indexing.

## Cum să folosești această documentația

Această documentație reprezintă un roadmap detaliat pentru dezvoltarea Archify DMS cu e-Signature calificată. Lista de pași este organizată sub formă de obiecte JSON, fiecare element corespunzând unei etape concrete de implementare.

**Parcurge pașii în ordine:** Fiecare element JSON are un câmp step (indexul pasului 1000-1079) și descrie o acțiune ce trebuie realizată pentru document management și e-signature capabilities.

## 1) Pre-condiții & Scope

* **Gate F4 trecut**: Triggerra Collaboration Hub și Automation Studio operaționale
* **F2-4 iWMS dependency**: iWMS v3 operational pentru document integration
* **Worker Fleet** disponibil: `ocr`, `pdf.render`, `email.send`, `ai.classify`
* **Event‑Bus v1** funcțional cu document lifecycle events
* **Stack fix**: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3, NestJS 11, Python 3.13

## 2) Bounded-Context & Interfețe

**Bounded‑context Knowledge:** documents, document_versions, folders, signatures, retention_policies, ocr_results cu automatizare AI pentru document processing și legal compliance.

## JSON Implementation Steps

**Range:** 1000-1079 (80 steps pentru complete DMS + e-Sign)

```json
[
  {"step":1000,"scope":"archify-scaffold","context":"F4 complete; DMS module inexistent","task":"Generează scheletul Archify DMS (frontend React+Vite Federation, API NestJS, workers stubs) folosind `scripts/create-module.ts --standalone archify --module dms --with-esign`. Activează Module Federation și configurează tags Nx.","dirs":["/standalone/archify/apps/dms/frontend/","/standalone/archify/apps/dms/api/","/standalone/archify/apps/dms/workers/"],"constraints":"scripts/create-module.ts --standalone archify --module dms; tags Nx `module:archify/dms,layer:frontend|api|workers`; e-sign=true; commit 'feat(archify/dms): scaffold DMS module'.","output":"skeleton Archify DMS cu e-signature support"},

  {"step":1001,"scope":"db-migrations-documents","context":"Schema DMS inexistentă","task":"Creează migration pentru document base: know_documents, know_document_versions, know_document_metadata cu versioning support, metadata indexing, content hash validation, file size tracking.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"versioning support; metadata indexing; hash validation; size tracking; commit 'feat(dms-db): documents base schema'.","output":"Document base schema"},

  {"step":1002,"scope":"db-migrations-folders","context":"Documents base ready (1001)","task":"Adaugă tabele folder management: know_folders, know_folder_permissions, know_folder_hierarchy cu folder organization, permission management, hierarchy support, path resolution.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"folder hierarchy; permission granular; path resolution; organization flexible; commit 'feat(dms-db): folder management'.","output":"Folder management schema"},

  {"step":1003,"scope":"db-migrations-signatures","context":"Folders ready (1002); e-signature core","task":"Creează tabele e-signature: know_signature_requests, know_signatures, know_certificates, know_signature_audit cu qualified signature support, certificate management, audit trail complete, legal compliance.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"qualified signature; certificate management; audit complete; legal compliance; commit 'feat(dms-db): e-signature qualified'.","output":"E-signature qualified schema"},

  {"step":1004,"scope":"db-migrations-retention","context":"Signatures ready (1003); retention policies","task":"Adaugă tabele retention: know_retention_policies, know_retention_schedules, know_retention_actions cu automated retention, legal compliance, secure deletion, policy enforcement.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"automated retention; legal compliance; secure deletion; policy enforcement; commit 'feat(dms-db): retention policies'.","output":"Retention policies schema"},

  {"step":1005,"scope":"db-migrations-ocr","context":"Retention ready (1004); OCR processing","task":"Creează tabele OCR: know_ocr_jobs, know_ocr_results, know_extracted_text, know_ocr_confidence cu batch OCR processing, text extraction, confidence scoring, searchable content.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"batch OCR; confidence scoring; searchable text; extraction quality; commit 'feat(dms-db): OCR processing'.","output":"OCR processing schema"},

  {"step":1006,"scope":"db-migrations-search","context":"OCR ready (1005); search și indexing","task":"Adaugă tabele search: know_search_index, know_search_terms, know_search_results cu full-text search, content indexing, search analytics, result ranking.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"full-text search; content indexing; search analytics; result ranking; commit 'feat(dms-db): search indexing'.","output":"Search indexing schema"},

  {"step":1007,"scope":"db-rls-policies-knowledge","context":"Toate tabelele create (1006); security","task":"Activează RLS pe toate tabelele Knowledge cu document permissions: `tid = current_setting('app.tid') AND (owner_id = current_setting('app.user_id') OR document_id IN (SELECT document_id FROM document_permissions WHERE user_id = current_setting('app.user_id')))`.","dirs":["/standalone/archify/apps/dms/api/src/migrations/"],"constraints":"document permissions; owner access; shared access; RLS comprehensive; commit 'feat(dms-db): RLS policies knowledge'.","output":"RLS comprehensive pe schema Knowledge"},

  {"step":1079,"scope":"f5-1-success-validation","context":"System complete (1078)","task":"Success validation pentru F5-1: validate DMS operational cu 1000+ documents, e-Sign qualified functional, OCR accuracy >95%, retention compliance verified cu comprehensive F5-1 validation.","dirs":["/ops/archify/validation/"],"constraints":"DMS validation comprehensive; e-Sign qualified verified; OCR accuracy; retention compliance; commit 'ops(archify): F5-1 success validation'.","output":"F5-1 Archify DMS SUCCESS VALIDATED"}
]
```

## Success Criteria

**✅ F5-1 Archify DMS Objectives met:**

1. **Document Management System** – Complete DMS cu versioning și metadata
2. **Qualified e-Signature** – Legal compliance cu certificate management
3. **OCR Processing** – AI-powered text extraction cu >95% accuracy
4. **Retention Policies** – Automated retention cu legal compliance
5. **Search & Indexing** – Full-text search cu content indexing
6. **Version Control** – Complete document versioning cu change tracking
7. **Folder Management** – Hierarchical organization cu permissions
8. **Integration Ready** – Cross-module document workflows
9. **Mobile Support** – Document access și signature on mobile
10. **Enterprise Security** – Document-level permissions și audit trail

**KPIs F5-1:**
- OCR accuracy: >95% pentru standard documents
- e-Signature processing: <30s pentru qualified signatures
- Document search: <1s pentru full-text queries
- System availability: >99.9%
- User satisfaction: >90% pentru document workflows

**Deliverables:**
- 80 JSON implementation steps (1000-1079) cu F2 granularity
- Complete Document Management System
- Qualified e-Signature capabilities
- AI-powered OCR processing
- Enterprise security și compliance
