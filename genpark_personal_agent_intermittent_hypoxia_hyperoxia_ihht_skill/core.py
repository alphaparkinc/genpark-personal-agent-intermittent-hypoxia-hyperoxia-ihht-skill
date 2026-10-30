# -*- coding: utf-8 -*-
"""Intermittent Hypoxia-Hyperoxia Therapy (IHHT) Simulator for GenPark Personal Agent."""
import json
from typing import Dict, Any

class IntermittentHypoxiaHyperoxiaSimulator:
    @staticmethod
    def simulate_ihht_hypoxic_interval_dose(hypoxic_fio2_pct: float, interval_duration_minutes: float, cycles_count: int, user_baseline_spo2: float = 98.0) -> Dict[str, Any]:
        # Standard sea level FiO2 = 20.9%
        delta_fio2 = max(0.0, 20.9 - hypoxic_fio2_pct)
        total_hypoxic_minutes = interval_duration_minutes * cycles_count
        hypoxic_dose_units = round(delta_fio2 * total_hypoxic_minutes, 1)
        
        # Target arterial SpO2 response
        target_spo2_min = max(78.0, round(user_baseline_spo2 - (delta_fio2 * 1.6), 1))
        
        if hypoxic_dose_units >= 200.0:
            induction = "ROBUST_HIF1A_STABILIZATION_AND_MITOPHAGY"
            mitochondrial_effect = "Triggers selective destruction of aged/mutated mitochondria; stimulates erythropoietin (EPO) and VEGF."
        elif hypoxic_dose_units >= 100.0:
            induction = "MODERATE_CELLULAR_ACCLIMATIZATION"
            mitochondrial_effect = "Enhances cellular antioxidant defense enzymes (SOD, catalase)."
        else:
            induction = "MILD_CONDITIONING"
            mitochondrial_effect = "Minimal transcriptional activation."

        return {
            "hypoxic_fraction_fio2_pct": hypoxic_fio2_pct,
            "hyperoxic_recovery_fio2_pct": 36.0,
            "cycles_planned": cycles_count,
            "total_hypoxia_time_minutes": total_hypoxic_minutes,
            "cumulative_hypoxic_dose": hypoxic_dose_units,
            "expected_spo2_nadir_pct": target_spo2_min,
            "mitochondrial_cleansing_tier": induction,
            "cellular_mechanism": mitochondrial_effect
        }

    @staticmethod
    def generate_ihht_session_safety_guards(resting_hr: float, age: int) -> Dict[str, Any]:
        max_safe_hr = int((220 - age) * 0.75)
        return {
            "emergency_hyperoxia_trigger_spo2_pct": 75.0,
            "maximum_allowable_tachycardia_bpm": max_safe_hr,
            "hyperoxic_switch_action": "Immediately switch gas supply to 36% O2 for 3 minutes if SpO2 drops below 75% for > 15 seconds.",
            "contraindications": "Absolute: Acute infections, severe uncontrolled COPD, active malignancy, severe cardiac arrhythmias."
        }
