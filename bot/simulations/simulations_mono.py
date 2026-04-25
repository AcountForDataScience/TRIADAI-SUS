### imports
# some basic utils
import os
import csv
import datetime

#data and calculations - mostly unused here
# import numpy as np
import pandas as pd
import math
import random
import statistics
from enum import Enum

#telebot necessities
import telebot
from telebot import types
from telebot.util import quick_markup, generate_random_token
from telebot.formatting import escape_markdown

# @title

if os.getenv('RENDER') == "True":
    print("Running on Render")
else:
    from dotenv import load_dotenv
    load_dotenv()
# changing dictionaries to Enums

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
    CONTROLlED    = (0.3, 'Controlled situation')
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
    

## Достовірність розвідданих
Intelligence_Confidence_dic = {
    "90%": 0.9,
    "50%": 0.5,
    "20%": 0.2
}

## Невизначеність / шум
Volatility_dic = {
    "Low": 0.3,
    "Medium": 0.6,
    "High": 0.9
}

## Максимальний горизонт планування
Max_Planning_Time = 48

## Часовий тиск
Time_Pressure_dic = {
    "Strategic Analysis": 48,
    "Operational level": 6,
    "Crisis decision": 0.5
}

#enum shuffling
def Shuffling_IC_V_TP(IC_Enum, V_Enum, TP_Enum):
    # Enums don't use .keys(), you just cast the class to a list
    IC_member = random.choice(list(IC_Enum))
    V_member = random.choice(list(V_Enum))
    TP_member = random.choice(list(TP_Enum))

    return IC_member, V_member, TP_member

Intelligence_Confidence_key, Volatility_key, Time_Pressure_key = Shuffling_IC_V_TP(Intelligence_Confidence, Volatility, Time_Pressure)

print(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
print(Intelligence_Confidence_key.name, Volatility_key.name, Time_Pressure_key.name)

IC = Intelligence_Confidence_key.value
V = Volatility_key.value
available_time = Time_Pressure_key.value
TP = 1 - (available_time / Max_Planning_Time)

##w1, w2, w3 — ваги (наприклад по 0.33)
w1, w2, w3 = 0.33, 0.33, 0.33
# Decision_Risk_Index = (1 - IC) * w1 + V * w2 + TP * w3

DRI = (1 - IC) * w1 + V * w2 + TP * w3
print('Decision_Risk_Index: ' + str(DRI))

# print('Decision_Risk_Index: ' + str(Decision_Risk_Index))


# def get_DRI_level(Decision_Risk_Index):
#     if Decision_Risk_Index < 0.3:
#         return "Situation under control"
#     elif Decision_Risk_Index < 0.6:
#         return "Maneuver risk"
#     elif Decision_Risk_Index < 0.8:
#         return "Crisis mode"
#     else:
#         return "Critical state"
# print(get_DRI_level(Decision_Risk_Index))

print(Decision_Risk_Index.classify(DRI).display_name)

def Shuffling_IC_V_TP(Intelligence_Confidence_dic , Volatility_dic, Time_Pressure_dic):

  Intelligence_Confidence_key = random.choice(list(Intelligence_Confidence_dic.keys()))
  Volatility_key = random.choice(list(Volatility_dic.keys()))
  Time_Pressure_key = random.choice(list(Time_Pressure_dic.keys()))

  return Intelligence_Confidence_key, Volatility_key, Time_Pressure_key

Intelligence_Confidence_key, Volatility_key, Time_Pressure_key = Shuffling_IC_V_TP(Intelligence_Confidence_dic , Volatility_dic, Time_Pressure_dic)

print(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
print(Intelligence_Confidence_dic[Intelligence_Confidence_key], Volatility_dic[Volatility_key],Time_Pressure_dic[Time_Pressure_key])

IC = Intelligence_Confidence_dic[Intelligence_Confidence_key]
V = Volatility_dic[Volatility_key]
available_time = Time_Pressure_dic[Time_Pressure_key]
TP = 1 - (available_time / Max_Planning_Time)

##w1, w2, w3 — ваги (наприклад по 0.33)
w1, w2, w3 = 0.33, 0.33, 0.33
Decision_Risk_Index = (1 - IC) * w1 + V * w2 + TP * w3

print('Decision_Risk_Index: ' + str(Decision_Risk_Index))

def get_DRI_level(Decision_Risk_Index):
    if Decision_Risk_Index < 0.3:
        return "Situation under control"
    elif Decision_Risk_Index < 0.6:
        return "Maneuver risk"
    elif Decision_Risk_Index < 0.8:
        return "Crisis mode"
    else:
        return "Critical state"
print(get_DRI_level(Decision_Risk_Index))

# -------------------------
# 1) Сценарій (одна комбінація)
# -------------------------
def Shuffling_IC_V_TP(Intelligence_Confidence_dic, Volatility_dic, Time_Pressure_dic):
    Intelligence_Confidence_key = random.choice(list(Intelligence_Confidence_dic.keys()))
    Volatility_key = random.choice(list(Volatility_dic.keys()))
    Time_Pressure_key = random.choice(list(Time_Pressure_dic.keys()))
    return Intelligence_Confidence_key, Volatility_key, Time_Pressure_key


# -------------------------
# 2) Рівні DRI
# -------------------------
def get_DRI_level(Decision_Risk_Index: float) -> str:
    if Decision_Risk_Index < 0.3:
        return "Situation under control"
    elif Decision_Risk_Index < 0.6:
        return "Maneuver risk"
    elif Decision_Risk_Index < 0.8:
        return "Crisis mode"
    else:
        return "Critical state"


# -------------------------
# 3) Monte Carlo навколо ФІКСОВАНОГО сценарію
# -------------------------
def Monte_Carlo_DRI_fixed_keys(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time,
    Intelligence_Confidence_key,
    Volatility_key,
    Time_Pressure_key,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0  # години шуму для available_time
):
    # базові значення сценарію
    base_IC = Intelligence_Confidence_dic[Intelligence_Confidence_key]
    base_V = Volatility_dic[Volatility_key]
    base_available_time = Time_Pressure_dic[Time_Pressure_key]

    # базовий TP і DRI (без шуму)
    base_TP = 1 - (base_available_time / Max_Planning_Time)
    base_dri = (1 - base_IC) * w1 + base_V * w2 + base_TP * w3

    dris = []
    levels = {"Situation under control": 0, "Maneuver risk": 0, "Crisis mode": 0, "Critical state": 0}

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

        lvl = get_DRI_level(dri)
        levels[lvl] += 1

    dris.sort()
    mean_dri = statistics.mean(dris)
    p90 = dris[int(0.90 * (n - 1))]

    level_share = {k: v / n for k, v in levels.items()}

    return {
        "n": n,
        "scenario": {
            "IC_key": Intelligence_Confidence_key,
            "V_key": Volatility_key,
            "TP_key": Time_Pressure_key,
            "IC": base_IC,
            "V": base_V,
            "available_time": base_available_time,
            "TP": base_TP,
        },
        "base_dri": base_dri,
        "mean_dri": mean_dri,
        "p90": p90,
        "level_share": level_share,
        "critical_tail": level_share["Critical state"],
        "crisis_or_worse": level_share["Crisis mode"] + level_share["Critical state"],
    }


# -------------------------
# 4) Форматування відповіді для Telegram
# -------------------------
def format_phase1_message(mc_result: dict) -> str:
    sc = mc_result["scenario"]

    # красиві % для IC (якщо ключі типу "50%" — просто показуємо ключ)
    ic_label = sc["IC_key"]
    v_label = sc["V_key"]
    t_label = sc["TP_key"]

    mean_dri = mc_result["mean_dri"]
    p90 = mc_result["p90"]
    base_dri = mc_result["base_dri"]

    crisis_or_worse = mc_result["crisis_or_worse"] * 100
    critical_tail = mc_result["critical_tail"] * 100

    return (
        "🛰️ Phase 1 — Reconnaisance (mission scenario)\n"
        f"Scenario: IC={ic_label}, Volatility={v_label}, Time={t_label}\n\n"
        "📌 Decision Risk Index (DRI)\n"
        f"• Base DRI: {base_dri:.3f} ({get_DRI_level(base_dri)})\n"
        f"• Mean DRI (MC): {mean_dri:.3f}\n"
        f"• P90 DRI (MC): {p90:.3f}\n\n"
        "⚠️ Risk level probability (Monte Carlo)\n"
        f"• Crisis+Critical: {crisis_or_worse:.1f}%\n"
        f"• Critical tail: {critical_tail:.1f}%\n"
    )


# -------------------------
# 5) One-shot: обрати сценарій + порахувати + текст
# -------------------------
def run_phase1(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0
) -> str:
    IC_key, V_key, TP_key = Shuffling_IC_V_TP(Intelligence_Confidence_dic, Volatility_dic, Time_Pressure_dic)

    mc = Monte_Carlo_DRI_fixed_keys(
        Intelligence_Confidence_dic=Intelligence_Confidence_dic,
        Volatility_dic=Volatility_dic,
        Time_Pressure_dic=Time_Pressure_dic,
        Max_Planning_Time=Max_Planning_Time,
        Intelligence_Confidence_key=IC_key,
        Volatility_key=V_key,
        Time_Pressure_key=TP_key,
        n=n,
        w1=w1, w2=w2, w3=w3,
        noise_ic=noise_ic, noise_v=noise_v, noise_time=noise_time
    )

    return format_phase1_message(mc)


def explain_monte_carlo_phase1(
    n: int = 5000,
    Max_Planning_Time: int | float = 48,
    w1: float = 0.33,
    w2: float = 0.33,
    w3: float = 0.33,
    noise_ic: float = 0.05,
    noise_v: float = 0.05,
    noise_time: float = 1.0,
    lang: str = "en"
) -> str:
    """
    Повертає коротке пояснення Monte Carlo для ФАЗИ 1 (для Telegram/AR).
    lang: "uk" або "en"
    """

    if lang.lower() == "en":
        return (
            "ℹ️ How Monte Carlo works (Phase 1 — Recon)\n"
            f"• Step 1: The bot picks ONE mission scenario: IC / Volatility / Available time.\n"
            f"• Step 2: We run {n} simulations around that scenario, adding uncertainty (noise):\n"
            f"  - IC varies by ±{noise_ic:.2f}\n"
            f"  - Volatility varies by ±{noise_v:.2f}\n"
            f"  - Available time varies by ±{noise_time:.1f}h\n"
            f"• Step 3: Each run computes DRI using weights w1={w1:.2f}, w2={w2:.2f}, w3={w3:.2f} "
            f"and Max planning time = {Max_Planning_Time}h.\n\n"
            "✅ Output:\n"
            "• Base DRI (no-noise scenario)\n"
            "• Mean DRI (average over all runs)\n"
            "• P90 DRI (bad-tail risk)\n"
            "• Crisis+Critical % and Critical tail %\n"
            "Meaning: not one forecast — a risk distribution under uncertainty."
        )

    # default: Ukrainian
    return (
        "ℹ️ Як працює Monte Carlo (ФАЗА 1 — Розвідка)\n"
        "• Крок 1: Бот обирає ОДИН сценарій місії: Достовірність розвідданих(Intelligence_Confidence - IC) / Невизначеність або шум(Volatility) / Доступное время(Available time).\n"
        f"• Крок 2: Запускаємо {n} симуляцій навколо цього сценарію, додаючи невизначеність (шум):\n"
        f"  - Достовірність розвідданих(IC) коливається на ±{noise_ic:.2f}\n"
        f"  - Невизначеність (Volatility) коливається на ±{noise_v:.2f}\n"
        f"  - Доступний час коливається на ±{noise_time:.1f} год\n"
        f"• Крок 3: У кожному прогоні рахуємо Decision Risk Index (DRI) — це інтегрований стратегічний індикатор з вагами w1={w1:.2f}, w2={w2:.2f}, w3={w3:.2f} "
        f"та Максимальний час планування(Max_Planning_Time) = {Max_Planning_Time} год.\n\n"
        "✅ На виході отримуємо:\n"
        "• Base DRI (сценарій без шуму)\n"
        "• Mean DRI (середній ризик)\n"
        "• P90 DRI (поганий хвіст ризику)\n"
        "• Ймовірність переходу в кризовий або критичний стан %\n"
        "Сенс: не один прогноз, а розподіл ризику в умовах невизначеності."
    )

def Monte_Carlo_Compare_COA_fixed_keys(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time,
    Intelligence_Confidence_key,
    Volatility_key,
    Time_Pressure_key,
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
    base_IC = Intelligence_Confidence_dic[Intelligence_Confidence_key]
    base_V = Volatility_dic[Volatility_key]
    base_available_time = Time_Pressure_dic[Time_Pressure_key]

    results = {}

    for coa_name, settings in COA_settings.items():
        dris = []
        levels = {
            "Situation under control": 0,
            "Maneuver risk": 0,
            "Crisis mode": 0,
            "Critical state": 0
        }

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

            lvl = get_DRI_level(dri)
            levels[lvl] += 1

        dris.sort()

        results[coa_name] = {
            "Mean_DRI": statistics.mean(dris),
            "P90": dris[int(0.90 * (n - 1))],
            "Critical_%": levels["Critical state"] / n,
            "Crisis_%": levels["Crisis mode"] / n,
            "Stable_%": levels["Situation under control"] / n,
            "Maneuver_%": levels["Maneuver risk"] / n,
        }

    # Рекомендація: нижчий P90, а при рівності — нижчий Critical хвіст
    coa_names = list(results.keys())
    best = min(
        coa_names,
        key=lambda name: (results[name]["P90"], results[name]["Critical_%"])
    )

    recommendation = f"Suggestion: **{best}** (minimal P90, and/or lesser Critical tail)."

    return results, recommendation


def format_coa_message(scenario_keys, coa_results, recommendation) -> str:
    IC_key, V_key, TP_key = scenario_keys

    message = f"""
🧭 Compare CoA (Fixed scenario)
Scenario keys: IC={IC_key}, Volatility={V_key}, Time={TP_key}

    """
    for coa, d in coa_results.items():
        message += f"\n — **{coa}**"
        message += f"\n  Mean DRI: {d['Mean_DRI']:.3f} | P90: {d['P90']:.3f}"
        message += f"\n  Crisis: {d['Crisis_%']*100:.1f}% | Critical: {d['Critical_%']*100:.1f}% | Stable: {d['Stable_%']*100:.1f}%\n"
    message += "\n✅ " + recommendation
    return message

def Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time,
    Intelligence_Confidence_key,
    Volatility_key,
    Time_Pressure_key,
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
    base_IC = Intelligence_Confidence_dic[Intelligence_Confidence_key]
    base_V = Volatility_dic[Volatility_key]
    base_available_time = Time_Pressure_dic[Time_Pressure_key]

    def Win_Probability_From_DRI(dri: float) -> float:
        # DRI ↑ -> WinProb ↓ ; при dri == threshold => 0.5
        return 1.0 / (1.0 + math.exp(k * (dri - threshold)))

    for coa_name, settings in COA_settings.items():
        dris = []
        win_probs = []

        levels = {
            "Situation under control": 0,
            "Maneuver risk": 0,
            "Crisis mode": 0,
            "Critical state": 0
        }

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

            lvl = get_DRI_level(dri)
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
            "Critical_%": levels["Critical state"] / n,
            "Crisis_%": levels["Crisis mode"] / n,
            "Maneuver_%": levels["Maneuver risk"] / n,
            "Stable_%": levels["Situation under control"] / n,

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

    recommendation = (
        f"According to integral criterion (WinProb_mean − Critical_tail) best course of action is: **{best}**."
    )

    return results, recommendation

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
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time,
    Intelligence_Confidence_key,
    Volatility_key,
    Time_Pressure_key,
    n=10000,
    w1=0.33, w2=0.33, w3=0.33,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0
):
    """
    Scenario sensitivity (fixed_keys):
    - беремо один сценарій (IC/V/Time) як базу
    - далі симулюємо невизначеність шумом і дивимось, що найбільше рухає DRI
    """

    base_IC = Intelligence_Confidence_dic[Intelligence_Confidence_key]
    base_V = Volatility_dic[Volatility_key]
    base_available_time = Time_Pressure_dic[Time_Pressure_key]

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
            "IC_key": Intelligence_Confidence_key,
            "V_key": Volatility_key,
            "TP_key": Time_Pressure_key
        },
        "spearman_corr": {"IC": rIC, "V": rV, "TP": rTP},
        "influence_share": share,
        "combined_score": score,
        "DRI_mean": statistics.mean(DRI_list),
        "DRI_p90": dri_sorted[int(0.90 * (n - 1))]
    }

def build_ar_summary_short(
    scenario_keys,          # (IC_key, V_key, TP_key) e.g. ("50%", "High", "6h")
    dri_stats,              # {"base_dri": float, "p90": float, "crisis_plus": float, "critical_tail": float}
    coa_rows,               # list of dicts: [{"name":"Наступ","p90":0.81,"win":0.43,"crit":0.15}, ...]
    recommendation,         # {"coa":"Перегрупування","why":"lowest P90 + lowest Critical"}
    sensitivity=None        # optional: {"top":"TP", "order":["TP","V","IC"]} or {"shares":{"TP":0.48,...}}
):
    """
    Повертає 4 короткі рядки для AR-екрана (1 погляд = 1 рішення).
    Формат:
      TOP:    IC=50% | Vol=High | Time=6h
      CENTER: DRI 0.62 Crisis | P90 0.78
      WARN:   Crisis+ 41% | Critical 12%
      BOTTOM: COA: Regroup (P90↓ Crit↓ Win↑) | Driver: TP>V>IC
    """

    # --- helpers ---
    def lvl(dri: float) -> str:
        # якщо у тебе вже є get_DRI_level — можеш замінити на нього
        if dri < 0.3:
            return "Controlled"
        elif dri < 0.6:
            return "Maneuver"
        elif dri < 0.8:
            return "Crisis"
        else:
            return "Critical"

    def pct(x: float) -> str:
        return f"{x*100:.0f}%"

    def f3(x: float) -> str:
        return f"{x:.2f}"

    def normalize_coa_name(name: str) -> str:
        # короткі лейбли для AR
        mapping = {
            "Наступ": "Offense",
            "Перегрупування": "Regroup",
            "Оборона": "Defense",
            "Захист": "Defense"
        }
        return mapping.get(name, name)

    # --- 1) TOP: scenario snapshot ---
    IC_key, V_key, TP_key = scenario_keys
    line_top = f"IC={IC_key} | Vol={V_key} | Time={TP_key}"

    # --- 2) CENTER: risk ---
    base_dri = float(dri_stats["base_dri"])
    p90_dri = float(dri_stats["p90"])
    line_center = f"DRI {f3(base_dri)} {lvl(base_dri)} | P90 {f3(p90_dri)}"

    # --- 3) WARN: tails ---
    crisis_plus = float(dri_stats["crisis_plus"])
    critical_tail = float(dri_stats["critical_tail"])
    line_warn = f"Crisis+ {pct(crisis_plus)} | Critical {pct(critical_tail)}"

    # --- 4) BOTTOM: recommendation + driver ---
    rec_coa = recommendation.get("coa", "")
    rec_short = normalize_coa_name(rec_coa)

    # якщо передали sensitivity, покажемо Driver
    driver_str = ""
    if sensitivity:
        if "order" in sensitivity and sensitivity["order"]:
            driver_str = "Driver: " + ">".join(sensitivity["order"])
        elif "top" in sensitivity and sensitivity["top"]:
            driver_str = "Driver: " + str(sensitivity["top"])
        elif "shares" in sensitivity and isinstance(sensitivity["shares"], dict):
            order = sorted(sensitivity["shares"].items(), key=lambda x: x[1], reverse=True)
            driver_str = "Driver: " + ">".join([k for k, _ in order])

    # Невеликий “індикатор чому” (за даними COA)
    # Знайдемо рядок для рекомендованого COA і покажемо три стрілки
    arrows = ""
    rec_row = next((r for r in coa_rows if r.get("name") == rec_coa), None)
    if rec_row:
        arrows = f"(P90 {f3(rec_row['p90'])} | Win {pct(rec_row['win'])} | Crit {pct(rec_row['crit'])})"
    else:
        why = recommendation.get("why", "")
        arrows = f"({why})" if why else ""

    line_bottom = f"COA: {rec_short} {arrows}"
    if driver_str:
        line_bottom += f" | {driver_str}"

    return [line_top, line_center, line_warn, line_bottom]

Save_Dataframe = False
if Save_Dataframe:  
  flattened_rows = []
  for run_key, data in score_table.items():

      print(f"raw data: \n {data} \n------------------")
      # 1. Extract metadata by index
      user_id   = data[0]
      user_name = data[1]
      run_id    = data[2]
      dirname   = data[3]
      datestamp = data[4]

      # 2. Iterate through the remaining items (the scores)
      # data[5:] takes everything from the 6th element to the end
      for score_tuple in data[5:]:
        print(score_tuple)
        value, test_name, *context = score_tuple

        flattened_rows.append({
            "user_id": user_id,
            "user_name": user_name,
            "date": datestamp,
            "run_id": run_id,
            "direction": dirname,
            "test_name": test_name,
            "score": value,
            "context": context
        })

  # 3. Create the DataFrame
  df = pd.DataFrame(flattened_rows)

  if os.getenv("COLAB_RELEASE_TAG"):
      from google.colab import drive
      #if not on Render, importing drive lib for files
      drive.mount('/content/drive/')
      save_path = '/content/drive/MyDrive/Colab/Telegram test/'
  elif os.getenv("RENDER"):
      save_path = '' #saving into current working directory
      # unless we want to invest into
  else:
      save_path = os.path.join(os.getcwd(), 'temp')
      # saves into CWD / temp subpath

  scorefile = save_path + 'scores.csv'
  print(scorefile)
  if os.path.isfile(scorefile):
      print("Appending scores")
      # mode = 'a' for append
      df.to_csv(scorefile, mode='a', index=False, header=False)
  else:
      print("File not found, creating new...")
      df.to_csv(scorefile, encoding='utf-8', index=False)

Test_Score_Dataframe = False

import pandas as pd

if Test_Score_Dataframe:
  flattened_rows = []
  for run_key, data in score_table.items():

      print(f"raw data: \n {data} \n------------------")
      # 1. Extract metadata by index
      user_id   = data[0]
      user_name = data[1]
      run_id    = data[2]
      dirname   = data[3]
      datestamp = data[4]

      # 2. Iterate through the remaining items (the scores)
      # data[5:] takes everything from the 6th element to the end
      for score_tuple in data[5:]:
        print(score_tuple)
        value, test_name, *context = score_tuple

        flattened_rows.append({
            "user_id": user_id,
            "user_name": user_name,
            "date": datestamp,
            "run_id": run_id,
            "direction": dirname,
            "test_name": test_name,
            "score": value,
            "context": context
        })

  # 3. Create the DataFrame
  df = pd.DataFrame(flattened_rows)


  print(f"  > DataFrame for the score table: <\n{df}")

  # 4. Score sum
  summary_df = df.groupby(['user_id', 'run_id', 'direction']).agg(
        total_score=('score', 'sum'),
        test_count=('test_name', 'count')
    ).reset_index()

  print(f"---< Score summary: >--- \n{summary_df}\n------------------------")
