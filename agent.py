import time
class Agent:
    def __init__(self, seat, x=-3, y=3):

        self.seat = seat # string
        self.row, self.column_letter = self._parse_seat(seat) # int, string
        self.layout = "3-3"
        self.x = x
        self.y = y
        self.boarding_group = 0
        self.seated = False

        # build column mapping with aisles included
        self.column_map, self.aisle_indices = self._build_column_map()
        self.column_index = self.column_map[self.column_letter] # column int

    def set_boarding_group(self, number):
        self.boarding_group = number
        return self.boarding_group 

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
        if direction == "u": return self.x, self.y - 1
        if direction == "d": return self.x, self.y + 1
        if direction == "l": return self.x - 1, self.y
        if direction == "r": return self.x + 1, self.y
        raise ValueError("Invalid direction")

    def is_occupied(self, x, y):
        return (x, y) in self.occupied

    def move(self, other_agents = None):
        
        if self.seated == True:
            print(f"Agent: {self.seat}: agent is seated.")
            return False
        else:
            self.x, self.y = self._next_position("r")
            if self.x < self.row:
                print(f"Agent: {self.seat}: moves forward")
                self.x = nx
                print(f"Agent: {self.seat}: curr pos: {self.x}")
                return True
            elif self.x == self.row:
                if self.is_blocked_by_seated(other_agents):
                    print(f"Agent: {self.seat}: Person sitting in the way, taking a little longer to be seated.")
                    time.sleep(5)
                    print(f"Agent {self.seat}: seated.")
                    return False
                else:
                    print(f"Agent: {self.seat}: No one is sitting in the way, taking a seat.")
                    time.sleep(1)
                    print(f"Agent {self.seat}: seated.")
                    self.x = nx
                    self.y = ny
                    self.seated = True
                    return True
            else:
                raise SyntaxError("Fel i Agent.move()")

    def position(self):
        return (self.x, self.y)

    def is_blocked_by_seated(self, other_agents = list):
        """
        direct integer range check between seat column and nearest aisle index
        """

        my_row = self.row
        my_col = self.column_index


        if my_col < self.aisle_indices:
            col_range = range(my_col, int(self.aisle_indices))
        else:
            col_range = range(self.aisle_indices+1, my_col)

        for other in other_agents:
            if not other.seated:
                continue
            if other.row != my_row:
                continue
            if other.column_index in col_range:
                return True

        return False
