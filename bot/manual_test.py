# region Send-Receive
# Manually testing php_send

from php_send import send_to_php, AR_format

from simulations import (
    # P1 Parameters
    Intelligence_Confidence,
    Volatility,
    Time_Pressure,
    Decision_Risk_Index, #output parameter
    # P1 functions
    P1_Shuffle,
    P1_Monte_Carlo,
    P1_Compare_CoA,
    P1_WinProb,
    P1_Sensitivity_Analysis,
)

IC,V,TP = P1_Shuffle(Intelligence_Confidence,Volatility,Time_Pressure) # type: ignore
print(IC.display_name,V.display_name,TP.display_name)
results, rec = P1_WinProb(IC,V,TP,n=1000)
results = results[rec]
dri_mean, dri_p90, tail_crit = results['Mean_DRI'],results['P90_DRI'],results['Critical_%']
print(dri_mean, dri_p90, tail_crit)
params = {
    "Intel"     : IC,
    "Volatility": V,
    "Time pres.": TP,
    "Mean DRI"  : dri_mean,
    "p90 DRI"   : dri_p90,
    "Critical tail": tail_crit,
}
print("\\============/")
print(AR_format(params,60))

    # parameters (Intelligence Confidence, Volatility, Time Pressure, Max Planning Time (optional) )
    # Decision Risk Index(base, simulated p90, simulated mean)
    # Critical Tail,  Win probability, Sensitiity Analysis
    # Team Name, Direction, total Score, timestamp
    
    # region parameters flat
# print("---")
# parameters = {
#     "Team_Name"     : None,
#     "Direction"     : None,
#     "total_score"   : None,
#     "date"          : None,
#     "Intelligence Confidence": None, 
#     "Volatility"        : None, 
#     "Time Pressure"     : None, 
#     # "Max Planning Time": 48,
#     "DRI"       : None,
#     "DRI_p90"   : None,
#     "DRI_mean"  : None,
#     "Critical Tail"     : None,  
#     "Win probability"   : None, 
#     "Sensitivity Analysis": None,
# }

# print(AR_format(parameters))
    # endregion

    # region parameters structured
import json

p1_params = {
    "Intelligence Confidence": None, 
    "Volatility"            : None, 
    "Time Pressure"         : None, 
    # "Max Planning Time": 48,
}

dri = {
    "base"  : None,
    "p90"   : None,
    "mean"  : None,
}

sim_details = {
    "Critical Tail"     : None,  
    "Win probability"   : None, 
    "Sensitivity Analysis": None,
}

data_to_send = {
    "Team_Name"     : None,
    "Direction"     : None,
    "total_score"   : None,
    "date"          : None,
    "Simulation Parameters" : p1_params,
    "Decision Risk Index"   : dri,
    "Simulation Details"    : sim_details,
}

json_data = json.dumps(data_to_send)
print(f"---\n{json_data}\n---")
print(json.dumps(data_to_send, sort_keys=True, indent=2))

    # endregion

# endregion

"""
simulation_results[chat_id]['P1'] contains all the data
data = simulation_results[chat_id]['P1']
data['base_dri']
data['mean_dri']
data['p90']
data['critical_tail']

CoA['best'] = best
for key, value in CoA.items:
    CoA[key] = value
simulation_results[chat_id]['P1']['CoA'] = CoA

simulation_results[chat_id]['P1']['sens'] = sens
"""

# print("/===test===\\")
# test = 'lol'
# if test == 'lmao' or 'lol':
#     print(f"yes, it's <{test}>")
# else:
#     print("whoddafookareyou?")


# region Formatting tests

# from telebot import formatting

# message = formatting.format_text(
#     formatting.mbold('Hello'),
#     formatting.mitalic('World'),
#     separator=" "
# )
# print(message)

# endregion