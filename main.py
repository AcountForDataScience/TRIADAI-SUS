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

# import telebot
# from telebot import types
# from telebot.formatting import escape_markdown

### quick API ###

#--------- API KEY ---------#
print("acquiring tokens")
print(os.getenv('Test_env'))
bot_token = os.getenv('BOT_TOKEN')

# #exception debug
# class MyExceptionHandler(telebot.ExceptionHandler):
#   def handle(self, exception):
#     # Log the error or perform other actions
#     print(f'An exception occurred: {exception}')
#     # Example: send a notification to an admin via bot.send_message()
#     return True  # Indicate that the exception is handled
# bot = telebot.TeleBot(bot_token, parse_mode=None, exception_handler=MyExceptionHandler)

#initiate the telegram bot. #can update to "MARKDOWN" parse mode for simple Rich text capabilites
bot = telebot.TeleBot(bot_token, parse_mode=None)

print("<info>: Telegram bot is initialized")

### Global Variables ###
# here we use empty dictionaries
# they get filled in the following manner
# <varname> = {<chat_id>: <data dic>}


simulation_results      = {}
simulation_parameters   = {}
strategic_direction_name= {}
custom_name             = {}

user_locale   = {}

score_table   = {}
current_score = {}
# planned usage:
# current_score[user_id] = [user_id, run_id, direction_name]
# current_score[user_id].append(score, test, context))
# score_table[run_id] = current_score[user_id]
# i.e. :
# score_table[run_id] = {
#     user_id,
#     user_name,
#     run_id,
#     name,
#     date_stamp, #using ISO date
#     score(value, test name, context[]),
#     score(value, test name, context[]),
#     score(value, test name, context[])
# }


###########
## LOGIC ##
###########

##-----------------------------##
#   Інформаційні повідомлення   #
##-----------------------------##

#надіслати основну інформацію
def send_description(message):
  print("Description")
  markup = types.InlineKeyboardMarkup()
  backbtn = types.InlineKeyboardButton("<< back", callback_data="init_menu")
  markup.add(backbtn)

  chat_id = message.chat.id

  #this is a message with line break support
  #markdown markup, periods must be escaped
  message_text = """
Welcome to the *TRIADAI\\-SUS* Framework
_AI/AR\-Driven Strategic Uncertainty & Decision Simulation Environment_

*TRIADAI\-SUS* is a strategic wargaming and decision\\-support framework designed to strengthen command thinking and improve military strategic planning under uncertainty\.
This simulation environment introduces modern Artificial Intelligence methods into the decision\\-making process and demonstrates how data\-driven tools can support commanders at operational and strategic levels\.

🎯 Purpose of the Framework
TRIADAI\\-SUS is designed for:
 • Enhancing strategic command thinking during military planning and crisis response
 • Introducing modern AI algorithms into professional military education
 • Explaining how AI tools support evidence\\-based decision\\-making in complex and uncertain environments
 • Demonstrating when to apply specific analytical methods, such as:
   ○ Monte Carlo simulation — to explore uncertainty
     and compare alternative courses of action
   ○ Random Forest models — to forecast
     operational outcomes and risks
   ○ Neural Networks — to detect patterns in
     complex, dynamic environments
   ○ Sensitivity Analysis — to identify
     the most influential decision factors

🧠 What You Will Experience
Within the simulation, participants will:
 • Evaluate alternative Courses of Action \(COA\)
 • Observe Win Probability and risk indicators in real time
 • Understand how uncertainty affects operational success
 • Learn to interpret AI\\-generated recommendations
 • Develop structured decision\\-making under time pressure
  """
  # bot.send_message(chat_id, message_text, parse_mode="MarkdownV2", reply_markup = markup)
  bot.edit_message_text(message_text, chat_id, message.id, parse_mode="MarkdownV2", reply_markup = markup)
  # || надіслати опис

# запит на інформацію
@bot.callback_query_handler(func=lambda call: call.data == "init_info")
def handle_send_description(call):
  bot.answer_callback_query(call.id)
  send_description(call.message)
# || запит на інформацію

# виклик меню
@bot.callback_query_handler(func=lambda call: call.data == "init_menu")
def handle_send_main_menu(call):
  bot.answer_callback_query(call.id)
  show_menu(call.message, False)
# || виклик меню

# початковий екран
@bot.message_handler(commands=["start"])
def send_welcome(message):
  # username handling
  global custom_name
  user_id = message.chat.id
  if not custom_name.get(user_id):
    next = bot.send_message(message.chat.id, "You've launched the Strategic Uncertainty Simulation bot. Please enter your preferred name")
    bot.register_next_step_handler(next, rename_user)
  else:

    bot.send_message(message.chat.id, f"You've launched the Strategic Uncertainty Simulation bot, {custom_name[user_id]}")

    # bot.send_message(message.chat.id, f"Your Chat ID is: {message.chat.id}")
    show_menu(message)
# || початковий екран

# name or rename user
@bot.message_handler(commands=["rename"])
def command_rename(message):
  global custom_name
  user_id = message.chat.id
  if not custom_name.get(user_id):
    next = bot.send_message(message.chat.id, "Please enter your preferred name:")
  else:
    next = bot.send_message(message.chat.id, f"your current name is:{custom_name[user_id]}. Enter a new name:")
  bot.register_next_step_handler(next, rename_user)

def rename_user(message):
  global custom_name

  markup = types.InlineKeyboardMarkup()
  btn_rename = types.InlineKeyboardButton("Rename direction", callback_data="init_rename", style="danger")
  btn_start = types.InlineKeyboardButton("🚀Start scenario", callback_data="start_simulation",style="success")
  markup.add(btn_start, btn_rename)

  custom_name[message.chat.id] = message.text
  # print(custom_name[message.chat.id])
  # bot.reply_to(message, f"Evaluating the \"{strategic_direction_name[message.chat.id]}.\" direction", reply_markup=markup)
  show_menu(message)

# меню команд
def show_menu(message, send_new = True):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton("🚀 Start Scenario", callback_data="init_start", style="success")
    button2 = types.InlineKeyboardButton("Bot Description", callback_data="init_info")

    # Each line adds a row of buttons
    markup.add(button1, button2)

    message_text = "Select menu option to proceed"

    if send_new:
      bot.send_message(message.chat.id, message_text, reply_markup=markup)
    else:
      bot.edit_message_text(message_text, message.chat.id, message.id, reply_markup=markup)
# || меню команд


##-----------------------------##
#         Phase  One            #
##-----------------------------##

# ---> init_start is the entry point callback

# Початок Першої фази
@bot.callback_query_handler(func=lambda call: call.data == "init_start")
def handle_start_phase_one(call):
  bot.answer_callback_query(call.id, "Preparing the simulation") #removes loading symbol
  # bot.send_message(call.message.chat.id, "Розпочинаємо симуляцію")
  next = bot.send_message(call.message.chat.id, "Simulation has started\. Please choose *strategic direction*\n\\(enter direction name below\\):", parse_mode="MarkdownV2")
  # Hand off the flow to the 'name_strategic_direction' function
  bot.register_next_step_handler(next, name_strategic_direction)
# || Початок Симуляції

# Назва напрямку
def name_strategic_direction(message):
  # print("name strat direction")
  global strategic_direction_name

  markup = types.InlineKeyboardMarkup()

  # btn_param = types.InlineKeyboardButton("Визначити параметри", callback_data="init_set_parameters")
  btn_rename = types.InlineKeyboardButton("Rename direction", callback_data="init_rename", style="danger")
  btn_start = types.InlineKeyboardButton("🚀Start scenario", callback_data="start_simulation",style="success")

  # Each line adds a row of buttons
  markup.add(btn_start, btn_rename)
  # markup.add(btn_param)

  strategic_direction_name[message.chat.id] = message.text
  # print(strategic_direction_name[message.chat.id])
  bot.reply_to(message, f"Evaluating the \"{strategic_direction_name[message.chat.id]}.\" direction", reply_markup=markup)

# переназвати напрямок
@bot.callback_query_handler(func=lambda call: call.data == "init_rename")
def handle_name_strategic_direction(call):
  bot.answer_callback_query(call.id) #removes loading symbol
  next = bot.send_message(call.message.chat.id, "Please choose *strategic direction*\n\(enter direction name below\):", parse_mode="MarkdownV2")
  # Hand off the flow to the 'name_strategic_direction' function
  bot.register_next_step_handler(next, name_strategic_direction)

# # визначити параметри
# @bot.callback_query_handler(func=lambda call: call.data == "init_set_parameters")
# def game_set_parameters(call):
#   bot.answer_callback_query(call.id, "Немає параметрів для визначення") #removes loading symbol
#   pass


# початок симуляції
@bot.callback_query_handler(func=lambda call: call.data == "start_simulation")
def handle_simulation_p1_start(call):
  bot.answer_callback_query(call.id, "selecting parameters...")
  # print("start - callback")
  simulation_phase_one_results(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "p1_restart")
def handle_simulation_p1_restart(call):
  bot.answer_callback_query(call.id, "shuffling parameters...")
  # print("restart")
  simulation_phase_one(call.message.chat.id)
  simulation_phase_one_results(call.message)

### simulation scenario
def simulation_phase_one(chat_id):
# #if we transition to custom keys or values, new definition could be:
# def simulation_phase_one(message, IC_key, V_key, TP_key):

  global simulation_parameters #in case we need to circle back to parameters
  global simulation_results #results are stored here per-user

  # #this requires definitions of the following variables somewhere else:
    # Intelligence_Confidence_dic
    # Volatility_dic
    # Time_Pressure_dic
    # Max_Planning_Time
    #

    #shuffle parameters - later possibly define parameters as well
  IC_key, V_key, TP_key = Shuffling_IC_V_TP(Intelligence_Confidence_dic, Volatility_dic, Time_Pressure_dic)

  simulation_parameters[chat_id] = {
      "IC" : IC_key,
      "VL" : V_key,
      "TP" : TP_key,
      "PT" : Max_Planning_Time,
      "n"  : 5000,
      #also recording weights here
      "weights": {
        "w1" : 0.33,
        "w2" : 0.33,
        "w3" : 0.33
      }
  }

  p1_results = run_phase1(
      Intelligence_Confidence_dic,
      Volatility_dic,
      Time_Pressure_dic,
      Max_Planning_Time,
      n=5000
  )

  simulation_results[chat_id] = { "P1" : p1_results}
  # print(simulation_results)
#simulation end

def simulation_phase_one_results(message):
  # print("results_started")

  global strategic_direction_name #using this to explicitly mention the direction being evaluated.
  global simulation_results #results are stored here per-user
  if not message.chat.id in simulation_results:
    simulation_phase_one(message.chat.id)

  markup = types.InlineKeyboardMarkup()

  btn_restart = types.InlineKeyboardButton("Shuffle parameters", callback_data="p1_restart", style="danger")
  btn_explain = types.InlineKeyboardButton("How this works?", callback_data="p1_explain",style="primary")
  btn_next = types.InlineKeyboardButton("Confirm and continue", callback_data="p1_confirm_parameters", style="success")

  # Each line adds a row of buttons
  markup.add(btn_restart, btn_explain)
  markup.add(btn_next)

  # print("ready to send")
  response_text = f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\n\n" + simulation_results[message.chat.id]["P1"]
  # print(response_text)
  bot.edit_message_text(response_text, message.chat.id, message.id, reply_markup=markup)
#end of phase one monte carlo

@bot.callback_query_handler(func=lambda call: call.data == "p1_explain")
def handle_p1_explain(call):
  bot.answer_callback_query(call.id)
  simulation_phase_one_explain(call.message)

### simulation scenario
def simulation_phase_one_explain(message):
  global simulation_parameters #we use some params from here

  # explain = explain_monte_carlo_phase1(
  #     simulation_parameters[message.chat.id]["n"],
  #     Max_Planning_Time=simulation_parameters[message.chat.id]["PT"],
  #     w1=0.33, w2=0.33, w3=0.33,
  #     noise_ic=0.05,
  #     noise_v=0.05,
  #     noise_time=1.0,
  #     lang="en")

  explain = """
  *Initial Strategic Environment Assessment*

_Decision Risk Index \(DRI\)_ — Operational Readiness Indicator
At the start of the simulation, the system evaluates the operational environment using four key planning parameters\\.
 These parameters reflect the level of uncertainty, time constraints, and information reliability that will shape your decisions\\.

Input Parameters
1\\. Intelligence Confidence
  _Represents the reliability and completeness of available intelligence\\._
  High confidence: 90%
  Moderate confidence: 50%
  Low confidence: 20%
`Intelligence_Confidence_dic = {"90%": 0\.9, "50%": 0\.5, "20%": 0\.2}`

2\\. Operational Volatility
  _Describes the level of unpredictability in the environment\._
  Low volatility: Stable and predictable conditions
  Medium volatility: Changing operational dynamics
  High volatility: Rapid and uncertain developments
`Volatility_dic = {"Low": 0\.3, "Medium": 0\.6, "High": 0\.9}`

3\\. Maximum Planning Time
  _48 hours — the maximum available time horizon for strategic planning under normal conditions\\. _

4\\. Time Pressure
  _Defines how urgently a decision must be made\\._
  Strategic Analysis: 48 hours
  Operational Level: 6 hours
  Crisis Decision: 0\\.5 hours
`Time_Pressure_dic = {"Strategic Analysis": 48, "Operational level": 6, "Crisis decision": 0\.5}`

_Decision Risk Index \(DRI\)_
Based on these parameters, the framework calculates the Decision Risk Index \(DRI\) — a quantitative indicator of the decision environment\.
The DRI helps commanders understand how difficult, unstable, and time\-constrained the situation is before selecting a Course of Action\.

Operational Environment Classification
The calculated DRI determines the decision environment:
_Situation Under Control_
  DRI < 0\\.30
  The environment is stable\\. Decisions can be made with sufficient time and reliable information\\.
_Maneuver Risk_
  0\\.30 ≤ DRI < 0\\.60
  The situation requires careful coordination and risk management\\.
_Crisis Mode_
  0\\.60 ≤ DRI < 0\\.80
  Time pressure and uncertainty significantly affect decision\-making\\.
_Critical State_
  DRI ≥ 0\\.80
  The environment is unstable and highly time\\-sensitive\. Decisions must be made under severe constraints\\.

ℹ️ How Monte Carlo works
• Step 1: The bot picks ONE mission scenario: IC / Volatility / Available time\\.
• Step 2: We run 5000 simulations around that scenario, adding uncertainty \(noise\):
  \- IC varies by ±0\\.05
  \- Volatility varies by ±0\\.05
  \- Available time varies by ±1\\.0h
• Step 3: Each run computes DRI using weights w1\=0\\.33, w2\=0\\.33, w3\=0\\.33 and Max planning time \= 48h\.

✅ Output:
• Base DRI \(no\-noise scenario\)
• Mean DRI \(average over all runs\)
• P90 DRI \(bad\-tail risk\)
• Crisis\+Critical % and Critical tail %
Meaning: not one forecast — a risk distribution under uncertainty\.

  """

  markup = types.InlineKeyboardMarkup()
  btn_back = types.InlineKeyboardButton("<< back", callback_data="start_simulation", style="success")

  # Each line adds a row of buttons
  markup.add(btn_back)

  bot.edit_message_text(explain, message.chat.id, message.id, reply_markup=markup)

#Підтвердження параметрів
@bot.callback_query_handler(func=lambda call: call.data == "p1_confirm_parameters")
def handle_simulation_p1_confirm_parameters(call):
  bot.answer_callback_query(call.id, "parameters are confirmed")
  print("p1 parameters confirmed")
  # scoring
  global current_score
  run_id = generate_random_token()
  # user_id = call.from_user.id
  user_id = call.message.chat.id
  global custom_name
  user_name = custom_name[user_id]
  timestamp = datetime.date.today()
  print(timestamp)
  current_score[user_id] = [
      user_id,
      user_name,
      run_id,
      strategic_direction_name[user_id],
      timestamp.isoformat() #in a better format
  ]
  # print(f"score record created for {run_id}:\n{current_score[call.from_user.id]}")

  simulation_phase_one_analyze(call.message)

def simulation_phase_one_analyze(message):
  markup = types.InlineKeyboardMarkup()
  # btn_CoA = types.InlineKeyboardButton("Compare CoA", callback_data="p1_analysis:Compare CoA")
  # btn_SAnal = types.InlineKeyboardButton("Sensitivity Analysis", callback_data="p1_analysis:Sensitivity Analysis")
  # btn_WinP = types.InlineKeyboardButton("Win Probability", callback_data="p1_analysis:Win Probability")
  # btn_AR = types.InlineKeyboardButton("AR summary", callback_data="p1_analysis:AR Summary")
  # btn_conclude = types.InlineKeyboardButton("Phase 2 suggestions", callback_data="p1_placeholder:Phase one conclusion")

  # Each line adds a row of buttons
  # markup.add(btn_CoA,btn_WinP,btn_SAnal)
  # markup.add(btn_AR,btn_conclude)
  # markup.add(btn_AR)

  # markup = quick_markup({
  #   # 'Test CoA'                  : {'callback_data': 'p1_analysis:Test CoA'},
  #   'Test Sensitivity analysis' : {'callback_data': 'p1_analysis:Test Sens'},
  #   'Test Win Probability'      : {'callback_data': 'p1_analysis:Test WinP'}
  # }, row_width=2)

  btn_Test_Sens = types.InlineKeyboardButton(
      "Test Sensitivity Analysis",
      callback_data="p1_analysis:Test Sens")
  btn_Test_WinP = types.InlineKeyboardButton(
      "Test Win Probability",
      callback_data="p1_analysis:Test WinP")
  btn_Conclude = types.InlineKeyboardButton(
      "Complete simulation",
      callback_data="p1_analysis:Conclude")

  Sens = WinP = False

  user_id = message.chat.id

  for i in range(4, len(current_score[user_id])):
    if current_score[user_id][i][1] == 'Sensitivity':
      Sens = True
    if current_score[user_id][i][1] == 'Win Probability':
      WinP = True

  if not Sens and not WinP:
    markup.add(btn_Test_Sens, btn_Test_WinP)
  elif not Sens:
    markup.add(btn_Test_Sens)
  elif not WinP:
    markup.add(btn_Test_WinP)
  else:
    markup.add(btn_Conclude)

  bot.edit_message_reply_markup(
        chat_id=message.chat.id,
        message_id=message.id,
        reply_markup=markup
    )

  # bot.edit_message_text(
  #       chat_id=message.chat.id,
  #       message_id=message.id,
  #       text=f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\n\n {simulation_results[message.chat.id]["P1"]}",
  #       reply_markup=markup
  #   )

#обробка додаткових виводів
@bot.callback_query_handler(func=lambda call: call.data.startswith("p1_analysis:"))
def handle_p1_analysis(call):
  callback = call.data.split(':')[1] # розділяємо дані колбеку і використовуємо другу частину (після двокрапки)
  bot.answer_callback_query(call.id, text=f"processing {callback}...")

  if callback == "Score Sens":
    callback=call.data.split(':')[2]
    print(callback)
    simulation_p1_score_sens(call.message,callback)

  if callback == "Score WinP":
    callback=call.data.split(':')[2]
    print(callback)
    simulation_p1_score_winp(call.message,callback)

  if callback == "Simulation Details":
      simulation_phase_one_analyze(call.message)
  elif callback == "Compare CoA":
      simulation_p1_compare_coa(call.message)
  elif callback == "Sensitivity Analysis":
      simulation_p1_sensitivity_analysis(call.message)
  elif callback == "Win Probability":
      simulation_p1_win_probability(call.message)
  # scoring block
  elif callback == "Test CoA":
      simulation_p1_compare_coa(call.message)
  elif callback == "Test Sens":
      simulation_p1_test_sens(call.message)
  elif callback == "Test WinP":
      simulation_p1_test_winp(call.message)
  # end scoring block
  elif callback == "AR Summary":
      simulation_p1_AR_summary(call.message)
  elif callback == "Conclude":
      simulation_p1_conclude(call.message)
  else:
      # Fallback or generic pass
      pass

  print(f"processed callback: {callback}")

# scoring #######################################
def simulation_p1_test_sens(message):
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  message_text=f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\n\n {simulation_results[message.chat.id]["P1"]} \n\n Given these parameters, choose the largest contributor.",

  markup = quick_markup({
    'Intelligence Confidence' : {'callback_data': 'p1_analysis:Score Sens:IC'},
    'Volatility'              : {'callback_data': 'p1_analysis:Score Sens:V'},
    'Time pressure'           : {'callback_data': 'p1_analysis:Score Sens:TP'}
  }, row_width=3)

  bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup)

def simulation_p1_score_sens(message,answer):
  global simulation_parameters
  global strategic_direction_name
  global current_score
  user_id = message.chat.id

  sens = Sensitivity_Analysis_DRI_fixed_keys(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time=simulation_parameters[user_id]["PT"],
    Intelligence_Confidence_key=simulation_parameters[user_id]["IC"],
    Volatility_key=simulation_parameters[user_id]["VL"],
    Time_Pressure_key=simulation_parameters[user_id]["TP"],
    n=simulation_parameters[user_id]["n"],
    w1=w1, w2=w2, w3=w3,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0
  )

  # print(sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0])

  answer_key = sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0]

  #prettify
  match answer:
    case 'V' : answer = "Volatility"
    case 'IC': answer = "Intel Confidence"
    case 'TP': answer = "Time Pressure"
  match answer_key:
    case 'V' : answer_key = "Volatility"
    case 'IC': answer_key = "Intel Confidence"
    case 'TP': answer_key = "Time Pressure"


  if answer == answer_key:
    # print("correct")
    score_text = f"your answer {answer} is correct"
    current_score[user_id].append((
        1,
        "Sensitivity",
        simulation_parameters[user_id],
        sens
        ))
  else:
    # print("incorrect")
    score_text = f"your answer {answer} is incorrect: it's {answer_key}"
    current_score[user_id].append((
        0,
        "Sensitivity",
        simulation_parameters[user_id],
        sens
        ))

  influence_share = {k: round(v*100, 1) for k, v in sens["influence_share"].items()}
  message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
Scenario parameters:  Intel:  {sens["scenario"]['IC_key']},   Volatility: {sens["scenario"]['V_key']}, Time pressure: {sens["scenario"]['TP_key']}
Spearman correlation: Intel:  {sens["spearman_corr"]['IC']:.2f}, Volatility: {sens["spearman_corr"]['V']:.2f},  Time pressure: {sens["spearman_corr"]['TP']:.2f}
Influence share:      Intel:  {influence_share['IC']:.2f}, Volatility: {influence_share['V']:.2f}, Time pressure: {influence_share['TP']:.2f}

{score_text}
  """

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message)

def simulation_p1_test_winp(message):
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  message_text=f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\n\n {simulation_results[message.chat.id]["P1"]} \n\n Given these parameters, choose the course of action with highest Win Probability.",

  markup = quick_markup({
    'Attack'  : {'callback_data': 'p1_analysis:Score WinP:Attack'},
    'Regroup' : {'callback_data': 'p1_analysis:Score WinP:Regroup'}
  }, row_width=3)

  bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup)

def simulation_p1_score_winp(message,answer):
  global simulation_parameters
  global strategic_direction_name
  global current_score
  user_id = message.chat.id

  w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
  coa_wp, rec = Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(
      Intelligence_Confidence_dic,
      Volatility_dic,
      Time_Pressure_dic,
      Max_Planning_Time=simulation_parameters[user_id]["PT"],
      Intelligence_Confidence_key=simulation_parameters[user_id]["IC"],
      Volatility_key=simulation_parameters[user_id]["VL"],
      Time_Pressure_key=simulation_parameters[user_id]["TP"],
      n=simulation_parameters[user_id]["n"],
      w1=w1, w2=w2, w3=w3,
      k=8,
      threshold=0.6,
      noise_ic=0.05, noise_v=0.05, noise_time=1.0
  )

  # print(sorted(coa_wp.items(), key=lambda item: item[1]["WinProb_Mean"]-item[1]["Critical_%"], reverse=True)[0][0])

  answer_key = sorted(coa_wp.items(), key=lambda item: item[1]["WinProb_Mean"]-item[1]["Critical_%"], reverse=True)[0][0]

  if answer == answer_key:
    # print("correct")
    score_text = f"Chosen course of action {answer} has highest win probability"
    current_score[user_id].append((
        1,
        "Win Probability",
        simulation_parameters[user_id],
        coa_wp
        ))
  else:
    # print("incorrect")
    score_text = f"Chosen course of action {answer} is incorrect: {answer_key} has highest win probability"
    current_score[user_id].append((
        0,
        "Win Probability",
        simulation_parameters[user_id],
        coa_wp
        ))

  IC_key, V_key, TP_key = simulation_parameters[user_id]["IC"], simulation_parameters[user_id]["VL"], simulation_parameters[user_id]["TP"]
  compare_stats_text = f"Scenario: {IC_key}, {V_key}, {TP_key}\n"
  for key, value in coa_wp.items():
    compare_stats_text += f"for {key} CoA, 90 percentile win probability is at {value.get('WinProb_P90'):.2f} with a {value.get('Critical_%')*100:.2f}% critical tail\n"

  # print(compare_stats_text)

  message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
  {compare_stats_text}
  {rec}

  {score_text}
  """

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message)
# scoring #######################################


def simulation_p1_compare_coa(message):
  #display CoA comparison and all the buttons
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
  coa_results, recommendation = Monte_Carlo_Compare_COA_fixed_keys(
      Intelligence_Confidence_dic,
      Volatility_dic,
      Time_Pressure_dic,
      Max_Planning_Time=simulation_parameters[user_id]["PT"],
      Intelligence_Confidence_key=simulation_parameters[user_id]["IC"],
      Volatility_key=simulation_parameters[user_id]["VL"],
      Time_Pressure_key=simulation_parameters[user_id]["TP"],
      n=simulation_parameters[user_id]["n"],
      w1=w1, w2=w2, w3=w3,
      noise_ic=0.05, noise_v=0.05, noise_time=1.0
  )

  IC_key, V_key, TP_key = simulation_parameters[user_id]["IC"], simulation_parameters[user_id]["VL"], simulation_parameters[user_id]["TP"]
  message_text = f"Evaluating the \"{strategic_direction_name[user_id]}\" direction: \n{format_coa_message((IC_key, V_key, TP_key), coa_results, recommendation)}"

  # print(message_text)
  # print(coa_results)
  # print(recommendation)

  # message_text = escape_markdown(message_text)
  # bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id,parse_mode='MARKDOWN_V2')

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message) #bring back menu buttons
  # end compare CoA


def simulation_p1_sensitivity_analysis(message):
  #display CoA sensitivity analysis and all the buttons
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  sens = Sensitivity_Analysis_DRI_fixed_keys(
    Intelligence_Confidence_dic,
    Volatility_dic,
    Time_Pressure_dic,
    Max_Planning_Time=simulation_parameters[user_id]["PT"],
    Intelligence_Confidence_key=simulation_parameters[user_id]["IC"],
    Volatility_key=simulation_parameters[user_id]["VL"],
    Time_Pressure_key=simulation_parameters[user_id]["TP"],
    n=simulation_parameters[user_id]["n"],
    w1=w1, w2=w2, w3=w3,
    noise_ic=0.05, noise_v=0.05, noise_time=1.0
  )

  # print(sens["scenario"])
  # print(sens["spearman_corr"])
  # # Combined sensitivity score = spearman x influence share
  # print({k: round(v*100, 1) for k, v in sens["influence_share"].items()})

  influence_share = {k: round(v*100, 1) for k, v in sens["influence_share"].items()}
  message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
Scenario parameters:  Intel:  {sens["scenario"]['IC_key']},   Volatility: {sens["scenario"]['V_key']}, Time pressure: {sens["scenario"]['TP_key']}
Spearman correlation: Intel:  {sens["spearman_corr"]['IC']:.2f}, Volatility: {sens["spearman_corr"]['V']:.2f},  Time pressure: {sens["spearman_corr"]['TP']:.2f}
Influence share:      Intel:  {influence_share['IC']:.2f}, Volatility: {influence_share['V']:.2f}, Time pressure: {influence_share['TP']:.2f}
  """

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message) #bring back menu buttons
  #end sensitivity analysis

def simulation_p1_win_probability(message):
  #display win probability and all the buttons
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
  coa_wp, rec = Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(
      Intelligence_Confidence_dic,
      Volatility_dic,
      Time_Pressure_dic,
      Max_Planning_Time=simulation_parameters[user_id]["PT"],
      Intelligence_Confidence_key=simulation_parameters[user_id]["IC"],
      Volatility_key=simulation_parameters[user_id]["VL"],
      Time_Pressure_key=simulation_parameters[user_id]["TP"],
      n=simulation_parameters[user_id]["n"],
      w1=w1, w2=w2, w3=w3,
      k=8,
      threshold=0.6,
      noise_ic=0.05, noise_v=0.05, noise_time=1.0
  )

  IC_key, V_key, TP_key = simulation_parameters[user_id]["IC"], simulation_parameters[user_id]["VL"], simulation_parameters[user_id]["TP"]
  print("Scenario:", IC_key, V_key, TP_key)
  print(coa_wp)
  print(rec)

  compare_stats_text = f"Scenario: {IC_key}, {V_key}, {TP_key}\n"
  for key, value in coa_wp.items():
    compare_stats_text += f"for {key} CoA, 90 percentile win probability is at {value.get('WinProb_P90'):.2f} with a {value.get('Critical_%')*100:.2f}% critical tail\n"

  print(compare_stats_text)

  message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
  {compare_stats_text}
  {rec}
  """


  # message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
  # Parameters: {IC_key} {V_key} {TP_key}
  # {rec}
  # """

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message) #bring back menu buttons
  #end win probability

def simulation_p1_AR_summary(message):
  #use placeholder data for AR summary
  #later we should save or re-run CoA, Sensitivity, and Win Probability
  #analysis and use that data for AR summary
  global simulation_parameters
  global strategic_direction_name
  user_id = message.chat.id

  scenario_keys = ("50%", "High", "6h")
  dri_stats = {"base_dri": 0.62, "p90": 0.78, "crisis_plus": 0.41, "critical_tail": 0.12}
  coa_rows = [
      {"name": "Attack", "p90": 0.81, "win": 0.43, "crit": 0.15},
      {"name": "Regroup", "p90": 0.70, "win": 0.55, "crit": 0.06},
  ]
  recommendation = {"coa": "Regroup", "why": "lowest P90 + lowest Critical"}
  sensitivity = {"order": ["TP", "V", "IC"]}

  lines = build_ar_summary_short(scenario_keys, dri_stats, coa_rows, recommendation, sensitivity)

  # Вивід як 4 рядки (під Telegram або AR HUD)
  message_text = "\n".join(lines)

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
  simulation_phase_one_analyze(message) #bring back menu buttons
  #end AR Summary

  pass

def simulation_p1_conclude(message):
  # see Transition Gate Function
  # pass

  # temporarily using this to display scores

  global current_score
  global score_table
  user_id = message.chat.id
  score = 0

  for i in range(5, len(current_score[user_id])):
    score += current_score[user_id][i][0]
  message_text = f"Total score is {score} points for run {current_score[user_id][1]}"
  # print(message_text)
  run_id = current_score[user_id][2]
  score_table[run_id] = current_score[user_id]

  bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)


#обробка тимчасових кніпок
@bot.callback_query_handler(func=lambda call: call.data.startswith("p1_placeholder:"))
def handle_placeholder(call):
  callback = call.data.split(':')[1] #split the function and take second part only
  bot.answer_callback_query(call.id, text=f"Processing {callback}...")

  if callback == "btn_a":
      handle_logic_a(call.message)
  elif callback == "btn_b":
      handle_logic_b(call.message)
  else:
      # Fallback or generic pass
      pass

  print(f"Universal Handler caught: {callback}")


# виклик АР підсумку
@bot.callback_query_handler(func=lambda call: call.data == "AR_summary")
def handle_AR_summary(call):
  bot.answer_callback_query(call.id)
  AR_summary = AR_summary_placeholder(simulation_results)

  markup = types.InlineKeyboardMarkup()
  restart = types.InlineKeyboardButton("Restart", callback_data="init_Start")
  markup.add(restart)

  bot.send_message(call.message.chat.id, f"AR: {AR_summary}", reply_markup=markup)


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

### START BOT

print("<info>: Bot is listening")
bot.infinity_polling()

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
