# Roadmap Numeriqo People & Payroll (F3)

> **Scop:** să implementăm **Numeriqo People & Payroll** ca modulul responsabil de **Human Resources Management & Romanian Payroll** în suita GeniusERP – cu integrare profundă de **workeri REGES** (reges pentru Revisal online) și interoperabilitate completă cu **Manufacturing** (labor tracking), **Accounting** (cost accounting), și ecosistemul complet pentru closed-loop HR operations.

**Target F3:** Motor salarizare RO + Employee Management + Time Tracking + Benefits Administration + REGES Compliance + Labor Cost Integration.

**Bounded-context People:** employees, contracts, positions, departments, time_tracking, payroll_runs, salary_components, benefits, leave_management, performance_evaluation cu automatizare completă pentru Romanian labor law compliance și REGES integration.

**Workers integrati:** 
`reges` (REGES Online pentru Inspecția Muncii), `report.kpi` (KPI-uri HR în timp real), `pdf.render` (contracte și rapoarte HR), `email.send` (notificări HR), `tax.vat` (calcule sociale și fiscale)

## Preconditions

**Prerequisite obligatorii:**
* **F3-2 Complete** – Numeriqo Accounting operațional (cost accounting integration)
* **F3-1 Manufacturing** – Labor tracking din work orders disponibil
* **Worker Fleet** disponibil: `reges`, `report.kpi`, `pdf.render`, `email.send`, `tax.vat`
* **Event Bus v1** – naming convention `<module>.<context>.<event>` funcțional
* **Database PG17** – multi-tenancy RLS activă cu politici standard
* **Observability Stack** – Prometheus/Grafana/Tempo/Loki operațional

## Events published by People & Payroll

* **`hr.employee.hired`**: angajare nouă cu date complete
* **`hr.employee.contract.changed`**: modificare contract de muncă
* **`hr.employee.terminated`**: încetare contract de muncă
* **`hr.payroll.run.completed`**: finalizare rulare salarizare
* **`hr.timesheet.submitted`**: pontaj submis pentru aprobare
* **`hr.leave.approved`**: aprobare concediu/absentă
* **`hr.performance.evaluated`**: evaluare performanță completată

## Events consumed by People & Payroll

* `manufacturing.work_order.started` - înregistrare timp lucru pe work order
* `manufacturing.work_order.completed` - finalizare timp lucru pentru costing
* `accounting.period.closed` - calculare cost total labor per perioadă
* `manufacturing.terminal.clock_in` - pontaj începere lucru
* `manufacturing.terminal.clock_out` - pontaj încheiere lucru

---

## JSON Implementation Steps

**Range:** 700-799 (100 steps target pentru complexity HR + Romanian Labor Law Compliance)

**Naming Convention:**
- Workers: `<domain>.<action>` (hr.reges, hr.payroll)
- Events: `<module>.<context>.<event>` (hr.employee.hired)
- Tables: snake_case cu prefixe (hr_employees, hr_contracts, hr_payroll_runs)

```json
[
  {"step":700,"scope":"hr-scaffold","context":"F3-2 Accounting complete; modul HR inexistent","task":"Generează scheletul Numeriqo People & Payroll (frontend React+Vite Federation, API NestJS, workers stubs) folosind `scripts/create-module.ts --standalone numeriqo --module people --with-compliance`. Activează Module Federation remoteEntry și configurează tags Nx.","dirs":["/standalone/numeriqo/apps/people/frontend/","/standalone/numeriqo/apps/people/api/","/standalone/numeriqo/apps/people/workers/"],"constraints":"scripts/create-module.ts --standalone numeriqo --module people; tags Nx `module:numeriqo/people,layer:frontend|api|workers`; compliance=true; commit 'feat(numeriqo/people): scaffold HR module'.","output":"skeleton HR complete cu FE+API+Workers"},

  {"step":701,"scope":"db-migrations-employees","context":"Schema HR inexistentă; Romanian labor law requirements","task":"Creează migration pentru employees base: hr_employees, hr_personal_data, hr_addresses cu date personale complete, CNP validation, date contact, emergency contacts conform cerințele românești HR.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"CNP validation RO; GDPR compliance; personal data encrypted; UUID PK; commit 'feat(hr-db): employees base RO'.","output":"Employees schema Romanian compliant"},

  {"step":702,"scope":"db-migrations-organizational","context":"Employees base ready (701); organizational structure","task":"Adaugă tabele organizaționale: hr_departments, hr_positions, hr_organizational_units cu hierarchy management, reporting relationships, cost centers mapping pentru analytical accounting.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"hierarchy levels unlimited; cost centers FK; reporting structure; commit 'feat(hr-db): organizational structure'.","output":"Organizational structure schema"},

  {"step":703,"scope":"db-migrations-contracts","context":"Organizational ready (702); employment contracts","task":"Creează tabele contracts: hr_contracts, hr_contract_amendments, hr_salary_components cu contract types (permanent, fixed-term, trial), salary structure, benefits, working conditions conform Codul Muncii RO.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"Romanian contract types; Codul Muncii compliance; salary components detailed; commit 'feat(hr-db): contracts Romanian'.","output":"Employment contracts schema RO"},

  {"step":704,"scope":"db-migrations-time-tracking","context":"Contracts ready (703); time and attendance","task":"Adaugă tabele time tracking: hr_timesheets, hr_time_entries, hr_attendance, hr_working_schedules cu flexible working hours, overtime calculation, night shifts, holidays conform legislație română.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"overtime calculation RO; night shift premiums; holiday calendar RO; commit 'feat(hr-db): time tracking RO'.","output":"Time tracking schema Romanian"},

  {"step":705,"scope":"db-migrations-payroll","context":"Time tracking ready (704); payroll processing","task":"Creează tabele payroll: hr_payroll_runs, hr_payroll_entries, hr_salary_calculations, hr_deductions cu gross-to-net calculation, social contributions Romanian (CAS, CASS, income tax), meal vouchers, transport allowances.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"Romanian social contributions; tax calculation 2024 rates; meal vouchers calculation; commit 'feat(hr-db): payroll Romanian'.","output":"Payroll calculation schema RO"},

  {"step":706,"scope":"db-migrations-benefits","context":"Payroll ready (705); benefits administration","task":"Adaugă tabele benefits: hr_benefits, hr_benefit_enrollments, hr_medical_insurance, hr_pension_plans cu private health insurance, meal vouchers, transport benefits, additional pension conform opțiuni românești.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"Romanian benefits standard; medical insurance providers; meal vouchers legal limits; commit 'feat(hr-db): benefits RO'.","output":"Benefits administration schema"},

  {"step":707,"scope":"db-migrations-leave","context":"Benefits ready (706); leave management","task":"Creează tabele leave: hr_leave_types, hr_leave_requests, hr_leave_balances, hr_holidays cu annual leave (CO), sick leave (CM), maternity leave, legal holidays Romanian calendar.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"Romanian leave types; legal holidays calendar; maternity/paternity leave; commit 'feat(hr-db): leave management RO'.","output":"Leave management schema Romanian"},

  {"step":708,"scope":"db-migrations-performance","context":"Leave ready (707); performance management","task":"Adaugă tabele performance: hr_performance_reviews, hr_objectives, hr_competencies, hr_development_plans cu goal setting, competency framework, career development, succession planning.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"competency framework standard; goal tracking; development planning; commit 'feat(hr-db): performance management'.","output":"Performance management schema"},

  {"step":709,"scope":"db-migrations-reges-compliance","context":"Performance ready (708); REGES requirements","task":"Creează tabele REGES compliance: hr_reges_submissions, hr_employment_registry, hr_contract_changes cu REGES data mapping, submission history, validation errors, Revisal format support.","dirs":["/standalone/numeriqo/apps/people/api/src/migrations/"],"constraints":"REGES format exact; Revisal XML schema; submission tracking complete; commit 'feat(hr-db): REGES compliance'.","output":"REGES compliance schema"},

  {"step":710,"scope":"db-rls-policies-hr","context":"Toate tabelele HR create (709); RLS standard suite","task":"Activează Row Level Security pe toate tabelele HR cu politica standard extended: `tid = current_setting('app.tid') AND (whid = current_setting('app.whid') OR whid IS NULL) AND (mid = current_setting('app.mid') OR mid IS NULL)`. Include GDPR access control pentru date personale.","dirs":["/standalone/numeriqo/apps/people/api/src/db/rls/"],"constraints":"RLS standard cu GDPR controls; personal data restricted; commit 'feat(hr-db): RLS policies GDPR'.","output":"RLS activ pe schema HR"},

  {"step":711,"scope":"entities-orm-hr","context":"RLS policies active (710); Romanian HR standards","task":"Definește entități TypeORM pentru toate tabelele HR: Employee, Contract, Department, Position, Timesheet, PayrollRun, Benefit cu relationships complete și GDPR compliance decorators.","dirs":["/standalone/numeriqo/apps/people/api/src/entities/"],"constraints":"relationships complete; GDPR annotations; Romanian standards; no logic în entities; commit 'feat(hr-api): TypeORM entities HR'.","output":"HR entities complete"},

  {"step":712,"scope":"repositories-hr","context":"Entities ready (711); complex HR queries","task":"Implementează repositories pattern pentru HR: EmployeeRepository, PayrollRepository, TimeTrackingRepository, BenefitsRepository cu complex query builders pentru rapoarte HR, cost calculations, compliance reports.","dirs":["/standalone/numeriqo/apps/people/api/src/repositories/"],"constraints":"complex queries HR optimized; no business logic; payroll calculations ready; commit 'feat(hr-api): repositories HR'.","output":"HR repositories layer"},

  {"step":713,"scope":"dto-validation-hr","context":"Repositories ready (712); Romanian HR validation","task":"Creează DTO cu class-validator pentru toate operations: CreateEmployeeDto, PayrollRunDto, ContractDto, TimesheetDto cu validări specifice românești (CNP, IBAN, tax codes).","dirs":["/standalone/numeriqo/apps/people/api/src/dto/"],"constraints":"Romanian validation rules; CNP validation; IBAN Romanian; commit 'feat(hr-api): DTOs validation RO'.","output":"HR DTOs validate Romanian"},

  {"step":714,"scope":"services-employee-management","context":"DTOs ready (713); employee lifecycle","task":"Implementează EmployeeService cu operații: createEmployee, updateEmployee, terminateEmployee, rehireEmployee, transferEmployee cu business rules pentru employee lifecycle și REGES notifications.","dirs":["/standalone/numeriqo/apps/people/api/src/services/employee/"],"constraints":"employee lifecycle complete; REGES integration; business rules RO; unit tests ≥85%; commit 'feat(hr-api): Employee service'.","output":"Employee management service"},

  {"step":715,"scope":"services-payroll-calculation","context":"Employee service ready (714); payroll core","task":"Implementează PayrollService pentru Romanian payroll: calculateGrossToNet, calculateSocialContributions, calculateIncomeTax, processMealVouchers, calculateOvertime cu algoritmi de calcul conformi legislației 2024.","dirs":["/standalone/numeriqo/apps/people/api/src/services/payroll/"],"constraints":"Romanian tax rates 2024; social contributions accurate; overtime calculation legal; commit 'feat(hr-api): Payroll service RO'.","output":"Payroll calculation service Romanian"},

  {"step":716,"scope":"services-time-tracking","context":"Payroll service ready (715); time and attendance","task":"Implementează TimeTrackingService: recordTimeEntry, calculateWorkedHours, processOvertime, validateTimesheets, integrateManufacturingTime cu integration Manufacturing labor tracking.","dirs":["/standalone/numeriqo/apps/people/api/src/services/time/"],"constraints":"Manufacturing integration; overtime automatic; validation rules; commit 'feat(hr-api): Time tracking service'.","output":"Time tracking service cu Manufacturing"},

  {"step":717,"scope":"services-benefits-administration","context":"Time tracking ready (716); benefits management","task":"Implementează BenefitsService: manageBenefitEnrollments, calculateMealVouchers, processMedicalInsurance, managePensionContributions cu Romanian benefits specifice și cost calculation.","dirs":["/standalone/numeriqo/apps/people/api/src/services/benefits/"],"constraints":"Romanian benefits calculation; medical insurance integration; pension contributions; commit 'feat(hr-api): Benefits service RO'.","output":"Benefits administration service"},

  {"step":718,"scope":"services-leave-management","context":"Benefits service ready (717); leave processing","task":"Implementează LeaveService: requestLeave, approveLeave, calculateLeaveBalance, processMaternityLeave, manageSickLeave cu Romanian leave types și legal requirements.","dirs":["/standalone/numeriqo/apps/people/api/src/services/leave/"],"constraints":"Romanian leave types; maternity leave calculation; sick leave validation; commit 'feat(hr-api): Leave service RO'.","output":"Leave management service Romanian"},

  {"step":719,"scope":"services-performance-management","context":"Leave service ready (718); performance reviews","task":"Implementează PerformanceService: conductReview, setObjectives, trackCompetencies, planDevelopment, manageSuccession cu performance review workflows și career development.","dirs":["/standalone/numeriqo/apps/people/api/src/services/performance/"],"constraints":"review workflows; objective tracking; development planning; commit 'feat(hr-api): Performance service'.","output":"Performance management service"},

  {"step":720,"scope":"controllers-employee-management","context":"Employee service ready (714); employee API","task":"Controller Employee Management: CRUD operations pentru /employees endpoints cu employee lifecycle management, search, filtering, reporting conform GDPR restrictions.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/employee/"],"constraints":"GDPR compliance API; employee lifecycle; search optimized; p95 <300ms; commit 'feat(hr-api): Employee controller'.","output":"Employee Management API"},

  {"step":721,"scope":"controllers-payroll","context":"Payroll service ready (715); payroll API","task":"Controller Payroll: endpoints pentru payroll processing (/payroll/run, /calculate, /reports) cu Romanian payroll calculation, payslips generation, payroll reports.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/payroll/"],"constraints":"payroll calculation Romanian; payslips generation; reports detailed; commit 'feat(hr-api): Payroll controller RO'.","output":"Payroll Processing API Romanian"},

  {"step":722,"scope":"controllers-time-attendance","context":"Time tracking service ready (716); time API","task":"Controller Time & Attendance: endpoints pentru time tracking (/timesheets, /attendance, /overtime) cu Manufacturing integration, mobile time entry, approval workflows.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/time/"],"constraints":"Manufacturing integration API; mobile support; approval workflows; commit 'feat(hr-api): Time controller'.","output":"Time & Attendance API"},

  {"step":723,"scope":"controllers-benefits","context":"Benefits service ready (717); benefits API","task":"Controller Benefits Administration: endpoints pentru benefits management (/benefits/enroll, /medical-insurance, /meal-vouchers) cu Romanian benefits calculation și enrollment.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/benefits/"],"constraints":"Romanian benefits API; enrollment workflows; calculation real-time; commit 'feat(hr-api): Benefits controller RO'.","output":"Benefits Administration API"},

  {"step":724,"scope":"controllers-leave","context":"Leave service ready (718); leave API","task":"Controller Leave Management: endpoints pentru leave processing (/leave/request, /approve, /calendar) cu Romanian leave types, approval workflows, leave calendar integration.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/leave/"],"constraints":"Romanian leave types API; approval workflows; calendar integration; commit 'feat(hr-api): Leave controller RO'.","output":"Leave Management API Romanian"},

  {"step":725,"scope":"controllers-performance","context":"Performance service ready (719); performance API","task":"Controller Performance Management: endpoints pentru performance reviews (/performance/review, /objectives, /development) cu review workflows, goal tracking, development planning.","dirs":["/standalone/numeriqo/apps/people/api/src/controllers/performance/"],"constraints":"review workflows API; goal tracking; development planning; commit 'feat(hr-api): Performance controller'.","output":"Performance Management API"},

  {"step":726,"scope":"event-bus-hr","context":"Event Bus v1 operational; controllers ready (725)","task":"Integrează Event Bus client în HR API cu publish/subscribe capabilities. Configure topic routing și message serialization pentru HR events cu GDPR compliance.","dirs":["/standalone/numeriqo/apps/people/api/src/events/bus/"],"constraints":"SDK TS bus conform F2; GDPR compliance; contract tests; commit 'feat(hr-api): Event Bus integration'.","output":"Event Bus HR ready"},

  {"step":727,"scope":"events-publish-employee","context":"Event Bus ready (726); employee lifecycle","task":"Implementează event publishing pentru employee operations: `hr.employee.hired`, `hr.employee.contract.changed`, `hr.employee.terminated` cu payload complet pentru REGES integration.","dirs":["/standalone/numeriqo/apps/people/api/src/events/publishers/"],"constraints":"single publish post-commit; REGES data included; GDPR compliant; commit 'feat(hr-events): Employee events'.","output":"Employee lifecycle events published"},

  {"step":728,"scope":"events-publish-payroll","context":"Employee events ready (727); payroll processing","task":"Publică evenimente payroll: `hr.payroll.run.completed`, `hr.payslip.generated` cu payload pentru Accounting integration și cost allocation.","dirs":["/standalone/numeriqo/apps/people/api/src/events/publishers/"],"constraints":"Accounting integration data; cost allocation ready; commit 'feat(hr-events): Payroll events'.","output":"Payroll processing events"},

  {"step":729,"scope":"events-publish-time","context":"Payroll events ready (728); time tracking","task":"Emite evenimente time tracking: `hr.timesheet.submitted`, `hr.overtime.calculated` pentru Manufacturing cost integration și project costing.","dirs":["/standalone/numeriqo/apps/people/api/src/events/publishers/"],"constraints":"Manufacturing cost data; project tracking; commit 'feat(hr-events): Time tracking events'.","output":"Time tracking events published"},

  {"step":730,"scope":"events-publish-leave","context":"Time events ready (729); leave management","task":"Publică leave events: `hr.leave.approved`, `hr.leave.balance.updated` pentru capacity planning și resource allocation în Manufacturing și projects.","dirs":["/standalone/numeriqo/apps/people/api/src/events/publishers/"],"constraints":"capacity planning data; resource allocation info; commit 'feat(hr-events): Leave events'.","output":"Leave management events"},

  {"step":731,"scope":"events-consume-manufacturing","context":"Event publishing complete (730); Manufacturing integration","task":"Consumer pentru `manufacturing.work_order.started`, `manufacturing.work_order.completed` → automatic time tracking integration pentru labor costing și payroll calculation.","dirs":["/standalone/numeriqo/apps/people/api/src/events/consumers/"],"constraints":"idempotent processing; labor costing accurate; payroll integration; commit 'feat(hr-events): consume manufacturing'.","output":"Manufacturing labor integration"},

  {"step":732,"scope":"events-consume-terminals","context":"Manufacturing consumer ready (731); shop floor integration","task":"Subscriber `manufacturing.terminal.clock_in`, `manufacturing.terminal.clock_out` → time tracking automatic pentru shop floor workers cu validation și overtime calculation.","dirs":["/standalone/numeriqo/apps/people/api/src/events/consumers/"],"constraints":"terminal validation; overtime automatic; shop floor specific; commit 'feat(hr-events): consume terminals'.","output":"Shop floor time tracking integration"},

  {"step":733,"scope":"events-consume-accounting","context":"Terminal consumer ready (732); cost accounting","task":"Consumă evenimente Accounting: `accounting.period.closed` → finalize payroll costs, labor cost allocation, analytical accounting pentru departments și projects.","dirs":["/standalone/numeriqo/apps/people/api/src/events/consumers/"],"constraints":"cost allocation complete; analytical accounting; department costing; commit 'feat(hr-events): consume accounting'.","output":"Accounting cost integration"},

  {"step":734,"scope":"worker-reges-integration","context":"Workers fleet available; REGES requirements","task":"Integrează worker `reges` pentru REGES Online submission: collect employee data, format Revisal XML, validate schema, submit la Inspecția Muncii cu certificat digital și progress tracking.","dirs":["/standalone/numeriqo/apps/people/workers/reges/"],"constraints":"Revisal XML schema valid; certificate digital auth; SOAP Web Service; commit 'feat(hr-workers): REGES integration'.","output":"REGES Online submission"},

  {"step":735,"scope":"worker-report-kpi-hr","context":"REGES worker ready (734); HR KPIs","task":"Implementează `report.kpi` pentru HR KPIs: employee turnover, absenteeism rates, overtime statistics, payroll costs, headcount analytics cu dashboard integration.","dirs":["/standalone/numeriqo/apps/people/workers/report-kpi/"],"constraints":"HR KPIs accurate; real-time calculation; dashboard format; commit 'feat(hr-workers): HR KPIs'.","output":"HR KPIs real-time"},

  {"step":736,"scope":"worker-pdf-render-hr","context":"KPI worker operational (735); HR documents","task":"Integrează `pdf.render` pentru HR documents: employment contracts, payslips, performance reviews, certificates cu Romanian templates și legal compliance.","dirs":["/standalone/numeriqo/apps/people/workers/pdf-render/"],"constraints":"Romanian legal templates; contract compliance; payslip format legal; commit 'feat(hr-workers): PDF HR documents'.","output":"HR PDF documents Romanian"},

  {"step":737,"scope":"worker-email-notifications-hr","context":"PDF worker ready (736); HR communications","task":"Implementează `email.send` integration pentru HR notifications: payslip delivery, contract renewals, performance review reminders, leave approval notifications cu template system.","dirs":["/standalone/numeriqo/apps/people/workers/email-send/"],"constraints":"notification templates HR; payslip secure delivery; reminder automation; commit 'feat(hr-workers): HR notifications'.","output":"HR email notifications"},

  {"step":738,"scope":"worker-tax-calculation","context":"Email worker ready (737); tax integration","task":"Integrez `tax.vat` pentru social contributions și tax calculations: CAS calculation, CASS calculation, income tax calculation, meal vouchers tax treatment cu Romanian tax rules.","dirs":["/standalone/numeriqo/apps/people/workers/tax-calc/"],"constraints":"Romanian tax rules 2024; social contributions accurate; meal vouchers compliance; commit 'feat(hr-workers): Tax calculation RO'.","output":"Tax calculation Romanian compliant"},

  {"step":739,"scope":"auth-rbac-hr","context":"API controllers complete (725); HR security","task":"Implementează RBAC guards pentru HR: scopes `hr.*` (employee.read, payroll.process, performance.manage, personal.data.access) cu granular permissions și GDPR compliance.","dirs":["/standalone/numeriqo/apps/people/api/src/guards/"],"constraints":"granular HR permissions; GDPR compliance enforced; personal data restricted; commit 'feat(hr-auth): RBAC HR GDPR'.","output":"HR authorization GDPR compliant"},

  {"step":740,"scope":"auth-gdpr-compliance","context":"RBAC ready (739); data protection","task":"Middleware pentru GDPR compliance: personal data access logging, consent management, data retention policies, right to erasure implementation cu audit trail complet.","dirs":["/standalone/numeriqo/apps/people/api/src/middleware/gdpr/"],"constraints":"GDPR full compliance; consent tracking; data erasure; audit trail; commit 'feat(hr-auth): GDPR compliance complete'.","output":"GDPR compliance comprehensive"},

  {"step":741,"scope":"auth-data-encryption","context":"GDPR ready (740); data protection","task":"Implementează encryption pentru personal data: CNP encryption, salary encryption, personal details encryption cu key management și transparent decryption pentru authorized access.","dirs":["/standalone/numeriqo/apps/people/api/src/middleware/encryption/"],"constraints":"personal data encrypted; key management secure; transparent access; commit 'feat(hr-auth): Data encryption GDPR'.","output":"Personal data encryption"},

  {"step":742,"scope":"otel-tracing-hr","context":"Observability stack ready; HR tracing","task":"Activează OpenTelemetry în HR API: HTTP requests, database operations, Event Bus, Worker calls cu service.name=numeriqo/people-api și GDPR-compliant tracing.","dirs":["/standalone/numeriqo/apps/people/api/src/config/otel/"],"constraints":"traces end-to-end HR; GDPR compliant tracing; no PII în traces; commit 'feat(hr-otel): HR tracing GDPR'.","output":"HR traces în Tempo"},

  {"step":743,"scope":"prometheus-metrics-hr","context":"OTel active (742); HR metrics","task":"Expune Prometheus metrics pentru HR: HTTP standard + HR metrics (employees_total, payroll_runs_total, timesheets_submitted_total, reges_submissions_total).","dirs":["/standalone/numeriqo/apps/people/api/src/config/metrics/"],"constraints":"prefix numeriqo_hr_*; HR KPIs included; no PII în metrics; commit 'feat(hr-metrics): HR metrics'.","output":"HR metrics în Prometheus"},

  {"step":744,"scope":"logging-hr-structured","context":"Metrics ready (743); HR logging","task":"Configurează structured logging pentru HR operations: JSON format, correlation-id, GDPR compliance, PII masking, audit trail integration, retention policies.","dirs":["/standalone/numeriqo/apps/people/api/src/config/logging/"],"constraints":"PII masked completely; GDPR compliant; audit integration; retention legal; commit 'feat(hr-logging): HR logging GDPR'.","output":"HR logging GDPR compliant"},

  {"step":745,"scope":"frontend-scaffold-hr","context":"API complete cu observability (744)","task":"Bootstrap HR frontend: React 19 + Vite 5 Federation + MUI 6 + Tailwind 3 cu Module Federation remoteEntry pentru HR UI integration în Shell cu GDPR consent management.","dirs":["/standalone/numeriqo/apps/people/frontend/"],"constraints":"Federation config HR modules; GDPR consent UI; privacy by design; commit 'feat(hr-ui): frontend bootstrap GDPR'.","output":"HR UI skeleton GDPR"},

  {"step":746,"scope":"frontend-routing-hr","context":"Frontend bootstrap ready (745)","task":"Setup routing pentru HR pages: /people/employees, /payroll, /time-tracking, /benefits, /performance, /reports cu React Router, lazy loading, și GDPR access controls.","dirs":["/standalone/numeriqo/apps/people/frontend/src/routes/"],"constraints":"lazy loading HR pages; GDPR access controls; privacy routing; commit 'feat(hr-ui): routing HR GDPR'.","output":"HR routing GDPR compliant"},

  {"step":747,"scope":"frontend-data-layer-hr","context":"Routing ready (746)","task":"Configurează data layer pentru HR: TanStack Query pentru server state, Axios client cu JWT interceptors, GDPR-compliant error handling, PII protection în client state.","dirs":["/standalone/numeriqo/apps/people/frontend/src/api/"],"constraints":"GDPR compliant client; PII protection; error boundaries privacy; commit 'feat(hr-ui): data layer GDPR'.","output":"HR data layer GDPR"},

  {"step":748,"scope":"frontend-state-management-hr","context":"Data layer operational (747)","task":"Setup state management cu Zustand pentru HR: Employee state, Payroll state, Time state cu GDPR compliance, PII encryption în client storage, consent management.","dirs":["/standalone/numeriqo/apps/people/frontend/src/stores/"],"constraints":"state GDPR compliant; PII client encrypted; consent integrated; commit 'feat(hr-ui): state management GDPR'.","output":"HR state stores GDPR"},

  {"step":749,"scope":"frontend-employee-management","context":"State management ready (748)","task":"Implementează Employee Management pages: Employee List cu filtering, Employee Profile cu GDPR controls, Employee Editor cu consent, Search cu privacy restrictions.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/employee/"],"constraints":"GDPR controls integrated; consent management; privacy by design; commit 'feat(hr-ui): Employee management GDPR'.","output":"Employee management UI GDPR"},

  {"step":750,"scope":"frontend-payroll-interface","context":"Employee UI ready (749)","task":"Creează Payroll interface: Payroll Run dashboard, Payslip viewer cu security, Payroll reports cu access controls, Tax calculations cu Romanian specifics.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/payroll/"],"constraints":"payslip security strict; access controls granular; Romanian tax display; commit 'feat(hr-ui): Payroll interface secure'.","output":"Payroll interface secure"},

  {"step":751,"scope":"frontend-time-tracking","context":"Payroll UI ready (750)","task":"Implementează Time Tracking interface: Timesheet entry cu mobile support, Attendance dashboard, Overtime tracking, Manufacturing integration display cu real-time updates.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/time/"],"constraints":"mobile time entry optimized; Manufacturing integration UI; real-time updates; commit 'feat(hr-ui): Time tracking mobile'.","output":"Time tracking interface mobile"},

  {"step":752,"scope":"frontend-benefits-admin","context":"Time UI ready (751)","task":"Dezvolt Benefits Administration interface: Benefits enrollment cu guided flows, Medical insurance management, Meal vouchers tracking, Romanian benefits specifice.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/benefits/"],"constraints":"guided enrollment flows; Romanian benefits display; insurance integration; commit 'feat(hr-ui): Benefits admin RO'.","output":"Benefits administration interface"},

  {"step":753,"scope":"frontend-leave-management","context":"Benefits UI ready (752)","task":"Creează Leave Management interface: Leave request cu calendar integration, Approval workflows, Leave balance tracking, Romanian leave types cu legal compliance display.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/leave/"],"constraints":"calendar integration smooth; approval workflows clear; Romanian compliance display; commit 'feat(hr-ui): Leave management RO'.","output":"Leave management interface"},

  {"step":754,"scope":"frontend-performance","context":"Leave UI ready (753)","task":"Implementează Performance Management interface: Performance reviews cu structured forms, Objectives tracking, Competency assessment, Development planning cu career paths.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/performance/"],"constraints":"structured review forms; objective tracking visual; career path display; commit 'feat(hr-ui): Performance management'.","output":"Performance management interface"},

  {"step":755,"scope":"frontend-dashboards-hr","context":"Core pages complete (754)","task":"Implementează HR dashboards: Executive HR Dashboard cu KPIs, Real-time Workforce Analytics, Compliance Dashboard cu REGES status, Cost Analytics cu labor costs.","dirs":["/standalone/numeriqo/apps/people/frontend/src/pages/dashboard/"],"constraints":"real-time workforce data; executive HR KPIs; compliance status; commit 'feat(hr-ui): HR Dashboards executive'.","output":"HR analytics dashboards"},

  {"step":756,"scope":"frontend-mobile-responsive-hr","context":"Dashboards ready (755)","task":"Optimizează HR UI pentru mobile devices: responsive employee tables, touch-friendly time entry, offline capability pentru time tracking, PWA features HR.","dirs":["/standalone/numeriqo/apps/people/frontend/src/"],"constraints":"PWA HR ready; offline time tracking; responsive employee data; commit 'feat(hr-ui): mobile responsive HR'.","output":"HR mobile optimized"},

  {"step":757,"scope":"api-testing-unit-hr","context":"API services complete (719)","task":"Teste unit comprehensive pentru HR services: EmployeeService (95% coverage), PayrollService (95% coverage), TimeTrackingService (90% coverage), BenefitsService (85% coverage).","dirs":["/standalone/numeriqo/apps/people/api/tests/unit/"],"constraints":"coverage targets HR; mock dependencies; payroll calculation tests; commit 'test(hr-api): unit tests HR'.","output":"HR unit tests comprehensive"},

  {"step":758,"scope":"api-testing-integration-hr","context":"Unit tests ready (757)","task":"Teste integration pentru HR API: database operations cu GDPR, Event Bus integration, Worker communication, RLS verification, REGES integration testing.","dirs":["/standalone/numeriqo/apps/people/api/tests/integration/"],"constraints":"real database tests; GDPR validation; REGES integration verified; commit 'test(hr-api): integration tests HR'.","output":"HR integration tests"},

  {"step":759,"scope":"frontend-testing-hr","context":"Frontend complete (756)","task":"Teste frontend HR: Vitest unit tests pentru components, React Testing Library pentru pages, E2E tests cu Playwright pentru critical HR workflows cu GDPR compliance.","dirs":["/standalone/numeriqo/apps/people/frontend/tests/"],"constraints":"component tests 80%; E2E HR workflows; GDPR compliance testing; commit 'test(hr-ui): frontend tests HR'.","output":"HR frontend tested"},

  {"step":760,"scope":"api-testing-e2e-hr","context":"Frontend tests ready (759)","task":"E2E testing HR workflows: Hire Employee → Create Contract → Process Payroll → REGES Submission cu database verification, Event publishing verification, GDPR compliance validation.","dirs":["/standalone/numeriqo/apps/people/tests/e2e/"],"constraints":"complete HR workflows; GDPR validation E2E; REGES submission tested; commit 'test(hr-e2e): HR workflows complete'.","output":"HR E2E verified"},

  {"step":761,"scope":"performance-testing-hr","context":"E2E tests complete (760)","task":"Performance testing cu k6: Employee operations (p95 <500ms), Payroll calculation (1000 employees <30s), Time tracking entry (p95 <200ms), REGES submission (p95 <5s).","dirs":["/standalone/numeriqo/apps/people/tests/performance/"],"constraints":"SLA targets HR specific; payroll performance critical; REGES timing compliant; commit 'perf(hr): HR benchmarks'.","output":"HR performance verified"},

  {"step":762,"scope":"load-testing-hr","context":"Performance benchmarks ready (761)","task":"Load testing HR API: concurrent employee operations (50 users), simultaneous payroll processing (10 concurrent runs), time tracking high volume (500 entries/min), REGES concurrent submissions.","dirs":["/standalone/numeriqo/apps/people/tests/load/"],"constraints":"HR load realistic; payroll accuracy under load; REGES stability; commit 'perf(hr): load testing HR'.","output":"HR load tested"},

  {"step":763,"scope":"security-testing-hr","context":"Load tests complete (762)","task":"Security testing HR: GDPR compliance verification, personal data encryption, access control testing, PII protection validation, REGES security, audit trail security.","dirs":["/standalone/numeriqo/apps/people/tests/security/"],"constraints":"GDPR security critical; PII protection verified; audit security tested; commit 'security(hr): HR security verification'.","output":"HR security verified"},

  {"step":764,"scope":"contract-testing-events-hr","context":"Event system operational (733)","task":"Contract testing pentru HR events: publish/subscribe contracts, event schema validation, consumer compatibility, GDPR-compliant event versioning support.","dirs":["/standalone/numeriqo/apps/people/tests/contracts/"],"constraints":"Pact contracts HR events; schema validation; GDPR compliance; commit 'test(hr-contracts): event contracts HR'.","output":"HR event contracts"},

  {"step":765,"scope":"contract-testing-workers-hr","context":"Workers integration complete (738)","task":"Contract tests pentru Worker integration: REGES worker contracts, KPI reporting contracts, PDF generation contracts, tax calculation contracts cu Romanian specifics.","dirs":["/standalone/numeriqo/apps/people/tests/contracts/workers/"],"constraints":"worker API contract verification; Romanian compliance; REGES contracts detailed; commit 'test(hr-contracts): worker contracts'.","output":"HR worker contracts"},

  {"step":766,"scope":"compliance-testing-reges","context":"Worker contracts ready (765)","task":"REGES compliance testing: Revisal XML schema validation, employee data accuracy, submission process verification, Inspecția Muncii integration, certificate digital authentication.","dirs":["/standalone/numeriqo/apps/people/tests/compliance/"],"constraints":"REGES requirements complete; Revisal schema verified; certificate auth tested; commit 'test(compliance): REGES verification'.","output":"REGES compliance verified"},

  {"step":767,"scope":"gdpr-compliance-testing","context":"REGES testing ready (766)","task":"GDPR compliance comprehensive testing: personal data protection, consent management, right to erasure, data portability, breach notification, retention policies testing.","dirs":["/standalone/numeriqo/apps/people/tests/compliance/gdpr/"],"constraints":"GDPR full compliance tested; all rights verified; breach procedures tested; commit 'test(compliance): GDPR comprehensive'.","output":"GDPR compliance comprehensive"},

  {"step":768,"scope":"deployment-helm-hr","context":"Compliance verified (767)","task":"Creează Helm chart HR: API deployment, frontend deployment, ingress configuration, services cu HR specific configuration, GDPR security requirements.","dirs":["/standalone/numeriqo/infra/helm/people/"],"constraints":"multi-environment support; GDPR security; PII protection; commit 'feat(helm): HR base chart GDPR'.","output":"HR Helm chart"},

  {"step":769,"scope":"deployment-helm-secrets-hr","context":"Base chart ready (768)","task":"ExternalSecrets pentru HR: database credentials, Event Bus config, REGES certificates, Worker credentials, observability endpoints cu vault integration și GDPR compliance.","dirs":["/infra/k8s/externalsecrets/people/"],"constraints":"no secrets în repo; GDPR compliant secrets; certificate management; commit 'feat(helm): HR secrets GDPR'.","output":"HR secrets managed GDPR"},

  {"step":770,"scope":"deployment-helm-monitoring-hr","context":"Secrets ready (769)","task":"Monitoring configuration Helm pentru HR: ServiceMonitor pentru Prometheus, log aggregation config GDPR-compliant, alert rules HR specific, dashboard provisioning.","dirs":["/standalone/numeriqo/infra/helm/people/monitoring/"],"constraints":"HR specific alerts; GDPR monitoring compliance; PII protection monitoring; commit 'feat(helm): HR monitoring GDPR'.","output":"HR monitoring config"},

  {"step":771,"scope":"deployment-argocd-hr","context":"Helm complete cu monitoring (770)","task":"ArgoCD Application definition pentru HR: namespace dedicat, sync policies conservative, health checks HR specific, rollback configuration cu GDPR data protection.","dirs":["/infra/k8s/argocd/apps/people/"],"constraints":"health checks HR endpoints; conservative sync; GDPR data protection; commit 'feat(argocd): HR app GDPR'.","output":"HR ArgoCD managed"},

  {"step":772,"scope":"deployment-ci-pipeline-hr","context":"ArgoCD ready (771)","task":"CI/CD pipeline HR: GitHub Actions pentru build/test/deploy, Trivy security scans cu thresholds GDPR (CRITICAL=0, HIGH≤1, MEDIUM≤5), SBOM generation, Cosign signing cu GDPR compliance.","dirs":["/.github/workflows/people-ci.yml"],"constraints":"security thresholds GDPR critical; SBOM HR specific; GDPR compliance CI; commit 'ci(hr): complete pipeline GDPR'.","output":"HR CI/CD GDPR-grade"},

  {"step":773,"scope":"observability-grafana-hr","context":"Monitoring config ready (770)","task":"Grafana dashboards HR: Executive HR Dashboard, Workforce Analytics, GDPR Compliance Monitoring cu consent tracking, REGES Status, Cost Analytics cu labor cost breakdown.","dirs":["/infra/grafana/provisioning/dashboards/people/"],"constraints":"executive HR KPIs; GDPR compliance tracking; REGES status monitoring; commit 'feat(obs): HR dashboards executive'.","output":"HR Grafana dashboards"},

  {"step":774,"scope":"observability-alerting-hr","context":"Dashboards ready (773)","task":"Alert rules HR: Payroll processing delays, REGES submission failures, GDPR compliance violations, High absenteeism, Contract expiration alerts cu escalation policies HR.","dirs":["/infra/prometheus/rules/people/"],"constraints":"HR business impact alerts; GDPR violation alerts; REGES compliance alerts; commit 'feat(obs): HR alerting comprehensive'.","output":"HR alerting comprehensive"},

  {"step":775,"scope":"documentation-api-hr","context":"API complete (760)","task":"Swagger documentation HR API: endpoints documentation complete, HR DTO schemas, example requests Romanian, authentication requirements cu GDPR compliance notes.","dirs":["/standalone/numeriqo/apps/people/api/docs/"],"constraints":"complete HR API documentation; Romanian examples; GDPR compliance documented; commit 'docs(hr-api): Swagger complete GDPR'.","output":"HR API docs complete"},

  {"step":776,"scope":"documentation-user-manual-hr","context":"UI complete (756)","task":"User manual HR: Employee management guide, Payroll processing Romanian, Time tracking procedures, Benefits enrollment, Leave management, Performance reviews cu screenshots și workflows.","dirs":["/docs/people/user-manual/"],"constraints":"comprehensive HR guide; Romanian procedures; GDPR compliance guide; commit 'docs(hr): user manual complete'.","output":"HR user documentation"},

  {"step":777,"scope":"documentation-compliance-hr","context":"GDPR compliance verified (767)","task":"Compliance documentation HR: GDPR implementation guide, REGES procedures, Romanian labor law compliance, Data protection procedures, Audit trail documentation.","dirs":["/docs/people/compliance/"],"constraints":"GDPR requirements complete; REGES procedures detailed; labor law compliance; commit 'docs(compliance): HR Romanian GDPR'.","output":"HR compliance documentation"},

  {"step":778,"scope":"documentation-technical-hr","context":"System complete (774)","task":"Technical documentation HR: architecture overview, integration patterns Manufacturing/Accounting, event schemas HR, worker contracts REGES, deployment guide GDPR security.","dirs":["/docs/people/technical/"],"constraints":"technical depth HR; integration examples; GDPR architecture; commit 'docs(hr): technical documentation'.","output":"HR technical docs"},

  {"step":779,"scope":"training-materials-hr","context":"Documentation complete (778)","task":"Training materials HR: video tutorials payroll Romanian, interactive guides GDPR compliance, best practices HR, troubleshooting guide, FAQ pentru HR users și managers.","dirs":["/docs/people/training/"],"constraints":"multimedia training HR; practical examples Romanian; GDPR training comprehensive; commit 'docs(hr): training materials'.","output":"HR training ready"},

  {"step":780,"scope":"demo-data-seed-hr","context":"System functional (779)","task":"Demo data HR: sample employees anonymized, contracts templates Romanian, payroll test data, timesheets examples, benefits enrollments pentru demonstration cu GDPR anonymization.","dirs":["/core/scripts/seed/people/"],"constraints":"GDPR anonymized data; realistic Romanian examples; no real PII; commit 'feat(seed): HR demo data anonymized'.","output":"HR demo data GDPR"},

  {"step":781,"scope":"migration-utilities-hr","context":"Demo data ready (780)","task":"Migration utilities HR: legacy HR system import, employee data transformation cu GDPR compliance, payroll data conversion, validation utilities pentru customer onboarding.","dirs":["/core/scripts/migration/people/"],"constraints":"GDPR compliant migration; data transformation secure; validation comprehensive; commit 'feat(migration): HR utilities GDPR'.","output":"HR migration tools GDPR"},

  {"step":782,"scope":"backup-recovery-hr","context":"Migration tools ready (781)","task":"Backup și recovery procedures HR: automated HR backups cu encryption, GDPR-compliant backup retention, point-in-time recovery, personal data protection în backups.","dirs":["/core/scripts/backup/people/"],"constraints":"GDPR backup compliance; personal data encrypted; recovery tested; commit 'feat(backup): HR procedures GDPR'.","output":"HR backup/recovery GDPR"},

  {"step":783,"scope":"monitoring-synthetic-hr","context":"Backup procedures ready (782)","task":"Synthetic monitoring HR: health check endpoints, critical workflow monitoring HR, payroll calculation validation, REGES integration availability tracking, GDPR compliance monitoring.","dirs":["/core/monitoring/synthetic/people/"],"constraints":"critical HR path monitoring; payroll validation; REGES status tracking; commit 'feat(monitoring): HR synthetic'.","output":"HR synthetic monitoring"},

  {"step":784,"scope":"capacity-planning-hr","context":"Monitoring complete (783)","task":"Capacity planning HR: employee growth analysis, payroll processing scalability, time tracking volume projections, REGES submission capacity cu optimization recommendations HR.","dirs":["/docs/people/capacity/"],"constraints":"HR scalability analysis; payroll performance optimization; REGES capacity planning; commit 'docs(capacity): HR planning'.","output":"HR capacity planning"},

  {"step":785,"scope":"compliance-validation-final-hr","context":"Capacity planning ready (784)","task":"Final compliance validation HR: GDPR completeness verification, REGES requirements verification, Romanian labor law compliance, audit trail completeness, data protection effectiveness.","dirs":["/core/compliance/people/"],"constraints":"GDPR complete; REGES compliance verified; labor law compliance; commit 'feat(compliance): HR final validation'.","output":"HR compliance final"},

  {"step":786,"scope":"integration-testing-suite-hr","context":"Compliance validated (785)","task":"Integration test suite HR: full HR system integration, cross-module compatibility cu Manufacturing/Accounting, data flow verification, GDPR compliance în integration, audit trail integrity.","dirs":["/tests/integration/people/"],"constraints":"complete HR integration; cross-module testing; GDPR integration compliance; commit 'test(integration): HR suite complete'.","output":"HR integration test suite"},

  {"step":787,"scope":"release-preparation-hr","context":"Integration tests ready (786)","task":"Release preparation HR: version tagging, release notes HR, deployment checklist GDPR, rollback procedures cu personal data protection, stakeholder communication.","dirs":["/releases/people/F3/"],"constraints":"comprehensive HR release; GDPR rollback procedures; stakeholder communication; commit 'release(hr): F3 preparation complete'.","output":"HR release ready"},

  {"step":788,"scope":"go-live-checklist-hr","context":"Release prepared (787)","task":"Go-live checklist HR: production readiness GDPR verification, monitoring setup confirmation, support procedures HR, escalation paths, success criteria HR definition.","dirs":["/ops/people/go-live/"],"constraints":"GDPR production readiness; support procedures ready; success criteria clear; commit 'ops(hr): go-live checklist GDPR'.","output":"HR go-live ready"},

  {"step":789,"scope":"post-deployment-monitoring-hr","context":"Go-live ready (788)","task":"Post-deployment monitoring HR: success metrics tracking HR, user adoption monitoring, performance baseline HR, issue tracking setup cu GDPR priority classification.","dirs":["/ops/people/post-deploy/"],"constraints":"HR success metrics; adoption tracking; performance baseline; commit 'ops(hr): post-deploy monitoring'.","output":"HR post-deploy monitoring"},

  {"step":790,"scope":"continuous-improvement-hr","context":"Post-deploy monitoring active (789)","task":"Continuous improvement framework HR: feedback collection HR users, performance optimization, feature enhancement pipeline, user experience improvements, REGES updates tracking.","dirs":["/ops/people/improvement/"],"constraints":"improvement framework HR; user feedback integrated; REGES updates tracked; commit 'ops(hr): continuous improvement'.","output":"HR continuous improvement"},

  {"step":791,"scope":"regulatory-updates-hr","context":"Improvement framework ready (790)","task":"Framework pentru regulatory updates HR: Romanian labor law changes monitoring, REGES updates, GDPR regulation changes, automatic compliance verification, update deployment procedures.","dirs":["/ops/people/regulatory/"],"constraints":"regulatory monitoring automated; compliance verification; update procedures; commit 'ops(regulatory): HR updates framework'.","output":"HR regulatory updates framework"},

  {"step":792,"scope":"gdpr-ongoing-compliance","context":"Regulatory framework ready (791)","task":"GDPR ongoing compliance framework: privacy impact assessments, data protection audits, consent management updates, breach response procedures, regular compliance reviews.","dirs":["/ops/people/gdpr/"],"constraints":"GDPR ongoing compliance; privacy audits regular; breach procedures tested; commit 'ops(gdpr): ongoing compliance'.","output":"GDPR ongoing compliance"},

  {"step":793,"scope":"data-retention-hr","context":"GDPR framework ready (792)","task":"Data retention HR: employee data retention policies, payroll retention legal, personal data archival, secure deletion procedures conform Romanian labor law și GDPR.","dirs":["/ops/people/retention/"],"constraints":"retention policies legal; secure archival; deletion procedures compliant; commit 'ops(retention): HR compliance'.","output":"HR data retention compliant"},

  {"step":794,"scope":"disaster-recovery-hr","context":"Retention compliance ready (793)","task":"Disaster recovery specific pentru HR data: employee backup verification, payroll continuity, GDPR compliance în disaster scenarios, personal data protection în recovery.","dirs":["/ops/people/disaster-recovery/"],"constraints":"HR backup verified; payroll continuity assured; GDPR disaster compliance; commit 'ops(dr): HR disaster recovery'.","output":"HR disaster recovery ready"},

  {"step":795,"scope":"user-acceptance-testing-hr","context":"Disaster recovery ready (794)","task":"User Acceptance Testing cu HR users: real scenarios testing HR, Romanian payroll workflows, GDPR compliance verification, REGES submission testing, user feedback collection.","dirs":["/tests/uat/people/"],"constraints":"real HR user scenarios; Romanian workflows; GDPR verification; feedback comprehensive; commit 'test(uat): HR user acceptance'.","output":"HR UAT complete"},

  {"step":796,"scope":"production-cutover-plan-hr","context":"UAT complete (795)","task":"Production cutover plan pentru HR: employee data migration final cu GDPR compliance, payroll system switch procedures, rollback plan HR, user communication, success validation criteria.","dirs":["/ops/people/cutover/"],"constraints":"GDPR migration plan; payroll continuity; rollback tested; communication clear; commit 'ops(cutover): HR production plan'.","output":"HR production cutover ready"},

  {"step":797,"scope":"payroll-calendar-setup","context":"Production cutover ready (796)","task":"Setup payroll calendar Romanian: monthly payroll schedule, tax deadlines calendar, social contributions deadlines, REGES submission schedule, compliance calendar integration.","dirs":["/ops/people/calendar/"],"constraints":"Romanian payroll calendar; tax deadlines accurate; REGES schedule compliant; commit 'ops(calendar): payroll schedule RO'.","output":"Payroll calendar Romanian ready"},

  {"step":798,"scope":"employee-onboarding-process","context":"Payroll calendar ready (797)","task":"Employee onboarding process automation: new hire workflow, contract generation automatic, REGES registration automation, benefits enrollment guided, initial training assignment.","dirs":["/ops/people/onboarding/"],"constraints":"onboarding workflow complete; REGES automation; benefits guided; training automated; commit 'ops(onboarding): employee automation'.","output":"Employee onboarding automated"},

  {"step":799,"scope":"hr-success-validation","context":"Onboarding process ready (798)","task":"Final HR success validation: all Romanian labor law requirements met, GDPR compliance complete, REGES integration verified, payroll accuracy confirmed, user satisfaction validated.","dirs":["/ops/people/validation/"],"constraints":"labor law compliance complete; GDPR verified; REGES working; payroll accurate; users satisfied; commit 'ops(validation): HR success confirmed'.","output":"HR system success validated"}
]
```

## Success Criteria

**✅ F3 People & Payroll Objectives met:**

1. **Motor salarizare RO** – Complete Romanian payroll system cu social contributions și income tax
2. **Employee Management** – Full employee lifecycle cu GDPR compliance
3. **REGES Integration** – Automatic submission la Inspecția Muncii via Revisal online
4. **Time Tracking** – Integration cu Manufacturing labor tracking și overtime calculation
5. **Benefits Administration** – Romanian benefits (meal vouchers, medical insurance, pension)
6. **Leave Management** – Romanian leave types cu legal compliance (CO, CM, maternity)
7. **Performance Management** – Review workflows cu objectives și development planning
8. **Accounting Integration** – Cost accounting pentru salarii și analytical accounting
9. **GDPR Compliance** – Complete data protection cu consent management și encryption
10. **Romanian Compliance** – Labor law compliance cu Codul Muncii RO
11. **Mobile Support** – PWA pentru time tracking și employee self-service
12. **Analytics** – Real-time HR KPIs și workforce analytics

**KPIs F3:**
- Payroll processing: 1000 employees în <30s
- REGES submission: <5s pentru standard submission
- Time tracking entry: <200ms pentru mobile entry
- Employee operations: <500ms pentru standard operations
- GDPR compliance: 100% personal data encrypted
- System availability: >99.9% pentru payroll operations
- User satisfaction: >85% pentru mobile time tracking

**Deliverables:**
- 100 JSON implementation steps (700-799)
- Complete HR Management System Romanian
- Romanian payroll engine cu social contributions
- REGES integration pentru Revisal online
- Manufacturing labor integration pentru costing
- GDPR-compliant personal data management
- Mobile-first time tracking și self-service
- Enterprise security cu RBAC și audit trail
