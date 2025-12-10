import joblib
import os
from typing import Dict, List, Optional, Union
import warnings
import pandas as pd


class ModelService:
    
    def __init__(self, models_dir: str = "../all_dataset/models"):
        self.models_dir = models_dir
        self.production_model = None
        self.shipping_model = None
        self.production_features = None
        self.shipping_features = None
        
    def load_models(self):

        prod_path = os.path.join(self.models_dir, "rf_prod_full_dataset.joblib")
        ship_path = os.path.join(self.models_dir, "rf_shipping_model_full.joblib")

        if not os.path.exists(prod_path):
            raise FileNotFoundError(f"Production model not found: {prod_path}")
        if not os.path.exists(ship_path):
            raise FileNotFoundError(f"Shipping model not found: {ship_path}")
        
        self.production_model = joblib.load(prod_path)
        self.shipping_model = joblib.load(ship_path)
        
        # daftar fitur
        self.production_features = [
            'target_ton', 'progress_ratio', 'differential', 'utilization_pct',
            'planned_loading_ton', 'temp_avg_c', 'rain_peak_mm', 'humidity_avg_pct',
            'realized_ton_roll_4w', 'tonnage_moved_ton'
        ]
        
        self.shipping_features = [
            'weekly_ship_demand_ton', 'weekly_trips_total', 'supply_alignment_ratio',
            'truck_to_ship_utilization', 'avg_cycle_time_weighted', 'jetty_id_num',
            'weekly_truck_supply_ton_lag1', 'weekly_truck_supply_ton_roll4',
            'avg_cycle_time_min', 'tonnage_moved_ton'
        ]
    
    def _prepare_input(self, input_data, feature_list, model_type):
        """Siapkan input aman dan lengkap"""

        if isinstance(input_data, dict):
            input_data = [input_data]

        rows = []
        original = []

        for record in input_data:
            row = {}
            orig = {}

            for feature in feature_list:
                if feature not in record:
                    row[feature] = 0.0
                    orig[feature] = 0.0
                    warnings.warn(f"[{model_type}] Missing '{feature}', default=0.0")
                else:
                    row[feature] = record[feature]
                    orig[feature] = record[feature]

            rows.append(row)
            original.append(orig)

        df = pd.DataFrame(rows, columns=feature_list)
        return df, original
    
    def predict_production(self, input_data):
        if self.production_model is None:
            raise ValueError("Call load_models() first.")

        X, original = self._prepare_input(input_data, self.production_features, "production")
        preds = self.production_model.predict(X)

        return [{
            "prediction": float(p),
            "model_type": "production",
            "input_features": original[i]
        } for i, p in enumerate(preds)]
    
    def predict_shipping(self, input_data):
        if self.shipping_model is None:
            raise ValueError("Call load_models() first.")

        X, original = self._prepare_input(input_data, self.shipping_features, "shipping")
        preds = self.shipping_model.predict(X)

        return [{
            "prediction": float(p),
            "model_type": "shipping",
            "input_features": original[i]
        } for i, p in enumerate(preds)]
