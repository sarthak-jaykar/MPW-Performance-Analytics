# Business Case & Project Charter

## Project Overview

| Attribute | Details |
|---|---|
| **Project** | Manufacturing, Procurement & Warehousing (MPW) Performance Analytics |
| **Organization** | Apex Electronics Manufacturing Pvt. Ltd. |
| **Domain** | Electronics Manufacturing / Operations / Supply Chain |
| **Reporting Period** | FY2025 |
| **Primary Tool** | Power BI |
| **Analytical Support** | Python / Pandas |

---

## 1. Executive Context

Apex Electronics is a fictional mid-sized electronics manufacturer operating one assembly plant, two inbound warehouses and three SMT production lines.

During FY2025, the plant did not achieve its planned production volume:

| Measure | FY2025 Result |
|---|---:|
| Planned Output | 1,600,000 units |
| Good Output | 1,436,406 units |
| Production Shortfall | 163,594 units |
| Plan Attainment | 89.78% |
| Downtime | 1,688.0 hours |

The initial management assumption was that the production gap was primarily a shopfloor execution problem. The project tests that assumption by examining upstream procurement and inbound warehouse performance alongside production and quality indicators.

---

## 2. Business Problem

Management needs to understand **why planned output is not being converted into good finished production** and which operational constraints should receive priority.

The analysis therefore follows the operational chain:

**Supplier Delivery → Warehouse Intake → Material Availability → Production Execution → Quality Yield**

The objective is to identify the most material operational constraints and translate them into practical management actions.

---

## 3. Project Objectives

1. Measure production performance against plan.
2. Identify lines and products contributing most to production shortfall.
3. Quantify downtime and its major causes.
4. Evaluate supplier delivery reliability and lead-time variance.
5. Assess inbound warehouse processing performance.
6. Identify material-starvation exposure within production runs.
7. Assess quality losses through yield and rejection metrics.
8. Prioritize operational interventions based on evidence.

---

## 4. Key Business Questions

### Manufacturing

- Is the plant meeting its planned output?
- Which production lines contribute most to the shortfall?
- Which products have weaker plan attainment?
- How much scheduled runtime is being lost to downtime?

### Procurement

- Which suppliers deliver late most frequently?
- Which suppliers have the largest delivery variance?
- Which critical materials are exposed to supplier risk?

### Warehousing

- How long does inbound material take to become available after receipt?
- Which warehouse shows greater processing pressure?
- How frequently does inbound processing exceed the operating benchmark?

### Cross-Functional Operations

- How significant is material starvation as a production constraint?
- Which combination of supplier, warehouse, production and quality issues should management address first?

---

## 5. Operational Scope

### Manufacturing

- 1 assembly plant
- 3 SMT production lines
- 20 finished products
- Production output, runtime, downtime and quality performance

### Procurement & Inbound

- 12 suppliers
- 40 raw materials
- Purchase-order delivery performance
- Contracted vs. actual lead time
- Delivery variance

### Warehousing

- `WH-01` — Central Logistics Hub
- `WH-02` — Plant Inbound Depot
- Dock-to-stock processing performance

### Out of Scope

- Financial accounting
- Sales/customer analytics
- HR analytics
- Transportation optimization
- Full demand forecasting
- Advanced production scheduling optimization
- Full ERP implementation analysis

---

## 6. Analytical Approach

The project follows a business-first workflow:

**Business Problem → Data Design → Data Generation → Validation → Python EDA → Power BI Model → DAX → Dashboard → Insights → Recommendations**

The dataset is intentionally compact. The purpose is to support a strong operational dashboard and demonstrate analytical reasoning rather than reproduce a complete manufacturing ERP system.

---

## 7. Expected Management Outcome

The dashboard should allow management to move from:

**What happened? → Where did it happen? → What operational factor is associated with the gap? → What should management prioritize?**

The final recommendations focus on four areas:

1. Supplier reliability and critical-material resilience
2. Production-line reliability, particularly Line 2
3. Inbound warehouse processing performance
4. Quality improvement for high-rejection products
