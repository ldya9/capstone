#!/usr/bin/env python3
"""
merge_model_ready_final.py

Merge semua FE → Handle missing → Drop ID → Siap modeling.
Support:
- Production FE (base)
- Fleet & Heavy Equipment FE
- Stockpile FE
- Truck-to-Ship FE (dengan atau tanpa pit_id)
- Weather FE
"""

import pandas as pd
from pathlib import Path
import numpy as np

# -------------------------------
# PATH CONFIG
# -------------------------------
BASE = Path("../all_dataset/feature_dataset")
OUT = Path("../all_dataset/merge_dataset")
OUT.mkdir(exist_ok=True, parents=True)

def load_if_exists(p: Path, parse_week=True):
    """Load CSV jika ada, parse week_start jika perlu"""
    if not p.exists():
        return None
    return pd.read_csv(p, parse_dates=["week_start"] if parse_week else None)

# -------------------------------
# LOAD FE DATA
# -------------------------------
prod = load_if_exists(BASE / "production_fe.csv")
fleet = load_if_exists(BASE / "fleet_fe.csv")
he = load_if_exists(BASE / "heavy_equipment_fe.csv")
stock = load_if_exists(BASE / "stockpile_fe.csv")
truck = load_if_exists(BASE / "truck_to_ship_fe.csv")
weather = load_if_exists(BASE / "weather_fe.csv")

# -------------------------------
# BASE: PRODUCTION
# -------------------------------
main = prod.copy()
print(f"[INFO] Base rows: {len(main)}")

# -------------------------------
# SAFE MERGE HELPER
# -------------------------------
def safe_merge(left, right, on, how="left", right_name="right"):
    if right is None:
        return left
    keys = on if isinstance(on, list) else [on]
    right_cols = [c for c in right.columns if c not in left.columns or c in keys]
    merged = left.merge(right[right_cols], on=keys, how=how)
    print(f"[MERGE] {right_name}: left_rows={len(left)}, right_rows={len(right)} -> merged_rows={len(merged)}")
    return merged

# -------------------------------
# PIT-LEVEL MERGE
# -------------------------------
main = safe_merge(main, fleet, on=["week_start","pit_id"], right_name="fleet")
main = safe_merge(main, he, on=["week_start","pit_id"], right_name="heavy_equipment")

# -------------------------------
# STOCKPILE-LEVEL MERGE
# -------------------------------
if stock is not None:
    stock_cols = [c for c in stock.columns if c not in main.columns or c in ["week_start","pit_id"]]
    main = safe_merge(main, stock[stock_cols], on=["week_start","pit_id"], right_name="stockpile")

# -------------------------------
# TRUCK-TO-SHIP MERGE
# -------------------------------
if truck is not None:
    if "pit_id" in truck.columns:
        # Aggregate per pit
        agg = truck.groupby(["week_start","pit_id"])[[
            "tonnage_moved_ton","trip_count","weekly_truck_supply_ton",
            "weekly_ship_demand_ton","supply_alignment_ratio",
            "truck_to_ship_utilization"
        ]].sum().reset_index()
        main = safe_merge(main, agg, on=["week_start","pit_id"], right_name="truck_agg")
    else:
        # Aggregate per week saja
        agg = truck.groupby("week_start")[[
            "tonnage_moved_ton","trip_count","weekly_truck_supply_ton",
            "weekly_ship_demand_ton","supply_alignment_ratio",
            "truck_to_ship_utilization"
        ]].sum().reset_index()
        main = safe_merge(main, agg, on="week_start", right_name="truck_agg_week")

# -------------------------------
# WEATHER MERGE
# -------------------------------
main = safe_merge(main, weather, on="week_start", right_name="weather")

# -------------------------------
# HANDLE MISSING VALUES
# -------------------------------
num_cols = main.select_dtypes(include=[np.number]).columns
cat_cols = main.select_dtypes(include=["object"]).columns

main[num_cols] = main[num_cols].fillna(0)
for c in cat_cols:
    main[c] = main[c].fillna(main[c].mode()[0])

print("[INFO] Missing values filled.")

# -------------------------------
# DROP ID YANG TIDAK PERLU
# -------------------------------
main = main.drop(columns=["pit_id","stockpile","stockpile_id"], errors="ignore")
print("[INFO] ID columns dropped, ready for modeling.")

# -------------------------------
# SAVE FINAL MERGED DATASET
# -------------------------------
out_file = OUT / "merged_model_ready.csv"
main.to_csv(out_file, index=False)
print(f"[OK] Saved model-ready dataset -> {out_file}")
