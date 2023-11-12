import chess
import chess.svg
import chess.engine
import copy
import numpy as np
import pygame
from minimax import ChessPlayer
from pygame.locals import QUIT, MOUSEBUTTONDOWN


def display_board(board):
    print(board)

# Function to play an interactive game in the console
def play_interactive_game_console():
    board = chess.Board()
    player = ChessPlayer(board)

    while not board.is_game_over():
        print("\n" + "=" * 20)
        display_board(board)
        print("=" * 20 + "\n")

        if board.turn == chess.WHITE:
            # Human player's move
            move_uci = str(player.play_chess())
        else:
            # Bot's move      
            move_uci = input("Enter your move (in UCI format, e.g., 'e2e4'): ")
            if move_uci.lower() == 'exit':
                break

        if chess.Move.from_uci(move_uci) in board.legal_moves:
            board.push(chess.Move.from_uci(str(move_uci)))
        else:
            print("Invalid move. Try again.")

    print("Game Over")
    print("Result: " + board.result())

# Run the interactive game in the console
play_interactive_game_console()