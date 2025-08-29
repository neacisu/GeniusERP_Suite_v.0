# Master Roadmap Index - GeniusERP Suite v0.1

**Hierarchical Numbering System: F-P-M-SSS**
- **F** = Phase number (0–6)
- **P** = Sub-phase/module index (01, 02, 03...)  
- **M** = Sub-module/feature group (optional, two digits)
- **SSS** = Sequential step number (three digits, 000-999)

## Execution Order & Module Prefixes

### Phase F0 - Foundation & Infrastructure
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Foundation | F0-01 | F0-01-000 → F0-01-125 | `3_roadmap_f_0_foundation_infrastructure.md` | ✅ **COMPLETE** |

### Phase F1 - Core Platform  
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Shell Gateway | F1-01 | F1-01-000 → F1-01-040 | `5_roadmap_f_1_1_shell_gateway.md` |
| 2 | Admin Core | F1-02 | F1-02-000 → F1-02-050 | `6_roadmap_f_1_2_admin_core.md` |
| 3 | Base Workers | F1-03 | F1-03-000 → F1-03-070 | `7_roadmap_f_1_3_base_workers.md` |

### Phase F2 - Commercial Core Apps
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Vettify CRM | F2-01 | F2-01-000 → F2-01-099 | `9_roadmap_f_2_1_vettify.md` |
| 2 | Mercantiq Sales | F2-02 | F2-02-000 → F2-02-099 | `10_roadmap_f_2_2_mercantiq_sales_billing.md` |
| 3 | Mercantiq Procurement | F2-03 | F2-03-000 → F2-03-099 | `11_roadmap_f_2_3_mercantiq_procurement.md` |
| 4 | iWMS v3 | F2-04 | F2-04-000 → F2-04-099 | `12_roadmap_f_2_4_iwms_v3.md` |

### Phase F3 - Operational & Financial Backbone  
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Manufacturing | F3-01 | F3-01-000 → F3-01-199 | `14_roadmap_f_3_1_numeriqo_manufacturing.md` |
| 2 | Accounting | F3-02 | F3-02-000 → F3-02-099 | `15_roadmap_f_3_2_numeriqo_accounting.md` |
| 3 | People & Payroll | F3-03 | F3-03-000 → F3-03-099 | `16_roadmap_f_3_3_numeriqo_people_payroll.md` |

### Phase F4 - Collaboration & Automation
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Collaboration Hub | F4-01 | F4-01-000 → F4-01-099 | `18_roadmap_f_4_1_triggerra_collaboration_hub.md` |
| 2 | Automation Studio | F4-02 | F4-02-000 → F4-02-099 | `19_roadmap_f_4_2_triggerra_automation_studio.md` |

### Phase F5 - Knowledge & Analytics
| Order | Module | Prefix | Range | File |
|-------|--------|--------|-------|------|
| 1 | Archify DMS | F5-01 | F5-01-000 → F5-01-079 | `21_roadmap_f_5_1_archify_dms.md` |
| 2 | Cerniq BI | F5-02 | F5-02-000 → F5-02-099 | `22_roadmap_f_5_2_cerniq_cognitive_bi.md` |

## Benefits of Hierarchical System

✅ **Guaranteed Uniqueness:** Each module owns its 000-999 sequence  
✅ **Scalable Growth:** Add modules without renumbering existing ones  
✅ **Clear Ownership:** Step ID instantly shows Phase + Module  
✅ **No More Fractions:** F1-03-045a instead of 274.5  
✅ **Preserved Chronology:** Master index maintains execution order  
✅ **Future-Proof:** System scales to 1000 steps per module  

## Migration Path

1. **Phase 1:** Convert F1 modules as proof-of-concept
2. **Phase 2:** Update cross-references and context dependencies  
3. **Phase 3:** Extend to F2-F6 systematically
4. **Phase 4:** Remove old flat numbering completely

## Cross-Reference Format

When referencing steps from other phases:
- **Internal:** "step F1-03-025"
- **Cross-phase:** "F0-01-110 Foundation infrastructure"  
- **Context:** "après F1-02-030 Admin RBAC setup"

This eliminates ambiguity and preserves traceability across the entire suite.
