# DAX Measures Reference Guide

**Project:** Manufacturing, Procurement & Warehousing (MPW) Performance Analytics  
**Model:** Compact two-fact star schema  
**Measure Container:** `_Measures`

This document catalogs the primary DAX measures used in the Power BI report. The measures are grouped by business purpose rather than by page.

---

## 1. Manufacturing & Output

### Total Planned Qty

```dax
Total Planned Qty =
SUM(Fact_ProductionRun[PlannedQty])
```

**Purpose:** Total scheduled production quantity.

**Format:** Whole number

### Total Produced Qty

```dax
Total Produced Qty =
SUM(Fact_ProductionRun[ProducedQty])
```

**Purpose:** Total units produced before quality rejection.

**Format:** Whole number

### Total Good Qty

```dax
Total Good Qty =
SUM(Fact_ProductionRun[GoodQty])
```

**Purpose:** Total accepted finished units.

**Format:** Whole number

### Total Rejected Qty

```dax
Total Rejected Qty =
SUM(Fact_ProductionRun[RejectedQty])
```

**Purpose:** Total rejected/scrapped units.

**Format:** Whole number

### Production Shortfall

```dax
Production Shortfall =
[Total Planned Qty] - [Total Good Qty]
```

**Purpose:** Gap between planned production and good output.

**Format:** Whole number

### Plan Attainment %

```dax
Plan Attainment % =
DIVIDE([Total Good Qty], [Total Planned Qty], 0)
```

**Purpose:** Percentage of planned output delivered as good production.

**Format:** Percentage, 1 decimal place

---

## 2. Quality

### Yield %

```dax
Yield % =
DIVIDE([Total Good Qty], [Total Produced Qty], 0)
```

**Purpose:** Percentage of produced units accepted as good.

**Format:** Percentage, 1 decimal place

### Rejection Rate %

```dax
Rejection Rate % =
DIVIDE([Total Rejected Qty], [Total Produced Qty], 0)
```

**Purpose:** Share of production rejected during quality inspection.

**Format:** Percentage, 1 decimal place

### Scrap Impact Units

```dax
Scrap Impact Units =
SUM(Fact_ProductionRun[RejectedQty])
```

**Purpose:** Unit volume lost to rejection.

**Format:** Whole number

---

## 3. Capacity & Downtime

### Total Planned Run Hours

```dax
Total Planned Run Hours =
SUM(Fact_ProductionRun[PlannedRunHours])
```

**Purpose:** Scheduled production runtime.

**Format:** Decimal, 1 decimal place

### Total Actual Run Hours

```dax
Total Actual Run Hours =
SUM(Fact_ProductionRun[ActualRunHours])
```

**Purpose:** Actual production runtime.

**Format:** Decimal, 1 decimal place

### Total Downtime Hours

```dax
Total Downtime Hours =
SUM(Fact_ProductionRun[DowntimeHours])
```

**Purpose:** Recorded production downtime.

**Format:** Decimal, 1 decimal place

### Capacity Utilization %

```dax
Capacity Utilization % =
DIVIDE([Total Actual Run Hours], [Total Planned Run Hours], 0)
```

**Purpose:** Actual runtime achieved relative to scheduled runtime.

**Format:** Percentage, 1 decimal place

### Capacity Loss %

```dax
Capacity Loss % =
DIVIDE(
    [Total Downtime Hours],
    [Total Actual Run Hours] + [Total Downtime Hours],
    0
)
```

**Purpose:** Share of total scheduled operating time represented by downtime.

**Format:** Percentage, 1 decimal place

---

## 4. Procurement & Supplier Performance

### Total Inbound POs

```dax
Total Inbound POs =
COUNTROWS(Fact_InboundProcurement)
```

**Purpose:** Number of inbound procurement records.

**Format:** Whole number

### On-Time POs

```dax
On-Time POs =
CALCULATE(
    COUNTROWS(Fact_InboundProcurement),
    Fact_InboundProcurement[DeliveryVarianceDays] <= 0
)
```

**Purpose:** Inbound records received on or before the contracted lead-time expectation.

**Format:** Whole number

### Total Late POs

```dax
Total Late POs =
CALCULATE(
    COUNTROWS(Fact_InboundProcurement),
    Fact_InboundProcurement[DeliveryVarianceDays] > 0
)
```

**Purpose:** Inbound records exceeding contracted lead time.

**Format:** Whole number

### Supplier On-Time %

```dax
Supplier On-Time % =
DIVIDE([On-Time POs], [Total Inbound POs], 0)
```

**Purpose:** Overall supplier delivery reliability.

**Format:** Percentage, 1 decimal place

### Avg Actual Lead Days

```dax
Avg Actual Lead Days =
AVERAGE(Fact_InboundProcurement[ActualLeadDays])
```

**Purpose:** Average actual supplier lead time.

**Format:** Decimal, 1 decimal place

### Avg Delivery Variance Days

```dax
Avg Delivery Variance Days =
AVERAGE(Fact_InboundProcurement[DeliveryVarianceDays])
```

**Purpose:** Average deviation from contracted lead time. Positive values indicate delay.

**Format:** Decimal, 1 decimal place

---

## 5. Warehouse & Cross-Functional Diagnostics

### Avg Dock to Stock Days

```dax
Avg Dock to Stock Days =
AVERAGE(Fact_InboundProcurement[DockToStockDays])
```

**Purpose:** Average time from dock receipt to warehouse availability.

**Format:** Decimal, 1 decimal place

### Delayed Intake POs

```dax
Delayed Intake POs =
CALCULATE(
    COUNTROWS(Fact_InboundProcurement),
    Fact_InboundProcurement[DockToStockDays] > 2.0
)
```

**Purpose:** Number of inbound records exceeding the report's common two-day operating benchmark.

**Format:** Whole number

> **Model note:** The warehouse dimension contains warehouse-specific benchmarks. This measure uses a common 2.0-day analytical benchmark for dashboard comparability.

### Warehouse Delay %

```dax
Warehouse Delay % =
DIVIDE([Delayed Intake POs], [Total Inbound POs], 0)
```

**Purpose:** Share of inbound records exceeding the common processing benchmark.

**Format:** Percentage, 1 decimal place

### Intake SLA Breach %

```dax
Intake SLA Breach % =
DIVIDE(
    CALCULATE(
        COUNTROWS(Fact_InboundProcurement),
        Fact_InboundProcurement[DockToStockDays] > 2.0
    ),
    [Total Inbound POs],
    0
)
```

**Purpose:** Same breach concept expressed directly as a percentage.

**Format:** Percentage, 1 decimal place

### Material Starved Runs

```dax
Material Starved Runs =
CALCULATE(
    COUNTROWS(Fact_ProductionRun),
    Fact_ProductionRun[MaterialStarvationFlag] = 1
)
```

**Purpose:** Production runs flagged as experiencing material starvation.

**Format:** Whole number

### Material Shortage Downtime Hours

```dax
Material Shortage Downtime Hours =
CALCULATE(
    [Total Downtime Hours],
    Fact_ProductionRun[DowntimeReason] = "Material Shortage"
)
```

**Purpose:** Downtime attributed to material shortages.

**Format:** Decimal, 1 decimal place

### Shortfall from Material Starvation

```dax
Shortfall from Material Starvation =
CALCULATE(
    [Production Shortfall],
    Fact_ProductionRun[DowntimeReason] = "Material Shortage"
)
```

**Purpose:** Production shortfall observed within runs categorized as material-shortage events.

**Format:** Whole number

> **Interpretation note:** This measure should be described as shortfall associated with material-starvation runs, not as a statistically isolated causal estimate.

---

## Measure Design Principles

- Measures are grouped by business process rather than dashboard page.
- Ratios use `DIVIDE()` to avoid divide-by-zero errors.
- KPI definitions are kept simple and auditable.
- The model prioritizes business readability over unnecessary DAX complexity.
- Cross-functional measures should be interpreted as operational associations unless the underlying data provides transaction-level causal evidence.
