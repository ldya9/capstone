from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

from core.models import ModelService
from core.optimization import OptimizationServiceV2


app = FastAPI(
    title="Mining Value Chain Optimization API",
    description="Production & Shipping Prediction + Optimization",
    version="1.0"
)

# --- init model & optimizer ---
model_service = ModelService(models_dir="all_dataset/models")
model_service.load_models()

optimizer = OptimizationServiceV2()


class ProductionInput(BaseModel):
    target_ton: float
    progress_ratio: float
    differential: float
    utilization_pct: float
    planned_loading_ton: float
    temp_avg_c: float
    rain_peak_mm: float
    humidity_avg_pct: float
    realized_ton_roll_4w: float
    tonnage_moved_ton: float

class ShippingInput(BaseModel):
    weekly_ship_demand_ton: float
    weekly_trips_total: float
    supply_alignment_ratio: float
    truck_to_ship_utilization: float
    avg_cycle_time_weighted: float
    jetty_id_num: float
    weekly_truck_supply_ton_lag1: float
    weekly_truck_supply_ton_roll4: float
    avg_cycle_time_min: float
    tonnage_moved_ton: float

class BatchProduction(BaseModel):
    data: List[ProductionInput]

class BatchShipping(BaseModel):
    data: List[ShippingInput]

# ---------------------------------------
# 4. Routes
# ---------------------------------------

@app.get("/")
def home():
    return {"message": "Mining Optimization API is running"}

@app.post("/predict/production")
def predict_production(payload: BatchProduction):
    data_dicts = [item.dict() for item in payload.data]
    preds = model_service.predict_production(data_dicts)
    return {"predictions": preds}


@app.post("/predict/shipping")
def predict_shipping(payload: BatchShipping):
    data_dicts = [item.dict() for item in payload.data]
    preds = model_service.predict_shipping(data_dicts)
    return {"predictions": preds}


@app.post("/optimize")
def optimize(payload: BatchProduction):
    data_dicts = [item.dict() for item in payload.data]
    preds = model_service.predict_production(data_dicts)
    results = optimizer.optimize(preds, [])
    return {"optimization": results}
