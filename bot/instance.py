import telebot, os
# from os import getenv

#--------- Load Environment ---------#

# used to separate local testing from production run
if os.getenv('RENDER'):
    print("Running on Render")
else:
    from dotenv import load_dotenv
    load_dotenv()
    print(os.getenv('Test_env'))

# allowed_gamemodes = [
#         'default',
#         'command',
# ]
# if os.getenv('Test_env'):
#     allowed_gamemodes.append('test')

#--------- API KEY ---------#
print("acquiring tokens")
bot_token = os.getenv('BOT_TOKEN')

#initiate the telegram bot. #can update to "MARKDOWN" parse mode for simple Rich text capabilites
bot = telebot.TeleBot(bot_token, parse_mode=None)
