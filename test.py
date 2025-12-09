import numpy as np

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
            print(f"Agent: {self.seat}: agent is seated.")
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
                if self.seat_pause < 2:                     # paus first
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
                if self.seat_pause < 3:                     # paus first
                    self.seat_pause += 1
                else:
                    self.y = self.column_index
            elif self.is_blocked_by_seated(other_agents) == 2:
                if self.seat_pause < 4:                     # paus first
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
            if a.x == nx and a.ny == ny:
                blocked = True
        if not blocked:
            self.x, self.y = nx, ny
    else: 
        ValueError("error in movement to the right.")



        # else:
        #     if abs(self.y - self.column_index) == 1:
        #         self.y = self.column_index
        #         self.seated = True
        #     elif self.is_blocked_by_seated(other_agents) == 1:
        #         if paus < 1:
        #             paus += 1
        #         else:
        #             self.y = self.column_index
        #             self.seated = True
                
        #     elif self.is_blocked_by_seated(other_agents) == 2:
        #         if paus < 2:
        #             paus += 1
        #         else:
        #             self.y = self.column_index
        #             self.seated = True
        #     else: 
        #         if self.y < self.column_index:
        #             self.x, self.y = self._next_position("u")
        #         elif self.y > self.column_index:
        #             self.x, self.y = self._next_position("d")
    


            # först titta var agent is seated. 
            # sitter personen i aisle seat och det är ledigt, så är det bara att sätta sig. 
            # sitter den i middle seat, checka ifall aisle seat är ledigt. gå isåfall dit
            
    elif self.x < self.row:


        if self.seated == True:
            print(f"Agent: {self.seat}: agent is seated.")
            return False
        else:
            nx, ny = self._next_position("r")
            for a in other_agents:
                if a is self: #lagt till
                    continue #lagt till
                if a.x == nx and a.y == ny:
                    print(f"Blocked py agent {a.seat}")
                    self.blocked = True
            if self.blocked:
                self.blocked = False
                return self.blocked
            else:
                if nx <= self.row:
                    print(f"Agent: {self.seat}: moves forward")
                    #time.sleep(0.5)
                    self.x = nx
                    self.blocked = False #Lagt till
                    print(f"Agent: {self.seat}: curr pos: {self.x}")
                    return
                elif self.x == self.row or nx == self.row:
                    if self.is_blocked_by_seated(other_agents)==True:
                        print(f"Agent: {self.seat}: Person sitting in the way, taking a little longer to be seated.")
                        #time.sleep(5)
                        print(f"Agent {self.seat}: seated.")
                        self.y = self.column_index
                        print(f"Agent: {self.seat}: curr pos: {self.x}, {self.y}")
                        self.seated = True
                        self.blocked = False
                        return
                    else:
                        if self.y <= self.column_index:
                            nx, ny = self._next_position("u")

                        else:# self.y >= self.column_index:
                            nx, ny = self._next_position("d")
                        print(f"Agent: {self.seat}: No one is sitting in the way, taking a seat.")
                        #time.sleep(1)
                        print(f"Agent {self.seat}: seated.")
                        self.y = ny
                        self.blocked = False
                        print(f"Agent: {self.seat}: curr pos: {self.x}, {self.y}")
                        if self.y == self.column_index:
                            self.seated = True
                else:
                    raise SyntaxError("Something wrong in Agent.move()")
                