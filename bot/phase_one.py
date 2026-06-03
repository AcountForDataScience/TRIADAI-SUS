# a few basics until I figure out a cleaner way
from telebot import types
from telebot.util import quick_markup, generate_random_token
import datetime

# simulation functions
from bot.simulations import (
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

# bot instance so I can use decorators 
from bot.instance import bot

# global variables
# to do: replace with a database at some later point
from bot.state import (
    back_where,
    gamemode,
    simulation_results,
    simulation_parameters,
    strategic_direction_name,
    custom_name,
    user_locale,
    score_table,
    current_score
)

questions = {}

# Prettify output text
from bot.format_messages import (
    # Static Strings
    message_p1_explain,
    # Dynamic Strings
    format_phase1_message,
    explain_monte_carlo_phase1,
    format_coa_message,
)
import bot.format_messages as getmessage

from bot.php_send import send_to_php, AR_format # stuff to send messages to AR goggles 

# region Phase One

##-----------------------------##
#         Phase  One            #
##-----------------------------##

# ---> init_start is the entry point callback
@bot.callback_query_handler(func=lambda call: call.data == "init_start")
def handle_start_phase_one(call):
    bot.answer_callback_query(call.id, "Preparing the simulation") #removes loading symbol
    next = bot.send_message(call.message.chat.id, getmessage.init_direction, parse_mode="MarkdownV2")
    
    # Hand off the flow to the 'name_strategic_direction' function
    bot.register_next_step_handler(next, name_strategic_direction)
    

# Назва напрямку
    # region Name direction
def name_strategic_direction(message):
    direction = message.text

    markup = types.InlineKeyboardMarkup()
    # btn_param = types.InlineKeyboardButton("Визначити параметри", callback_data="init_set_parameters")
    btn_rename = types.InlineKeyboardButton(getmessage.button_direction_rename, callback_data="init_rename", style="danger")
    btn_start = types.InlineKeyboardButton(getmessage.button_direction_confirm.format(direction = direction[:20]), callback_data="start_simulation",style="success")

    # Each line adds a row of buttons
    markup.add(btn_start, btn_rename)
    # markup.add(btn_param)

    strategic_direction_name[message.chat.id] = message.text
    # print(strategic_direction_name[message.chat.id])
    bot.reply_to(message, getmessage.init_direction_confirm.format(direction = strategic_direction_name[message.chat.id]), reply_markup=markup)

# переназвати напрямок
@bot.callback_query_handler(func=lambda call: call.data == "init_rename")
def handle_name_strategic_direction(call):
    bot.answer_callback_query(call.id) #removes loading symbol
    next = bot.send_message(call.message.chat.id, getmessage.init_direction_rename, parse_mode="MarkdownV2")
    # Hand off the flow to the 'name_strategic_direction' function
    bot.register_next_step_handler(next, name_strategic_direction)

    # endregion

# визначити параметри
@bot.callback_query_handler(func=lambda call: call.data == "init_set_parameters")
def game_set_parameters(call):
  bot.answer_callback_query(call.id) #removes loading symbol
  pass


# початок симуляції
@bot.callback_query_handler(func=lambda call: call.data == "start_simulation")
def handle_simulation_p1_start(call):
    bot.answer_callback_query(call.id, "selecting parameters...")
    simulation_phase_one_results(call.message)

@bot.callback_query_handler(func=lambda call: call.data == "p1_restart")
def handle_simulation_p1_restart(call):
    bot.answer_callback_query(call.id, "shuffling parameters...")
    simulation_phase_one(call.message.chat.id)
    simulation_phase_one_results(call.message)


### simulation scenario

    #region P1 Monte-Carlo
def simulation_phase_one(chat_id):
    IC, V, TP = P1_Shuffle(Intelligence_Confidence, Volatility, Time_Pressure) # type: ignore
    run_sample = 5000

    simulation_parameters[chat_id] = {
        "IC" : IC,
        "VL" : V,
        "TP" : TP,
        "PT" : 48, # Max_Planning_Time = 48
        "n"  : run_sample,
        #also recording weights here
        "weights": {
            "w1" : 0.33,
            "w2" : 0.33,
            "w3" : 0.33
        }
    }

    p1_results = P1_Monte_Carlo(
        IC,
        V,
        TP,
        n=run_sample
    )

    simulation_results[chat_id] = { "P1" : format_phase1_message(p1_results)}
    simulation_results[chat_id]["P1_raw"] = p1_results
    if gamemode[chat_id] == 'test':
        print(simulation_results)
    #simulation end

def simulation_phase_one_results(message):
    if not message.chat.id in simulation_results:
        simulation_phase_one(message.chat.id)

    markup = types.InlineKeyboardMarkup()

    btn_restart = types.InlineKeyboardButton(getmessage.button_parameters_shuffle, callback_data="p1_restart", style="danger")
    btn_explain = types.InlineKeyboardButton(getmessage.button_explain_phase1, callback_data="p1_explain",style="primary")
    btn_next    = types.InlineKeyboardButton(getmessage.button_parameters_confirm, callback_data="p1_confirm_parameters", style="success")

    # Each line adds a row of buttons
    markup.add(btn_restart, btn_explain)
    markup.add(btn_next)

    response_text = getmessage.init_direction_confirm[:-1].format(direction = strategic_direction_name[message.chat.id]) + ": " + simulation_results[message.chat.id]["P1"]
    bot.edit_message_text(response_text, message.chat.id, message.id, reply_markup=markup)

#end of phase one monte carlo
    #endregion

    #region Explain P1
@bot.callback_query_handler(func=lambda call: call.data == "p1_explain")
def handle_p1_explain(call):
    bot.answer_callback_query(call.id)
    simulation_phase_one_explain(call.message)

def simulation_phase_one_explain(message):

    # explain = explain_monte_carlo_phase1(
    #     simulation_parameters[message.chat.id]["n"],
    #     Max_Planning_Time=simulation_parameters[message.chat.id]["PT"],
    #     w1=0.33, w2=0.33, w3=0.33,
    #     noise_ic=0.05,
    #     noise_v=0.05,
    #     noise_time=1.0,
    #     lang="en")

    explain = message_p1_explain

    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton(getmessage.button_back, callback_data="start_simulation", style="success")

    # Each line adds a row of buttons
    markup.add(btn_back)

    bot.edit_message_text(explain, message.chat.id, message.id, reply_markup=markup, parse_mode="MarkdownV2")
    #endregion

#Підтвердження параметрів
@bot.callback_query_handler(func=lambda call: call.data == "p1_confirm_parameters")
def handle_simulation_p1_confirm_parameters(call):
    bot.answer_callback_query(call.id, "parameters are confirmed")
    
    # scoring
    run_id = generate_random_token()
    user_id = call.message.chat.id
    user_name = custom_name[user_id]
    timestamp = datetime.date.today()
    if gamemode[user_id] == 'test':
        print(f"run #{run_id} @{timestamp}")
    current_score[user_id] = { "Metadata": {
            'user_id'   : user_id,
            'user_name' : user_name,
            'direction' : strategic_direction_name[user_id],
            'run_id'    : run_id,
            'datestamp' : timestamp.isoformat() #in a better format   
        },
        "Phase One": {
            'IC'        : simulation_parameters[user_id]['IC'],
            'VL'        : simulation_parameters[user_id]['VL'],
            'TP'        : simulation_parameters[user_id]['TP'],
            'PT'        : simulation_parameters[user_id]['PT'],
            'base_dri'  : simulation_results[user_id]["P1_raw"]["base_dri"],
            'mean_dri'  : simulation_results[user_id]["P1_raw"]["mean_dri"],
            'p90_dri'   : simulation_results[user_id]["P1_raw"]["p90"],
            'critical_tail':simulation_results[user_id]["P1_raw"]["critical_tail"],
        }
    }
    if gamemode[user_id] == 'test':
        print(f"score record created for {run_id}:\n{current_score[call.from_user.id]}")

    simulation_phase_one_analyze(call.message)

def simulation_phase_one_analyze(message):
    markup = types.InlineKeyboardMarkup()

    # if gamemode[user_id] == 'command':
    #     btn_CoA = types.InlineKeyboardButton("Compare CoA", callback_data="p1_analysis:Compare CoA")
    #     btn_SAnal = types.InlineKeyboardButton("Sensitivity Analysis", callback_data="p1_analysis:Sensitivity Analysis")
    #     btn_WinP = types.InlineKeyboardButton("Win Probability", callback_data="p1_analysis:Win Probability")
    #     btn_AR = types.InlineKeyboardButton("AR summary", callback_data="p1_analysis:AR Summary")
    #     btn_conclude = types.InlineKeyboardButton("Phase 2 suggestions", callback_data="p1_placeholder:Phase one conclusion")

    #     Each line adds a row of buttons
    #     markup.add(btn_CoA,btn_WinP,btn_SAnal)
    #     markup.add(btn_AR,btn_conclude)
    #     markup.add(btn_AR)

    #     markup = quick_markup({
    #     # 'Test CoA'                  : {'callback_data': 'p1_analysis:Test CoA'},
    #     'Test Sensitivity analysis' : {'callback_data': 'p1_analysis:Test Sens'},
    #     'Test Win Probability'      : {'callback_data': 'p1_analysis:Test WinP'}
    #     }, row_width=2)

    btn_Test_Sens = types.InlineKeyboardButton(
        getmessage.button_test_sensitivity,
        callback_data="p1_analysis:Test Sens")
    btn_Test_WinP = types.InlineKeyboardButton(
        getmessage.button_test_winprobability,
        callback_data="p1_analysis:Test WinP")
    btn_Conclude = types.InlineKeyboardButton(
        getmessage.button_test_complete_p1,
        callback_data="p1_analysis:Conclude")

    Sens = WinP = False

    user_id = message.chat.id

    if 'Sensitivity' in current_score[user_id]:
        Sens = True
    if 'Win Probability' in current_score[user_id]:
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


    # region Scoring
@bot.callback_query_handler(func=lambda call: call.data.startswith("p1_analysis:"))
def handle_p1_analysis(call):
    callback = call.data.split(':')[1] # split callback data at ":" and use everything after "p1_analysis"
    bot.answer_callback_query(call.id, text=f"processing {callback}...")

    if callback == "Score Sens":
        callback=call.data.split(':')[2]
        # print(callback)
        simulation_p1_score_sens(call.message,callback)

    if callback == "Score WinP":
        callback=call.data.split(':')[2]
        # print(callback)
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
    
    elif callback == "Conclude":
        simulation_p1_conclude(call.message)
    else:
        # Fallback or generic pass
        pass
    # print(f"processed callback: {callback}")

        # region Scoring Sensitivity
def simulation_p1_test_sens(message):
    user_id = message.chat.id
    message_text = getmessage.sens_score_ask(strategic_direction_name[message.chat.id], simulation_results[message.chat.id]["P1"])

    markup = quick_markup({
        getmessage.button_IC : {'callback_data': 'p1_analysis:Score Sens:IC'},
        getmessage.button_VL : {'callback_data': 'p1_analysis:Score Sens:V'},
        getmessage.button_TP : {'callback_data': 'p1_analysis:Score Sens:TP'}
    }, row_width=3)

    bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")

def simulation_p1_score_sens(message,answer):
    user_id = message.chat.id
    w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
    
    sens = P1_Sensitivity_Analysis(
        Intelligence_Confidence=simulation_parameters[user_id]["IC"],
        Volatility=simulation_parameters[user_id]["VL"],
        Time_Pressure=simulation_parameters[user_id]["TP"],
        Max_Planning_Time=simulation_parameters[user_id]["PT"],
        n=simulation_parameters[user_id]["n"],
        w1=w1, w2=w2, w3=w3,
        noise_ic=0.05, noise_v=0.05, noise_time=1.0
    )

    if gamemode[user_id] == 'test':
        print('sensitivity analysis p1#355')
        print(sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True))
    answer_key = sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0]

    def prettify(parameter):
        match parameter:
            case 'V' : return "Volatility"
            case 'IC': return "Intel Confidence"
            case 'TP': return "Time Pressure"

    if answer == answer_key:
        correct = 1
        score_text = f"your answer {prettify(answer)} is correct"
    else:
        correct = 0
        score_text = f"your answer {prettify(answer)} is incorrect: it's {prettify(answer_key)}"
    
    current_score[user_id]['Sensitivity'] = {
        'score'     : correct,
        'question'  : "Sensitivity",
        'answer'    : prettify(answer),
        'context'   : sens,
    }

    influence_share = {k: round(v*100, 1) for k, v in sens["influence_share"].items()}

    message_text = "\n\n".join([
        getmessage.sens_score_answer(strategic_direction_name[user_id],sens,influence_share),
        score_text
        ])

    save_sens = {}
    save_sens['best'] = answer_key
    save_sens['spearman_corr'] = sens['spearman_corr']
    save_sens['influence_share'] = sens['influence_share']
    save_sens['combined_score'] = sens['combined_score']

    simulation_results[user_id]['P1_raw']['sens'] = save_sens
    if gamemode[user_id] == 'test':
        print(f"SENSITIVITY:\n{save_sens}")
        print(f"simresults:\n{simulation_results[user_id]['P1_raw']}")

    if gamemode[user_id] == 'default':
        message_text = "your answer has been recorded"

    bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id, parse_mode="MarkdownV2")
    simulation_phase_one_analyze(message)

        # endregion
        
        # region Scoring Win Probability
def simulation_p1_test_winp(message):
    user_id = message.chat.id
    message_text=getmessage.winp_score_ask(strategic_direction_name[message.chat.id],simulation_results[message.chat.id]["P1"])
 
    markup = quick_markup({
        'Attack'  : {'callback_data': 'p1_analysis:Score WinP:Attack'},
        'Regroup' : {'callback_data': 'p1_analysis:Score WinP:Regroup'}
    }, row_width=3)

    bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")

def simulation_p1_score_winp(message,answer):
    user_id = message.chat.id

    w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
    coa_wp, rec = P1_WinProb(
        Intelligence_Confidence=simulation_parameters[user_id]["IC"],
        Volatility=simulation_parameters[user_id]["VL"],
        Time_Pressure=simulation_parameters[user_id]["TP"],
        Max_Planning_Time=simulation_parameters[user_id]["PT"],
        n=simulation_parameters[user_id]["n"],
        w1=w1, w2=w2, w3=w3,
        k=8,
        threshold=0.6,
        noise_ic=0.05, noise_v=0.05, noise_time=1.0
    )

    if gamemode[user_id] == 'test':
        print('win probability p1#434')
        print(sorted(coa_wp.items(), key=lambda item: item[1]["WinProb_Mean"]-item[1]["Critical_%"], reverse=True))

    answer_key = sorted(coa_wp.items(), key=lambda item: item[1]["WinProb_Mean"]-item[1]["Critical_%"], reverse=True)[0][0]

    if answer == answer_key:
        correct = 1
        score_text = f"Chosen course of action {answer} has highest win probability"
    else:
        correct = 0
        score_text = f"Chosen course of action {answer} is incorrect: {answer_key} has highest win probability"
 
    current_score[user_id]['Win Probability'] = {
        'score'     : correct,
        'question'  : "Win Probability",
        'answer'    : answer,
        'context'   : coa_wp,
    }

    message_text = "\n".join([
        getmessage.winp_score_answer(strategic_direction_name[user_id],simulation_parameters[user_id],coa_wp,rec),
        score_text,
    ])

    WinP = {}
    WinP['best'] = answer_key
    for key, value in coa_wp.items():
        WinP[key] = value
    simulation_results[user_id]['P1_raw']['WinP'] = WinP

    if gamemode[user_id] == 'test':
        print(f"WinProb:\n{WinP}")

    if gamemode[user_id] == 'default':
        message_text = "your answer has been recorded"
    
    bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id, parse_mode="MarkdownV2")
    simulation_phase_one_analyze(message)
        #endregion
    
    #endregion
# scoring #######################################

    #region deprecated? 
def simulation_p1_compare_coa(message):
    #display CoA comparison and all the buttons
    user_id = message.chat.id

    w1,w2,w3 = simulation_parameters[user_id]['weights'].values()
    coa_results, recommendation = P1_Compare_CoA(
        Max_Planning_Time=simulation_parameters[user_id]["PT"],
        Intelligence_Confidence=simulation_parameters[user_id]["IC"],
        Volatility=simulation_parameters[user_id]["VL"],
        Time_Pressure=simulation_parameters[user_id]["TP"],
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
    user_id = message.chat.id
 
    w1,w2,w3 = simulation_parameters[user_id]['weights'].values()   
    sens = P1_Sensitivity_Analysis(
        Intelligence_Confidence=simulation_parameters[user_id]["IC"],
        Volatility=simulation_parameters[user_id]["VL"],
        Time_Pressure=simulation_parameters[user_id]["TP"],
        Max_Planning_Time=simulation_parameters[user_id]["PT"],
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
    coa_wp, rec = P1_WinProb(
        Intelligence_Confidence=simulation_parameters[user_id]["IC"],
        Volatility=simulation_parameters[user_id]["VL"],
        Time_Pressure=simulation_parameters[user_id]["TP"],
        Max_Planning_Time=simulation_parameters[user_id]["PT"],
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
    # endregion deprecated stuff? 



def simulation_p1_conclude(message):
    # see Transition Gate Function
    # pass

    # temporarily using this to display scores
    user_id = message.chat.id
    run_id = current_score[user_id].get('Metadata').get('run_id')
    datestamp = current_score[user_id].get('Metadata').get('datestamp')
    name = current_score[user_id].get('Metadata').get('user_name')
    direction = current_score[user_id].get('Metadata').get('direction')
    score = 0
    score_table[run_id] = current_score[user_id]

    # for v in current_score[user_id].values():
    #     for k2,v2 in v.items():
    #         if k2 == 'score':
    #             score += v2

    score = sum(v['score'] for v in current_score[user_id].values() if isinstance(v, dict) and 'score' in v)

    if gamemode[user_id] == 'test':
        print("Lookie here! Scores!")
        print(current_score[user_id])
    
    if gamemode[user_id] in ('command', 'test'):
        message_text = f"Total score is {score} points for run ID: `{run_id}` ({datestamp})\n\
You were playing as {name} on {direction} direction."
    else:
        message_text = "your scores were recorded"
    
    # bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id)
    send_score_call_id = ":".join(['send_score',run_id])
    markup = quick_markup({
        'Proceed to Phase 2' : {'callback_data': 'p2:select regiments'},
        'Send scores' : {'callback_data': send_score_call_id}, 
    }, row_width = 1)
    bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id,reply_markup=markup)

#endregion


@bot.callback_query_handler(func=lambda call: call.data.startswith("send_score"))
def handle_send_scores(call):
    bot.answer_callback_query(call.id)
    user_id = call.message.chat.id
    run_id = call.data.split(':')[1]
    run_scores = score_table[run_id]
    score = 0
    print(run_scores)


    datestamp   = run_scores['Metadata'].get('datestamp')
    name        = run_scores['Metadata'].get('user_name')
    direction   = run_scores['Metadata'].get('direction')

    score = sum(v['score'] for v in current_score[user_id].values() if isinstance(v, dict) and 'score' in v)
    
    sim_params = run_scores["Phase One"]
    IC,VL,TP,PT,base,mean,p90,tail = sim_params.values()
    
    ans_wp = run_scores["Win Probability"]['answer']
    results = run_scores["Win Probability"]['context']
    ans_sens = run_scores["Sensitivity"]['answer']
    sens = run_scores["Sensitivity"]['context']

    wscores = {
        coa: results[coa]["WinProb_Mean"] - results[coa]["Critical_%"]
        for coa in results
    }
    WinP = max(wscores.keys(), key=lambda c: wscores[c])
    Sens = sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0]

    parameters = {
        "Team_Name"     : name,
        "Direction"     : direction,
        "Total_score"   : score,
        "Date"          : datestamp,
        "Intelligence_Confidence": IC.display_name, 
        "Volatility"        : VL.display_name, 
        "Time_Pressure"     : TP.display_name, 
        # "Max Planning Time": 48,
        "DRI"       : base,
        "DRI_p90"   : p90,
        "DRI_mean"  : mean,
        "Critical_Tail"     : tail,  
        "Win_probability"   : WinP, 
        "WP_answered"      : ans_wp,
        "Sensitivity_Analysis": Sens,
        "SA_answered"      : ans_sens,
    }
    if gamemode[user_id] == 'test':
        print(AR_format(parameters))
    send_to_php(AR_format(parameters))