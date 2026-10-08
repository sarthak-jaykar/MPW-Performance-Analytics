import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# 1. Initialization and Reproducibility
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

OUTPUT_DIR = os.path.join("data", "raw")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------------------------------------
# 2. DIMENSION TABLES GENERATION
# ---------------------------------------------------------

# Dim_Date (Calendar Year 2025)
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range = pd.date_range(start_date, end_date, freq="D")

dim_date = pd.DataFrame(
    {
        "Date": date_range,
        "Year": date_range.year,
        "Quarter": "Q" + date_range.quarter.astype(str),
        "MonthNum": date_range.month,
        "MonthName": date_range.strftime("%b"),
        "MonthYear": date_range.strftime("%b %Y"),
        "WeekNum": date_range.isocalendar().week,
        "IsWeekend": (date_range.weekday >= 5).astype(int),
    }
)

# Dim_Warehouse
dim_warehouse = pd.DataFrame(
    [
        {
            "WarehouseID": "WH-01",
            "WarehouseName": "Central Logistics Hub",
            "TargetDockToStockDays": 1.5,
        },
        {
            "WarehouseID": "WH-02",
            "WarehouseName": "Plant Inbound Depot",
            "TargetDockToStockDays": 2.0,
        },
    ]
)

# Dim_Supplier (12 Suppliers)
supplier_data = [
    {
        "SupplierID": "SUP-01",
        "SupplierName": "Apex Micro Devices",
        "CategoryProvided": "Semiconductors",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 25,
        "SupplierRiskProfile": "High Risk",
    },
    {
        "SupplierID": "SUP-02",
        "SupplierName": "Silicon Circuits Corp",
        "CategoryProvided": "PCBs",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 18,
        "SupplierRiskProfile": "Moderate Risk",
    },
    {
        "SupplierID": "SUP-03",
        "SupplierName": "Transistor Dynamics",
        "CategoryProvided": "Semiconductors",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 22,
        "SupplierRiskProfile": "Moderate Risk",
    },
    {
        "SupplierID": "SUP-04",
        "SupplierName": "Shenzhen Core Tech",
        "CategoryProvided": "Semiconductors",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 30,
        "SupplierRiskProfile": "High Risk",
    },
    {
        "SupplierID": "SUP-05",
        "SupplierName": "EuroConnect Electronics",
        "CategoryProvided": "Passive Components",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 12,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-06",
        "SupplierName": "Kyoto Passive Components",
        "CategoryProvided": "Passive Components",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 14,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-07",
        "SupplierName": "Vanguard Multilayer PCBs",
        "CategoryProvided": "PCBs",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 20,
        "SupplierRiskProfile": "Moderate Risk",
    },
    {
        "SupplierID": "SUP-08",
        "SupplierName": "Precision Alloy Castings",
        "CategoryProvided": "Enclosures & Plastics",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 15,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-09",
        "SupplierName": "FormaPlast Molding",
        "CategoryProvided": "Enclosures & Plastics",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 10,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-10",
        "SupplierName": "AmpVolt Transformers",
        "CategoryProvided": "Passive Components",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 16,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-11",
        "SupplierName": "Delta Interconnects",
        "CategoryProvided": "Passive Components",
        "SupplierTier": "Tier 2",
        "ContractedLeadDays": 12,
        "SupplierRiskProfile": "Stable",
    },
    {
        "SupplierID": "SUP-12",
        "SupplierName": "Nordic Sensor Systems",
        "CategoryProvided": "Semiconductors",
        "SupplierTier": "Tier 1",
        "ContractedLeadDays": 21,
        "SupplierRiskProfile": "Stable",
    },
]
dim_supplier = pd.DataFrame(supplier_data)

# Dim_Material (40 Materials mapped to Supplier Categories)
material_data = []
categories = [
    "Semiconductors",
    "PCBs",
    "Passive Components",
    "Enclosures & Plastics",
]
mat_idx = 1
for cat in categories:
    num_items = 10
    critical_prob = (
        0.7 if cat in ["Semiconductors", "PCBs"] else 0.2
    )  # Criticality bias
    for i in range(num_items):
        is_crit = "Critical" if random.random() < critical_prob else "Standard"
        material_data.append(
            {
                "MaterialID": f"MAT-{mat_idx:03d}",
                "MaterialName": f"{cat[:4].upper()}-Component-{i+1}",
                "Category": cat,
                "Criticality": is_crit,
                "SafetyStockUnits": (
                    random.randint(500, 2000)
                    if is_crit == "Critical"
                    else random.randint(200, 800)
                ),
            }
        )
        mat_idx += 1
dim_material = pd.DataFrame(material_data)

# Dim_Product (20 Finished Goods)
product_categories = ["Industrial IoT", "Consumer Audio", "Power Systems"]
complexity_tiers = ["High", "Medium", "Low"]
product_data = []

for i in range(1, 21):
    cat = product_categories[(i - 1) % len(product_categories)]
    line = f"Line {((i - 1) % 3) + 1}"

    # Align Line 2 with complex IoT systems for operational pressure
    if line == "Line 2":
        comp = random.choice(["High", "Medium"])
        target_yield = 0.94 if comp == "High" else 0.96
    elif line == "Line 3":
        comp = random.choice(["Medium", "Low"])
        target_yield = 0.97
    else:
        comp = random.choice(["High", "Medium", "Low"])
        target_yield = 0.98 if comp == "Low" else 0.95

    product_data.append(
        {
            "ProductID": f"PRD-{i:02d}",
            "ProductName": f"Apex {cat.split()[0]} Model-{i}",
            "ProductCategory": cat,
            "ComplexityTier": comp,
            "PrimaryLine": line,
            "TargetYieldPct": target_yield,
        }
    )
dim_product = pd.DataFrame(product_data)

# ---------------------------------------------------------
# 3. FACT_INBOUNDPROCUREMENT (~1,100 Records)
# ---------------------------------------------------------
supplier_mat_map = {
    cat: dim_material[dim_material["Category"] == cat]["MaterialID"].tolist()
    for cat in categories
}

procurement_records = []
total_pos = 1100

for i in range(1, total_pos + 1):
    po_id = f"PO-2025-{i:04d}"
    order_date = start_date + timedelta(days=random.randint(0, 310))

    supp = dim_supplier.sample(1).iloc[0]
    supp_id = supp["SupplierID"]
    supp_cat = supp["CategoryProvided"]
    contracted_lead = supp["ContractedLeadDays"]
    risk = supp["SupplierRiskProfile"]

    mat_id = random.choice(supplier_mat_map[supp_cat])
    wh_id = "WH-01" if random.random() < 0.6 else "WH-02"

    ordered_qty = int(random.choice([500, 1000, 1500, 2500, 5000]))
    # Short shipment is rare (97% fully delivered)
    received_qty = (
        ordered_qty
        if random.random() > 0.05
        else int(ordered_qty * random.uniform(0.90, 0.98))
    )

    # Lead Time Variance based on risk profile
    if risk == "High Risk":
        # 40% chance of substantial delay
        if random.random() < 0.40:
            variance_days = random.randint(4, 14)
            cause = (
                "Supplier Manufacturing Delay"
                if random.random() < 0.7
                else "Logistics Transit Delay"
            )
        else:
            variance_days = random.randint(-2, 2)
            cause = "On-Time"
    elif risk == "Moderate Risk":
        if random.random() < 0.20:
            variance_days = random.randint(2, 6)
            cause = "Logistics Transit Delay"
        else:
            variance_days = random.randint(-2, 1)
            cause = "On-Time"
    else:  # Stable
        variance_days = (
            random.randint(-3, 1) if random.random() > 0.05 else random.randint(1, 3)
        )
        cause = "On-Time" if variance_days <= 0 else "Warehouse Intake Bottleneck"

    actual_lead = max(2, contracted_lead + variance_days)
    expected_delivery = order_date + timedelta(days=int(contracted_lead))
    actual_delivery = order_date + timedelta(days=int(actual_lead))

    # Dock-to-Stock cycle: WH-02 experiences bottlenecks in Q3/Q4
    is_q3_q4 = actual_delivery.month >= 7
    if wh_id == "WH-02" and is_q3_q4 and random.random() < 0.35:
        dock_to_stock = round(random.uniform(3.0, 5.5), 1)
        if cause == "On-Time":
            cause = "Warehouse Intake Bottleneck"
    else:
        dock_to_stock = round(
            random.uniform(1.0, 2.2) if wh_id == "WH-01" else random.uniform(1.5, 2.5),
            1,
        )

    putaway_date = actual_delivery + timedelta(days=int(np.ceil(dock_to_stock)))

    procurement_records.append(
        {
            "PO_ID": po_id,
            "OrderDate": order_date.strftime("%Y-%m-%d"),
            "ExpectedDeliveryDate": expected_delivery.strftime("%Y-%m-%d"),
            "ActualDeliveryDate": actual_delivery.strftime("%Y-%m-%d"),
            "PutawayDate": putaway_date.strftime("%Y-%m-%d"),
            "SupplierID": supp_id,
            "MaterialID": mat_id,
            "WarehouseID": wh_id,
            "OrderedQty": ordered_qty,
            "ReceivedQty": received_qty,
            "ActualLeadDays": actual_lead,
            "DeliveryVarianceDays": variance_days,
            "DockToStockDays": dock_to_stock,
            "DelayRootCause": cause,
        }
    )

fact_inbound = pd.DataFrame(procurement_records)

# ---------------------------------------------------------
# 4. FACT_PRODUCTIONRUN (~2,100 Records)
# ---------------------------------------------------------
production_records = []
total_wos = 2100

for i in range(1, total_wos + 1):
    wo_id = f"WO-2025-{i:04d}"
    exec_date = start_date + timedelta(days=random.randint(5, 360))

    prod = dim_product.sample(1).iloc[0]
    prod_id = prod["ProductID"]
    line_id = prod["PrimaryLine"]
    complexity = prod["ComplexityTier"]
    wh_id = "WH-01" if random.random() < 0.65 else "WH-02"

    planned_qty = int(random.choice([300, 500, 800, 1000, 1200]))
    planned_run_hrs = round(planned_qty / 100.0, 1)  # standard speed: 100 units/hr

    # Check for operational stress events
    is_q3_q4 = exec_date.month >= 7
    starvation_chance = 0.22 if (wh_id == "WH-02" and is_q3_q4) else 0.08

    # Downtime and Starvation assignment
    # Explicit default assignments so pandas never flags NaN
    material_starved = 0
    downtime_cause = "No Downtime"  # <--- Change from "None" to "No Downtime"
    downtime_hrs = 0.0

    rand_val = random.random()
    if rand_val < starvation_chance:
        material_starved = 1
        downtime_cause = "Material Shortage"
        downtime_hrs = round(random.uniform(2.5, 6.0), 1)
    elif line_id == "Line 2" and random.random() < 0.20:
        material_starved = 0
        downtime_cause = "Equipment Breakdown"
        downtime_hrs = round(random.uniform(2.0, 5.0), 1)
    elif random.random() < 0.12:
        material_starved = 0
        downtime_cause = "Tooling/Setup Delay"
        downtime_hrs = round(random.uniform(1.0, 2.5), 1)

    actual_run_hrs = round(max(1.0, planned_run_hrs - (downtime_hrs * 0.7)), 1)

    # Output Volume derived from actual run time vs downtime
    if downtime_hrs > 0:
        loss_ratio = downtime_hrs / (planned_run_hrs + downtime_hrs)
        produced_qty = int(planned_qty * max(0.40, 1.0 - loss_ratio))
    else:
        # Normal variation: -3% to +3%
        produced_qty = int(planned_qty * random.uniform(0.97, 1.03))

    # Scrap/Defects governed strictly by product complexity
    if complexity == "High":
        scrap_rate = random.uniform(0.06, 0.10)
    elif complexity == "Medium":
        scrap_rate = random.uniform(0.03, 0.05)
    else:  # Low
        scrap_rate = random.uniform(0.01, 0.02)

    rejected_qty = int(round(produced_qty * scrap_rate))
    good_qty = produced_qty - rejected_qty  # Mathematical identity enforced

    production_records.append(
        {
            "WorkOrderID": wo_id,
            "ExecutionDate": exec_date.strftime("%Y-%m-%d"),
            "ProductID": prod_id,
            "WarehouseID": wh_id,
            "LineID": line_id,
            "PlannedQty": planned_qty,
            "ProducedQty": produced_qty,
            "GoodQty": good_qty,
            "RejectedQty": rejected_qty,
            "PlannedRunHours": planned_run_hrs,
            "ActualRunHours": actual_run_hrs,
            "DowntimeHours": downtime_hrs,
            "DowntimeReason": downtime_cause,
            "MaterialStarvationFlag": material_starved,
        }
    )

fact_production = pd.DataFrame(production_records)

# ---------------------------------------------------------
# 5. EXPORT TABLES TO CSV
# ---------------------------------------------------------
tables = {
    "Dim_Date.csv": dim_date,
    "Dim_Warehouse.csv": dim_warehouse,
    "Dim_Supplier.csv": dim_supplier,
    "Dim_Material.csv": dim_material,
    "Dim_Product.csv": dim_product,
    "Fact_InboundProcurement.csv": fact_inbound,
    "Fact_ProductionRun.csv": fact_production,
}

print(f"Generating MPW dataset into: {OUTPUT_DIR}")
for filename, df in tables.items():
    path = os.path.join(OUTPUT_DIR, filename)
    df.to_csv(path, index=False)
    print(f" Saved {filename} ({len(df):,} rows)")

print("\nDataset generation completed successfully.")
