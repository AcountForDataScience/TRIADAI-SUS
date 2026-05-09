from typing import TypedDict
class Force(TypedDict):
    name: str
    params: dict[str, float]
    combat_keys: list[str]
    baseline_keys: list[str]

# class Forces(TypedDict):
#     name: str
#     force: Force
    
# force: Force = {
#     "name":,
#     "params":,
#     "combat_keys":,
#     "baseline_keys":
# }

# Example Forces

# region Ground Forces
Ground_Forces = {
    "Combat_unit_readiness": 0.75,
    "Armored_vehicle_availability": 0.70,
    "Artillery_readiness": 0.72,
    "Infantry_strength": 0.78,
    "Ammunition_sustainability": 0.65,
    "Mobility_capacity": 0.70,
    "Terrain_adaptability": 0.68,
    "Fire_support_availability": 0.73,
    "Command_stability": 0.80,
    "Logistics_resilience": 0.70,
    "Maintenance_capacity": 0.66,
    "Operational_tempo_sustainability": 0.69
}

Ground: Force = {
    "name": "Ground Forces",
    "params": Ground_Forces,
    "combat_keys":[
        "Combat_unit_readiness",
        "Armored_vehicle_availability",
        "Artillery_readiness",
        "Infantry_strength",
        "Ammunition_sustainability",
        "Mobility_capacity",
        "Terrain_adaptability",
        "Fire_support_availability"
    ],
    "baseline_keys":[
        "Command_stability",
        "Logistics_resilience",
        "Maintenance_capacity",
        "Operational_tempo_sustainability"
    ]
}
# endregion

# region Air Force
Air_Force = {
    "Aircraft_availability": 0.68,
    "Sortie_generation_rate": 0.64,
    "Air_defense_coverage": 0.72,
    "Pilot_readiness": 0.75,
    "Precision_strike_capability": 0.67,
    "Airbase_survivability": 0.62,
    "Fuel_sustainability": 0.66,
    "Maintenance_turnaround": 0.63,
    "Command_stability": 0.78,
    "Logistics_resilience": 0.69,
    "Maintenance_capacity": 0.65,
    "Operational_tempo_sustainability": 0.64
}

Airforce: Force = {
    "name": "Air Force",
    "params":Air_Force,
    "combat_keys":[
        "Aircraft_availability",
        "Sortie_generation_rate",
        "Air_defense_coverage",
        "Pilot_readiness",
        "Precision_strike_capability",
        "Airbase_survivability",
        "Fuel_sustainability",
        "Maintenance_turnaround"
    ],
    "baseline_keys":[
        "Command_stability",
        "Logistics_resilience",
        "Maintenance_capacity",
        "Operational_tempo_sustainability"
    ]
}
# endregion

# region Unmanned Systems Forces
Unmanned_Forces = {
    "Drone_availability": 0.77,
    "Operator_readiness": 0.74,
    "EW_resistance": 0.61,
    "Communication_reliability": 0.68,
    "ISR_coverage": 0.79,
    "Battery_power_sustainability": 0.66,
    "Autonomy_capability": 0.63,
    "Replacement_rate": 0.72,
    "Command_stability": 0.76,
    "Logistics_resilience": 0.67,
    "Maintenance_capacity": 0.64,
    "Operational_tempo_sustainability": 0.71
}

USF: Force = {
    "name":"Unmanned Systems Forces",
    "params":Unmanned_Forces,
    "combat_keys":[
        "Drone_availability",
        "Operator_readiness",
        "EW_resistance",
        "Communication_reliability",
        "ISR_coverage",
        "Battery_power_sustainability",
        "Autonomy_capability",
        "Replacement_rate"
    ],
    "baseline_keys":[
        "Command_stability",
        "Logistics_resilience",
        "Maintenance_capacity",
        "Operational_tempo_sustainability"
    ]
}
# endregion

# region Medical Forces
Medical_Forces = {
    "Medical_personnel_availability": 0.73,
    "Evacuation_capacity": 0.69,
    "Hospital_bed_capacity": 0.71,
    "Surgical_throughput": 0.68,
    "Medical_supply_sustainability": 0.66,
    "Transport_evacuation_time_efficiency": 0.64,
    "Recovery_rate": 0.72,
    "Staff_fatigue_resistance": 0.60,
    "Command_stability": 0.77,
    "Logistics_resilience": 0.70,
    "Maintenance_capacity": 0.62,
    "Operational_tempo_sustainability": 0.65
}

Medical: Force = {
    "name": "Medical Forces",
    "params": Medical_Forces,
    "combat_keys":[
        "Medical_personnel_availability",
        "Evacuation_capacity",
        "Hospital_bed_capacity",
        "Surgical_throughput",
        "Medical_supply_sustainability",
        "Transport_evacuation_time_efficiency",
        "Recovery_rate",
        "Staff_fatigue_resistance"
    ],
    "baseline_keys":[
        "Command_stability",
        "Logistics_resilience",
        "Maintenance_capacity",
        "Operational_tempo_sustainability"
    ]
}
# endregion
