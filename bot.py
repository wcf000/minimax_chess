"""
The Brandeis Quant Club ML/AI Competition (November 2023)

Author: @Ephraim Zimmerman
Email: quants@brandeis.edu
Website: brandeisquantclub.com; quants.devpost.com

Description:

For any technical issues or questions please feel free to reach out to
the "on-call" hackathon support member via email at quants@brandeis.edu

Website/GitHub Repository:
You can find the latest updates, documentation, and additional resources for this project on the
official website or GitHub repository: https://github.com/EphraimJZimmerman/chess_hackathon_23

License:
This code is open-source and released under the MIT License. See the LICENSE file for details.
"""

import random
from minimax import ChessPlayer
import chess
import time
from collections.abc import Iterator
from contextlib import contextmanager
import test_bot

@contextmanager
def game_manager() -> Iterator[None]:
    """Creates context for game."""

    print("===== GAME STARTED =====")
    ping: float = time.perf_counter()
    try:
        # DO NOT EDIT. This will be replaced w/ judging context manager.
        yield
    finally:
        pong: float = time.perf_counter()
        total = pong - ping
        print(f"Total game time = {total:.3f} seconds")
    print("===== GAME ENDED =====")

class Bot:
    def __init__(self, fen=None):
        self.board = chess.Board(fen if fen else "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    def check_move_is_legal(self, initial_position, new_position) -> bool:

        """
            To check if, from an initial position, the new position is valid.

            Args:
                initial_position (str): The starting position given chess notation.
                new_position (str): The new position given chess notation.

            Returns:
                bool: If this move is legal
        """

        return chess.Move.from_uci(initial_position + new_position) in self.board.legal_moves

    def next_move(self) -> str:
        """
            The main call and response loop for playing a game of chess.

            Returns:
                str: The current location and the next move.
        """

        # Assume that you are playing an arbitrary game. This function, which is
        # the core "brain" of the bot, should return the next move in any circumstance.
        chess_player = ChessPlayer(self.board)
        move = chess_player.play_chess()
        return move


# Add promotion stuff

if __name__ == "__main__":
    win_count = 0
    drawn_count = 0
    lose_count = 0
    total_game = 3
    count_game = 0
    total_game_time = 0.0 
    
    total_start_time = time.perf_counter()

    for i in range(0, total_game):
        count_game += 1
        chess_bot = Bot()  # you can enter a FEN here, like Bot("...")
        with game_manager():

            """
            
            Feel free to make any adjustments as you see fit. The desired outcome 
            is to generate the next best move, regardless of whether the bot 
            is controlling the white or black pieces. The code snippet below 
            serves as a useful testing framework from which you can begin 
            developing your strategy.
    
            """

            playing = True
            while playing:
                if chess_bot.board.turn:
                    chess_bot.board.push_san(test_bot.get_move(chess_bot.board))
                else:
                    chess_bot.board.push(chess_bot.next_move())
                print(chess_bot.board, end="\n\n")

                if chess_bot.board.is_game_over():
                    if chess_bot.board.is_stalemate():
                        print("Is stalemate")
                    elif chess_bot.board.is_insufficient_material():
                        print("Is insufficient material")
                    # EX: Outcome(termination=<Termination.CHECKMATE: 1>, winner=True)
                    outcome = chess_bot.board.outcome()
                    print(outcome)
                    if outcome.winner is False:
                        win_count += 1
                    elif outcome.winner is None:
                        drawn_count += 1
                    else:
                        lose_count += 1
                    playing = False
    total_end_time = time.perf_counter()

    # Calculate the total game time for all games
    total_game_time = total_end_time - total_start_time

    print("Total game time for all games = {:.3f} seconds".format(total_game_time))
    print("win rate", win_count / total_game)
    print("drawn rate", drawn_count / total_game)
    print("lose rate", lose_count / total_game)
    print("game rounds", count_game)
