# Authors: Zeddar, Conrad
# Associations: Indie Academy Discord Server
# License: MIT

import random
import time

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from indie_math import indie_seq, indie_oeis, indie_collatz, indie_pig
from indie_utils import logger
import indie_help
import config

import pandas as pd
import os
import json

oeis_in_progress = False

class IndieBot(commands.Bot):
    def __init__(self, prefix, bot_id) -> None:
        super().__init__(command_prefix=prefix)
        self.prefix = prefix
        self.bot_id = bot_id
        self.paths = {}
        if bot_id in config.data_paths:
            self.paths["data"] = config.data_paths[bot_id]
        else:
            self.paths["data"] = config.data_paths["default"]
        self.slash = SlashCommand(self, sync_commands=True)        
        
        # Call initialization helper methods
        self.initialize_paths()
        self.initialize_events()
        self.initialize_commands()
        
        ### TODO: There seems to be a problem with this
        # self.initialize_help_commands()

        self.data = {}
        # Initialising data files
        self.data_frame_files = {
            "messages",
            "user_histories",
            "global_stats"
        }
        for data_file in self.data_frame_files:
            path = self.paths["data"]+data_file+config.data_file_extension
            if os.path.isfile(path):
                self.data[data_file] = pd.read_csv(path)
            else:
                self.data[data_file] = pd.DataFrame({})
                self.data[data_file].to_csv(path)

        self.json_files = {
            "balances",
        }
        for json_file in self.json_files:
            path = self.paths["data"]+json_file+".json"
            if os.path.isfile(path):
                try:
                    self.data[json_file] = json.loads(path)
                except:
                    self.data[json_file] = {}
                    with open(path, 'w') as fp:
                        json.dump(self.data[json_file], fp)
            else:
                self.data[json_file] = {}
                with open(path, 'w') as fp:
                    json.dump(self.data[json_file], fp)


    def initialize_paths(self):
        """
        Helper method to ensure all needed directories are in order
        """
        for path in self.paths:
            self.force_path_to_exist(self.paths[path])          

    def force_path_to_exist(self, path) -> bool:
        """
        Helper method to create a file or directory of a certain path if it does not exist,
        then also returns whether or not the path existed.
        """
        exists = os.path.exists(path)
        if not exists:
            os.makedirs(path)
        return exists

    # [Method is run on construction]
    def initialize_events(self) -> None:
        """
        Helper method to set actionable events in order
        """

        @self.event
        async def on_ready():
            await self.change_presence(activity=discord.Game("around"))
            print("IndieBot is live.")
            # continuously save self's data files
            # while True:
            #     time.sleep(config.miliseconds_to_save)
            #     self.save_data()

        @self.event
        async def on_message(message):
            # - datetime
            # - author
            # - server
            # - channel
            # - command name (None if not command)
            # - input size [# characters] (a way of monitoring usage, to enforce any necessary limits)
            # - output size [# characters] (a way of monitoring usage, to enforce any necessary limits)
            # - gas fee (we can manually set gas fees per command in a csv, or at some point adjust them dynamically)

            df = self.data["messages"]
            df2 = pd.DataFrame({
                'message_id': [str(message.id)],
                'datetime': [str(message.created_at.now())],
                'author_id': [str(message.author.id)],
                'author_name': [str(message.author.name)],
                'server': [str(message.guild)],
                'channel': [str(message.channel)],
                'input_size': [str(len(message.content))],
            })

            # Compute other information to be stored
            # new_data['command_name']
            # new_data['output_size']
            # new_data['gas_fee']

            df = df.append(pd.DataFrame(df2))
            path = self.paths["data"]+"messages"+config.data_file_extension
            df.to_csv(path)
            self.data["messages"] = df

            await self.process_commands(message)

    # [Method is run on construction]
    def initialize_commands(self) -> None:
        """
        Helper method to set actionable commands in order
        """

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

        @self.command(name="save")
        @logger("modonly")
        async def save(ctx, *args):
            self.save_data()
            await ctx.message.channel.send("Saved.")

        @self.command(name="balance")
        @logger("all")
        async def balance(ctx, *args):
            bals = self.data["balances"]
            user = ctx.message.author.id
            bal = 0
            if user in bals:
                bal = bals[user]
            else:
                bals[user] = 0            
            await ctx.message.channel.send(ctx.message.author.name+", your balance is "+str(bal)+".")

        @self.command(name="credit")
        @logger("modonly")
        async def credit(ctx, *args):
            """
            Command with credit users mentioned with first float arg detected
            """
            users_mentioned = ctx.message.mentions
            credit = 0
            for arg in args:
                try:
                    credit = float(arg)
                    await ctx.message.channel.send("Credited succesfully, "+ctx.message.author.name+".")
                    break
                except:
                    pass
            bals = self.data["balances"]
            for user in users_mentioned:
                if user.id in bals:
                    bals[user.id] += credit
                else:
                    bals[user.id] = credit

        @self.command(name="debit")
        @logger("modonly")
        async def debit(ctx, *args):
            """
            Command with credit users mentioned with first float arg detected
            """
            users_mentioned = ctx.message.mentions
            debit = 0
            for arg in args:
                try:
                    debit = float(arg)
                    await ctx.message.channel.send("Debited succesfully, "+ctx.message.author.name+".")
                    break
                except:
                    pass
            bals = self.data["balances"]
            for user in users_mentioned:
                if user.id in bals:
                    bals[user.id] -= debit
                else:
                    bals[user.id] = -debit                           
            

    def initialize_help_commands(self) -> None:
        """
        Helper method to set actionable help commands in order
        """

        @self.command(name="help")
        @logger("all")
        async def help_command(ctx, *args):
            if len(args) == 0:
                await ctx.message.channel.send(indie_help.summary())
            else:
                await ctx.message.channel.send(indie_help.specific(args))

    def save_data(self):
        for df in self.data_frame_files:
            path = self.paths["data"]+df+config.data_file_extension
            self.data[df].to_csv(path)
        for json_file in self.json_files:
            path = self.paths["data"]+json_file+".json"
            with open(path, 'w') as fp:
                json.dump(self.data[json_file], fp)
                

        
                