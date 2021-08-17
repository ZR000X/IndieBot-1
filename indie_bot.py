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
        self.config = {}
        self.config["paths"] = {}
        if bot_id in config.data_paths:
            self.config["paths"]["data"] = config.data_paths[bot_id]
        else:
            self.config["paths"]["data"] = f"dat/botdat/{bot_id}"
        if config.data_file_extension is not None:
            self.config["data_file_extension"] = ".dat"

        self.slash = SlashCommand(self, sync_commands=True)        
        
        # Call initialization helper methods
        self.initialize_paths()
        self.initialize_events()
        self.initialize_commands()
        
        ### TODO: There seems to be a problem with this
        # self.initialize_help_commands()

        self.data = {} # This object contains all of this bot's data
        # Initialising data files
        self.data_files = {
            "messages.csv": "df",
            "user_histories.csv": "df",
            "global_stats.csv": "df",
            "balances.json": "dict",
            "users.json": "list",
            "users_asked_to_be_registered.json": "list"
        }

        for df in self.data_files:
            self.data[df] = self.get_data(name=df[:df.find(".")],ext=df[df.find("."):])
            if self.data[df] is None:
                ext = self.data_files[df]
                if ext == "df":
                    self.data[df] = pd.DataFrame()
                elif ext == "dict":
                    self.data[df] = {}
                elif ext == "list":
                    self.data[df] = []

    def get_data(self, name, ext):
        """
        Allows other code to seamlessly fetch data by name and extension
        """
        data_path = self.config["paths"]["data"]
        file_path = data_path + "/" + name + "." + ext
        if os.path.exists(file_path):
            if ext == "json":
                with open(file_path, 'w') as fp:
                    return json.load(fp)
            if ext == "dtf":
                return pd.read_csv(file_path)

    def sav_data(self, data, name, ext, overwrite=False) -> bool:
        """
        Allows other code to seamlessly save a chunk of data by name and extension,
        returns True if successful, false if not
        """
        data_path = self.config["paths"]["data"]
        file_path = data_path + "/" + name + "." + ext        
        if overwrite or not os.path.exists(file_path):
            if ext == "json":
                with open(file_path, 'w') as fp:
                    json.dump(data, fp)
                return True
            if ext == "dtf":
                if type(data) is pd.DataFrame:
                    data.to_csv(file_path)
                    return True
        return False

    def initialize_paths(self):
        """
        Helper method to ensure all needed directories are in order
        """
        for path in self.config["paths"]:
            self.force_path_to_exist(self.config["paths"][path])          

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

            if message.author == self:
                return

            df = self.data["messages.dtf"]
            if df is None:
                df = pd.DataFrame()

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
            self.sav_data(df, "messages", "dtf")
            self.data["messages.dtf"] = df

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
            self.save_data_files()
            await ctx.message.channel.send("Saved.")

        @self.command(name="balance")
        @logger("all")
        async def balance(ctx, *args):
            bals = self.data["balances.json"]
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
            user_mention = ctx.author.mention
            credit = 0
            for arg in args:
                try:
                    credit = float(arg)
                    await ctx.message.channel.send(user_mention+", we have successfully debited as you commanded.")
                    break
                except:
                    pass
            bals = self.data["balances.json"]
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
            user_mention = ctx.author.mention
            debit = 0
            for arg in args:
                try:
                    debit = float(arg)
                    await ctx.message.channel.send(user_mention+", we have successfully debited as you commanded.")
                    break
                except:
                    pass
            bals = self.data["balances.json"]
            for user in users_mentioned:
                if user.id in bals:
                    bals[user.id] -= debit
                else:
                    bals[user.id] = -debit

        @self.command(name="register")
        @logger("all")
        async def register(ctx, *args):
            """
            This command will trigger a check if the user is registered,
            if not, the bot will ask them to review the terms and conditions and accept,
            if they accept, the bot will consider them registered
            """
            user = ctx.message.author
            user_mention = ctx.author.mention
            chan_mention = "<#876850365730021386>"
            
            if user in self.data["users.json"]:
                await ctx.message.channel.send(user_mention+", you are already registered. :blue_heart:")
            else:
                self.data["users_asked_to_be_registered.json"].append(user)
                await ctx.message.channel.send(user_mention+", do you accept the "+chan_mention+
                " (Indie Library Terms of Service). Command .accept if you do. :blue_heart:")
        
        @self.command(name="accept")
        @logger("all")
        async def accept(ctx, *args):
            """
            This command will trigger a check if the user has asked to be registered.
            If they have, then calling this triggers adding them to registered users.
            If they have not, they will be asked to type .register first.
            """
            user = ctx.message.author
            user_mention = "<@"+str(user.id)+">"

            if user in self.data["users_asked_to_be_registered.json"]:
                self.data["users.json"].append(user)
                self.data["users_asked_to_be_registered.json"].remove(user)
                await ctx.message.channel.send(user_mention+", you have been successfully registered. :blue_heart:")
            else:
                await ctx.message.channel.send(user_mention+", have not commanded .register yet. "
                "Please do so first. :blue_heart:")

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

    def save_data_files(self, overwrite=True):
        for df in self.data_files:
            self.sav_data(data=self.data[df],name=df[:df.find(".")],
                ext=df[df.find("."):],overwrite=overwrite)
