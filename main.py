import telebot

import os 

# importing local bot/handlers module
# it handles bot logic
from bot.handlers import register_handlers 

#--------- Load Environment ---------#
# used for local testing
if os.getenv('RENDER') == "True":
    print("Running on Render")
else:
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv('Test_env'))

#--------- API KEY ---------#
print("acquiring tokens")
bot_token = os.getenv('BOT_TOKEN')

#initiate the telegram bot. #can update to "MARKDOWN" parse mode for simple Rich text capabilites
bot = telebot.TeleBot(bot_token, parse_mode=None)
register_handlers(bot)
print("<info>: Telegram bot is initialized")

#--------- START BOT ---------#
if __name__ == "__main__": # Gatekeeper function
    # it prevents bot starting if imported as a part of another package
    print("<info>: Bot is listening")
    bot.infinity_polling()
