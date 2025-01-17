"""
This module seems to run games of Connect4 between two AI competitors, ShmulyAI and YosefAI.
 To keep track of which AI wins more games and find put which is better.

Features:
- Has a timeout to make sure AIs dont take to long.
- Uses random strategy as a backup in case of timeout.
- Keeps track of game results (wins / ties) and shows scores at the end.
"""

import Connect4Game
import DanielBatyrevAI as DanielAI
import copy
import func_timeout
import ShmulyStudentAI as ShmulyAI
import YosefBirnbaumAI as YosefAI

# AI competitors, alternating as Player 1 and Player 2 between games
competitor_list = [ShmulyAI.NotRandomStrategy(), YosefAI.AI_strategy()]

# maximum time allowed for move
MAX_WAIT_TIME = 1

# stores game results
winners = list()

# random strategy- backup in case of timeout
random_choice = DanielAI.RandomStrategy()

# run 1000 games
for game_nr in range(1000):
    print(game_nr + 1)  # show current game number
    tie = False  # track if game ends in tie
    game = Connect4Game.Connect4Game()  # initialize new game

    while game.winner is None:  # continue until someone wins
        game_safety_copy = copy.deepcopy(game)  # create a safe copy of the game for the AI

        try:
            # AI tries to make a move within the allowed time (above)
            move = func_timeout.func_timeout(
                MAX_WAIT_TIME, competitor_list[game.current_player - 1].strategy, [game_safety_copy])
        except func_timeout.FunctionTimedOut:
            # if AI times out use the random strategy
            print(f'Timeout exceeded: {competitor_list[game.current_player - 1].name} performs random move')
            move = random_choice.strategy(game_safety_copy)

        # apply the move to game
        game.make_move(move)

        # check for tie (if no valid moves left)
        if 0 == sum(map(game.is_valid_move, range(7))):
            tie = True
            break

    # add game result
    if tie:
        winners.append("tie")
    else:
        winners.append(competitor_list[game.current_player - 1].name)

    # switch the order of competitors for the next game
    competitor_list.reverse()

# summarize results
dictionary = {}
for item in winners:
    dictionary[item] = dictionary.get(item, 0) + 1

# display the final results
print(dictionary)
