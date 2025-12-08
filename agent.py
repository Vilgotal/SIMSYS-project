class Agent:
    def __init__(self, seat, layout="3-3", x=0, y=0,
                 grid_width=None, grid_height=None, occupied=None):

        self.seat = seat
        self.row, self.column_letter = self._parse_seat(seat)
        self.layout = layout

        self.x = x
        self.y = y
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.occupied = occupied if occupied is not None else set()

        self.seated = False

        # build column mapping with aisles included
        self.column_map, self.aisle_indices = self._build_column_map()
        self.column_index = self.column_map[self.column_letter]

    def _parse_seat(self, seat):
        num = ""
        letter = ""
        for ch in seat:
            if ch.isdigit():
                num += ch
            else:
                letter += ch.upper()
        if not num or not letter:
            raise ValueError("Invalid seat format")
        return int(num), letter

    def _build_column_map(self):
        """
        Produces seat-letter → index mapping including aisle positions.
        Also returns the aisle index/indices.
        """

        if self.layout == "3-3":
            letters = ["A","B","C","D","E","F"]
            # Aisle between C and D → aisle index = 3
            col_map = {letters[i]: i + (1 if i >= 3 else 0) for i in range(6)}
            aisle_indices = {3}

        elif self.layout == "3-3-3":
            letters = ["A","B","C","D","E","F","G","H","I"]
            # Two aisles: after C and after F
            # insert +1 after D-F block, +2 after A-C
            col_map = {}
            for i, L in enumerate(letters):
                if i <= 2:            # A B C
                    col_map[L] = i
                elif 3 <= i <= 5:     # D E F
                    col_map[L] = i + 1   # after aisle1
                else:                 # G H I
                    col_map[L] = i + 2   # after aisle2

            aisle_indices = {3, 7}

        else:
            raise ValueError("Unsupported layout")

        return col_map, aisle_indices

    def _next_position(self, direction):
        if direction == "up": return self.x, self.y - 1
        if direction == "down": return self.x, self.y + 1
        if direction == "left": return self.x - 1, self.y
        if direction == "right": return self.x + 1, self.y
        raise ValueError("Invalid direction")

    def is_occupied(self, x, y):
        return (x, y) in self.occupied

    def move(self, direction):
        nx, ny = self._next_position(direction)

        if self.grid_width is not None and not (0 <= nx < self.grid_width):
            return False
        if self.grid_height is not None and not (0 <= ny < self.grid_height):
            return False
        if self.is_occupied(nx, ny):
            return False

        self.x, self.y = nx, ny
        return True

    def position(self):
        return self.x, self.y

    def is_blocked_by_seated(self, other_agents):
        """
        direct integer range check between seat column and nearest aisle index
        """

        my_row = self.row
        my_col = self.column_index

        # nearest aisle
        nearest_aisle = min(self.aisle_indices, key=lambda a: abs(a - my_col))

        if my_col < nearest_aisle:
            col_range = range(my_col + 1, nearest_aisle)
        else:
            col_range = range(nearest_aisle + 1, my_col)

        for other in other_agents:
            if not other.seated:
                continue
            if other.row != my_row:
                continue
            if other.column_index in col_range:
                return True

        return False
