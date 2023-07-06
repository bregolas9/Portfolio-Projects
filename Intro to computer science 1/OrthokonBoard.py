# Author: Brendan Bordine
# Date: June 2, 2021
# Description: A class called OrthokonBoard which represents the board for a two player game called
# Orthokon which is played on a 4x4 board.
class OrthokonBoard:
    """Creates a class called OrthokonBoard which represents the board for a two player game called
    Orthokon which is played on a 4x4 board."""
    board = []
    current_state = ""

    def __init__(self):
        """Initializes the board and the current state of the game."""
        self.current_state = "UNFINISHED"
        self.board = [["Y", "Y", "Y", "Y"],
                      ["", "", "", ""],
                      ["", "", "", ""],
                      ["R", "R", "R", "R"]]

    def get_current_state(self):
        """Returns the current state of the game."""
        rs = []
        ys = []
        for row in self.board:
            for val in row:
                if val == "R":
                    rs.append("R")
                if val == "Y":
                    ys.append("Y")
                print(val)

        if len(rs) == 0:
            self.current_state = "YELLOW_WON"
        if len(ys) == 0:
            self.current_state = "RED_WON"

        return self.current_state

    def make_move(self, piece_row, piece_column, square_row, square_column):
        """Lets a player make a move in the game. This function lets the player pick a place if it is in bounds
        and the rules of the game are not broken. The player can move Orthogonally or Diagonally. The player cannot
         place on another piece."""
        player_letter = self.board[piece_row][piece_column]

        if self.board[piece_row][piece_column] == "R":
            opponent_letter = "Y"
        if self.board[piece_row][piece_column] == "Y":
            opponent_letter = "R"

        # Bad data filtering
        if self.current_state != "UNFINISHED" or \
                piece_row < 0 or piece_row > 3 or \
                piece_column < 0 or piece_column > 3 or \
                square_row < 0 or square_row > 3 or \
                square_column < 0 or square_column > 3:
            return False

        # Orthogonal move
        if piece_row == square_row:
            if square_column > piece_column:
                """Right"""
                for i in range(3 - piece_column):
                    if self.board[square_row][3-i] != "":
                        return False
                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

            elif piece_column > square_column:
                """Left"""
                for i in range(piece_column):
                    if self.board[square_row][i] != "":
                        return False

                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

        if piece_column == square_column:
            if piece_row > square_row:
                """Up"""
                for i in range(piece_row):
                    if self.board[square_column][i] != "":
                        return False

                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

            elif square_row > piece_row:
                """Down"""
                for i in range(3 - piece_row):
                    if self.board[square_column][3-i] != "":
                        return False

                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

        """Diagonal move"""
        if abs(square_column - piece_column) == abs(square_row - piece_row):
            r = 0
            if piece_column > square_column and piece_row > square_row:
                """Up left"""
                if piece_column > piece_row:
                    r = piece_row
                else:
                    r = piece_column
                for i in range(r):
                    if self.board[piece_row - i - 1][piece_column - i - 1] != "":
                        return False

                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

            if piece_column > square_column and piece_row < square_row:
                """Down left"""
                if piece_column > piece_row:
                    r = piece_column - piece_row
                else:
                    r = piece_column

                for i in range(r):
                    if self.board[piece_row + i + 1][piece_column - i - 1] != "":
                        return False

                """commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

            if square_row < piece_row and square_column > piece_column:
                """Up right"""
                if piece_column < piece_row:
                    r = piece_row - piece_column
                else:
                    r = piece_row

                for i in range(r):
                    if self.board[piece_row - i - 1][piece_column + i + 1] != "":
                        return False

                """Commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

            if square_column > piece_column and square_row > piece_row:
                """Down right"""
                if piece_column < piece_row:
                    r = square_column - piece_column
                else:
                    r = square_row - piece_row

                for i in range(r):
                    if self.board[piece_row + i + 1][piece_column + i + 1] != "":
                        return False

                """Commit move"""
                self.board[square_row][square_column] = self.board[piece_row][piece_column]
                self.board[piece_row][piece_column] = ""

                self.__check_and_update_squares(player_letter, opponent_letter, square_row, square_column)

                return True

        else:
            return True

    def __check_and_update_squares(self, player_letter, opponent_letter, square_row, square_column):
        """Once the player makes a move, this function is called to see if any of the player's tokens are
        changed color."""
        if self.board[square_row+1][square_column] == opponent_letter:
            self.board[square_row+1][square_column] = player_letter
        if self.board[square_row-1][square_column] == opponent_letter:
            self.board[square_row-1][square_column] = player_letter
        if self.board[square_row][square_column-1] == opponent_letter:
            self.board[square_row][square_column-1] = player_letter
        if self.board[square_row][square_column+1] == opponent_letter:
            self.board[square_row][square_column+1] = player_letter

