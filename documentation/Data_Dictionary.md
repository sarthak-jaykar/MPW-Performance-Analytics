# Data Dictionary & Schema Specification

**Project:** MPW Performance Analytics  
**Model:** Compact two-fact star schema  
**Reporting Period:** FY2025

---

## 1. Model Overview

The Power BI model contains two primary fact tables supported by shared dimensions.

### Fact tables

- `Fact_ProductionRun` — production execution and quality-related output.
- `Fact_InboundProcurement` — supplier delivery and inbound warehouse-processing records.

### Dimensions

- `Dim_Date`
- `Dim_Product`
- `Dim_Material`
- `Dim_Supplier`
- `Dim_Warehouse`

The model is intentionally compact to support cross-functional operational analysis without unnecessary ERP-level complexity.

---

## 2. Fact Tables

### `Fact_ProductionRun`

Contains production-run records across the assembly lines.

| Column | Type | Role | Description |
|---|---|---|---|
| `WorkOrderID` | Integer | Primary Key | Unique production work-order identifier. |
| `ExecutionDate` | Date | Foreign Key | Production execution date. |
| `ProductID` | Text | Foreign Key | Product manufactured during the run. |
| `WarehouseID` | Text | Foreign Key | Warehouse associated with material staging for the run. |
| `LineID` | Text | Dimension Ref | Assembly line identifier. |
| `PlannedQty` | Integer | Measure | Planned production quantity. |
| `ProducedQty` | Integer | Measure | Total units produced. |
| `GoodQty` | Integer | Measure | Units accepted as good output. |
| `RejectedQty` | Integer | Measure | Units rejected during quality inspection. |
| `PlannedRunHours` | Decimal | Measure | Planned production runtime. |
| `ActualRunHours` | Decimal | Measure | Generated actual production runtime. |
| `DowntimeHours` | Decimal | Measure | Recorded downtime associated with the run. |
| `DowntimeReason` | Text | Category | Primary downtime reason. |
| `MaterialStarvationFlag` | Integer | Flag | `1` when the run experienced material starvation; otherwise `0`. |

**Business rule:** `ProducedQty = GoodQty + RejectedQty`.

### `Fact_InboundProcurement`

Contains inbound purchase-order and warehouse-processing records.

| Column | Type | Role | Description |
|---|---|---|---|
| `PO_ID` | Integer | Primary Key | Unique inbound purchase-order record. |
| `OrderDate` | Date | Date | Purchase-order date. |
| `ExpectedDeliveryDate` | Date | Date | Expected supplier delivery date. |
| `ActualDeliveryDate` | Date | Date | Actual supplier delivery date. |
| `PutawayDate` | Date | Date | Date material became available after warehouse putaway. |
| `SupplierID` | Text | Foreign Key | Supplier fulfilling the order. |
| `MaterialID` | Text | Foreign Key | Raw material purchased. |
| `WarehouseID` | Text | Foreign Key | Receiving warehouse. |
| `OrderedQty` | Integer | Measure | Quantity ordered. |
| `ReceivedQty` | Integer | Measure | Quantity received. |
| `ActualLeadDays` | Integer | Measure | Actual elapsed supplier lead time. |
| `DeliveryVarianceDays` | Integer | Measure | Actual lead time minus contracted lead time. Positive values indicate delay. |
| `DockToStockDays` | Decimal | Measure | Time from receipt at the dock to warehouse availability. |
| `DelayRootCause` | Text | Category | Primary inbound delay category. |

---

## 3. Dimension Tables

### `Dim_Product`

| Column | Description |
|---|---|
| `ProductID` | Unique finished-product identifier. |
| `ProductName` | Product description. |
| `ProductCategory` | Product category. |
| `ComplexityTier` | Manufacturing complexity: High, Medium or Low. |
| `PrimaryLine` | Primary assembly line associated with the product. |
| `TargetYieldPct` | Target first-pass yield percentage for the product. |

### `Dim_Supplier`

| Column | Description |
|---|---|
| `SupplierID` | Unique supplier identifier. |
| `SupplierName` | Supplier name. |
| `CategoryProvided` | Primary component category supplied. |
| `SupplierTier` | Supplier tier classification. |
| `ContractedLeadDays` | Contracted supplier lead time in days. |
| `SupplierRiskProfile` | Risk classification: High Risk, Moderate Risk or Stable. |

### `Dim_Material`

| Column | Description |
|---|---|
| `MaterialID` | Unique raw-material identifier. |
| `MaterialName` | Material description. |
| `Category` | Material category. |
| `Criticality` | Critical or Standard. |
| `SafetyStockUnits` | Configured safety-stock quantity for the material. |

### `Dim_Warehouse`

| Column | Description |
|---|---|
| `WarehouseID` | Warehouse identifier. |
| `WarehouseName` | Operational warehouse name. |
| `TargetDockToStockDays` | Warehouse-specific processing benchmark. |

### `Dim_Date`

| Column | Description |
|---|---|
| `Date` | Calendar date for FY2025. |
| `Year` | Calendar year. |
| `Quarter` | Calendar quarter. |
| `MonthNum` | Month number. |
| `MonthName` | Month name. |
| `Day` | Day of month. |
| `DayOfWeek` | Day-of-week label. |
| `IsWeekend` | Weekend indicator. |

---

## 4. KPI Mapping

| KPI | Primary Source |
|---|---|
| Plan Attainment % | `Fact_ProductionRun` |
| Production Shortfall | `Fact_ProductionRun` |
| Capacity Utilization % | `Fact_ProductionRun` |
| Downtime Hours | `Fact_ProductionRun` |
| Yield % | `Fact_ProductionRun` |
| Rejection Rate % | `Fact_ProductionRun` |
| Supplier On-Time % | `Fact_InboundProcurement` |
| Average Lead Time | `Fact_InboundProcurement` |
| Delivery Variance | `Fact_InboundProcurement` |
| Dock-to-Stock Days | `Fact_InboundProcurement` |
| Warehouse Delay % | `Fact_InboundProcurement` |
| Material Starved Runs | `Fact_ProductionRun` |

---

## 5. Data Notes

- The dataset is synthetic and created for portfolio demonstration.
- All dates fall within FY2025.
- Quantities are designed to maintain logical production relationships.
- The model is intentionally smaller than a production ERP schema.
- Supplier delivery, warehouse processing and production indicators are analyzed together to support operational root-cause diagnosis; the model should not be interpreted as transaction-level proof of direct causality between an individual supplier event and an individual production order.
