import copy

class InvalidMoveError(Exception):
    """Custom exception for invalid moves in the puzzle."""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

class PuzzleSolver:
    """Class for solving puzzles with cells and dot-based link rules."""
    
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def fill_x_around_completed_cells(self, row, col):
        """Fill 'x' in slots around cells when link quota is met."""
        cell_value = self.puzzle.get_value(row, col)
        if cell_value != ' ':
            required_links = int(cell_value)
            links_count = self.puzzle.count_links(row, col)
            x_count = self.puzzle.count_xes(row, col)

            if links_count == required_links and links_count + x_count != 4:
                self._fill_x_around(row, col)

    def dot_link_rules(self, row, col):
        """Ensure dots have exactly zero or two links."""
        links_count = self.puzzle.count_links(row, col)
        x_count = self.puzzle.count_xes(row, col)

        if links_count == 2 and x_count < 2:
            self._fill_x_around(row, col)
        elif x_count == 2 and links_count == 1:
            self._fill_remaining_with_links(row, col)
        elif x_count == 3:
            self._fill_x_around(row, col)

    def enforce_cell_link_rules(self, row, col):
        """If cell's remaining spaces match its link quota, fill them with links."""
        cell_value = self.puzzle.get_value(row, col)
        if cell_value != ' ':
            required_links = int(cell_value)
            links_count = self.puzzle.count_links(row, col)
            x_count = self.puzzle.count_xes(row, col)

            if links_count < required_links and 4 - x_count == required_links:
                self._fill_remaining_with_links(row, col)

    def handle_adjacent_threes(self, row, col):
        """Handle adjacent '3' cells, enforce valid link placements."""
        if self.puzzle.get_value(row, col) != '3':
            return

        next_row = row + 2
        next_col = col + 2

        if next_row < self.puzzle.height and self.puzzle.get_value(next_row, col) == '3':
            self._enforce_vertical_links(row, col)
        elif next_col < self.puzzle.width and self.puzzle.get_value(row, next_col) == '3':
            self._enforce_horizontal_links(row, col)

    def _fill_x_around(self, row, col):
        """Fill 'x' in all surrounding slots."""
        self.puzzle.cond_set_x(row - 1, col)
        self.puzzle.cond_set_x(row + 1, col)
        self.puzzle.cond_set_x(row, col - 1)
        self.puzzle.cond_set_x(row, col + 1)

    def _fill_remaining_with_links(self, row, col):
        """Fill remaining empty slots around a dot with links."""
        self.puzzle.cond_set_link(row - 1, col, '|')
        self.puzzle.cond_set_link(row + 1, col, '|')
        self.puzzle.cond_set_link(row, col - 1, '-')
        self.puzzle.cond_set_link(row, col + 1, '-')

    def _enforce_vertical_links(self, row, col):
        """Enforce links for vertically adjacent cells."""
        self.puzzle.cond_set_link(row - 1, col, '|')
        self.puzzle.cond_set_link(row + 1, col, '|')

    def _enforce_horizontal_links(self, row, col):
        """Enforce links for horizontally adjacent cells."""
        self.puzzle.cond_set_link(row, col - 1, '-')
        self.puzzle.cond_set_link(row, col + 1, '-')


class PuzzleBoard:
    """Puzzle board that handles the state of the puzzle."""
    
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.board = [[' ' for _ in range(width)] for _ in range(height)]

    def get_value(self, row, col):
        """Get the value at a specific row and column."""
        return self.board[row][col] if 0 <= row < self.height and 0 <= col < self.width else None

    def count_links(self, row, col):
        """Count how many links are adjacent to a cell or dot."""
        return sum([1 for r, c in self._get_adjacent(row, col) if self.get_value(r, c) in ['-', '|']])

    def count_xes(self, row, col):
        """Count how many 'x' are adjacent to a cell or dot."""
        return sum([1 for r, c in self._get_adjacent(row, col) if self.get_value(r, c) == 'x'])

    def cond_set_x(self, row, col):
        """Conditionally set 'x' at a cell if it's empty."""
        if self.get_value(row, col) == ' ':
            self.board[row][col] = 'x'

    def cond_set_link(self, row, col, link_type):
        """Conditionally set a link (either '-' or '|') at a specific location."""
        if self.get_value(row, col) == ' ':
            self.board[row][col] = link_type

    def _get_adjacent(self, row, col):
        """Return a list of coordinates for adjacent cells."""
        return [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]


puzzle = PuzzleBoard(5, 5)
solver = PuzzleSolver(puzzle)

solver.fill_x_around_completed_cells(2, 2)
