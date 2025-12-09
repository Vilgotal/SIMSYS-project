import time
import numpy as np

### What to fix
# boundary box around player. 
# different speeds for different players?
# add luggage storing


class Agent:
    def __init__(self, seat = "", spawn = []):

        self.seat = seat        # string 13A
        self.row, self.column_letter = self._parse_seat(seat) # int, string 13, A
        self.layout = "3-3" 
        self.x = spawn[0]
        self.y = spawn[1]
        self.boarding_group = None 
        self.seated = False             
        self.spawned = False            
        self.tinkerobject = None
        self.tinkertext = None
        self.blocked = False
        self.seat_pause = 0
        self.luggage_pause = 0
        self.lug_storage_probability = np.
        

        self.column_map, self.aisle_indices = self._build_column_map()
        self.column_index = self.column_map[self.column_letter] # column int

    def set_boarding_group(self, number):
        self.boarding_group = number
        return self.boarding_group 
    
    def set_tinker_object(self, tinkerobject):
        self.tinkerobject = tinkerobject

    def set_tinker_text(self, tinkertext):
        self.tinkertext = tinkertext

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
            aisle_indices = 3

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
        if direction == "d": return self.x, self.y - 0.5
        if direction == "u": return self.x, self.y + 0.5
        if direction == "l": return self.x - 0.5, self.y
        if direction == "r": return self.x + 0.5, self.y
        raise ValueError("Invalid direction")


    def position(self):
        return (self.x, self.y)

    
    def is_blocked_by_seated(self, other_agents = None):
        """
        direct integer range check between seat column and nearest aisle index
        """

        my_row = self.row
        my_col = self.column_index

        # Minimal fix: säkerställ att aisle behandlas som int och skapa ett konsekvent, exklusivt intervall
        aisle = int(self.aisle_indices)

        if my_col < aisle:
            # exkludera egen kolumn och gångkolumn
            col_range = np.arange(my_col + 1, aisle)
        else:
            col_range = np.arange(aisle + 1, my_col)

        if other_agents:
            for other in other_agents:
                if not other.seated:
                    continue
                elif other.row != my_row:
                    continue
                elif other.column_index in col_range:
                    if abs(other.column_index-aisle) == 1:
                        return 1
                    elif abs(other.column_index-aisle) ==2:
                        return 2
        return 0


    def move(self, other_agents = None): 
        if self.seated:
            if self.x == self.row and self.y == self.column_index:
                ... #print(f"Agent: {self.seat}: agent is seated.")
            else: 
                self.seated = False
        elif self.x == self.row:
            if self.y == self.aisle_indices:
                pass#has luggage, make a paus. then move towards seat?
            if self.y == self.column_index:
                self.seated = True
            elif abs(3 - self.column_index) == 1: # if desired seat is aisle seat, then just sit down, doesn't matter.
                self.y = self.column_index
                self.seated = True
            elif abs(3 - self.column_index) == 2: # if desired seat is middle seat, then if aisle seat is used. paus. Other wise go towards seat. 
                if self.is_blocked_by_seated(other_agents) == 1: # if aisle seat is used.
                    if self.seat_pause < 10:                     # paus first
                        self.seat_pause += 1
                    else:
                        self.y = self.column_index              # then jump to desired seat.
                else:                                           # if aisle seat isn't used.
                    if self.y < self.column_index:
                        self.x, self.y = self._next_position("u")
                    elif self.y > self.column_index:
                        self.x, self.y = self._next_position("d")
                    else:
                        ValueError("error in move. ???!?!?")
            elif abs(3-self.column_index) == 3: # if desired seat is window seat
                if self.is_blocked_by_seated(other_agents) == 1:
                    if self.seat_pause < 2:                     # paus first
                        self.seat_pause += 1
                    else:
                        self.y = self.column_index
                elif self.is_blocked_by_seated(other_agents) == 2:
                    if self.seat_pause < 3:                     # paus first
                        self.seat_pause += 1
                    else:
                        self.y = self.column_index
                else:
                    if self.y < self.column_index:
                        self.x, self.y = self._next_position("u")
                    elif self.y > self.column_index:
                        self.x, self.y = self._next_position("d")
                    else:
                        ValueError("error in move. ???!?!?")
            else: #never a case that should happen
                ValueError("Should never be able to get here.")
        elif self.x < self.row:
            nx, ny = self._next_position("r")
            blocked = False
            for a in other_agents:
                if a.x == nx and a.y == ny:
                    blocked = True
            if not blocked:
                self.x, self.y = nx, ny
        else: 
            ValueError("error in movement to the right.")