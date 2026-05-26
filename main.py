from bot import bot 
#importing handlers registers them
from bot import handlers
# from bot import mtest_handlers #should not be active

print(f"<info>: Telegram bot @{bot.get_me().username} {{{bot.bot_id}}} is initialized")

#--------- START BOT ---------#
if __name__ == "__main__": # Gatekeeper function
    # it prevents bot starting if imported as a part of another package
    print("<info>: Bot is listening")
    bot.infinity_polling()
