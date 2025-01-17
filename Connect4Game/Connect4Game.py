"""
This module defines the Connect4 game (the board and checking valid moves/winner).
Also defines an abstract class for creating AI strategies.

Classes:
    Connect4GameStrategy: An abstract base class for defining Connect4 strategies.
    Connect4Game: A class implementing basic Connect4 game.
"""

from abc import ABC, abstractmethod


class Connect4GameStrategy(ABC):
    """
    An abstract base class for Connect4 game strategies.

    This class defines the interface for creating AI strategies.
    """

    def __init__(self):
        """
        For initializing Connect4GameStrategy.
        """
        ...

    @abstractmethod
    def strategy(self, game_safety_copy):
        """
        Provides the best move according to strategy logic.

        Args:
            game_safety_copy (Connect4Game): A copy of the current game state.
        
        Returns:
            int: Column index (0-6) for the next move.
        """
        ...


class Connect4Game:
    """
    Provides basic Connect4 game functionality.

    Attributes:
        board (list[list[int]]): A 2D list representing game board.
        current_player (int): Current player (1 or 2).
        winner (int or None): Winning player (1 or 2) or None if game is not done yet.
    """

    def __init__(self):
        """
        Sets up a new Connect4 game.
        """
        self.board = [[0] * 7 for _ in range(6)]  # 6 rows 7 columns
        self.current_player = 1  # Player 1 starts
        self.winner = None  

    def is_valid_move(self, column):
        """
        Checks if a move is valid in that column.

        Move is valid if the column index within 0-6 and there is at least
        one empty cell in the column.

        Args:
            column (int): The column index (0-6).

        Returns:
            bool: True if the move is valid otherwise false.
        """
        if not (0 <= column < 7):  # check column index
            return False
        return self.board[0][column] == 0  # make sure column is not full

    def make_move(self, column):
        """
        Makes move for the current player.

        Move is only made if it is valid and there is no winner yet.
        After the move check for a winner and change player.

        Args:
            column (int): Column (0-6) where move will be made.
        """
        if not self.is_valid_move(column) or self.winner is not None:
            return  # dont process invalid move
        for row in range(5, -1, -1):  # start from bottom row
            if self.board[row][column] == 0:  # find lowest empty spot
                self.board[row][column] = self.current_player  # insert piece on board
                if self.check_winner(row, column):  # check for winner
                    self.winner = self.current_player
                else:
                    self.current_player = 3 - self.current_player  # switch player
                return

    def check_winner(self, row, col):
        """
        Checks if the game has been won.

        Checks all possible directions (horizontal -, vertical |, pos diagonal/ ,neg diagonal \).

        Args:
            row (int): Row index.
            col (int): Column index.

        Returns:
            bool: True if current player wins otherwise False.
        """
        # directions to check
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        # check for 4 connected pieces in any direction
        results = [self.check_line(row, col, dr, dc) for dr, dc in directions]
        return any(results)  # true if any direction has a winning line

    def check_line(self, row, col, dr, dc):
        """
        Checks a single direction for a line of four connected pieces.

        Args:
            row (int): Starting row index.
            col (int): Starting column index.
            dr (int): Row direction increment 
            dc (int): Column direction increment
        Returns:
            bool: True if line of 4 connected pieces is found otherwise false.
        """
        count = 0  # counter for consecutive pieces
        row = row - dr * 3  # start 3 steps back in the given direction
        col = col - dc * 3
        for _ in range(7):  # check up to 7 positions in the given direction
             if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == self.current_player:
                count += 1
                if count == 4:  # return true if 4 in a row
                    return True
            else:
                count = 0  # reset count if a other piece empty spot
            row += dr  # move to the next position
            col += dc

        return False  # no winner