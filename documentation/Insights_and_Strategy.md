# Insights & Management Strategy

## Executive Interpretation

FY2025 production finished at **89.78% plan attainment**, leaving a shortfall of **163,594 good units** against the annual plan.

The dashboard indicates that the shortfall is not explained by a single issue. The strongest operational signals come from **material starvation, supplier reliability, Line 2 downtime, inbound warehouse latency and quality losses**.

The findings below use a **Finding → Evidence → Business Impact → Action** structure.

---

## Finding 1 — Material Starvation Is a Major Production Constraint

### Finding

Material availability is a significant contributor to production downtime and should be treated as an upstream operational constraint rather than only a shopfloor scheduling issue.

### Evidence

Material-shortage downtime accounts for **886.2 hours across 211 events**, representing approximately **52.5% of the 1,688.0 recorded downtime hours**.

### Business Impact

When required components are unavailable, scheduled production capacity cannot be converted into finished output. This increases production shortfall and creates avoidable schedule disruption.

### Recommended Action

Introduce a material-constrained production-release process in which critical component availability is confirmed before production orders are released to the line.

---

## Finding 2 — Supplier Reliability Risk Is Concentrated in Key Semiconductor Vendors

### Finding

Supplier delivery performance is uneven, with two key semiconductor suppliers showing materially weaker on-time performance than the wider supplier base.

### Evidence

- **Shenzhen Core Tech (`SUP-04`)** — 34.88% on-time delivery
- **Apex Micro Devices (`SUP-01`)** — 38.20% on-time delivery
- Average delivery variance was approximately **+3.83 days** and **+3.46 days**, respectively.

### Business Impact

Poor delivery reliability increases the probability that critical components will be unavailable when production requires them, increasing exposure to material-starvation events.

### Recommended Action

Prioritize these suppliers for supplier-performance reviews, recovery plans and qualified secondary sourcing for critical components. Revisit safety-stock policy for high-criticality materials based on actual supplier reliability.

---

## Finding 3 — Line 2 Is the Main Internal Production Bottleneck

### Finding

Line 2 combines weak plan attainment with substantial equipment-breakdown downtime, making it the most important internal production constraint.

### Evidence

- Line 2 production shortfall: **77,847 units**
- Share of plant shortfall: approximately **47.6%**
- Line 2 plan attainment: **84.71%**
- Equipment-breakdown downtime: **436.1 hours**

### Business Impact

Persistent reliability problems on Line 2 reduce available production capacity and increase the risk of missed output, particularly for products allocated to the line.

### Recommended Action

Prioritize preventive-maintenance review, equipment reliability analysis and feeder/SMT maintenance on Line 2. Track breakdown hours and plan attainment as the primary recovery measures.

---

## Finding 4 — WH-02 Shows Deteriorating Inbound Processing Performance

### Finding

The Plant Inbound Depot (`WH-02`) shows increasing dock-to-stock cycle time during the second half of the year.

### Evidence

- WH-01 remained around **1.56–1.59 days**.
- WH-02 increased from approximately **2.15 days in H1** to **2.82 days in H2**.
- Peak observed processing time reached approximately **5.4 days**.

### Business Impact

Inbound material that has physically arrived but has not completed receiving and putaway is not immediately available for operational use. This can amplify the effect of supplier delays.

### Recommended Action

Introduce priority receiving lanes for critical materials, improve pre-arrival information such as advance shipping notices, and review staffing/capacity during high-volume inbound periods.

---

## Finding 5 — Quality Losses Are Concentrated in More Complex Products

### Finding

Higher-complexity assemblies show greater rejection exposure than lower-complexity products.

### Evidence

High-complexity assemblies show rejection rates in the approximate **6%–10% range**, compared with the overall plant rejection rate of **3.46%**.

### Business Impact

Higher scrap reduces good output even when total production volume is maintained, and the cost impact is potentially greater for products containing higher-value electronic components.

### Recommended Action

Prioritize root-cause quality reviews for the highest-rejection products and strengthen process controls around the production steps associated with those assemblies.

---

## Prioritized Management Action Plan

| Priority | Domain | Initiative | Target Metric |
|---|---|---|---|
| **P1** | Procurement | Dual-source critical components and review safety-stock policy | Supplier OTD > 85% |
| **P2** | Manufacturing | Reliability and preventive-maintenance program for Line 2 | Line 2 attainment ≥ 92% |
| **P3** | Warehousing | Fast-track receiving and putaway for critical materials at WH-02 | WH-02 cycle time < 1.8 days |
| **P4** | Quality | Root-cause improvement program for high-scrap products | Plant scrap < 2.0% |

---

## Management Takeaway

The dashboard suggests that improving production output requires action **upstream as well as on the shopfloor**.

The highest-priority sequence is:

**Improve supplier reliability → protect critical-material availability → reduce Line 2 downtime → improve inbound processing → reduce high-complexity scrap.**

This provides management with a practical operational roadmap rather than a dashboard that only reports historical KPIs.
