import itertools
import random

# game and AI logic

class Minesweeper():
    """
    Minesweeper game representation
    """
    # gameplay code

    def __init__(self, height=8, width=8, mines=8):
    # define initial board with default values (8, 8, 8)

        # Set initial width, height, and number of mines
        self.height = height
        # assign height attribute to height argument (default of 8)
        self.width = width
        # assign width attribute to width argument (default of 8)
        self.mines = set()
        # assign mines attribute to empty set

        # Initialize an empty field with no mines
        self.board = []
        # assign board to empty list
        for i in range(self.height):
        # iterate over rows
            row = []
            # assign row to empty list
            for j in range(self.width):
            # iterate over columns
                row.append(False)
                # append False to column (indicates no mine in position)
            self.board.append(row)
            # append rows to board (so board is a list of row lists)
            

        # Add mines randomly
        while len(self.mines) != mines:
        # while the length of the mines set is not equal to number of mines
            i = random.randrange(height)
            # randrange method returns a random element from a range
            # assign a random number within height range to i
            j = random.randrange(width)
            # assign a random number within width range to j
            if not self.board[i][j]:
            # board is False at position [i][j] (indicats no mine)
                self.mines.add((i, j))
                # add position as tuple (i, j) to mines set
                self.board[i][j] = True
                # assign board at position [i][j] as True (indicates mine)

        # At first, player has found no mines
        self.mines_found = set()
        # assign mines_found attribute to an empty set (no mines found)

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")
        # prints text based representation of board with location of mines

    def is_mine(self, cell):
    # define is_mine method (returns true if cell has a mine)
        i, j = cell
        # assign firt component of cell to i, second to j
        return self.board[i][j]
        # return True if board at position [i][j] has mine

    def nearby_mines(self, cell):
    # define nearby_mines method (returns number of mines around cell)
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0
        # assign count to 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
        # iterate over rows within one row, !!! why cell[0] + 2
            for j in range(cell[1] - 1, cell[1] + 2):
            # iterate over cols within one cols, !!! why cell[1] + 2

                # Ignore the cell itself
                if (i, j) == cell:
                # if position is cell
                    continue
                    # then ignore/continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                # if i, j positions are in bounds
                    if self.board[i][j]:
                    # if board at position i, j is True (indicatess mine)
                        count += 1
                        # increment count

        return count
        # return count (number of nearby mines)

    def won(self):
    # define won method (returns True if all mines flagged)
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines
        # return true if mine_found is the same as number of mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    # represents logical sentences that contain cells and counts

    def __init__(self, cells, count):
    # define Sentence class with cells and count attributes
        self.cells = set(cells)
        # cells attribute includes a set of cells entered as argument
        self.count = count
        # count attribute is a count of mine cells entered as argument

    def __eq__(self, other):
    # define builtin __eq__ method
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
    # define builtin __str__ method
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        raise NotImplementedError

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """
    # infers which moves to make based on knowledge

    def __init__(self, height=8, width=8):
    # height and width is 8 by default

        # Set initial height and width
        self.height = height
        self.width = width
        # variables of initial height and width set to value of arguments

        # Keep track of which cells have been clicked on
        self.moves_made = set()
        # assign moves_made to empty set

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()
        # assign mines and safe to empty sets

        # List of sentences about the game known to be true
        self.knowledge = []
        # assign knowledge to empty list

    def mark_mine(self, cell):
    # define method to mark cell as mine
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        # add cell to mines using add method
        for sentence in self.knowledge:
        # iterate over sentences in knowledge
            sentence.mark_mine(cell)
            # modify sentence using mark_mine function to indicate cell mine

    def mark_safe(self, cell):
    # define method to mark cell as safe
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        # add cell to safe using add method
        for sentence in self.knowledge:
        # iterate over sentences in knowledge
            sentence.mark_safe(cell)
            # modify sentence using mark_safe function to indicate sell safe

    def add_knowledge(self, cell, count):
    # define method to add knowledge to knowledge base
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        raise NotImplementedError

    def make_safe_move(self):
    # define method to return a safe move
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        raise NotImplementedError

    def make_random_move(self):
    # define method to return a random move
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        raise NotImplementedError
