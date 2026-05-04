# from telebot.formatting import escape_markdown
# from simulations import(
from bot.simulations import (
    Intelligence_Confidence ,
    Volatility              ,
    Time_Pressure           ,
    # Max_Planning_Time       , # defaults to "=48" hours
    Decision_Risk_Index     ,
)
# from bot.simulations import P1_Shuffle as Shuffle
# from bot.simulations import P1_Monte_Carlo as Monte_Carlo_DRI_fixed_keys
# from bot.simulations import P1_Compare_CoA as Monte_Carlo_Compare_COA_fixed_keys
# from bot.simulations import P1_WinProb as Monte_Carlo_Compare_COA_With_WinProb_fixed_keys
# from bot.simulations import P1_Sensitivity_Analysis as Sensitivity_Analysis_DRI_fixed_keys

# Intelligence_Confidence_key, Volatility_key, Time_Pressure_key = Shuffle(
#     Intelligence_Confidence ,
#     Volatility              ,
#     Time_Pressure           ,
# )

from telebot.formatting import escape_markdown

linebreak : str = "~                     ~​" # MarkdownV2 line breakw/ zero width space

# region Welcome message
message_bot_welcome = """
    Welcome to the *TRIADAI−SUS* Framework
    _AI/AR−Driven Strategic Uncertainty & Decision Simulation Environment_

    *TRIADAI−SUS* is a strategic wargaming and decision−support framework designed to strengthen command thinking and improve military strategic planning under uncertainty\\.
    This simulation environment introduces modern Artificial Intelligence methods into the decision−making process and demonstrates how data−driven tools can support commanders at operational and strategic levels\\.

    🎯 Purpose of the Framework
    TRIADAI−SUS is designed for:
    • Enhancing strategic command thinking during military planning and crisis response
    • Introducing modern AI algorithms into professional military education
    • Explaining how AI tools support evidence−based decision−making in complex and uncertain environments
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
    • Evaluate alternative Courses of Action \\(COA\\)
    • Observe Win Probability and risk indicators in real time
    • Understand how uncertainty affects operational success
    • Learn to interpret AI−generated recommendations
    • Develop structured decision−making under time pressure
    """
# endregion

# region Explain Phase One
message_p1_explain = """
    *Initial Strategic Environment Assessment*

    _Decision Risk Index \\(DRI\\)_ — Operational Readiness Indicator
    At the start of the simulation, the system evaluates the operational environment using four key planning parameters\\.
    These parameters reflect the level of uncertainty, time constraints, and information reliability that will shape your decisions\\.

    Input Parameters
    1\\. Intelligence Confidence
    _Represents the reliability and completeness of available intelligence\\._
    High confidence: 90%
    Moderate confidence: 50%
    Low confidence: 20%
    `Intelligence_Confidence_dic = {"90%": 0\\.9, "50%": 0\\.5, "20%": 0\\.2}`

    2\\. Operational Volatility
    _Describes the level of unpredictability in the environment\\._
    Low volatility: Stable and predictable conditions
    Medium volatility: Changing operational dynamics
    High volatility: Rapid and uncertain developments
    `Volatility_dic = {"Low": 0\\.3, "Medium": 0\\.6, "High": 0\\.9}`

    3\\. Maximum Planning Time
    _48 hours — the maximum available time horizon for strategic planning under normal conditions\\. _

    4\\. Time Pressure
    _Defines how urgently a decision must be made\\._
    Strategic Analysis: 48 hours
    Operational Level: 6 hours
    Crisis Decision: 0\\.5 hours
    `Time_Pressure_dic = {"Strategic Analysis": 48, "Operational level": 6, "Crisis decision": 0\\.5}`

    _Decision Risk Index \\(DRI\\)_
    Based on these parameters, the framework calculates the Decision Risk Index \\(DRI\\) — a quantitative indicator of the decision environment\\.
    The DRI helps commanders understand how difficult, unstable, and time−constrained the situation is before selecting a Course of Action\\.

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
    Time pressure and uncertainty significantly affect decision−making\\.
    _Critical State_
    DRI ≥ 0\\.80
    The environment is unstable and highly time−sensitive\\. Decisions must be made under severe constraints\\.

    ℹ️ How Monte Carlo works
    • Step 1: The bot picks ONE mission scenario: IC / Volatility / Available time\\.
    • Step 2: We run 5000 simulations around that scenario, adding uncertainty \\(noise\\):
    \\- IC varies by ±0\\.05
    \\- Volatility varies by ±0\\.05
    \\- Available time varies by ±1\\.0h
    • Step 3: Each run computes DRI using weights w1\\=0\\.33, w2\\=0\\.33, w3\\=0\\.33 and Max planning time \\= 48h\\.

    ✅ Output:
    • Base DRI \\(no−noise scenario\\)
    • Mean DRI \\(average over all runs\\)
    • P90 DRI \\(bad−tail risk\\)
    • Crisis\\+Critical % and Critical tail %
    Meaning: not one forecast — a risk distribution under uncertainty\\.

    """
# endregion

# region MC Telegram message format
# -------------------------
# 4) Форматування відповіді для Telegram
# -------------------------
def format_phase1_message(mc_result: dict) -> str:
    sc = mc_result["scenario"]

    # красиві % для IC (якщо ключі типу "50%" — просто показуємо ключ)
    ic_label = Intelligence_Confidence.classify(sc['IC']).display_name
    v_label = Volatility.classify(sc['V']).display_name
    t_label = Time_Pressure.classify(sc['TP']).display_name

    mean_dri = mc_result["mean_dri"]
    p90 = mc_result["p90"]
    base_dri = mc_result["base_dri"]

    crisis_or_worse = mc_result["crisis_or_worse"] * 100
    critical_tail = mc_result["critical_tail"] * 100

    return (
        "🛰️ Phase 1 — Reconnaisance (mission scenario)\n"
        f"Scenario: IC={ic_label}, Volatility={v_label}, Time={t_label}\n\n"
        "📌 Decision Risk Index (DRI)\n"
        f"• Base DRI: {base_dri:.3f} ({Decision_Risk_Index.classify(base_dri).display_name})\n"
        f"• Mean DRI (MC): {mean_dri:.3f}\n"
        f"• P90 DRI (MC): {p90:.3f}\n\n"
        "⚠️ Risk level probability (Monte Carlo)\n"
        f"• Crisis+Critical: {crisis_or_worse:.1f}%\n"
        f"• Critical tail: {critical_tail:.1f}%\n"
    )



# -------------------------
# 5) One-shot: обрати сценарій + порахувати + текст
# -------------------------
# def run_phase1(
#     Intelligence_Confidence_dic,
#     Volatility_dic,
#     Time_Pressure_dic,
#     Max_Planning_Time,
#     n=10000,
#     w1=0.33, w2=0.33, w3=0.33,
#     noise_ic=0.05, noise_v=0.05, noise_time=1.0
# ) -> str:
#     IC_key, V_key, TP_key = Shuffling_IC_V_TP(Intelligence_Confidence_dic, Volatility_dic, Time_Pressure_dic)

#     mc = Monte_Carlo_DRI_fixed_keys(
#         Intelligence_Confidence_dic=Intelligence_Confidence_dic,
#         Volatility_dic=Volatility_dic,
#         Time_Pressure_dic=Time_Pressure_dic,
#         Max_Planning_Time=Max_Planning_Time,
#         Intelligence_Confidence_key=IC_key,
#         Volatility_key=V_key,
#         Time_Pressure_key=TP_key,
#         n=n,
#         w1=w1, w2=w2, w3=w3,
#         noise_ic=noise_ic, noise_v=noise_v, noise_time=noise_time
#     )

#     return format_phase1_message(mc)


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
            "• Base DRI (no−noise scenario)\n"
            "• Mean DRI (average over all runs)\n"
            "• P90 DRI (bad−tail risk)\n"
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
# endregion

# mc = Monte_Carlo_DRI_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
# # print(f"raw:\n{mc}")
# print("===Monte Carlo fixed keys===")
# print(f"{format_phase1_message(mc)}\n\nraw:\n{mc}")

# region Coa TG message
def format_coa_message(scenario_keys, coa_results, best) -> str:
    IC_key, V_key, TP_key = scenario_keys

    recommendation = f"Suggestion: **{best}** (minimal P90, and/or lesser Critical tail)."
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
# endregion

# results, best = Monte_Carlo_Compare_COA_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)

# print("===Monte Carlo CoA fixed keys===")
# print(format_coa_message((Intelligence_Confidence_key, Volatility_key, Time_Pressure_key),results,best))

# region WinP TG message



# endregion

# results, best = Monte_Carlo_Compare_COA_With_WinProb_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key)
# recommendation = (
#     f"According to integral criterion (WinProb_mean − Critical_tail) best course of action is: **{best}**."
# )
# print(recommendation)
# print("===Monte Carlo Win Probability fixed keys===")

# region sensitivity TG message

# endregion
# print(Sensitivity_Analysis_DRI_fixed_keys(Intelligence_Confidence_key, Volatility_key, Time_Pressure_key))
# print("===Sesitivity Analysis fixed keys===")

# region scoring
    # region sensitivity
def sens_score_ask(strategic_direction_name: str, P1_simulation_results: str):
    message_text = "".join([
        "Evaluating the \"", escape_markdown(strategic_direction_name), "\" strategic direction:\n",
        escape_markdown(P1_simulation_results), # implicit \n in format
        "~                    ~​\n\n",
        " \\> *Which parameter has the greatest impact on the outcome?*"
    ])
    return message_text

def sens_score_answer(strategic_direction_name: str, sens: dict[str,object], influence_share: dict[str,float]):
    
    message_text = "".join([
    escape_markdown(
    f"""Evaluating the \"{strategic_direction_name}\" direction:
    Scenario parameters:
        Intel:  {sens["scenario"]['IC_key'].display_name},
        Volatility: {sens["scenario"]['V_key'].display_name},
        Time pressure: {sens["scenario"]['TP_key'].display_name}
    Spearman correlation:
        Intel:  {sens["spearman_corr"]['IC']:.2f}, 
        Volatility: {sens["spearman_corr"]['V']:.2f},
        Time pressure: {sens["spearman_corr"]['TP']:.2f}
    Influence share:     
        Intel:  {influence_share['IC']:.2f}, 
        Volatility: {influence_share['V']:.2f}, 
        Time pressure: {influence_share['TP']:.2f}
    """), # type: ignore # pyright: ignore[reportIndexIssue]
    "~                     ~​"
    ])
    return message_text
    # endregion

    # region Win Probability
def winp_score_ask(strategic_direction_name: str, P1_simulation_results: str):
    message_text = "".join([
        "Evaluating the \"", escape_markdown(strategic_direction_name), "\" strategic direction:\n",
        escape_markdown(P1_simulation_results), # implicit \n in format
        "~                    ~​\n\n",
        " \\> *Which course of action has the highest Win Probability?*"
    ])
    return message_text

def winp_score_answer(strategic_direction_name: str, simulation_parameters:dict[str,object], coa_wp:dict[str,object], rec:str):

    IC_key, V_key, TP_key = simulation_parameters["IC"], simulation_parameters["VL"], simulation_parameters["TP"]
    compare_stats_text = f"Scenario: IC: {IC_key.display_name}\\, V: {V_key.display_name}\\, TP: {TP_key.display_name}\n" # type: ignore
    for key, value in coa_wp.items():
        compare_stats_text += escape_markdown(f"  for {key} CoA, 90 percentile win probability is at {value.get('WinProb_P90'):.2f} with a {value.get('Critical_%')*100:.2f}% critical tail\n") # type: ignore

    
    message_text = f"""Evaluating the \"{escape_markdown(strategic_direction_name)}\" direction:
{compare_stats_text}
{f"According to integral criterion \\(WinProb\\_mean − Critical\\_tail\\) best course of action is: *{rec}*\\."}
~                     ~​
    """
    print(message_text)
    return message_text

    # endregion

# endregion

# print(sens_score_ask("name", "parameters\ncome\nhere"))

# region AR Summary
def build_ar_summary_short(
    scenario_keys,          # (IC_key, V_key, TP_key) e.g. ("50%", "High", "6h")
    dri_stats,              # {"base_dri": float, "p90": float, "crisis_plus": float, "critical_tail": float}
    coa_rows,               # list of dicts: [{"name":"Наступ","p90":0.81,"win":0.43,"crit":0.15}, ...]
    recommendation,         # {"coa":"Перегрупування","why":"lowest P90 + lowest Critical"}
    sensitivity=None        # optional: {"top":"TP", "order":["TP","V","IC"]} or {"shares":{"TP":0.48,...}}
):
    """
    Повертає 4 короткі рядки для AR−екрана (1 погляд = 1 рішення).
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

# endregion

# print("AR Summary tested")

#region Regiments
    regiments = {    
        'Ground Forces'         : 'Ground',
        'Air Force'             : 'Airforce',
        'Navy'                  : 'Navy',
        'Airborne Assault F'    : 'Airborne',
        'Special Operations F'  : 'SOF',
        'Territorial Defense F' : 'TDF',
        'Unmanned Systems F'    : 'USF',
        'Support Forces'        : 'Support',
        'Logistics Forces'      : 'Logistic',
        'Medical Forces'        : 'Medical',
        'Signal and Cybersec F' : 'SigSec',
    }
#endregion

#region Phase two: Regiment parameters
def regiment_parameters(selection: list[str], raw: bool = False):
    # print(f"parameters formatting! received: {selection}")
    regiments = {    
        'Ground Forces'         : 'Ground',
        'Air Force'             : 'Airforce',
        'Navy'                  : 'Navy',
        'Airborne Assault F'    : 'Airborne',
        'Special Operations F'  : 'SOF',
        'Territorial Defense F' : 'TDF',
        'Unmanned Systems F'    : 'USF',
        'Support Forces'        : 'Support',
        'Logistics Forces'      : 'Logistic',
        'Medical Forces'        : 'Medical',
        'Signal and Cybersec F' : 'SigSec',
    }
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
    def pretty_display(force_parameters: dict[str,float]) -> str:
        output = ""
        for param, value in force_parameters.items():
            output += f"{param.replace("_"," ").capitalize()}: {value:.2f}\n"
        # print(f"-<Attention!>-")
        # print(output)
        return "```\n" + escape_markdown(output) + "\n```"

    parameters = {
        'Ground Forces'         : Ground_Forces,
        'Air Force'             : Air_Force,
        'Navy'                  : None,
        'Airborne Assault F'    : None,
        'Special Operations F'  : None,
        'Territorial Defense F' : None,
        'Unmanned Systems F'    : Unmanned_Forces,
        'Support Forces'        : None,
        'Logistics Forces'      : None,
        'Medical Forces'        : Medical_Forces,
        'Signal and Cybersec F' : None,
    }
    message_text = ""

    print("-----startmainloop")
    for regiment, alias in regiments.items():
        print(regiment)
        if alias in selection:
            # print(f"displayin {regiment} parameters")
            if raw:
                message_text += f"{regiment} parameters: \n ```python\n{str(parameters[regiment])\
                                                                            .replace('{','{\n\t')\
                                                                            .replace(',','\n\t')\
                                                                            .replace('}','\n}')\
                                                                        }```\n\n"
            else:
                message_text += f"{regiment} parameters: \n {pretty_display(parameters[regiment])}\n\n"
    return message_text
#endregion
