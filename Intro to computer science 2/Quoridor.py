# Author: Brendan Bordine
# Date: 8/12/21
# Description: Code which creates a playable game called Quoridor. The code is made of multiple classes which have
# multiple functions. These functions allow the players to move their pieces and to place walls within the game.

class QuoridorGame:
    """A class which initializes the game of Quoridor by itself."""
    def __init__(self):
        self._p1 = self.Pawn(4, 0)
        self._p2 = self.Pawn(4, 8)
        self.board = self.Board()
        self.board.place_piece(0, 4, "1")
        self.board.place_piece(8, 4, "2")
        self.count = 1
        self.placed_fences = []
        self._p1_fence_left = 10
        self._p2_fence_left = 10

    def get_placed_fences(self):
        """Returns fences already placed."""
        return self.placed_fences

    def move_pawn(self, player, cords):
        """Moves the players pawn when the user inputs which player they are and where their piece is moving to."""
        if player == 1:
            self.board.remove_piece(self._p1.get_x(), self._p1.get_y())
            self.board.place_piece(cords[0], cords[1], "1")
            self._p1.set_location(cords[0], cords[1])

        if player == 2:
            self.board.remove_piece(self._p2.get_x(), self._p2.get_y())
            self.board.place_piece(cords[0], cords[1], "2")
            self._p2.set_location(cords[0], cords[1])
        self.count_turns()
        return True

    def place_fence(self, player, orientation, coords):
        """Places a fence based on user input of orientation, coordinates, and which payer is placing it."""
        if player == 1:
            self._p1_fence_left -= 1
        if player == 2:
            self._p2_fence_left -= 1
        self.fence = self.Fence(player, orientation, coords[0], coords[1])
        self.placed_fences.append(self.fence.get_x())
        self.placed_fences.append(self.fence.get_y())
        self.placed_fences.append(self.fence.get_orientation())

    def count_turns(self):
        """Counts the turns that are taken all game."""
        self.count += 1

    class Board:
        """A class which represents the game board, which initializes by setting the length of the board to 9."""
        def __init__(self, length=9):
            self._length = length
            self._cell = [[None for c in range(self._length)]for r in range(self._length)]

        def remove_piece(self, row, col):
            """Removes a piece from the position given by the rwo-column index."""
            self._cell[col][row] = None

        def place_piece(self, row, col, piece):
            """Places a piece at the position given by the row-column index."""
            self._cell[row][col] = piece

        def print_board(self):
            """Displays the board."""
            print(self)

        def __str__(self):
            """The string representation of the board."""
            row_rest = '\n' + (' ' * 2) + ('+   ' * self._length) + '+' + '\n'
            row_one = '\n' + (' ' * 2) + ('+---' * self._length) + '+' + '\n'

            str_ = (' ' * 3) + row_one
            for r in range(0, self._length):
                str_ += '  |'
                for c in range(0, self._length):
                    str_ += ' ' + \
                            (str(self._cell[r][c])
                                if self._cell[r][c] is not None else ' ') + '  '
                    if c == 8:
                        str_ += '|'
                if 0 <= r <= 7:
                    str_ += row_rest
                else:
                    str_ += row_one

            return str_

        def __repr__(self):
            """Function for the REPL printing."""
            return self.__str__()

    class Fence:
        """A class which represents a fence, which is initialized by which player is placing it, what orientation the
        fence is being placed in, and the two coordinated at which the fence is being place."""
        def __init__(self, player, orientation, x, y):
            self._player = player
            self._orientation = orientation
            self._x_coordinate = x
            self._y_coordinate = y

        def get_x(self):
            """Returns the location of the fence by the x value."""
            return self._x_coordinate

        def set_x(self, new_x):
            """Sets the location of the fence with the x value."""
            self._x_coordinate = new_x

        def get_y(self):
            """Returns the location of the fence by the y value."""
            return self._y_coordinate

        def set_y(self, new_y):
            """Sets the location of the fence with the y value."""
            self._y_coordinate = new_y

        def get_orientation(self):
            """Returns the orientation of the placed fence."""
            return self._orientation

    class Pawn:
        """A class representing a pawn which initializes by the coordinated it is currently at."""
        def __init__(self, x, y):
            self._x_cooridate = x
            self._y_cooridate = y

        def get_x(self):
            """Returns the location of the pawn from the x coordinate."""
            return self._x_cooridate

        def get_y(self):
            """Returns the location of the pawn from the y coordinate."""
            return self._y_cooridate

        def set_location(self, x, y):
            """Sets the location of the pawn given the x and y coordinates."""
            self._x_cooridate = x
            self._y_cooridate = y

if __name__ == '__main__':
    q = QuoridorGame()
    q.board.print_board()
    q.move_pawn(2, (7,4))
    q.board.print_board()
    q.place_fence(1, "v", (6, 3))
    q.place_fence(2, "h", (5, 8))
    print(q.get_placed_fences())