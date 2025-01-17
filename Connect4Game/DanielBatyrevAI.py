"""
This module has a random strategy for the Connect4 game.
The strategy randomly selects a move from valid columns.

Classes:
    RandomStrategy: Implements the random move strategy for Connect4.
"""

import Connect4Game as Game
import random


class RandomStrategy(Game.Connect4GameStrategy):
    """
    A strategy class for Connect4 that makes random moves from valid columns.

    Attributes:
        name (str): Name of the strategy (or the one who made it).
    """

    def __init__(self, name="Daniel Batyrev"):
        """
        Sets the RandomStrategy with a name.

        Args:
            name (str): The name of the strategy. Defaults to "Daniel Batyrev".
        """
        self.name = name

    @classmethod
    def strategy(cls, game_safety_copy):
        """
        Determines the next move by randomly selecting a valid column.

        Args:
            game_safety_copy (Connect4Game): A safe copy of the current game state.
        
        Returns:
            int: valid column to drop piece in.
        """
        valid_moves = list()  # list to store valid columns
        for col in range(7):  # check all columns
            if game_safety_copy.is_valid_move(col):  # check if column is valid
                valid_moves.append(col)  # add valid columns to the list
        
        return random.choice(valid_moves)  #randomly choose from available columns
