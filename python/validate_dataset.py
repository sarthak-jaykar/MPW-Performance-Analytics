import os
import sys
import pandas as pd
import numpy as np

# Force UTF-8 on Windows consoles if available
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Determine path relative to script or execution root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "raw")

# Fallback check if script is run from project root directly
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join("data", "raw")


def load_tables():
    required_files = [
        "Dim_Date.csv",
        "Dim_Warehouse.csv",
        "Dim_Supplier.csv",
        "Dim_Material.csv",
        "Dim_Product.csv",
        "Fact_InboundProcurement.csv",
        "Fact_ProductionRun.csv",
    ]
    dfs = {}
    for f in required_files:
        path = os.path.join(DATA_DIR, f)
        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Missing file: {path}. Run generation script first."
            )
        dfs[f.replace(".csv", "")] = pd.read_csv(path)
    return dfs


def run_validations():
    print("=" * 65)
    print("MPW PERFORMANCE ANALYTICS -- DATA INTEGRITY & AUDIT SUITE")
    print("=" * 65)

    dfs = load_tables()
    failures = 0

    # 1. Null Value Audit
    print("\n[CHECK 1] Null Value Audit across all tables...")
    for name, df in dfs.items():
        null_count = df.isnull().sum().sum()
        if null_count > 0:
            print(f"  [FAIL] {name} contains {null_count} null values.")
            failures += 1
        else:
            print(f"  [PASS] {name} has 0 nulls.")

    # 2. Referential Integrity (Foreign Key Resolution)
    print("\n[CHECK 2] Referential Integrity & Foreign Key Resolution...")

    p_supp = set(dfs["Fact_InboundProcurement"]["SupplierID"]) - set(
        dfs["Dim_Supplier"]["SupplierID"]
    )
    p_mat = set(dfs["Fact_InboundProcurement"]["MaterialID"]) - set(
        dfs["Dim_Material"]["MaterialID"]
    )
    p_wh = set(dfs["Fact_InboundProcurement"]["WarehouseID"]) - set(
        dfs["Dim_Warehouse"]["WarehouseID"]
    )

    pr_prod = set(dfs["Fact_ProductionRun"]["ProductID"]) - set(
        dfs["Dim_Product"]["ProductID"]
    )
    pr_wh = set(dfs["Fact_ProductionRun"]["WarehouseID"]) - set(
        dfs["Dim_Warehouse"]["WarehouseID"]
    )

    fk_checks = [
        ("Fact_InboundProcurement -> Dim_Supplier", p_supp),
        ("Fact_InboundProcurement -> Dim_Material", p_mat),
        ("Fact_InboundProcurement -> Dim_Warehouse", p_wh),
        ("Fact_ProductionRun -> Dim_Product", pr_prod),
        ("Fact_ProductionRun -> Dim_Warehouse", pr_wh),
    ]

    for label, orphan_set in fk_checks:
        if orphan_set:
            print(f"  [FAIL] {label} has orphaned keys: {orphan_set}")
            failures += 1
        else:
            print(f"  [PASS] {label} (100% match)")

    # 3. Manufacturing Math & Operational Logic
    print("\n[CHECK 3] Manufacturing Math & Operational Logic...")
    prod_df = dfs["Fact_ProductionRun"]

    qty_mismatch = (
        prod_df["ProducedQty"] != (prod_df["GoodQty"] + prod_df["RejectedQty"])
    ).sum()
    if qty_mismatch > 0:
        print(
            f"  [FAIL] {qty_mismatch} rows violate ProducedQty = GoodQty + RejectedQty"
        )
        failures += 1
    else:
        print("  [PASS] ProducedQty = GoodQty + RejectedQty holds for all rows.")

    good_exceeds = (prod_df["GoodQty"] > prod_df["ProducedQty"]).sum()
    if good_exceeds > 0:
        print(f"  [FAIL] {good_exceeds} rows have GoodQty > ProducedQty")
        failures += 1
    else:
        print("  [PASS] GoodQty <= ProducedQty holds for all rows.")

    neg_down = (prod_df["DowntimeHours"] < 0).sum()
    if neg_down > 0:
        print(f"  [FAIL] {neg_down} rows contain negative DowntimeHours")
        failures += 1
    else:
        print("  [PASS] DowntimeHours >= 0 across all runs.")

    # 4. Procurement & Inbound Supply Invariants
    print("\n[CHECK 4] Procurement & Warehouse Flow Logic...")
    inb_df = dfs["Fact_InboundProcurement"]

    inb_df["OrderDate_dt"] = pd.to_datetime(inb_df["OrderDate"])
    inb_df["ActualDeliveryDate_dt"] = pd.to_datetime(inb_df["ActualDeliveryDate"])
    computed_lead = (inb_df["ActualDeliveryDate_dt"] - inb_df["OrderDate_dt"]).dt.days
    lead_mismatch = (inb_df["ActualLeadDays"] != computed_lead).sum()
    if lead_mismatch > 0:
        print(
            f"  [FAIL] {lead_mismatch} rows have mismatched ActualLeadDays vs date delta"
        )
        failures += 1
    else:
        print("  [PASS] ActualLeadDays aligns with calendar date deltas.")

    neg_dts = (inb_df["DockToStockDays"] <= 0).sum()
    if neg_dts > 0:
        print(f"  [FAIL] {neg_dts} rows have DockToStockDays <= 0")
        failures += 1
    else:
        print("  [PASS] DockToStockDays > 0 across all inbound receipts.")

    # Final Audit Summary
    print("\n" + "=" * 65)
    if failures == 0:
        print(">> ALL QUALITY GATES PASSED! Dataset is clean and ready.")
        print("=" * 65)
        return True
    else:
        print(f">> AUDIT FAILED: {failures} check(s) did not pass.")
        print("=" * 65)
        return False


if __name__ == "__main__":
    success = run_validations()
    if not success:
        sys.exit(1)
