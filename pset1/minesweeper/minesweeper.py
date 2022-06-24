import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation of where mines are located.
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

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are within one row and column of a
        given cell, not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game A sentence consists of a set of
    board cells, and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        # If number of cells is same as count then all cells have mines
        if self.count == len(self.cells) and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """

        # If count is zero then all cells are safe
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that a cell is
        known to be a mine.
        """

        # If mine cell in sentence then remove cell and decrement count
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that a cell is
        known to be safe.
        """

        # If safe cell in sentence then remove cell
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge to mark that cell as
        a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge to mark that cell as
        safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def clean(self):
        """
        Remove empty and duplicate sentences
        """
        # Remove empty (i.e. without cells) sentences
        for sentence in self.knowledge:
            if sentence.cells == set():
                self.knowledge.remove(sentence)

        # Remove duplicate sentences
        dup_rem = []
        for sentence in self.knowledge:
            if sentence not in dup_rem:
                dup_rem.append(sentence)
        self.knowledge = dup_rem

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given safe cell, how
        many neighboring cells have mines in them.

        This function:
            1) marks the cell as a move that has been made
            2) marks the cell as safe
            3) adds a new sentence to the AI's knowledge base based on the
               value of `cell` and `count`
            4) marks any additional cells as safe or as mines if it can be
               concluded based on the AI's knowledge base
            5) adds any new sentences to the AI's knowledge base if they can be
               inferred from existing knowledge
        """

        # 1. Mark cell as a move that has been made
        self.moves_made.add(cell)

        # 2. Mark cell as safe
        self.mark_safe(cell)

        # 3. Add sentence to knowledge base according to neighbors and count

        # Initialize undetermined set (cells not known to be safe/mines)
        undetermined = set()

        # Iterate over neighboring cells
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore original cell
                if (i, j) == cell:
                    continue
                # Ignore safe cells
                if (i, j) in self.safes:
                    continue
                # Ignore mine cells and decrement count
                if (i, j) in self.mines:
                    count -= 1
                    continue
                # Add undecided cells if on the game board
                if 0 <= i < self.height and 0 <= j < self.width:
                    undetermined.add((i, j))

        # Add undetermined and count to new_sentence and add to knowledge base
        new_sentence = Sentence(undetermined, count)
        self.knowledge.append(new_sentence)

        # 4. Mark additional cells as safe/mines according to knowledge base

        # Continue inferring knowledge until knowledge base stable
        unstable = True
        while unstable:
            unstable = False

            # Iterate over sentences
            safes = set()
            mines = set()
            for sentence in self.knowledge:
                # Assign known mine and safe cells to sets
                safes = safes.union(sentence.known_safes())
                mines = mines.union(sentence.known_mines())

                # If one or more mine or safe cells then mark as safe/mine
                if safes:
                    unstable = True
                    for safe in safes:
                        self.mark_safe(safe)
                if mines:
                    unstable = True
                    for mine in mines:
                        self.mark_mine(mine)
            self.clean()

        # 5. Add sentences to the AI's knowledge base from existing knowledge

            # Declare new_sentences list
            new_sentences = []

            # Iterate over sentences to compare sentences
            for first_sentence in self.knowledge:
                for second_sentence in self.knowledge:

                    # Ignore identical sentences
                    if first_sentence.cells == second_sentence.cells:
                        continue

                    # Create new sentences if sentence is subset
                    if first_sentence.cells.issubset(second_sentence.cells):
                        new_cells = second_sentence.cells - first_sentence.cells
                        new_count = second_sentence.count - first_sentence.count
                        new_sentence = Sentence(new_cells, new_count)
                        new_sentences.append(new_sentence)

            # Add new sentences to knowledge base
            for sentence in new_sentences:
                if sentence not in self.knowledge and sentence.cells != set():
                    self.knowledge.append(sentence)
                    unstable = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Determine available safe moves and return move if available
        safe = list(self.safes - self.moves_made)
        if len(safe) > 0:
            return safe[0]
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Iterate over gameboard cells and add available moves
        rand = []
        for i in range(self.height):
            for j in range(self.width):
                # Ignore moves mode
                if (i, j) in self.moves_made:
                    continue
                # Ignore mine cells
                elif (i, j) in self.mines:
                    continue
                # Add remaining cells
                else:
                    rand.append((i, j))

        # Return random move if available
        if len(rand) > 0:
            move = random.randint(0, len(rand) - 1)
            return rand[move]
        else:
            return None
        # Note, when knowledge available could select the move that has the
        # lowest probability of being a mine (cells / count)
