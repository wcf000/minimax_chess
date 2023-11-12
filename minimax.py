import chess
import chess.engine
import copy
import numpy as np

class ChessPlayer:
    def __init__(self, board):
        self.board = board
        self.move_count = 0

    def play_chess(self):
        self.move_count += 1
        turn = self.board.turn
        depth = 3
        if (self.is_early_game(self.board)):
            _, best_move = self.alpha_beta_search(self.board, 3, float('-inf'), float('inf'), turn)
        elif (self.is_mid_game):
            _, best_move = self.alpha_beta_search(self.board, 4, float('-inf'), float('inf'), turn)
        else:
            _, best_move = self.alpha_beta_search(self.board, 10, float('-inf'), float('inf'), turn)
        print("My move: ", best_move)
        return best_move

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_game_over(board):
            return self.evaluate_board(board), None

        legal_moves = list(self.get_legal_moves(board))  # Convert legal_moves to a list for indexing

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in legal_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in legal_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.alpha_beta_search(new_board, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
    
    def evaluate_board(self, board):
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000,
        }

        evaluation_score = 0

        pawn_table_white = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ])

        knight_table_white = np.array([
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20, 0, 0, 0, 0, -20, -40],
            [-30, 0, 10, 15, 15, 10, 0, -30],
            [-30, 5, 15, 20, 20, 15, 5, -30],
            [-30, 0, 15, 20, 20, 15, 0, -30],
            [-30, 5, 10, 15, 15, 10, 5, -30],
            [-40, -20, 0, 5, 5, 0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50],
        ])

        bishop_table_white = np.array([
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 10, 10, 5, 0, -10],
            [-10, 5, 5, 10, 10, 5, 5, -10],
            [-10, 0, 10, 10, 10, 10, 0, -10],
            [-10, 10, 10, 10, 10, 10, 10, -10],
            [-10, 5, 0, 0, 0, 0, 5, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20],
        ])

        rook_table_white = np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [0, 0, 0, 5, 5, 0, 0, 0],
        ])

        queen_table_white = np.array([
            [-20, -10, -10, -5, -5, -10, -10, -20],
            [-10, 0, 0, 0, 0, 0, 0, -10],
            [-10, 0, 5, 5, 5, 5, 0, -10],
            [-5, 0, 5, 5, 5, 5, 0, -5],
            [0, 0, 5, 5, 5, 5, 0, -5],
            [-10, 5, 5, 5, 5, 5, 0, -10],
            [-10, 0, 5, 0, 0, 0, 0, -10],
            [-20, -10, -10, -5, -5, -10, -10, -20],
        ])

        king_table_midgame_white = np.array([
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-30, -40, -40, -50, -50, -40, -40, -30],
            [-20, -30, -30, -40, -40, -30, -30, -20],
            [-10, -20, -20, -20, -20, -20, -20, -10],
            [20, 20, 0, 0, 0, 0, 20, 20],
            [20, 30, 10, 0, 0, 10, 30, 20],
        ])

        king_table_endgame_white = np.array([
            [-50, -40, -30, -20, -20, -30, -40, -50],
            [-30, -20, -10, 0, 0, -10, -20, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 30, 40, 40, 30, -10, -30],
            [-30, -10, 20, 30, 30, 20, -10, -30],
            [-30, -30, 0, 0, 0, 0, -30, -30],
            [-50, -30, -30, -30, -30, -30, -30, -50],
        ])
        
        pawn_table_black = self.mirror_board(pawn_table_white)
        knight_table_black = self.mirror_board(knight_table_white)
        bishop_table_black = self.mirror_board(bishop_table_white)
        rook_table_black = self.mirror_board(rook_table_white)
        queen_table_black = self.mirror_board(queen_table_white)
        king_table_midgame_black = self.mirror_board(king_table_midgame_white)
        king_table_endgame_black = self.mirror_board(king_table_endgame_white)

        for square in chess.SQUARES:
                piece = board.piece_at(square)

                if piece is not None:
                    piece_value = piece_values.get(piece.piece_type, 0)

                    # Determine which side the piece belongs to
                    side_multiplier = 1 if piece.color == chess.WHITE else -1

                    # Choose the appropriate piece-square table based on the side
                    if piece.piece_type == chess.PAWN:
                        piece_table = pawn_table_white if piece.color == chess.WHITE else pawn_table_black
                    elif piece.piece_type == chess.KNIGHT:
                        piece_table = knight_table_white if piece.color == chess.WHITE else knight_table_black
                    elif piece.piece_type == chess.BISHOP:
                        piece_table = bishop_table_white if piece.color == chess.WHITE else bishop_table_black
                    elif piece.piece_type == chess.ROOK:
                        piece_table = rook_table_white if piece.color == chess.WHITE else rook_table_black
                    elif piece.piece_type == chess.QUEEN:
                        piece_table = queen_table_white if piece.color == chess.WHITE else queen_table_black
                    elif piece.piece_type == chess.KING:
                        # Choose the appropriate table for the king based on midgame or endgame
                        king_table = None
                        if piece.color == chess.WHITE:
                            king_table = king_table_endgame_white if self.is_end_game(board) else king_table_midgame_white
                        else:
                            king_table = king_table_endgame_black if self.is_end_game(board) else king_table_midgame_black
                        piece_table = king_table

                    # Adjust the score based on the piece's position
                    evaluation_score += side_multiplier * (piece_value + piece_table[chess.square_rank(square)][chess.square_file(square)])
        
        if board.is_checkmate():
            evaluation_score += side_multiplier * 1000000

        # Check for stalemate.
        if board.is_stalemate():
            evaluation_score += side_multiplier * 0

        # Check for insufficient material.
        if board.is_insufficient_material():
            evaluation_score += side_multiplier * 0

        return evaluation_score

    def is_early_game(self, board):
        """
        Returns True if the given board is in the early game, False otherwise.
        """

        # Check the number of pieces on the board.
        piece_map = board.piece_map()
        if len(piece_map) > 30:
            return True

        # Check if both players have castled.
        if not board.has_kingside_castling_rights(chess.WHITE) or not board.has_queenside_castling_rights(chess.WHITE):
            return True
        if not board.has_kingside_castling_rights(chess.BLACK) or not board.has_queenside_castling_rights(chess.BLACK):
            return True

        # Return False if none of the above conditions are met.
        return False

    def is_mid_game(self, board):
        """
        Returns True if the given board is in the mid game, False otherwise.
        """

        return not self.is_early_game(board) and not self.is_end_game(board)

    def is_end_game(self, board):
        """
        Returns True if the given board is in the end game, False otherwise.
        """

        # Check the number of pieces on the board.
        piece_map = board.piece_map()
        if len(piece_map) <= 15:
            return True
        # Return False if none of the above conditions are met.
        return False
    
    def mirror_board(self, board_array):
    # Mirror the board array vertically (reflect along the horizontal axis)
        return np.flipud(board_array)
    
    def is_game_over(self, board):
        return board.is_game_over() or board.is_stalemate()

    def get_legal_moves(self, board):
        return board.legal_moves

    def make_move(self,board, move_uci):
            new_board = copy.deepcopy(board)
            new_board.push(chess.Move.from_uci(str(move_uci)))
            return new_board
