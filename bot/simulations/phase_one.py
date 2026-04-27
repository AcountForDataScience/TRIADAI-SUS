### imports
# import numpy as np
# import pandas as pd
import math, random, statistics
from enum import Enum


##----- Key Simulation Parameters -----##

# region Key Parameters
#--- Definitions ---#

## Достовірність розвідданих
class Intelligence_Confidence(Enum):
    # Defining the UPPER bound for each class
    HIGH    = (0.9,'90%')
    MEDIUM  = (0.5,'50%')
    LOW     = (0.2,'20%')

    def __init__(self, numeric_val, display_text):
      self._value_ = numeric_val  # This keeps intrinsic .value as a float
      self.display_name = display_text # And we still get pretty display name

    #classmethod adds support for intermediate risk levels.
    @classmethod
    def classify(cls, score: float):
        """Maps a float (0.0 - 1.0) to a RiskLevel."""
        for level in cls:
            if score <= level.value:
                return level
        return cls.HIGH  # Fallback for 1.0+

## Невизначеність / шум
class Volatility(Enum):
    # Defining the UPPER bound for each class
    HIGH    = (0.9,'High')
    MEDIUM  = (0.6,'Medium')
    LOW     = (0.3,'Low')

    def __init__(self, numeric_val, display_text):
      self._value_ = numeric_val  # This keeps intrinsic .value as a float
      self.display_name = display_text # And we still get pretty display name

    #classmethod adds support for intermediate risk levels.
    @classmethod
    def classify(cls, score: float):
        """Maps a float (0.0 - 1.0) to a RiskLevel."""
        for level in cls:
            if score <= level.value:
                return level
        return cls.HIGH  # Fallback for 1.0+

## Максимальний горизонт планування
Max_Planning_Time = 48

## Часовий тиск
class Time_Pressure(Enum):
    # Defining the UPPER bound for each class
    STRATEGIC   = (48,  'Strategic')
    OPERATIONAL = (6,   'Operational')
    CRISIS      = (0.5, 'Crisis')

    def __init__(self, numeric_val, display_text):
      self._value_ = numeric_val  # This keeps intrinsic .value as a float
      self.display_name = display_text # And we still get pretty display name

    #classmethod adds support for intermediate risk levels.
    @classmethod
    def classify(cls, score: float):
        """Maps a float (0.0 - 48) to a RiskLevel."""
        for level in cls:
            if score <= level.value:
                return level
        return cls.STRATEGIC  # Fallback for values over 48

## Індекс ризику
class Decision_Risk_Index(Enum):
    # Defining the UPPER bound for each class
    CONTROLLED    = (0.3, 'Controlled situation') # STABLE? 
    RISKY         = (0.6, 'Maneuver risk')
    CRISIS        = (0.8, 'Crisis mode')
    CRITICAL      = (1.0, 'Critical state')

    def __init__(self, numeric_val, display_text):
      self._value_ = numeric_val  # This keeps intrinsic .value as a float
      self.display_name = display_text # And we still get pretty display name

    #classmethod adds support for intermediate risk levels.
    @classmethod
    def classify(cls, score: float):
        """Maps a float (0.0 - 1.0) to a RiskLevel."""
        for level in cls:
            if score <= level.value:
                return level
        return cls.CRITICAL  # Fallback for 1.0+
# endregion

# region Shuffle parameters
#--- Shuffle scenario parameters ---#
def Shuffling_IC_V_TP(
    Intelligence_Confidence: Enum,
    Volatility: Enum,
    Time_Pressure: Enum,):
    # Enums don't use .keys(), you just cast the class to a list
    IC_member = random.choice(list(Intelligence_Confidence))
    V_member = random.choice(list(Volatility))
    TP_member = random.choice(list(Time_Pressure))

    return IC_member, V_member, TP_member
# endregion

# region tests
#--- test outputs ---#
# Intelligence_Confidence_key, Volatility_key, Time_Pressure_key = Shuffling_IC_V_TP(Intelligence_Confidence, Volatility, Time_Pressure)

# print(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
# print(Intelligence_Confidence_key.display_name, Volatility_key.display_name, Time_Pressure_key.display_name)

# IC = Intelligence_Confidence_key.value
# V = Volatility_key.value
# available_time = Time_Pressure_key.value
# TP = 1 - (available_time / Max_Planning_Time)

# ##w1, w2, w3 — ваги (наприклад по 0.33)
# w1, w2, w3 = 0.33, 0.33, 0.33
# # Decision_Risk_Index = (1 - IC) * w1 + V * w2 + TP * w3

# DRI = (1 - IC) * w1 + V * w2 + TP * w3
# DRI = Decision_Risk_Index.classify(DRI)
# print('Decision_Risk_Index: ' + DRI.display_name)

# endregion

# region CoA settings
# COA_settings = {
#     "Attack": {"V_multiplier": 1.15, "time_multiplier": 0.8},
#     "Regroup": {"V_multiplier": 0.85, "time_multiplier": 1.2}
# }
# endregion

# print("Key Parameters tested")

##----- Monte Carlo (fixed scenario) -----##

# region Monte Carlo

def Monte_Carlo_DRI_fixed_keys(
    Intelligence_Confidence: Enum,
    Volatility: Enum,
    Time_Pressure: Enum,
    Max_Planning_Time=48,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0  # години шуму для available_time
):
    # базові значення сценарію
    base_IC = Intelligence_Confidence.value
    base_V = Volatility.value
    base_available_time = Time_Pressure.value

    # базовий TP і DRI (без шуму)
    base_TP = 1 - (base_available_time / Max_Planning_Time)
    base_dri = (1 - base_IC) * w1 + base_V * w2 + base_TP * w3

    dris = []
    levels = {state: 0 for state in Decision_Risk_Index}
    # levels = {"Situation under control": 0, "Maneuver risk": 0, "Crisis mode": 0, "Critical state": 0}

    for _ in range(n):
        # шум навколо IC/V
        IC = min(1.0, max(0.0, random.uniform(base_IC - noise_ic, base_IC + noise_ic)))
        V = min(1.0, max(0.0, random.uniform(base_V - noise_v, base_V + noise_v)))

        # шум навколо часу (години), потім нормалізація в TP
        available_time = max(0.0, random.uniform(base_available_time - noise_time, base_available_time + noise_time))
        TP = 1 - (available_time / Max_Planning_Time)
        TP = min(1.0, max(0.0, TP))

        dri = (1 - IC) * w1 + V * w2 + TP * w3
        dris.append(dri)

        lvl = Decision_Risk_Index.classify(dri)
        levels[lvl] += 1

    dris.sort()
    mean_dri = statistics.mean(dris)
    p90 = dris[int(0.90 * (n - 1))]

    level_share = {k: v / n for k, v in levels.items()}

    return {
        "n": n,
        "scenario": {
            "IC": base_IC,
            "V": base_V,
            "available_time": base_available_time,
            "TP": base_TP,
        },
        "base_dri": base_dri,
        "mean_dri": mean_dri,
        "p90": p90,
        "level_share": level_share,
        "critical_tail": level_share[Decision_Risk_Index.CRITICAL],
        "crisis_or_worse": level_share[Decision_Risk_Index.CRISIS] + level_share[Decision_Risk_Index.CRITICAL],
    }

# endregion

# mc = Monte_Carlo_DRI_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key,Max_Planning_Time)
# print(f"raw:\n{mc}")

# print("Monte-Carlo tested")

# region Monte Carlo compare CoA
def Monte_Carlo_Compare_COA_fixed_keys(
    Intelligence_Confidence: Enum,
    Volatility: Enum,
    Time_Pressure: Enum,
    Max_Planning_Time=48,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0,
    COA_settings=None
):
    # дефолтні налаштування COA
    if COA_settings is None:
        COA_settings = {
            "Attack": {
                "V_multiplier": 1.15,
                "time_multiplier": 0.8
            },
            "Regroup": {
                "V_multiplier": 0.85,
                "time_multiplier": 1.2
            }
            # якщо треба — легко додати "Оборона": {...}
        }

    # БАЗА сценарію (фіксована)
    base_IC = Intelligence_Confidence.value
    base_V = Volatility.value
    base_available_time = Time_Pressure.value

    results = {}

    for coa_name, settings in COA_settings.items():
        dris = []
        levels = {state: 0 for state in Decision_Risk_Index}


        for _ in range(n):
            # 1) шум навколо IC/V/Time саме цього сценарію
            IC = min(1.0, max(0.0, random.uniform(base_IC - noise_ic, base_IC + noise_ic)))
            V0 = min(1.0, max(0.0, random.uniform(base_V  - noise_v,  base_V  + noise_v)))

            t0 = max(0.0, random.uniform(base_available_time - noise_time, base_available_time + noise_time))

            # 2) застосовуємо COA-мультиплікатори
            V = V0 * settings["V_multiplier"]
            V = min(1.0, max(0.0, V))

            available_time = t0 * settings["time_multiplier"]
            available_time = min(Max_Planning_Time, max(0.1, available_time))

            TP = 1 - (available_time / Max_Planning_Time)
            TP = min(1.0, max(0.0, TP))

            # 3) DRI
            dri = (1 - IC) * w1 + V * w2 + TP * w3
            dris.append(dri)

            lvl = Decision_Risk_Index.classify(dri)
            levels[lvl] += 1

        dris.sort()

        results[coa_name] = {
            "Mean_DRI": statistics.mean(dris),
            "P90": dris[int(0.90 * (n - 1))], # cast to int to avoid float type index
            "Critical_%": levels[Decision_Risk_Index.CRITICAL] / n,
            "Crisis_%": levels[Decision_Risk_Index.CRISIS] / n,
            "Stable_%": levels[Decision_Risk_Index.CONTROLLED] / n,
            "Maneuver_%": levels[Decision_Risk_Index.RISKY] / n,
        }

    # Рекомендація: нижчий P90, а при рівності — нижчий Critical хвіст
    coa_names = list(results.keys())
    best = min(
        coa_names,
        key=lambda name: (results[name]["P90"], results[name]["Critical_%"])
    )

    return results, best
# endregion

# results, best = Monte_Carlo_Compare_COA_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key,Max_Planning_Time)
# print(f"results: {results}\n with best being {best}.")
# # print(format_coa_message((Intelligence_Confidence_key, Volatility_key, Time_Pressure_key),results,best))

# print("CoA tested")

# region Monte Carlo compare WinProb
def Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(
    Intelligence_Confidence: Enum,
    Volatility: Enum,
    Time_Pressure: Enum,
    Max_Planning_Time=48,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    k=8,
    threshold=0.6,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0,
    COA_settings=None
):
    results = {}

    if COA_settings is None:
        COA_settings = {
            "Attack": {"V_multiplier": 1.15, "time_multiplier": 0.8},
            "Regroup": {"V_multiplier": 0.85, "time_multiplier": 1.2}
        }

    # ---- БАЗА (фіксований сценарій) ----
    base_IC = Intelligence_Confidence.value
    base_V = Volatility.value
    base_available_time = Time_Pressure.value

    def Win_Probability_From_DRI(dri: float) -> float:
        # DRI ↑ -> WinProb ↓ ; при dri == threshold => 0.5
        return 1.0 / (1.0 + math.exp(k * (dri - threshold)))

    for coa_name, settings in COA_settings.items():
        dris = []
        win_probs = []

        levels = {state: 0 for state in Decision_Risk_Index}

        for _ in range(n):
            # 1) шум навколо IC/V/Time саме цього сценарію
            IC = min(1.0, max(0.0, random.uniform(base_IC - noise_ic, base_IC + noise_ic)))
            V0 = min(1.0, max(0.0, random.uniform(base_V  - noise_v,  base_V  + noise_v)))
            t0 = max(0.0, random.uniform(base_available_time - noise_time, base_available_time + noise_time))

            # 2) COA-ефекти
            V = min(1.0, max(0.0, V0 * settings["V_multiplier"]))
            available_time = min(Max_Planning_Time, max(0.1, t0 * settings["time_multiplier"]))

            TP = 1 - (available_time / Max_Planning_Time)
            TP = min(1.0, max(0.0, TP))

            # 3) DRI
            dri = (1 - IC) * w1 + V * w2 + TP * w3
            dris.append(dri)

            lvl = Decision_Risk_Index.classify(dri)
            levels[lvl] += 1

            # 4) WinProb
            win_probs.append(Win_Probability_From_DRI(dri))

        dris.sort()
        win_probs.sort()

        # індекси квантилів коректно через (n-1)
        i10 = int(0.10 * (n - 1))
        i50 = int(0.50 * (n - 1))
        i90 = int(0.90 * (n - 1))

        results[coa_name] = {
            "Mean_DRI": statistics.mean(dris),
            "P90_DRI": dris[i90],
            "Critical_%": levels[Decision_Risk_Index.CRITICAL] / n,
            "Crisis_%"  : levels[Decision_Risk_Index.CRISIS] / n,
            "Maneuver_%": levels[Decision_Risk_Index.RISKY] / n,
            "Stable_%"  : levels[Decision_Risk_Index.CONTROLLED] / n,

            "WinProb_Mean": statistics.mean(win_probs),
            "WinProb_P10": win_probs[i10],
            "WinProb_P50": win_probs[i50],
            "WinProb_P90": win_probs[i90],
        }

    # ---- Рекомендація (можеш змінювати критерій) ----
    # інтегральний: WinProb_mean - Critical_tail (як у тебе)
    scores = {
        coa: results[coa]["WinProb_Mean"] - results[coa]["Critical_%"]
        for coa in results
    }
    best = max(scores.keys(), key=lambda c: scores[c])



    return results, best
# endregion

# results, best = Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
# recommendation = (
#     f"According to integral criterion (WinProb_mean − Critical_tail) best course of action is: **{best}**."
# )

# print(f"{results}\nbest: {best}")
# print("Win Probability tested")

# region Sensitivity Analysis
def _rank_list(values):
    sorted_idx = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)

    i = 0
    while i < len(values):
        j = i
        while j + 1 < len(values) and values[sorted_idx[j+1]] == values[sorted_idx[i]]:
            j += 1
        avg_rank = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[sorted_idx[k]] = avg_rank
        i = j + 1

    return ranks


def _pearson_corr(x, y):
    mx = statistics.mean(x)
    my = statistics.mean(y)

    num = sum((a - mx) * (b - my) for a, b in zip(x, y))
    denx = math.sqrt(sum((a - mx) ** 2 for a in x))
    deny = math.sqrt(sum((b - my) ** 2 for b in y))

    if denx == 0 or deny == 0:
        return 0.0

    return num / (denx * deny)


def Sensitivity_Analysis_DRI_fixed_keys(
    Intelligence_Confidence: Enum|int|float,
    Volatility: Enum|int|float,
    Time_Pressure: Enum|int|float,
    Max_Planning_Time=48,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0
):
    """
    Scenario sensitivity (fixed_keys):
    - беремо один сценарій (IC/V/Time) як базу
    - далі симулюємо невизначеність шумом і дивимось, що найбільше рухає DRI
    """
    # region validating inputs
    # Intelligence Confidence
    if isinstance(Intelligence_Confidence,Enum):
        base_IC = Intelligence_Confidence.value
    elif isinstance(Intelligence_Confidence,int|float):
        base_IC = Intelligence_Confidence
    else:
        raise TypeError(f"Expected numeric or Enum, got {type(Intelligence_Confidence).__name__}") 
    # Volatility
    if isinstance(Volatility,Enum):
        base_V = Volatility.value
    elif isinstance(Volatility,int|float):
        base_V = Volatility
    else:
        raise TypeError(f"Expected int or Enum, got {type(Volatility).__name__}") 
    # Time Pressure
    if isinstance(Time_Pressure,Enum):
        base_available_time = Time_Pressure.value
    elif isinstance(Time_Pressure,int|float):
        base_available_time = Time_Pressure
    else:
        raise TypeError(f"Expected int or Enum, got {type(Time_Pressure).__name__}") 
    
    # endregion

    IC_list, V_list, TP_list, DRI_list = [], [], [], []

    for _ in range(n):
        IC = min(1.0, max(0.0, random.uniform(base_IC - noise_ic, base_IC + noise_ic)))
        V  = min(1.0, max(0.0, random.uniform(base_V  - noise_v,  base_V  + noise_v)))

        available_time = max(0.0, random.uniform(base_available_time - noise_time, base_available_time + noise_time))
        available_time = min(Max_Planning_Time, max(0.1, available_time))

        TP = 1 - (available_time / Max_Planning_Time)
        TP = min(1.0, max(0.0, TP))

        dri = (1 - IC) * w1 + V * w2 + TP * w3

        IC_list.append(IC)
        V_list.append(V)
        TP_list.append(TP)
        DRI_list.append(dri)

    # Spearman = Pearson по рангах (твої helper-и)
    rIC = _pearson_corr(_rank_list(IC_list), _rank_list(DRI_list))
    rV  = _pearson_corr(_rank_list(V_list),  _rank_list(DRI_list))
    rTP = _pearson_corr(_rank_list(TP_list), _rank_list(DRI_list))

    strengths = {"IC": abs(rIC), "V": abs(rV), "TP": abs(rTP)}
    total = sum(strengths.values()) if sum(strengths.values()) != 0 else 1.0
    share = {k: v / total for k, v in strengths.items()}
    score = {k: v * v / total for k, v in strengths.items()} #share x spearman

    dri_sorted = sorted(DRI_list)

    return {
        "n": n,
        "scenario": {
            "IC_key": Intelligence_Confidence,
            "V_key": Volatility,
            "TP_key": Time_Pressure,
        },
        "spearman_corr": {"IC": rIC, "V": rV, "TP": rTP},
        "influence_share": share,
        "combined_score": score,
        "DRI_mean": statistics.mean(DRI_list),
        "DRI_p90": dri_sorted[int(0.90 * (n - 1))]
    }
# endregion

# print(Sensitivity_Analysis_DRI_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key))

# print("Sensitivity Analysis tested")



