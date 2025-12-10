#!/usr/bin/env python3
"""
validate_fe.py

Cek konsistensi semua Feature Engineering dataset:
- Kolom ada sesuai ekspektasi
- Tipe data benar
- Placeholder domain lengkap
- Missing values overview
"""

import pandas as pd
from pathlib import Path

# PATH CONFIG
BASE = Path("../all_dataset")
FE_DIR = BASE / "feature_dataset"

# Daftar file FE
fe_files = {
    "production": FE_DIR / "production_fe.csv",
    "fleet": FE_DIR / "fleet_fe.csv",
    "heavy_equipment": FE_DIR / "heavy_equipment_fe.csv",
    "stockpile": FE_DIR / "stockpile_fe.csv",
    "ship_schedule": FE_DIR / "ship_schedule_fe.csv",
    "truck_to_ship": FE_DIR / "truck_to_ship_fe.csv",
    "weather": FE_DIR / "weather.csv",
    "road": FE_DIR / "road_fe.csv"
}

# Placeholder kolom per domain (cek konsistensi)
expected_cols = {
    "production": [
        "week_start","pit_id","realized_ton","target_ton","progress_ratio",
        "differential","realized_vs_capacity_ratio","capacity_utilization_change",
        "equipment_supply_index","breakdown_impact",
        "realized_ton_lag1","realized_ton_lag2","realized_ton_roll_4w"
    ],
    "fleet": [
        "week_start","pit_id","effective_capacity_ton","total_active_equipment",
        "avg_operating_hours","breakdown_trucks","predicted_repair_hours"
    ],
    "heavy_equipment": [
        "week_start","pit_id","excavator_active","dozer_active","grader_active",
        "total_active_equipment","avg_operating_hours","fuel_burn_rate_lph",
        "avg_operating_hours_lag1","avg_operating_hours_lag2",
        "fuel_burn_rate_lph_roll_4w"
    ],
    "stockpile": [
        "week_start","stockpile_id","current_stock_ton","stock_after_loading_ton",
        "stock_change","shortage_flag","rolling_sum_inflow_4w","rolling_sum_outflow_4w",
        "cumulative_deficit"
    ],
    "ship_schedule": [
        "week_start","jetty_id","planned_load","ship_required_ton",
        "stock_after_vs_demand","ship_to_stock_ratio","reallocation_needed_flag",
        "queued_ships_estimate"
    ],
    "truck_to_ship": [
        "week_start","truck_id","jetty_id","tonnage_moved_ton","trip_count",
        "weekly_truck_supply_ton","weekly_ship_demand_ton","supply_alignment_ratio",
        "estimated_queue_hours","truck_to_ship_utilization","reassign_flag"
    ],
    "weather": [
        "location","week_start","operational_weather_index","weather_lag1","weather_trend_4w"
    ],
    "road": [
        "week_start","segment_id","road_condition_score","cycle_time_h","road_penalty"
    ]
}

# Fungsi cek konsistensi
def check_fe_consistency(name, path, expected):
    if not path.exists():
        print(f"❌ {name} FE file tidak ditemukan di {path}")
        return None
    
    # Load CSV dulu tanpa parse_dates
    df = pd.read_csv(path)
    
    # Jika week_start ada di file, convert ke datetime
    if "week_start" in df.columns:
        df["week_start"] = pd.to_datetime(df["week_start"], errors="coerce")
    
    # Cek kolom
    missing_cols = [c for c in expected if c not in df.columns]
    if missing_cols:
        print(f"⚠ {name}: kolom hilang -> {missing_cols}")
    else:
        print(f"✅ {name}: semua kolom ekspektasi ada")
    
    # Cek tipe data numerik vs object
    for col in df.columns:
        if df[col].dtype == "object":
            print(f"⚠ {name}: kolom {col} bertipe object, cek apakah seharusnya numerik")
    
    # Missing values summary
    missing_count = df.isna().sum()
    if missing_count.sum() > 0:
        print(f"ℹ {name}: ada missing values")
        print(missing_count[missing_count > 0])
    else:
        print(f"✅ {name}: tidak ada missing values")
    
    return df


# Loop semua FE
for k, f in fe_files.items():
    check_fe_consistency(k, f, expected_cols.get(k, []))
