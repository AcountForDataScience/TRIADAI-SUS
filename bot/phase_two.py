# a few basics until I figure out a cleaner way
from telebot import types
from telebot.util import quick_markup, generate_random_token
import datetime

# simulation functions
from bot.simulations import (
    #P2 functions
    P2_Strategic_Readiness,
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
import bot.format_messages as getmessage

from bot.php_send import send_to_php, AR_format # stuff to send messages to AR goggles 


# region Phase Two

@bot.callback_query_handler(func=lambda call: call.data.startswith("p2:"))
def handle_phase_two_callbacks(call):
    callback = call.data.split(':')[1] #split the function and take second part only

    if callback == "select regiments":
        bot.edit_message_text("Please select the regiments required for this operation.",call.message.chat.id, call.message.id)
        phase_two_select_regiments(call.message, [])
    elif callback == "select":
        regiment = call.data.split(':')[2]
        selection = call.data.split(':')[3:]

        if not regiment in [
            'Ground',
            'Airforce',
            'USF',
            'Medical',
        ]:
            bot.answer_callback_query(call.id, text=f"Can't select {regiment}")
        else:
            if not regiment in selection:
                selection.append(regiment)
                text = f"{regiment} is now selected"
            else:
                selection.remove(regiment)
                text = f"{regiment} is removed from selection"
            bot.answer_callback_query(call.id, text=text)
        phase_two_select_regiments(call.message, selection)
    elif callback == "confirm selected":
        selection = call.data.split(':')[2:]
        if any(selection):
            bot.answer_callback_query(call.id, text=f"Selection confirmed!")
            phase_two_selection_confirmed(call.message, selection)
        else:
            bot.answer_callback_query(call.id, text=f"Error: You must select at least one regiment!")
        # phase_two_regiment_info(call.message, selection)    
    elif callback == "selection info":
        bot.answer_callback_query(call.id)
        selection = call.data.split(':')[2:]
        phase_two_regiment_info(call.message, selection)
    elif callback == "back to p2":
        bot.answer_callback_query(call.id)
        # phase_two_next(call.message)
        back = back_where[call.message.chat.id].pop()
        if gamemode[call.message.chat.id] == 'test':
                print("back phase 2")
                print(f"--> {back}")
                print(f"back queue: \n{back_where[call.message.chat.id]}")
        back(call.message)
    elif callback == "readiness":
        bot.answer_callback_query(call.id)
        phase_two_MC(call.message)
    elif callback == 'askscore':
        callback = call.data.split(':')[2:]
        if gamemode[call.message.chat.id] == 'test':
            print(callback)
        if callback[0] == 'multi':
            if callback[1] == 'sri':
                bot.answer_callback_query(call.id)
                p2_score_sri_highest(call.message)
            elif callback[1] == 'critprob':
                bot.answer_callback_query(call.id)
                p2_score_crit_worst(call.message)
        elif callback[0] == 'single':
            if callback[1] == 'sri':
                bot.answer_callback_query(call.id)
                p2_score_sri_value(call.message)
            elif callback[1] == 'critprob':
                bot.answer_callback_query(call.id)
                p2_score_crit_value(call.message)
        # return
    elif callback == 'score':
        callback = call.data.split(':')[2:]
        answer_text = "your answer has been recorded"
        if gamemode[call.message.chat.id] in ('test','command'):
            answer_text = f"your answer '{callback[-1:]}' has been recorded"
        # bot.answer_callback_query(call.id, text = answer_text)
        p2_record_score(call.message, ":".join(callback[:-1]), callback[-1])
        bot.answer_callback_query(call.id, text = answer_text)
        p2_next_question(call.message)
    else:
        # Fallback or generic pass
        pass

    bot.answer_callback_query(call.id, text=f"Processed {callback}...")
    if gamemode[call.message.chat.id] == 'test':
        # print(callback)
        print(f"Universal P2 Handler caught: {callback}")

#region skip phase2
@bot.message_handler(commands=["phasetwo"])
def phase_two_skip(message):
    user_id = message.chat.id
    gamemode.setdefault(user_id, 'default')
    if not back_where.get(user_id):
        back_where[user_id] = []
    strategic_direction_name.setdefault(user_id, 'test_direction')
    simulation_parameters.setdefault(user_id, {})
    custom_name.setdefault(user_id, 'test_user')
    current_score[user_id] = { "Metadata": {
            'user_id'   : user_id,
            'user_name' : custom_name[user_id],
            'direction' : strategic_direction_name[user_id],
            'run_id'    : "discard_this_run_id",
            'datestamp' : "" #in a better format   
        },
    }

    message_text = "Please select the regiments required for this operation."

    markup = quick_markup({
    'Ground Forces'         : {'callback_data': 'p2:select:Ground'},
    'Air Force'             : {'callback_data': 'p2:select:Airforce'},
    'Navy'                  : {'callback_data': 'p2:select:Navy'},
    'Airborne Assault F'    : {'callback_data': 'p2:select:Airborne'},
    'Special Operations F'  : {'callback_data': 'p2:select:SOF'},
    'Territorial Defense F' : {'callback_data': 'p2:select:TDF'},
    'Unmanned Systems F'    : {'callback_data': 'p2:select:USF'},
    'Support Forces'        : {'callback_data': 'p2:select:Support'},
    'Logistics Forces'      : {'callback_data': 'p2:select:Logistics'},
    'Medical Forces'        : {'callback_data': 'p2:select:Medical'},
    'Signal and Cybersec F' : {'callback_data': 'p2:select:SigSec'},
    }, row_width=2)

    bot.send_message(message.chat.id, message_text, reply_markup=markup)
#endregion


def phase_two_select_regiments(message, selection: list[str]):
    user_id = message.chat.id
    if not strategic_direction_name.get(user_id):
        strategic_direction_name[user_id] = 'test_direction'
    if not custom_name.get(user_id):
        custom_name[user_id] = 'test_user'

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
    
    buttons = {}
    markup = types.InlineKeyboardMarkup()

    for regiment, alias in regiments.items():
        style = None
        if alias in selection:
            regiment = "✅ " + regiment
        #hardcoded "allowed" Forces
        if alias in ['Ground','Airforce','USF','Medical',]:
            style = "success"
        buttons[alias] = types.InlineKeyboardButton(
            regiment,
            callback_data=":".join(["p2:select",alias] + selection),
            style=style,
        )

    # Convert items to a list to allow indexing
    btn_list = list(buttons.items())
    
    # print("\n loop start \n--------\n")
    for i in range(0, len(btn_list), 2): #using 2 item step
    # Check if there is a next button available
        if i + 1 < len(btn_list):
            # print(btn_list[i][0] + " and " + btn_list[i+1][0])
            markup.add(btn_list[i][1],btn_list[i+1][1])
        else:
            # This handles the odd button at the end
            # print(btn_list[i][0])
            markup.add(btn_list[i][1])

    btn_confirm = types.InlineKeyboardButton(
    text = "Confirm Selection",
    callback_data=":".join(["p2:confirm selected"]+selection),
    style="primary"
    )
    markup.add(btn_confirm)

    bot.edit_message_reply_markup(message.chat.id, message.id,reply_markup=markup)

def phase_two_selection_confirmed(message, selection):
    user_id = message.chat.id
    simulation_parameters[user_id]['P2_raw'] = {"selection": selection}
    if gamemode[user_id] == 'test':
        print(f"selection confirmed: {simulation_parameters[user_id]['P2_raw']}")
    phase_two_next(message)

def phase_two_next(message):
    user_id = message.chat.id
    markup = types.InlineKeyboardMarkup()
    btn_readiness = types.InlineKeyboardButton(
    text = "Evaluate Readiness",
    callback_data="p2:readiness",
    # style="primary"
    )
    btn_info = types.InlineKeyboardButton(
    text = "get forces info",
    callback_data=":".join(["p2:selection info"]+simulation_parameters[user_id]['P2_raw']['selection']),
    # style="primary"
    )
    markup.add(btn_readiness, btn_info)
    back_where[user_id].append(phase_two_next)
    message_text = "What should we do next?"

    bot.edit_message_text(message_text,message.chat.id, message.id, parse_mode="MarkdownV2")
    bot.edit_message_reply_markup(message.chat.id, message.id,reply_markup=markup)
    

def phase_two_regiment_info(message, selection):

    message_text = getmessage.regiment_parameters(selection,raw=True)
    markup = quick_markup({
        getmessage.button_back : {'callback_data':'p2:back to p2'},
    })
    bot.edit_message_text(message_text,message.chat.id, message.id, parse_mode="MarkdownV2")
    bot.edit_message_reply_markup(message.chat.id, message.id,reply_markup=markup)

def phase_two_MC(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']
    all_results = P2_Strategic_Readiness(selection)
    simulation_parameters[user_id]['P2'] = all_results
    message_lines = ['Phase 2 simulation preview:']
    for alias, readiness in all_results.items():
        if gamemode[user_id] == 'test':
            print(alias,readiness)    
        message_lines += [
                        f"\t{alias} Force readiness:",
                        f"\t\tStrategic readiness Index: {readiness['mean_sri']:2.0%}",
                        f"\t\tmax: {readiness['max_sri']:.2f}, min: {readiness['min_sri']:.2f}, p10: {readiness['p10']:.2f}",
                        f"\t\tcrisis probability: {readiness['crisis_probability']:2.2%}",
                        ""
        ]
    message_text = "\n".join(message_lines)
    
    if gamemode[user_id] == 'default':
        message_text = "Phase two simulation complete. \n Proceed to testing"
    bot.edit_message_text(message_text,message.chat.id, message.id, parse_mode=None) 

    if len(selection) == 1:
        markup = quick_markup({
            "Question 1 (sri)" : {'callback_data':'p2:askscore:single:sri'},
            "Question 2 (crit%)" : {'callback_data':'p2:askscore:single:critprob'},
        }, row_width=2)
        questions[user_id] = [p2_score_sri_value,p2_score_crit_value]
        # questions[user_id] = []
    else:
        markup = quick_markup({
            "Question 1 (sri)" : {'callback_data':'p2:askscore:multi:sri'},
            "Question 2 (crit%)" : {'callback_data':'p2:askscore:multi:critprob'},
        }, row_width=2)
        questions[user_id] = [p2_score_sri_highest,p2_score_crit_worst]
        # questions[user_id] = []

    bot.edit_message_reply_markup(message.chat.id, message.id,reply_markup=markup)
    # region P2:Scoring

def p2_next_question(message):
    user_id = message.chat.id
    if questions[user_id]:
        next = questions[user_id].pop()
    else:
        next = p2_send_score
    next(message)


def p2_score_sri_highest(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']

    if p2_score_sri_value in questions[user_id]:
        questions[user_id].remove(p2_score_sri_value)

    message_text = "Which force has the highest Mean Strategic Readiness?"

    callback_prefix = "p2:score:multi:sri"
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for force in selection:
        button = types.InlineKeyboardButton(
            text = force,
            callback_data=":".join([callback_prefix, force]),
            # style="primary"
        )
        buttons.append(button)

    btn_view_force_info = types.InlineKeyboardButton(
        text = "Review Regiments",
        callback_data=":".join(["p2:selection info"]+selection),
        style="primary"
    )
    back_where[user_id].append(p2_score_sri_highest)

    markup.add(*buttons,row_width=2)
    markup.add(btn_view_force_info)

    bot.edit_message_text(message_text, message.chat.id,message.id, reply_markup=markup)
    # bot.edit_message_reply_markup()

        # Which force has highest critical probability [force a] [force b] [force c] [force d] [check force details]
def p2_score_crit_worst(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']

    if p2_score_crit_worst in questions[user_id]:
        questions[user_id].remove(p2_score_crit_worst)

    message_text = "Which force has the highest probability of crisis?"

    callback_prefix = "p2:score:multi:critprob"
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for force in selection:
        button = types.InlineKeyboardButton(
            text = force,
            callback_data=":".join([callback_prefix, force]),
            # style="primary"
        )
        buttons.append(button)

    btn_view_force_info = types.InlineKeyboardButton(
        text = "Review Regiments",
        callback_data=":".join(["p2:selection info"]+selection),
        style="primary"
    )
    back_where[user_id].append(p2_score_crit_worst)

    markup.add(*buttons,row_width=2)
    markup.add(btn_view_force_info)

    bot.edit_message_text(message_text, message.chat.id,message.id, reply_markup=markup)
    # bot.edit_message_reply_markup()
        
        # if one:

        # for the * force, what is the readiness level? [high] [maneuver] [crisis] [critical] 
def p2_score_sri_value(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']

    if p2_score_sri_value in questions[user_id]:
        questions[user_id].remove(p2_score_sri_value)

    if len(selection) == 1:
        force = selection[0]
    else:
        force = selection[1]
        # force = random.sample(selection,1)[0]
    
    simulation_parameters[user_id]['P2_question'] = force
    if gamemode[user_id] == 'test':
        print(selection)
        print(force)

    message_text = f"For the {force} force, what is the Strategic Readiness level?"
    answers = ["High","Maneuver","Crisis","Critical",]
    # sri = 0.5
    # if sri >= 0.8:
    #     sri_value = "High"
    # elif sri >= 0.6:
    #     sri_value = "Maneuver"
    # elif sri >= 0.4:
    #     sri_value = "Crisis"
    # else:
    #     sri_value = "Critical"

    callback_prefix = "p2:score:single:sri"
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for answer in answers:
        button = types.InlineKeyboardButton(
            text = answer,
            callback_data=":".join([callback_prefix, answer]),
            # style="primary"
        )
        buttons.append(button)

    btn_view_force_info = types.InlineKeyboardButton(
        text = "review foce info",
        callback_data=":".join(["p2:selection info",force]),
        style="primary"
    )
    back_where[user_id].append(p2_score_sri_value)

    markup.add(*buttons,row_width=2)
    markup.add(btn_view_force_info)

    bot.edit_message_text(message_text, message.chat.id,message.id, reply_markup=markup)


        # What is the crisis probability? [<20%] [20%-99%] [already in crisis].
def p2_score_crit_value(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']

    if p2_score_crit_value in questions[user_id]:
        questions[user_id].remove(p2_score_crit_value)

    if len(selection) == 1:
        force = selection[0]
    else:
        force = selection[1]
        # force = random.sample(selection,1)[0]
    
    simulation_parameters[user_id]['P2_question'] = force
    if gamemode[user_id] == 'test':
        print(selection)
        print(force)

    message_text = f"For the {force} force, what is the Crisis robability?"
    # answers = ["Below 20%","20-99%","Already in crisis",]
    answers = ["Safe","Risky","Crisis",]

    callback_prefix = "p2:score:single:critprob"
    markup = types.InlineKeyboardMarkup()
    buttons = []
    for answer in answers:
        button = types.InlineKeyboardButton(
            text = answer,
            callback_data=":".join([callback_prefix, answer]),
            # style="primary"
        )
        buttons.append(button)

    btn_view_force_info = types.InlineKeyboardButton(
        text = "review foce info",
        callback_data=":".join(["p2:selection info",force]),
        style="primary"
    )
    back_where[user_id].append(p2_score_crit_value)

    markup.add(*buttons,row_width=2)
    markup.add(btn_view_force_info)

    bot.edit_message_text(message_text, message.chat.id,message.id, reply_markup=markup)


        # endregion

def p2_record_score(message, question, answer):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']
    results = simulation_parameters[user_id]['P2']
    if gamemode[user_id] == 'test':
        print(f"record score for {question}: is {answer} correct?")

    if    question == 'multi:sri':
        question = "Strongest Force"
               
        max_sri = 0
        for force, result in results.items():
            if result["mean_sri"] >= max_sri:
                correct = force
                max_sri = result["mean_sri"]

        if answer == correct:
            score = 1
        else:
            score = 0
        if gamemode[user_id] == 'test':
            print(f"---scoring {question}:---\nanswer: {answer} | correct: {correct} | score: {score}")
        force_parameters = getmessage.regiment_parameters(selection,raw=True)
        force_readiness = simulation_parameters[user_id]['P2']
    elif question == 'multi:critprob':
        question = "Weakest Force"
        
        crittail = 0
        for force, result in results.items():
            if result["critical_probability"] >= crittail:
                correct = force
                crittail = result["critical_probability"]

        if answer == correct:
            score = 1
        else:
            score = 0
        if gamemode[user_id] == 'test':
            print(f"---scoring {question}:---\nanswer: {answer} | correct: {correct} | score: {score}")
        force_parameters = getmessage.regiment_parameters(selection,raw=True)
        force_readiness = simulation_parameters[user_id]['P2']
    elif question == 'single:sri':
        question = "Force Readiness"

        force = simulation_parameters[user_id]['P2_question']
        sri = simulation_parameters[user_id]['P2'][force]['mean_sri']
        if sri >= 0.8:
            correct = "High"
        elif sri >= 0.6:
            correct = "Maneuver"
        elif sri >= 0.4:
            correct = "Crisis"
        else:
            correct = "Critical"

        if answer == correct:
            score = 1
        else:
            score = 0

        if gamemode[user_id] == 'test':
            print(f"---scoring {question}:---\nanswer: {answer} | correct: {correct} | score: {score}")
        force_parameters = getmessage.regiment_parameters(selection,raw=True)
        force_readiness = simulation_parameters[user_id]['P2']
    elif question == 'single:critprob':
        question = "Force Vulnerability"

        force = simulation_parameters[user_id]['P2_question']
        crit = simulation_parameters[user_id]['P2'][force]['critical_probability']
        if crit <= 0.2:
            correct = "Safe"
        elif crit < 1:
            correct = "Risky"
        else:
            correct = "Crisis"
        
        if answer == correct:
            score = 1
        else:
            score = 0

        if gamemode[user_id] == 'test':
            print(f"---scoring {question}:---\nanswer: {answer} | correct: {correct} | score: {score}")
        force_parameters = getmessage.regiment_parameters(selection,raw=True)
        force_readiness = simulation_parameters[user_id]['P2']
    else:
        score = 0
        pass
    
    # if gamemode[user_id] == 'test':
    print(f"{question}: it's { answer if score else correct}!")

    # current_score[user_id].append((
    # score,
    # question,
    # answer,
    # force_parameters,
    # force_readiness
    # ))

    current_score[user_id][question] = {
        'score'     : score,
        'question'  : question,
        'answer'    : answer,
        'context'   : force_readiness,
        'answer_key': correct, #correct answer
    }
    # score,
    # question,
    # answer,
    # force_parameters,
    # force_readiness
    # ))


def phase_two_scoring(message):
    user_id = message.chat.id
    selection = simulation_parameters[user_id]['P2_raw']['selection']
    results = simulation_parameters[user_id]['P2']
    for alias in selection:
        if alias in results:
            print(f"{alias}: ---\n{results[alias]}")


# Shuffle questions:
# def phase_two_shuffle_questions(questions:list[function]):
#     return random.sample(questions, 2)
    # endregion

# endregion

def p2_send_score(message):
    user_id = message.chat.id
    message_text = "your scores have probably been recorded"
    if gamemode[user_id] == 'test':
        print(current_score[user_id])
    
    
    markup = quick_markup({
        'Send scores': {'callback_data':'phasetwo'},
        'Complete': {'callback_data':'complete'},
    })
    bot.edit_message_text(message_text, message.chat.id, message.id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("phasetwo"))
def handle_send_scores(call):
    bot.answer_callback_query(call.id)
    user_id = call.message.chat.id
    # from rich import print as pprint
    # pprint(current_score[user_id])

    run_scores = current_score[user_id]

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

    del run_scores["Metadata"]
    del run_scores["Phase One"]
    del run_scores["Win Probability"]
    del run_scores["Sensitivity"]

    for key in run_scores:
        if key not in parameters:
            pkey = key.replace(' ','_')
            print(f"{key}, {pkey}, ")
            parameters[pkey] = run_scores[key].get("answer_key")
            parameters[pkey + "_ans"] = run_scores[key].get("answer")
    if gamemode[user_id] == 'test':
        print(AR_format(parameters))
    send_to_php(AR_format(parameters))