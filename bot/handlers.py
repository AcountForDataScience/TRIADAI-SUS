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

# print("\nLOOK HERE:")
# print(Intelligence_Confidence.classify(0.7).display_name)

# bot instance so I can use decorators 
from bot.instance import bot

# global variables
# to do: replace with a database at some later point
from bot.state import (
    simulation_results,
    simulation_parameters,
    strategic_direction_name,
    custom_name,
    user_locale,
    score_table,
    current_score
)

# Prettify output text
from bot.format_messages import (
    # Static Strings
    message_bot_welcome,
    message_p1_explain,
    # Dynamic Strings
    format_phase1_message,
    explain_monte_carlo_phase1,
    format_coa_message,
)
import bot.format_messages as getmessage

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
    message_text = message_bot_welcome
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
        next = bot.send_message(message.chat.id, "You've launched the Strategic Uncertainty Simulation bot. Please enter your name or team name.")
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
        next = bot.send_message(message.chat.id, "Please enter your name or team name:")
    else:
        next = bot.send_message(message.chat.id, f"your current name is:{custom_name[user_id]}. Enter a new name:")
    bot.register_next_step_handler(next, rename_user)

def rename_user(message):
    global custom_name

    markup = types.InlineKeyboardMarkup()
    btn_rename = types.InlineKeyboardButton("Rename Team", callback_data="init_rename", style="danger")
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
    next = bot.send_message(call.message.chat.id, "Simulation has started\\. Please choose *strategic direction*\n\\(enter direction name below\\):", parse_mode="MarkdownV2")
    # Hand off the flow to the 'name_strategic_direction' function
    bot.register_next_step_handler(next, name_strategic_direction)
    # || Початок Симуляції

# Назва напрямку
def name_strategic_direction(message):
    # print("name strat direction")
    global strategic_direction_name

    markup = types.InlineKeyboardMarkup()

    direction = message.text

    # btn_param = types.InlineKeyboardButton("Визначити параметри", callback_data="init_set_parameters")
    btn_rename = types.InlineKeyboardButton("Rename direction", callback_data="init_rename", style="danger")
    btn_start = types.InlineKeyboardButton(f"Continue with {direction[:30]}", callback_data="start_simulation",style="success")

    # Each line adds a row of buttons
    markup.add(btn_start, btn_rename)
    # markup.add(btn_param)

    strategic_direction_name[message.chat.id] = message.text
    # print(strategic_direction_name[message.chat.id])
    bot.reply_to(message, f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" direction", reply_markup=markup)

# переназвати напрямок
@bot.callback_query_handler(func=lambda call: call.data == "init_rename")
def handle_name_strategic_direction(call):
    bot.answer_callback_query(call.id) #removes loading symbol
    next = bot.send_message(call.message.chat.id, "Please choose *strategic direction*\n\\(enter direction name below\\):", parse_mode="MarkdownV2")
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
    # print(f"alert\n{Intelligence_Confidence}\n{Volatility}\n{Time_Pressure}\n")
    IC, V, TP = P1_Shuffle(Intelligence_Confidence, Volatility, Time_Pressure)
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

    explain = message_p1_explain

    markup = types.InlineKeyboardMarkup()
    btn_back = types.InlineKeyboardButton("<< back", callback_data="start_simulation", style="success")

    # Each line adds a row of buttons
    markup.add(btn_back)

    bot.edit_message_text(explain, message.chat.id, message.id, reply_markup=markup, parse_mode="MarkdownV2")

#Підтвердження параметрів
@bot.callback_query_handler(func=lambda call: call.data == "p1_confirm_parameters")
def handle_simulation_p1_confirm_parameters(call):
    bot.answer_callback_query(call.id, "parameters are confirmed")
    # print("p1 parameters confirmed")
    
    # scoring
    global current_score
    run_id = generate_random_token()
    # user_id = call.from_user.id
    user_id = call.message.chat.id
    global custom_name
    user_name = custom_name[user_id]
    timestamp = datetime.date.today()
    # print(timestamp)
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

    for i in range(5, len(current_score[user_id])):
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
    elif callback == "AR Summary":
        simulation_p1_AR_summary(call.message)
    elif callback == "Conclude":
        simulation_p1_conclude(call.message)
    else:
        # Fallback or generic pass
        pass

    # print(f"processed callback: {callback}")

# from telebot.formatting import escape_markdown

# scoring #######################################
def simulation_p1_test_sens(message):
    global simulation_parameters
    global strategic_direction_name
    user_id = message.chat.id

    # message_text = "".join([
    #     "Evaluating the \"", escape_markdown(strategic_direction_name[message.chat.id]), "\" strategic direction:\n",
    #     escape_markdown(simulation_results[message.chat.id]["P1"]),
    #     "~                    ~\n\n",
    #     " \> *Which parameter has the greatest impact on the outcome?*"
    # ])
    # print(message_text)
#     message_text=f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\
# \n\n {simulation_results[message.chat.id]["P1"]} ------\n\n\
#  > Which parameter has the greatest impact on the outcome?",

    message_text = getmessage.sens_score_ask(strategic_direction_name[message.chat.id], simulation_results[message.chat.id]["P1"])

    markup = quick_markup({
        'Intell Confidence' : {'callback_data': 'p1_analysis:Score Sens:IC'},
        'Volatility'              : {'callback_data': 'p1_analysis:Score Sens:V'},
        'Time pressure'           : {'callback_data': 'p1_analysis:Score Sens:TP'}
    }, row_width=3)

    bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")
    # bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup)

def simulation_p1_score_sens(message,answer):
    global simulation_parameters
    global strategic_direction_name
    global current_score
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

    # print(sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0])

    answer_key = sorted(sens["combined_score"].items(), key=lambda item: item[1], reverse=True)[0][0]

    #prettify
    def prettify(parameter):
        match parameter:
            case 'V' : return "Volatility"
            case 'IC': return "Intel Confidence"
            case 'TP': return "Time Pressure"
        

    # match answer:
    #     case 'V' : answer = "Volatility"
    #     case 'IC': answer = "Intel Confidence"
    #     case 'TP': answer = "Time Pressure"
    # match answer_key:
    #     case 'V' : answer_key = "Volatility"
    #     case 'IC': answer_key = "Intel Confidence"
    #     case 'TP': answer_key = "Time Pressure"


    if answer == answer_key:
        # print("correct")
        score_text = f"your answer {prettify(answer)} is correct"
        current_score[user_id].append((
            1,
            "Sensitivity",
            simulation_parameters[user_id],
            sens
            ))
    else:
        # print("incorrect")
        score_text = f"your answer {prettify(answer)} is incorrect: it's {prettify(answer_key)}"
        current_score[user_id].append((
            0,
            "Sensitivity",
            simulation_parameters[user_id],
            sens
            ))

    influence_share = {k: round(v*100, 1) for k, v in sens["influence_share"].items()}

    # message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
    # Scenario parameters:  Intel:  {sens["scenario"]['IC_key']},   Volatility: {sens["scenario"]['V_key']}, Time pressure: {sens["scenario"]['TP_key']}
    # Spearman correlation: Intel:  {sens["spearman_corr"]['IC']:.2f}, Volatility: {sens["spearman_corr"]['V']:.2f},  Time pressure: {sens["spearman_corr"]['TP']:.2f}
    # Influence share:      Intel:  {influence_share['IC']:.2f}, Volatility: {influence_share['V']:.2f}, Time pressure: {influence_share['TP']:.2f}
    # ---------
    # {score_text}
    # """

    message_text = "\n\n".join([
        getmessage.sens_score_answer(strategic_direction_name[user_id],sens,influence_share),
        score_text
        ])

    bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id, parse_mode="MarkdownV2")
    simulation_phase_one_analyze(message)

def simulation_p1_test_winp(message):
    global simulation_parameters
    global strategic_direction_name
    user_id = message.chat.id

    message_text=getmessage.winp_score_ask(strategic_direction_name[message.chat.id],simulation_results[message.chat.id]["P1"])
    
    # f"Evaluating the \"{strategic_direction_name[message.chat.id]}\" strategic direction:\n\n {simulation_results[message.chat.id]["P1"]} ------\n\n >Which course of action has the highest Win Probability?",

    markup = quick_markup({
        'Attack'  : {'callback_data': 'p1_analysis:Score WinP:Attack'},
        'Regroup' : {'callback_data': 'p1_analysis:Score WinP:Regroup'}
    }, row_width=3)

    bot.edit_message_text(message_text,chat_id = user_id, message_id = message.id, reply_markup=markup, parse_mode="MarkdownV2")

def simulation_p1_score_winp(message,answer):
    global simulation_parameters
    global strategic_direction_name
    global current_score
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

    # IC_key, V_key, TP_key = simulation_parameters[user_id]["IC"], simulation_parameters[user_id]["VL"], simulation_parameters[user_id]["TP"]
    # compare_stats_text = f"Scenario: {IC_key}, {V_key}, {TP_key}\n"
    # for key, value in coa_wp.items():
    #     compare_stats_text += f"for {key} CoA, 90 percentile win probability is at {value.get('WinProb_P90'):.2f} with a {value.get('Critical_%')*100:.2f}% critical tail\n"

    # print(compare_stats_text)

#     message_text = f"""Evaluating the \"{strategic_direction_name[user_id]}\" direction:
# {compare_stats_text}
# {f"According to integral criterion (WinProb_mean − Critical_tail) best course of action is: **{rec}**."}
# ---------
# {score_text}
#     """

    message_text = "\n".join([
        getmessage.winp_score_answer(strategic_direction_name[user_id],simulation_parameters[user_id],coa_wp,rec),
        score_text,
    ])

    bot.edit_message_text(message_text,chat_id = message.chat.id, message_id = message.id, parse_mode="MarkdownV2")
    simulation_phase_one_analyze(message)
# scoring #######################################


def simulation_p1_compare_coa(message):
    #display CoA comparison and all the buttons
    global simulation_parameters
    global strategic_direction_name
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
    global simulation_parameters
    global strategic_direction_name
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

def simulation_p1_conclude(message):
    # see Transition Gate Function
    # pass

    # temporarily using this to display scores

    global current_score
    global score_table
    user_id = message.chat.id
    score = 0
    name = current_score[user_id][1]
    direction = current_score[user_id][3]
    run_id = current_score[user_id][2]
    score_table[run_id] = current_score[user_id]
    datestamp = current_score[user_id][4]

    for i in range(5, len(current_score[user_id])):
        score += current_score[user_id][i][0]
    
    message_text = f"Total score is {score} points for run ID: `{run_id}` ({datestamp})\n\
You were playing as {name} on {direction} direction."
    # print(message_text)


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
