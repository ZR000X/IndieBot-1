import random

# Challenges are tuples with the challenger and challengee names in it
challenges = []

# Games are instances of PigGame
games = []


class PigGame:

    @staticmethod
    def play(player, action):
        # Select a game and perform an action
        game = PigGame.get_game(player)
        if game:
            if action == "roll":
                return game.roll(player)
            elif action == "bank":
                return game.bank(player)
            elif action == "score":
                return game.score(player)
            elif action == "quit":
                return game.quit(player)
        else:
            return f"You have no game in progress, {player}. Would you like to CHALLENGE someone?"

    @staticmethod
    def get_game(player):
        # Find the game which the given player is part of
        for each in games:
            if each.player1 == player or each.player2 == player:
                return each
        return None

    @staticmethod
    def end_game(player):
        # Remove the game from the rolling list of games
        for each in games:
            if each.player1 == player or each.player2 == player:
                games.pop(games.index(each))

    def __init__(self, player1, player2, target=100):
        self.players = [player1, player2]

        # Player 1 stats
        self.player1 = player1
        self.player1points = 0
        self.player1bank = 0

        # Player 2 stats
        self.player2 = player2
        self.player2points = 0
        self.player2bank = 0

        # General game stats
        self.target = target
        self.turn = 0

    def roll(self, player):
        # Rolls a six-sided dice and determines whether the player earns points or ends their turn
        if self.turn == 0:
            if player == self.player1:
                roll = random.randint(1, 6)
                if roll == 1:
                    self.player1points = 0
                    self.turn = 1
                    return f"{self.player1} rolled a 1. They lose their accumulated points and their turn is over."
                else:
                    self.player1points += roll
                    return f"{self.player1} rolled a {roll}. They have accumulated {self.player1points} points."
            else:
                return f"It is not your turn, {player}. Wait for {self.player1} to roll!"
        elif self.turn == 1:
            if player == self.player2:
                roll = random.randint(1, 6)
                if roll == 1:
                    self.player2points = 0
                    self.turn = 0
                    return f"{self.player2} rolled a 1. They lose their accumulated points and their turn is over."
                else:
                    self.player2points += roll
                    return f"{self.player2} rolled a {roll}. They have accumulated {self.player2points} points."
            else:
                return f"It is not your turn, {player}. Wait for {self.player2} to roll!"

    def bank(self, player):
        # If the player has accumulated any points, they are banked and their turn is ended
        if self.turn == 0:
            if player == self.player1:
                if self.player1points > 0:
                    self.player1bank += self.player1points
                    out = f"{self.player1} banks {self.player1points} points. They now have {self.player1bank} points."
                    self.player1points = 0
                    self.turn = 1
                    if self.player1bank >= self.target:
                        out += f"\n{player} has won the game!"
                        PigGame.end_game(player)
                    return out
                else:
                    return f"You have no points to bank, {self.player1}. Roll the dice first!"
            else:
                return f"It is not your turn, {player}. Wait for {self.player1} to finish their turn!"
        elif self.turn == 1:
            if player == self.player2:
                if self.player2points > 0:
                    self.player2bank += self.player2points
                    out = f"{self.player2} banks {self.player2points} points. They now have {self.player2bank} points."
                    self.player2points = 0
                    self.turn = 0
                    if self.player2bank >= self.target:
                        out += f"\n{player} has won the game! Congratulations!"
                        PigGame.end_game(player)
                    return out
                else:
                    return f"You have no points to bank, {self.player2}. Roll the dice first!"
            else:
                return f"It is not your turn, {player}. Wait for {self.player2} to finish their turn!"

    def score(self, player):
        for each in games:
            if player in each.players:
                return f"{each.player1}: {each.player1bank} ({each.player1points} unbanked)\n{each.player2}: {each.player2bank} ({each.player2points} unbanked)"

    def quit(self, player):
        for each in games:
            if player in each.players:
                games.pop(games.index(self))
                return f"{player} has quit the game."
        return f"{player} is not part of any game."


class PigChallenge:

    def __init__(self, challenger, challengee, target=100):
        self.status = ""
        valid_challenge = True
        if challenger == challengee:
            valid_challenge = False
            self.status = "You cannot challenge yourself!"

        # Check if either challenger or challengee is already in a game
        for each in games:
            if challenger in each.players:
                valid_challenge = False
                self.status = f"You cannot make a challenge, as a game is already in progress for you."
                break
            elif challengee in each.players:
                valid_challenge = False
                self.status = f"Cannot challenge {challengee}, as a game is already in progress for them."
                break

        if valid_challenge:
            challenges.append((challenger, challengee, target))
            self.status = f"A challenge has been sent to {challengee}."

    @staticmethod
    def create_challenge(challenger, challengee, target=100):
        return PigChallenge(challenger, challengee, target)

    @staticmethod
    def accept_challenge(acceptor):
        # If a valid challenge exists for the user, accept it
        valid_accept = False
        challenger = ""
        for each in challenges:
            if each[1] == acceptor:
                challenger = each[0]
                games.append(PigGame(each[0], each[1], each[2]))
                challenges.pop(challenges.index(each))
                valid_accept = True
                break

        if valid_accept:
            return f"Challenge accepted by {acceptor}. Game has begun. First turn goes to {challenger}!"
        else:
            return f"{acceptor} has not been challenged."

    @staticmethod
    def reject_challenge(rejector):
        # If a valid challenge exists for the user, reject it
        valid_reject = False
        challenger = ""
        for each in challenges:
            if each[1] == rejector:
                challenger = each[0]
                valid_reject = True
                challenges.pop(challenges.index(each))
                break

        if valid_reject:
            return f"Challenge from {challenger} rejected by {rejector}. Sorry!"
        else:
            return f"{rejector} has not been challenged by anyone."
