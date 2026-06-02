# a few basics until I figure out a cleaner way
from telebot import types

# bot instance so I can use decorators 
from bot.instance import bot, allowed_gamemodes

# global variables
# to do: replace with a database at some later point
from bot.state import (
    back_where,
    gamemode,
    custom_name,
    user_locale,
)

# Prettify output text
from bot.format_messages import message_bot_welcome
import bot.format_messages as getmessage

# region set commands
    # currently unused. Might be useful down the line for scaling.
    
# bot.set_my_commands([
#     # types.BotCommand("command","description"),
 
#     types.BotCommand("start","Starts new Simulation"),
#     # types.BotCommand("exit","Stops the bot. Development only."),
#     types.BotCommand("rename","Set or Change your Team name"),
#     types.BotCommand("setmode","Set your gamemode. For example: /gamemode Command or /gamemode Default"),
#     # types.BotCommand("command","description"),
# ])

# endregion

# region Settings

# select gamemode
@bot.message_handler(commands=["setmode"])
def set_gamemode(message):
    user_id = message.chat.id
    text_parts = message.text.split()
    
    # Check if the user provided an argument after the command
    if len(text_parts) < 2:
        bot.reply_to(message, getmessage.error_invalid_mode)
        return
    mode = text_parts[1].lower()
    # acceptable gamemodes:

    # Literals (unused):
    # allowed_gamemodes = ['default',
    #          'command',
    #          'test',]
    if mode in allowed_gamemodes:
        gamemode[user_id] = mode
        bot.reply_to(message, f"{mode.capitalize()} mode is set.")
    else:
        bot.reply_to(message, getmessage.error_invalid_mode)
    return

# endregion

##-----------------------------##
#   Інформаційні повідомлення   #
##-----------------------------##

#region pre-game

# початковий екран
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    
    # set default gamemode
    # if set previously, does not overwrite.
    gamemode[user_id] = gamemode.setdefault(user_id,'default')
    back_where[user_id] = [] # reset back buttons
    
    if not custom_name.get(user_id):
        next = bot.send_message(message.chat.id, getmessage.init_welcome + " " + getmessage.init_request_name)
        bot.register_next_step_handler(next, rename_user)
    else:
        bot.send_message(message.chat.id, getmessage.init_welcome_known_name.format(name = custom_name[user_id]))   
        show_menu(message)
# || початковий екран

# name or rename user
@bot.message_handler(commands=["rename"])
def command_rename(message):
    global custom_name
    user_id = message.chat.id
    if not custom_name.get(user_id):
        next = bot.send_message(message.chat.id, getmessage.init_request_name)
    else:
        next = bot.send_message(message.chat.id, getmessage.init_rename_team.format(name=custom_name[user_id]))
    bot.register_next_step_handler(next, rename_user)

def rename_user(message):
    global custom_name

    markup = types.InlineKeyboardMarkup()
    btn_rename = types.InlineKeyboardButton(getmessage.button_team_rename, callback_data="init_rename", style="danger")
    btn_start = types.InlineKeyboardButton(getmessage.button_scenario_start, callback_data="start_simulation",style="success")
    markup.add(btn_start, btn_rename)

    custom_name[message.chat.id] = message.text
    # print(custom_name[message.chat.id])
    # bot.reply_to(message, f"Evaluating the \"{strategic_direction_name[message.chat.id]}.\" direction", reply_markup=markup)
    show_menu(message)

# меню команд
def show_menu(message, send_new = True):
    markup = types.InlineKeyboardMarkup()

    button1 = types.InlineKeyboardButton(getmessage.button_scenario_start, callback_data="init_start", style="success")
    button2 = types.InlineKeyboardButton(getmessage.button_bot_description, callback_data="init_info")

    # Each line adds a row of buttons
    markup.add(button1, button2)

    message_text = getmessage.init_menu_text

    if send_new:
        bot.send_message(message.chat.id, message_text, reply_markup=markup)
    else:
        bot.edit_message_text(message_text, message.chat.id, message.id, reply_markup=markup)
# || меню команд

#надіслати опис
def send_description(message):
    user_id = message.chat.id
    if gamemode[user_id] == 'test':
        print("<info>: sending Description")    
    markup = types.InlineKeyboardMarkup()
    backbtn = types.InlineKeyboardButton(getmessage.button_back, callback_data="init_menu")
    markup.add(backbtn)

    #this is a message with line break support
    #markdown markup, periods must be escaped
    message_text = message_bot_welcome
    # bot.send_message(chat_id, message_text, parse_mode="MarkdownV2", reply_markup = markup)
    bot.edit_message_text(message_text, user_id, message.id, parse_mode="MarkdownV2", reply_markup = markup)
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

#endregion
