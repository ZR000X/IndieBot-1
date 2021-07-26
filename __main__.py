# Authors: Zeddar
# Associations: Indie Academy Discord Server
# License: MIT

from indie_bot import IndieBot
from keep_alive import keep_alive
from asyncio import get_event_loop
import inf

bot = IndieBot(prefix=".")
print("Initializing...")
loop = get_event_loop()
loop.run_until_complete(bot.start(inf.TOKEN_DEV))
print("Bot loop complete.")  
keep_alive()