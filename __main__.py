# Authors: Zeddar
# Associations: Indie Academy Discord Server
# License: MIT

from indie_bot import IndieBot
from keep_alive import keep_alive
from asyncio import get_event_loop
import inf

# create bot instance
bot = IndieBot(prefix=".", bot_id="alpha")

# run loop
print("Initializing...")
loop = get_event_loop()
loop.run_until_complete(bot.start(inf.TOKEN_DEV))
print("Bot loop complete.")  

# keep alive
keep_alive()