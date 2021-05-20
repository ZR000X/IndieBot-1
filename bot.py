import discord
from discord.ext import commands

import random

# Math functions, the core of IndieBot
from indie_math import indie_seq, indie_oeis

oeis_in_progress = False


def command_wrapper(command):

    async def wrapper(ctx, *args):
        args = ctx.message.content.split(" ")
        print("Command used:", command.__name__)
        await command(ctx, *args)

    return wrapper


def create_bot_instance(prefix, bot_id):
    inst = commands.Bot(command_prefix=prefix)
    initialize_events(inst)
    initialize_commands(inst)
    return inst


def initialize_events(bot):

    @bot.event
    async def on_ready():
        await bot.change_presence(activity=discord.Game("around"))

    @bot.event
    async def on_message(message):
        await bot.process_commands(message)


def initialize_commands(bot):

    @bot.command(name="snr", pass_context=True)
    @command_wrapper
    async def snr(ctx, *args):
        args = args[1:]
        try:
            await ctx.message.channel.send(str(indie_seq.Seq([int(k) for k in args]).f()))
        except Exception as exc:
            await ctx.message.add_reaction("❌")
            print("SNR command error:", exc)

    @bot.command(name="oeis", pass_context=True)
    @command_wrapper
    async def oeis(ctx, *args):
        global oeis_in_progress
        args = args[1:]
        try:
            if not oeis_in_progress:
                oeis_in_progress = True
                if len(args[1:]) >= 2:
                    await ctx.message.channel.send(indie_oeis.get_sequence_from_b_file(raw[1]))
                else:
                    await ctx.message.channel.send(indie_oeis.get_sequence_from_b_file(str(random.randint(1, 341962))))
                oeis_in_progress = False
            else:
                await ctx.message.add_reaction("❌")
        except Exception as exc:
            await ctx.message.add_reaction("❌")
            print("OEIS command error:", exc)

