# Author: Mykola Lopushenko
# GitHub username: Mykola-Lopushenko
# Date: 08/13/2025
# Description: Animal-themed abstract board game

columns = "abcdefg"
rows = "1234567"
TANGERINE = "TANGERINE"
AMETHYST = "AMETHYST"
UNFINISHED = "UNFINISHED"
TANGERINE_WON = "TANGERINE_WON"
AMETHYST_WON = "AMETHYST_WON"

def correct_bounds(column_index, row_index):
    """
    Return True if the given board coordinates are within the range for column and row
    """
    return 0 <= column_index < 7 and 0 <= row_index < 7

def to_index(square):
    """
    Convert board square notation to indexes.
    """
    column_index = columns.index(square[0])
    row_index = rows.index(square[1])
    return column_index, row_index

def to_square(column_index, row_index):
    """
    Convert indexes to board square notation.
    """
    return f"{columns[column_index]}{rows[row_index]}"


class Piece:
    """
    Represents a universal game piece.
    Store piece type, color, and current position.
    """
    def __init__(self, color, position):
        """Initialize the piece with a color and board position."""
        self.color = color
        self.position = position

    def get_color(self):
        return self.color

    def get_position(self):
        return self.position

    def get_legal_moves(self, board_state):
        """
        Return a list of legal target positions based on piece type and board state.
        """
        raise NotImplementedError

    def friendly_piece(self, other_piece):
        """
        Return True if the other piece is the same color as this one.
        """
        return other_piece and self.color == other_piece.color


class Narwhal(Piece):
    """
    Inherits from Piece.
    Diagonal-jumping piece with distance 2.
    Also, can move 1 square orthogonally instead of its normal move
    """
    def get_legal_moves(self, board_state):
        """
        Returns legal diagonal jumps and 1-square orthogonal moves.
        """
        moves = []
        column_index, row_index = to_index(self.position)

        #Normal diagonal move with distance 2.
        diagonal_directions = [(2, 2), (2, -2), (-2, 2), (-2, -2)]
        for column_step, row_step in diagonal_directions:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        #1 square orthogonally move.
        orthogonal_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for column_step, row_step in orthogonal_directions:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        return moves

class Marmoset(Piece):
    """
    Inherits from Piece.
    Diagonal-sliding piece with distance up to 4 squares.
    Also, can move 1 square orthogonally instead of its normal move.
    """
    def get_legal_moves(self, board_state):
        """
        Return legal diagonal sliding moves up to distance 4 and 1-square orthogonal move.
        """
        moves = []
        column_index, row_index = to_index(self.position)

        #Normal diagonal sliding and stop when hitting any piece
        diagonal_steps = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for column_step, row_step in diagonal_steps:
            for distance in range(1, 5):
                new_column = column_index + column_step * distance
                new_row = row_index + row_step * distance
                if not correct_bounds(new_column, new_row):
                    break
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)

                if destination_piece is None:
                    moves.append(destination_square)
                    continue  # keep sliding
                # hit a piece: can capture enemy, then must stop
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)
                break  # blocked after encountering any piece

        #1 square orthogonally move.
        orthogonal_directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for column_step, row_step in orthogonal_directions:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        return moves

class Okapi(Piece):
    """
    Inherits from Piece.
    Orthogonal-jumping piece that moves only 1 square.
    Also, can move 1 square diagonally instead of its normal move.
    """
    def get_legal_moves(self, board_state):
        """
        Return legal orthogonal jump moves of distance 1 and 1-square diagonal moves.
        """
        moves = []
        column_index, row_index = to_index(self.position)

        #Only 1 orthogonal move
        orthogonal_steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for column_step, row_step in orthogonal_steps:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        #1-square diagonal move
        diagonal_steps = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for column_step, row_step in diagonal_steps:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        return moves

class Chinchilla(Piece):
    """
    Inherits from Piece.
    Orthogonal-sliding piece with distance up to 3 squares.
    Also, can move 1 square diagonally instead of its normal move.
    If captured, the game ends.
    """
    def get_legal_moves(self, board_state):
        """
        Return legal orthogonal sliding moves up to distance 3 and 1-square diagonal move.
        """
        moves = []
        column_index, row_index = to_index(self.position)

        #Normal orthogonal sliding and stops at first encountered piece
        orthogonal_steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for column_step, row_step in orthogonal_steps:
            for distance in range(1, 4):
                new_column = column_index + column_step * distance
                new_row = row_index + row_step * distance
                if not correct_bounds(new_column, new_row):
                    break
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)

                if destination_piece is None:
                    moves.append(destination_square)
                    continue  # keep sliding
                if not self.friendly_piece(destination_piece):  # hit a piece: can capture enemy, then must stop
                    moves.append(destination_square)
                break

        #1-square diagonal move
        diagonal_steps = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for column_step, row_step in diagonal_steps:
            new_column = column_index + column_step
            new_row = row_index + row_step
            if correct_bounds(new_column, new_row):
                destination_square = to_square(new_column, new_row)
                destination_piece = board_state.get(destination_square)
                if not self.friendly_piece(destination_piece):
                    moves.append(destination_square)

        return moves

class AnimalGame:
    """Control game flow, board state, and turns."""
    def __init__(self):
        """
        Initialize the board with all pieces in starting positions and track turn order.
        """
        self.board = {f"{col}{row}": None for col in columns for row in rows}
        self.turn = TANGERINE
        self.state = UNFINISHED
        self.starting_positions()

    def starting_positions(self):
        #Row 1. Start tangerine player's pieces
        first_order = [Narwhal, Marmoset, Okapi, Chinchilla, Okapi, Marmoset, Narwhal]
        for index, cls in enumerate(first_order):
            square = f"{columns[index]}1"
            self.board[square] = cls(TANGERINE, square)
        #Row 7. Start amethyst player's pieces
        for index, cls in enumerate(first_order):
            square = f"{columns[index]}7"
            self.board[square] = cls(AMETHYST, square)

    def get_game_state(self):
        """
        Return current game state: 'UNFINISHED', 'TANGERINE_WON', or 'AMETHYST_WON'.
        """
        return self.state

    def make_move(self, start_square, finish_square):
        """
        Attempt to move a piece from one square to another.
        Returns True if move is valid and executed, False otherwise.
        """
        if not self.is_valid_move(start_square, finish_square):
            return False

        piece = self.board[start_square]
        target = self.board[finish_square]

        # perform move
        self.board[start_square] = None
        self.board[finish_square] = piece
        piece.position = finish_square

        # win if a Chinchilla was captured
        if type(target) is Chinchilla:
            self.state = TANGERINE_WON if piece.get_color() == TANGERINE else AMETHYST_WON
            return True

        # change turn
        self.turn = AMETHYST if self.turn == TANGERINE else TANGERINE
        return True

    def is_valid_move(self, start_square, finish_square):
        """
        Check if a move is legal based on piece type, distance, direction, and board state.
        """
        # game must be active
        if self.state != UNFINISHED:
            return False

        # squares must exist and be in the board
        if (len(start_square) != 2 or len(finish_square) != 2 or
                start_square not in self.board or finish_square not in self.board):
            return False

        piece = self.board[start_square]
        if piece is None:
            return False

        # correct side to move
        if piece.get_color() != self.turn:
            return False

        # cannot capture own piece
        target_piece = self.board[finish_square]
        if piece.friendly_piece(target_piece):
            return False

        # end square must be one of the piece's legal destinations
        legal_moves = piece.get_legal_moves(self.board)
        return finish_square in legal_moves



