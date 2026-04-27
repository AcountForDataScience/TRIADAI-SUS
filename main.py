from bot import bot 
from bot import handlers #importing handlers registers them

print(f"<info>: Telegram bot {{{bot.bot_id}}} is initialized")

#--------- START BOT ---------#
if __name__ == "__main__": # Gatekeeper function
    # it prevents bot starting if imported as a part of another package
    print("<info>: Bot is listening")
    bot.infinity_polling()
