
command = []


def args_are(*args):
    # Check that the given arguments
    if len(command) < len(args):
        return False
    for n in range(len(args)):
        if command[n] != args[n]:
            return False
    return True


def summary():
    out = "```\n"
    out += "collatz: View the trajectory of the collatz function"
    out += "oeis: View a sequence in the OEIS\n"
    out += "pig: Play the dice game of pig\n"
    out += "snr: View the signature function of a sequence\n"
    out += "```\n"
    out += "Type `.help <command>` to view more details."
    return out


def specific(args):
    global command
    command = args

    if args_are("pig"):
        out = "Play the game of pig.\n"
        out += "```\n"
        out += "challenge <@user>: Challenge someone to a game of pig!\n"
        out += "accept: Accept another player's challenge\n"
        out += "reject: Reject another player's challenge\n"
        out += "roll: During a game, roll the dice to accumulate points\n"
        out += "bank: During a game, bank the points you've earned for that round\n"
        out += "score: View the current score of the game you're playing\n"
        out += "quit: End your current game prematurely\n"
        out += "```"
        return out
    elif args_are("collatz"):
        out = "View the trajectory of the collatz function for a given number.\n"
        out += "```\n"
        out += "collatz <number>: View the collatz trajectory of a number\n"
        out += "collatz <number> e: View the evenity trajectory of a number\n"
        out += "collatz <number> o: View the oddinity trajectory of a number\n"
        out += "```"
        return out
    elif args_are("snr"):
        out = "View the signature function of a given sequence.\n"
        out += "Each number in the sequence is its own argument. For example:"
        out += "```\n"
        out += "snr 1 1:   1, 1, 2, 3, 5, 8, 13, 21, ...\n"
        out += "snr 1 2 1: 1, 1, 3, 6, 13, 28, 60, 129, ...\n"
        out += "snr 2 1:   1, 2, 5, 12, 29, 70, 169, 408, ...\n"
        out += "```\n"
        out += "The input sequence can be any length!"
        return out
    elif args_are("oeis"):
        out = "Look up a sequence in the OEIS.\n"
        out += "```oeis <sequence number>: Look up a specific sequence```"
        out += "For example, `oeis 45` gives the Fibonacci numbers.\n"
        out += "If you do not provide any arguments, a random sequence is picked."
        return out
