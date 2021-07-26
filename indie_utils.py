import traceback
import random

import sys
sys.path.append(r'C:/dev/python/IndieBot/IB/dat')

mods = []

if not mods:
    with open(r"dat/mods.csv", "r+") as f:
        for each in f.readlines():
            mods.append(each.replace("\n", ""))


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
                elif command_type == "pig-math":
                    return ctx.message.channel.name == "pig-math" or ctx.message.channel.name == "bot-testing"
                elif command_type == "il":
                    # Put more particular permissions here
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

def shuffle(the_list, num_swaps: int = -1):
    length = len(the_list)
    if num_swaps < 0:
        num_swaps = length
    for i in range(num_swaps):
        swap1 = random.randint(0,length-1)
        swap2 = random.randint(0,length-1)
        first = the_list[swap1]
        the_list[swap1] = the_list[swap2]
        the_list[swap2] = first
    return the_list

def randints(size: int):
    the_list = []
    for i in range(size):
        the_list.append(i)    
    return shuffle(the_list)