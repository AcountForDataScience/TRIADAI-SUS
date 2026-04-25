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
