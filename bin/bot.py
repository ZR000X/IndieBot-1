import traceback
import random
import discord
from discord.ext import commands

# Math functions, the core of IndieBot
from indie_math import indie_seq, indie_oeis

mods = []
oeis_in_progress = False


def create_bot_instance(prefix, bot_id):
    global mods
    inst = commands.Bot(command_prefix=prefix)
    with open("dat/mods.csv", "r+") as f:
        for each in f.readlines():
            mods.append(each.replace("\n", ""))
        print(mods)
    initialize_events(inst)
    initialize_commands(inst)
    return inst


def initialize_events(bot):

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game("around"))
        print("IndieBot is live.")

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)


def initialize_commands(bot):

    def logger(command_type):

        # Encapsulates bot commands for added functionality
        def command_wrapper(command):

            # Where the magic happens. This gives commands more versatility
            async def function_wrapper(ctx):

                def has_permission():
                    global mods
                    if command_type == "modonly" and str(ctx.message.author.id) in mods:
                        return True
                    elif command_type == "all":
                        return True
                    else:
                        return False

                args = ctx.message.content.split(" ")[1:]
                print("Command used:", command.__name__)
                try:
                    if has_permission():
                        await command(ctx, *args)
                        # Log successful command usage
                        with open("dat/command_log.csv", "a+") as f:
                            f.write(f"{command.__name__},{ctx.message.author.id}\n")
                    else:
                        await ctx.message.add_reaction("❌")
                        print(
                            f"User {ctx.message.author.name} does not have permission to use command {command.__name__}")
                except Exception:
                    await ctx.message.add_reaction("❌")
                    print(traceback.format_exc())

            return function_wrapper

        return command_wrapper

    @bot.command(name="snr")
    @logger("all")
    async def snr(ctx, *args):
        await ctx.message.channel.send(str(indie_seq.Seq([int(k) for k in args]).f()))

    @bot.command(name="oeis")
    @logger("all")
    async def oeis(ctx, *args):
        global oeis_in_progress
        if not oeis_in_progress:
            oeis_in_progress = True
            if len(args) > 0:
                await ctx.message.channel.send(indie_oeis.get_sequence_from_b_file(args[0]))
            else:
                await ctx.message.channel.send(indie_oeis.get_sequence_from_b_file(str(random.randint(1, 341962))))
            oeis_in_progress = False
        else:
            await ctx.message.add_reaction("❌")

