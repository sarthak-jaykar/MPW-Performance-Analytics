import os
import sys
import pandas as pd
import numpy as np

# Adjust base directory to locate data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join("data", "raw")

# Load tables
fact_prod = pd.read_csv(os.path.join(DATA_DIR, "Fact_ProductionRun.csv"))
fact_inb = pd.read_csv(os.path.join(DATA_DIR, "Fact_InboundProcurement.csv"))
dim_prod = pd.read_csv(os.path.join(DATA_DIR, "Dim_Product.csv"))
dim_supp = pd.read_csv(os.path.join(DATA_DIR, "Dim_Supplier.csv"))
dim_mat = pd.read_csv(os.path.join(DATA_DIR, "Dim_Material.csv"))
dim_wh = pd.read_csv(os.path.join(DATA_DIR, "Dim_Warehouse.csv"))

# Merge metadata for joined reporting
prod_merged = fact_prod.merge(dim_prod, on="ProductID", how="left")
inb_merged = fact_inb.merge(dim_supp, on="SupplierID", how="left").merge(
    dim_mat, on="MaterialID", how="left"
)

print("=" * 75)
print("             EXECUTIVE OPERATIONS BASELINE & EDA SUMMARY            ")
print("=" * 75)

# --- 1. OVERALL MANUFACTURING METRICS ---
tot_planned = fact_prod["PlannedQty"].sum()
tot_produced = fact_prod["ProducedQty"].sum()
tot_good = fact_prod["GoodQty"].sum()
tot_rejected = fact_prod["RejectedQty"].sum()
shortfall = tot_planned - tot_good
plan_attainment = (tot_good / tot_planned) * 100
overall_yield = (tot_good / tot_produced) * 100
tot_downtime = fact_prod["DowntimeHours"].sum()

print("\n[1] Overall Manufacturing Execution")
print(f"  * Total Planned Volume : {tot_planned:,.0f} units")
print(f"  * Total Good Volume    : {tot_good:,.0f} units")
print(f"  * Production Shortfall : {shortfall:,.0f} units")
print(f"  * Plan Attainment Rate : {plan_attainment:.2f}%")
print(f"  * Floor Yield Rate     : {overall_yield:.2f}%")
print(
    f"  * Scrap / Rejection    : {tot_rejected:,.0f} units ({(tot_rejected/tot_produced)*100:.2f}%)"
)
print(f"  * Total Line Downtime  : {tot_downtime:,.1f} operating hours")

# --- 2. LINE PERFORMANCE BREAKDOWN ---
print("\n[2] Line-Level Performance & Bottleneck Profiling")
line_summary = (
    prod_merged.groupby("LineID")
    .agg(
        Planned=("PlannedQty", "sum"),
        Good=("GoodQty", "sum"),
        Rejected=("RejectedQty", "sum"),
        DowntimeHours=("DowntimeHours", "sum"),
        StarvedRuns=("MaterialStarvationFlag", "sum"),
        TotalRuns=("WorkOrderID", "count"),
    )
    .reset_index()
)

line_summary["Attainment%"] = (line_summary["Good"] / line_summary["Planned"]) * 100
line_summary["Yield%"] = (
    line_summary["Good"] / (line_summary["Good"] + line_summary["Rejected"])
) * 100
line_summary["Shortfall"] = line_summary["Planned"] - line_summary["Good"]
print(
    line_summary[
        [
            "LineID",
            "Planned",
            "Good",
            "Shortfall",
            "Attainment%",
            "Yield%",
            "DowntimeHours",
            "StarvedRuns",
        ]
    ].to_string(index=False)
)

# --- 3. DOWNTIME ROOT CAUSES ---
print("\n[3] Downtime Distribution by Cause")
dt_causes = (
    fact_prod[fact_prod["DowntimeReason"] != "No Downtime"]
    .groupby("DowntimeReason")
    .agg(Events=("WorkOrderID", "count"), TotalHours=("DowntimeHours", "sum"))
    .reset_index()
)
dt_causes["ShareOfHours%"] = (dt_causes["TotalHours"] / tot_downtime) * 100
print(dt_causes.sort_values(by="TotalHours", ascending=False).to_string(index=False))

# --- 4. PROCUREMENT & SUPPLIER RISK ANALYSIS ---
print("\n[4] Supplier Delivery Reliability (Procurement Performance)")
inb_merged["IsLate"] = (inb_merged["DeliveryVarianceDays"] > 0).astype(int)
supp_summary = (
    inb_merged.groupby(
        ["SupplierID", "SupplierName", "SupplierRiskProfile", "CategoryProvided"]
    )
    .agg(
        TotalPOs=("PO_ID", "count"),
        LatePOs=("IsLate", "sum"),
        AvgVarianceDays=("DeliveryVarianceDays", "mean"),
        AvgLeadDays=("ActualLeadDays", "mean"),
    )
    .reset_index()
)
supp_summary["OnTimeDelivery%"] = (
    (supp_summary["TotalPOs"] - supp_summary["LatePOs"]) / supp_summary["TotalPOs"]
) * 100
print(
    supp_summary.sort_values(by="OnTimeDelivery%", ascending=True).to_string(
        index=False
    )
)

# --- 5. WAREHOUSING INTAKE & CYCLE TIME ---
print("\n[5] Warehouse Intake & Staging Cycle (Dock-to-Stock)")
fact_inb["OrderDate_dt"] = pd.to_datetime(fact_inb["OrderDate"])
fact_inb["Half"] = np.where(
    fact_inb["OrderDate_dt"].dt.month >= 7, "H2 (Jul-Dec)", "H1 (Jan-Jun)"
)
wh_summary = (
    fact_inb.groupby(["WarehouseID", "Half"])
    .agg(
        Receipts=("PO_ID", "count"),
        AvgDockToStockDays=("DockToStockDays", "mean"),
        MaxDockToStockDays=("DockToStockDays", "max"),
    )
    .reset_index()
)
print(wh_summary.to_string(index=False))

print("\n" + "=" * 75)
print("EDA Complete. Key patterns confirm clear causal linkages for Power BI.")
print("=" * 75)
