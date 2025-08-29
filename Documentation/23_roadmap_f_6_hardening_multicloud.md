# Roadmap F6 · Hardening & Multi-Cloud

> **Scop:** să implementăm hardening-ul de securitate, disaster recovery multi-cloud și suita mobile pentru finalizarea platformei GeniusERP la enterprise-grade.

> **Timeline:** Q4 2026 (4 SW total)

---

## Gate F5 → F6

**Pre-condiții obligatorii pentru începerea F6:**
- **F5 Knowledge & Analytics completă:** Archify DMS + Cerniq BI operaționale
- **Entire Suite Operational:** Toate modulele F0-F5 sunt stabile în production
- **Performance Baseline:** SLO-uri stabilite și respectate pe toate modulele
- **Security Baseline:** Security audits interne trecute cu succes

---

## F6 Deliverables Overview

| Componentă | Durată | Obiectiv | Dependințe |
|------------|--------|----------|-------------|
| **Multi-cloud DR** | 2 SW | AKS ↔ EKS pilot, RTO 15 min | All core modules |
| **ISO 27001 Audit** | 1 SW | External audit stage 2 certification | DR ready |
| **Mobile Suite** | 1 SW | React Native offline parity | F2-4 iWMS |

---

## Architecture Overview

**Multi-Cloud DR:**
- Cross-cloud replication AKS ↔ EKS
- RTO (Recovery Time Objective): 15 minutes
- RPO (Recovery Point Objective): 5 minutes
- Automated failover testing

**ISO 27001 Certification:**
- External audit preparation
- ISMS (Information Security Management System) documentation
- Compliance verification pentru toate modulele
- Risk assessment și mitigation plans

**Mobile React Native Suite:**
- Offline-first architecture
- Key workflows mobile-optimized
- Data synchronization cu suite
- Focus pe iWMS mobile, Mercantiq mobile

---

## Gate F6 → Production Ready

**Criteriile de trecere:**
- Successful DR drill ≤ 15 min, no data loss
- ISO 27001 certificate obtained
- Mobile suite deployed cu offline capabilities
- Performance benchmarks met pe toate modulele
- Security penetration testing passed

---

## Future Roadmaps (F7)

După F6, platforma intră în **Continuous Improvement** cu:
- AI Config Advisor
- AI Vision GA
- Edge IoT Gateway GA  
- GDPR Portal GA
- Marketplace template-uri Automation Studio

> F6 marchează finalizarea implementation roadmap-ului principal al GeniusERP Suite v1.0.
