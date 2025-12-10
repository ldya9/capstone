class OptimizationServiceV2:

    def optimize(self, prod_preds, ship_preds):
        results = {}


        # 1. PRODUCTION OPTIMIZER

        for idx, item in enumerate(prod_preds):

            base = item["prediction"]
            f = item["input_features"]  

            adj = base
            reason = []

            # --- cuaca ---
            rain = f.get("rain_peak_mm", 0)
            hum  = f.get("humidity_avg_pct", 0)

            if rain > 20:
                adj *= 0.70
                reason.append("Heavy rain reduces productivity (-30%)")
            elif rain > 10:
                adj *= 0.85
                reason.append("Moderate rain (-15%)")

            if hum > 85:
                adj *= 0.95
                reason.append("High humidity slows operations (-5%)")

            # --- utilization ---
            util = f.get("utilization_pct", 80)
            if util < 60:
                adj *= 0.90
                reason.append("Low equipment utilization (-10%)")
            elif util > 85:
                adj *= 1.05
                reason.append("High utilization (+5%)")

            # --- progress vs target ---
            prog = f.get("progress_ratio", 1)
            if prog < 0.8:
                adj *= 1.10
                reason.append("Low progress, need production boost (+10%)")
            elif prog > 1.1:
                adj *= 0.90
                reason.append("Ahead of target, reduce (-10%)")

            # --- rolling performance ---
            roll4 = f.get("realized_ton_roll_4w", base)
            if roll4 < base * 0.9:
                adj *= 0.95
                reason.append("Recent rolling performance weak (-5%)")
            elif roll4 > base * 1.1:
                adj *= 1.05
                reason.append("Recent rolling performance strong (+5%)")

            # --- tonnage moved ---
            moved = f.get("tonnage_moved_ton", 0)
            if moved < base * 0.7:
                adj *= 0.95
                reason.append("Low tonnage moved indicates bottleneck (-5%)")
            elif moved > base:
                adj *= 1.05
                reason.append("Massive haul movement (+5%)")

            results[f"pit_{idx+1}"] = {
                "predicted_production": base,
                "optimal_allocation": adj,
                "reasons": reason
            }

        # 2. SHIPPING OPTIMIZER
        if ship_preds:
            ship_item = ship_preds[0]
            base_ship = ship_item["prediction"]
            f = ship_item["input_features"]

            adj = base_ship
            notes = []

            cycle = f.get("avg_cycle_time_min", 70)
            util = f.get("truck_to_ship_utilization", 0.7)
            supply_align = f.get("supply_alignment_ratio", 1)
            lag1 = f.get("weekly_truck_supply_ton_lag1", base_ship)
            roll4 = f.get("weekly_truck_supply_ton_roll4", base_ship)

            # cycle time
            if cycle > 80:
                adj *= 0.85
                notes.append("High cycle time reduces shipping (-15%)")

            # truck utilization
            if util < 0.6:
                adj *= 0.9
                notes.append("Low truck-to-ship utilization (-10%)")

            # supply alignment
            if supply_align < 0.8:
                adj *= 0.9
                notes.append("Truck supply mismatch (-10%)")

            # rolling supply trend
            if lag1 < base_ship * 0.9:
                adj *= 0.9
                notes.append("Supply dropped last week (-10%)")
            if roll4 < base_ship * 0.85:
                adj *= 0.9
                notes.append("4-week rolling supply down (-10%)")

            results["shipping"] = {
                "predicted_shipping_capacity": base_ship,
                "optimal_shipping_capacity": adj,
                "reasons": notes
            }

        return results
