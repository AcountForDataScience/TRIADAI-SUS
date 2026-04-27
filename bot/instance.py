import telebot, os

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
