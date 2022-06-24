import sys
import re
import random

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """

        # Initialize variable length to 0
        var_len = 0

        # Iterate over variables in domain
        for var in self.domains:

            # Assign variable length
            var_len = var.length

            # Retain values with lengths equal to variable length
            self.domains[var] = \
                [val for val in self.domains[var] if len(val) == var_len]

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
      
        # Track revisions
        revised = False

        # Check all overlaps
        overlaps = self.crossword.overlaps
        
        # Determine overlap position of x,y
        x_pos = overlaps[x, y][0]
        y_pos = overlaps[x, y][1]

        # Determine letters at overlap in variable x values
        x_letters = {}

        # Iterate over values in variable x
        for val in self.domains[x]:

            # Assign x overlap letter if overlap position within value length
            if len(val) >= x_pos:
                x_letters[val] = val[x_pos]

        # Determine letters at overlap in variable y values
        y_letters = {}

        # Iterate over values in variable y
        for val in self.domains[y]:

            # Assign y overlap letter if overlap position within value length
            if len(val) >= y_pos:
                y_letters[val] = val[y_pos]

        # If variable x letter not in variable y letters then remove value
        for x_key, x_value in x_letters.items():
            x_present = 0
            for y_value in y_letters.values():
                if x_value == y_value:
                    x_present = 1
                    break
            if x_present == 0:
                self.domains[x].remove(x_key)
                revised = True

        # Return revised
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        # If arcs is None then start with list of all arcs
        if arcs is None:

            # List of all arcs
            arcs = []

            # Check all overlaps (only xy pairs that overlap are arcs)
            overlaps = self.crossword.overlaps

            # Add overlaps to arcs
            for key, value in overlaps.items():
                if (key[1], key[0]) not in arcs and value is not None:
                    arcs.append(key)

        # Enforce arc consistency
        while len(arcs) != 0:
            x_current, y_current = arcs.pop(0)

            if self.revise(x_current, y_current):
                if len(self.domains[x_current]) == 0:
                    return False
                else:
                    for z in self.crossword.neighbors(x_current):
                        if z is not y_current and (x_current, z) not in arcs:
                            arcs.append((x_current, z))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Return false if some variables have no assigned values
        for var in self.domains.keys():
            if var not in assignment.keys():
                return False
            else:
                if assignment[var] is None:
                    return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Values are distinct
        val_list = []
        for val in assignment.values():
            val_list.append(val)
        val_set = set(val_list)
        if len(val_list) != len(val_set):
            return False

        # Values are the correct length
        var_len = 0
        val_len = 0
        for var, val in assignment.items():
            var_len = var.length
            val_len = len(val)
            if var_len != val_len:
                return False

        # No conflicts between neighbors (i.e. overlaps have same letter)
        for var, val in assignment.items():
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                if neighbor in assignment:
                    if val[overlap[0]] != assignment[neighbor][overlap[1]]:
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """

        # Store removed values in count
        count = {val: 0 for val in self.domains[var]}

        # List of unassigned neighbors
        neighbors = [neighbor for neighbor in self.crossword.neighbors(var)
            if neighbor not in assignment]

        # Add number of removed values from count
        for val_var in self.domains[var]:
            for neighbor in neighbors:
                overlap = self.crossword.overlaps[var, neighbor]
                for val_neighbor in self.domains[neighbor]:
                    if val_var[overlap[0]] != val_neighbor[overlap[1]]:
                        count[val_var] += 1

        # Order list and return values
        ordered = sorted(count.items(), key=lambda x: x[1])
        return [x[0] for x in ordered]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        # Unassigned variables
        var_una = [var for var in self.domains if var not in assignment]

        # Variable with the minimum number of values
        num_min = 1000
        var_min = []
        for var in var_una:
            num_var = len(self.domains[var])
            if num_var < num_min:
                num_min = num_var
                var_min.clear()
                var_min.append(var)
            elif num_var == num_min:
                var_min.append(var)

        # If no tie then return variable with minimum number of values
        if len(var_min) == 1:
            return var_min[0]

        # If tie then return variable with highest degree
        elif len(var_min) > 1:
            deg_max = 0
            var_max = []
            for var in var_min:
                deg_var = len(self.crossword.neighbors(var))
                if deg_var > deg_max:
                    deg_max = deg_var
                    var_max.clear()
                    var_max.append(var)
                elif deg_var == deg_max:
                    var_max.append(var)

            # If no tie then return variable with maximum degree
            if len(var_max) == 1:
                return var_max[0]

            # Otherwise return random variables
            else:
                return random.choice(var_una)

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """

        # Return assignment if complete
        if self.assignment_complete(assignment):
            return assignment

        # Otherwise backtrack to complete assignment, assign variable
        var = self.select_unassigned_variable(assignment)

        # Iterate over values for variable
        for val in self.order_domain_values(var, assignment):

            # Add value to variable
            assignment[var] = val

            # If the assignment is consistent
            if self.consistent(assignment):

                # Recursively call backtrack to complete all assignments
                result = self.backtrack(assignment)

                # If result complete then return result
                if result is not None:
                    return result

            # Otherwise remove assignment
            assignment.pop(var)

        # Return None if no solution
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
