import numpy as np

from simulations.forces import Force

def Monte_Carlo_Strategic_Readiness(
        # force_name : str,
        params: dict[str, float],
        combat_keys: list[str],
        baseline_keys: list[str],
        n_simulations=10000,
        variation=0.10,
        combat_weight=0.7,
        baseline_weight=0.3,
        ) -> dict[str, str|float|dict[str, float]]:

    results = []

    for _ in range(n_simulations):

        simulated = {}

        # simulate uncertainty for each parameter
        for key, value in params.items():
            simulated[key] = np.clip(
                np.random.normal(loc=value, scale=variation),
                0,
                1
            )

        # compute sub-indexes
        combat_power = np.mean([simulated[k] for k in combat_keys])
        system_readiness = np.mean([simulated[k] for k in baseline_keys])

        # final strategic readiness index
        sri = combat_weight * combat_power + baseline_weight * system_readiness

        results.append(sri)

    results = np.array(results)

    # readiness level shares
    level_share = {
        "high_readiness": float(np.mean(results >= 0.8)),
        "maneuver_readiness": float(np.mean((results >= 0.6) & (results < 0.8))),
        "crisis_readiness": float(np.mean((results >= 0.4) & (results < 0.6))),
        "critical_readiness": float(np.mean(results < 0.4))
    }

    return {
        # "force_name": force_name,
        "mean_sri": float(np.mean(results)),
        "p10": float(np.percentile(results, 10)),
        "p50_median": float(np.percentile(results, 50)),
        "p90": float(np.percentile(results, 90)),
        "min_sri": float(np.min(results)),
        "max_sri": float(np.max(results)),
        "crisis_probability": float(np.mean(results < 0.6)),
        "critical_probability": float(np.mean(results < 0.4)),
        "level_share": level_share
    }

def Monte_Carlo_Strategic_Readiness_All_Forces(
        forces_config: dict[str,Force],
        n_simulations=10000,
        variation=0.10,
        combat_weight=0.7,
        baseline_weight=0.3) -> dict[str,dict]:
    all_results = {}

    for force_name, config in forces_config.items():
        result = Monte_Carlo_Strategic_Readiness(
            # force_name=force_name,
            params=config["params"],
            combat_keys=config["combat_keys"],
            baseline_keys=config["baseline_keys"],
            n_simulations=n_simulations,
            variation=variation,
            combat_weight=combat_weight,
            baseline_weight=baseline_weight
        )
        all_results[force_name] = result

    return all_results

# import forces

# forces_config : dict[str,forces.Force] = {
#     forces.Airforce["name"] : forces.Airforce,
#     forces.Medical["name"] : forces.Medical
# }

# print("=====loop=====")
# for force_name, config in forces_config.items():
#     print("===" + force_name + "===")
#     # print(config)
#     print(config["params"])

# forces_config = [forces.Airforce, forces.Medical]

# print("=====loop=====")
# for force in forces_config:
#     print(force["name"])
#     print(force["params"])
#     print(force["combat_keys"])
#     print(force["baseline_keys"])

# Ground_Forces = {
#     "Combat_unit_readiness": 0.75,
#     "Armored_vehicle_availability": 0.70,
#     "Artillery_readiness": 0.72,
#     "Infantry_strength": 0.78,
#     "Ammunition_sustainability": 0.65,
#     "Mobility_capacity": 0.70,
#     "Terrain_adaptability": 0.68,
#     "Fire_support_availability": 0.73,
#     "Command_stability": 0.80,
#     "Logistics_resilience": 0.70,
#     "Maintenance_capacity": 0.66,
#     "Operational_tempo_sustainability": 0.69
# }

# from typing import TypedDict
# class Force(TypedDict):
#     name: str
#     params: dict[str, float]
#     combat_keys: list[str]
#     baseline_keys: list[str]

# class Forces(TypedDict):
#     name: str
#     force: Force


# Ground: Force = {
#     "name": "Ground Forces",
#     "params": Ground_Forces,
#     "combat_keys":[
#         "Armored_vehicle_availability",
#         "Infantry_strength",
#         "Ammunition_sustainability",
#         "Terrain_adaptability",
#         "Fire_support_availability",
#         "Logistics_resilience",
#         "Maintenance_capacity",
#         ],
#     "baseline_keys":[
#         "Combat_unit_readiness",
#         "Artillery_readiness",
#         "Mobility_capacity",
#         "Command_stability",
#         "Operational_tempo_sustainability",
#         ]
# }
# # print(Ground)
# # print(Monte_Carlo_Strategic_Readiness(Ground["name"],Ground["params"],Ground["combat_keys"],Ground["baseline_keys"]))

