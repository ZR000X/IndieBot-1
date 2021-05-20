# inf contains the bot token, which is excluded from this repo
import inf

from asyncio import get_event_loop

from bot import create_bot_instance

bot = create_bot_instance(".", 844015565243940864)

print("Initializing")
loop = get_event_loop()
loop.run_until_complete(bot.start(inf.TOKEN))
print("Bot loop complete.")
