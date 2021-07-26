# Authors: Conrad, Zeddar
# Associations: Indie Academy Discord Server
# License: MIT

import random

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from indie_math import indie_seq, indie_oeis, indie_collatz, indie_pig
from indie_utils import logger
import indie_help

import pandas as pd

oeis_in_progress = False

class IndieBot(commands.Bot):
    def __init__(self, prefix) -> None:
        super().__init__(command_prefix=prefix)
        self.prefix = prefix
        self.slash = SlashCommand(self, sync_commands=True)        
        self.initialize_events()
        self.initialize_commands()             

    # [Method is run on construction]
    def initialize_events(self):

        @self.event
        async def on_ready():
            await self.change_presence(activity=discord.Game("around"))
            print("IndieBot is live.")

        @self.event
        async def on_message(message):
            await self.process_commands(message)

    # [Method is run on construction]
    def initialize_commands(self):

        @self.command(name="snr")
        @logger("all")
        async def snr(ctx, *args):
            await ctx.message.channel.send(str(indie_seq.Seq([int(k) for k in args]).f()))

        @self.command(name="oeis")
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

        @self.command(name="collatz")
        @logger("all")
        async def collatz(ctx, *args):
            num = int(args[0])
            inity = "" if len(args) < 2 else args[1]

            collatz_results = indie_collatz.collatz_info(num)
            if len(inity) == 1:
                if inity == "e":
                    await ctx.message.channel.send(f"Evenity trajectory of {num}: {collatz_results.evenity_trajectory}")
                elif inity == "o":
                    await ctx.message.channel.send(f"Oddinity trajectory of {num}: {collatz_results.oddinity_trajectory}")
            else:
                await ctx.message.channel.send(f"Collatz trajectory of {num}: {collatz_results.collatz_trajectory}")

        @self.group(name="pig")
        @logger("pig-math")
        async def pig(ctx, *args):
            if ctx.invoked_subcommand is None:
                await ctx.message.add_reaction("❌")

        def get_user_id_from_mention(user_id):
            user_id = user_id.replace("<", "")
            user_id = user_id.replace(">", "")
            user_id = user_id.replace("@", "")
            user_id = user_id.replace("!", "")
            return user_id

        # Pig Math commands

        @pig.command(name="challenge")
        @logger("pig-math")
        async def pig_challenge(ctx, *args):
            challengee = get_user_id_from_mention(args[1])
            challengee = (await self.fetch_user(challengee)).name
            if len(args) > 2:
                point_target = int(args[2])
            else:
                point_target = 100
            pig_challenge = indie_pig.PigChallenge.create_challenge(ctx.message.author.name, challengee, point_target)
            await ctx.message.channel.send(pig_challenge.status)

        @pig.command(name="accept")
        @logger("pig-math")
        async def pig_accept(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigChallenge.accept_challenge(ctx.message.author.name))

        @pig.command(name="reject")
        @logger("pig-math")
        async def pig_reject(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigChallenge.reject_challenge(ctx.message.author.name))

        @pig.command(name="roll")
        @logger("pig-math")
        async def pig_roll(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigGame.play(ctx.message.author.name, "roll"))

        @pig.command(name="bank")
        @logger("pig-math")
        async def pig_bank(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigGame.play(ctx.message.author.name, "bank"))

        @pig.command(name="score")
        @logger("pig-math")
        async def pig_score(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigGame.play(ctx.message.author.name, "score"))

        @pig.command(name="quit")
        @logger("pig-math")
        async def pig_quit(ctx, *args):
            await ctx.message.channel.send(indie_pig.PigGame.play(ctx.message.author.name, "quit"))


    def initialize_help_commands(self):

        @self.command(name="help")
        @logger("all")
        async def help_command(ctx, *args):
            if len(args) == 0:
                await ctx.message.channel.send(indie_help.summary())
            else:
                await ctx.message.channel.send(indie_help.specific(args))
