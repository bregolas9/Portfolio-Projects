# project-10

**Remember that this project cannot be submitted late.**

Write a class called OrthokonBoard that represents the board for a two-player game that is played on a 4x4 grid. This class does not do everything needed to play a game - it's just responsible for handling the rules concerning the game board. Things like asking the user for moves, printing results for the user, keeping track of whose turn it is, and running the game loop would be the responsibility of one or more other classes. You're already familiar with breaking down a complex task into multiple functions. Likewise, a large, complex program can be simplified by being broken down into multiple classes, each of which has multiple methods. Objects of these different classes then interact with each other to accomplish the desired tasks. This is known as object-oriented programming (OOP). You'll encounter this more in CS 162. For assignment 10, you are only concerned with the OrthokonBoard class.

The board starts with four red pieces on row 0 and four yellow pieces on row 3. A valid move consists of a player moving one of their pieces orthogonally or diagonally **as far as it can go until it hits another piece or the edge of the board** (it must move at least one space). After the piece stops, any opponent pieces on **orthogonally** adjacent squares are flipped over to its color. The OrthokonBoard class doesn't keep track of whose turn it is, so it will allow multiple moves by the same player consecutively. A player wins upon making a move that either flips over the remaining opponent pieces or leaves the opponent without a move.

The class should have the following **private** data members: a representation of the board, and the current state, which holds one of the three following values: "RED_WON", "YELLOW_WON", or "UNFINISHED". 

It should have an init method that initializes the starting board positions, initializes the current_state to "UNFINISHED", and appropriately initializes any other data members. Tip: Probably the easiest way of representing the board is to use a list of lists.  The init method could then initialize the board to a list of 4 lists, each of which contains 4 empty strings (or whatever character you want to use to represent an empty space).

It should have a get method named get_current_state, which returns the current state.

It should have a method named make_move that takes four parameters - the row and column (in that order) of the piece being moved, and the row and column (in that order) of the square it's being moved to. If the game has already been won, or if the move is not valid, make_move should just **return False**. Otherwise, it should record the move, update the board and the current state, and **return True**. To update the current state, you need to detect if this move causes a win for either player.

It's not required, but you'll probably find it useful for testing and debugging to have a method that prints out the board.

Whether you think of the list indices as being [row][column] or [column][row] doesn't matter as long as you're consistent.

You are allowed to add other, **private**, methods to your class.

As a very simple example, your class could be used as follows:
```
board = OrthokonBoard()
board.make_move(3,2,1,0)  # The yellow player moves a piece diagonally, flipping one red piece to yellow
board.make_move(0,2,2,0)  # The red player moves a piece diagonally, flipping two yellow pieces to red
print(board.get_current_state())
```

Again, if you're not sure where to start:
- First try playing a few games to make sure you understand the rules (you could draw a board on paper and use coins for the pieces).
- Break the project down into small, discrete tasks, and then tackle the easiest ones first. For this project, we'll let you think about what that would look like.
- Test as you go, and know what the correct result should be before running a test.

Your file must be named: OrthokonBoard.py
