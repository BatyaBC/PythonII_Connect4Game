"""
Implements a connect4 GUI using tkinter library.

Classes:
    Connect4GUI: Class that manages the GUI.

The GUI allows a human player to play Connect 4 AI.
"""

import tkinter as tk
from tkinter import messagebox
import Connect4Game as game
import DanielBatyrevAI as DanielAI
import copy

# vars for different strategies
random_choice = DanielAI.RandomStrategy()
yosef_choice = YosefAI.AI_strategy()
shmuli_choice = ShmulyAI.NotRandomStrategy()


class Connect4GUI:
    """
    A class for creating and managing a GUI for the Connect 4 game.

    Attributes:
        master (tk.Tk): Root tkinter window.
        game (Connect4Game): Game object.
        buttons (list[tk.Button]): Buttons for selecting columns.
        canvas (tk.Canvas): Game board canvas.
    """

    def __init__(self, master):
        """
        Initializes Connect4GUI and sets up tkinter window and widgets.

        Args:
            master (tk.Tk): Root tkinter window.
        """
        self.master = master
        self.master.title("Connect 4")  # set title
        self.game = game.Connect4Game()  # initialize Connect 4 game

        # buttons for selecting columns
        self.buttons = []
        for col in range(7):
            button = tk.Button(master, text=str(col + 1), command=lambda c=col: self.make_move(c))
            button.grid(row=0, column=col)
            self.buttons.append(button)

        # canvas for game board
        self.canvas = tk.Canvas(master, width=7 * 60, height=6 * 60)
        self.canvas.grid(row=1, column=0, columnspan=7)
        self.draw_board()



    def make_move(self, column):
        """
        Handles player's move in the specified column.

        If the move is valid and game is not over, method updates the board,
        checks for winner and lets AI make a move.

        Args:
            column (int): Column (0-6) where player wants to go.
        """
        # make move
        self.game.make_move(column)
        self.draw_board()

        # check if player won
        if self.game.winner is not None:
            winner_text = f"Player {self.game.winner} wins!"
            messagebox.showinfo("Game Over", winner_text)  # display winner
            self.master.destroy() 
        else:
            # AI make move
            game_copy = copy.deepcopy(self.game)  # deep copy of the game for AI (prevent ai from corrupting game board)
            self.game.make_move(shmuli_choice.strategy(game_copy))
            self.draw_board()

            # check if AI won
            if self.game.winner is not None:
                winner_text = f"Player {self.game.winner} wins!"
                messagebox.showinfo("Game Over", winner_text)  # display winner
                self.master.destroy()

    def draw_board(self):
        """
        Draws current game board.
        """
        self.canvas.delete("all")  # clear canvas
        for row in range(6):
            for col in range(7):
                # set up box boundary points
                x0, y0 = col * 60, row * 60
                x1, y1 = x0 + 60, y0 + 60

                # draw grid
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

                # draw pieces if present
                if self.game.board[row][col] == 1:
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red", outline="red")
                elif self.game.board[row][col] == 2:
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="yellow", outline="yellow")

        # update buttons (disable buttons for full columns)
        for col in range(7):
            if self.game.board[0][col] == 0:  # not full
                self.buttons[col]["state"] = tk.NORMAL
            else:  # full  column
                self.buttons[col]["state"] = tk.DISABLED


if __name__ == "__main__":
    # create main tkinter window  start the game
    root = tk.Tk()
    app = Connect4GUI(root)
    root.mainloop()
