from agent import *
import random

# Could implement a probability creating outliers for the boarding methods. like if probability < certain noise,


def wilma_method(seats,spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    priority = {
        0: 0, 6: 0,
        1: 1, 5: 1,
        2: 2, 4: 2}
    for a in agents:
        a.boarding_group = priority.get(a.column_index, 3)
    agents.sort(key=lambda p: (p.boarding_group, random.random()))
    return agents

def get_priority(num):
    return (num - 1) // 5

def btf_method(seats,spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    max_seat = agents[-1].row #33
    priority = {
        0: 5, 3: 2,
        1: 4, 4: 1,
        2: 3, 5: 0}
    for a in agents:
        a.boarding_group = priority.get(get_priority(a.row), 6)
    agents.sort(key=lambda p: (p.boarding_group, random.random()))
    return agents

def random_order_method(seats, spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    agents.sort(key=lambda _: random.random())
    return agents

def hugo_method(seats, spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    max_seat = agents[-1].row
    priority_col = {
        0: 0, 6: 0,
        1: 1, 5: 1,
        2: 2, 4: 2}
    priority = {
        (0,0): 1, (1,0): 2, (2,0): 3,
        (0,1): 1, (1,1): 2, (2,1): 3,
        (0,2): 1, (1,2): 2, (2,2): 3,
        (0,3): 0, (1,3): 2, (2,3): 3,
        (0,4): 0, (1,4): 1, (2,4): 2,
        (0,5): 0, (1,5): 0, (2,5): 1,
        (0,6): 0, (1,6): 0, (2,6): 1,
        }
    for a in agents: 
        a.boarding_group = priority.get((priority_col.get(a.column_index), (a.row - 1) // 6), 4)
    agents.sort(key=lambda p: (p.boarding_group, random.random()))
    return agents

def vilgot_method(seats,spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]


    inner_third = [agents[-1].row,agents[-1].row-agents[-1].row//3]
    middle_third = [inner_third[-1],inner_third[-1]-agents[-1].row//3]
    closest_third = [middle_third[-1],middle_third[-1]-agents[-1].row//3]

    inner_third = np.arange(int(inner_third[0]),int(inner_third[1]),-1)
    middle_third = np.arange(int(middle_third[0]),int(middle_third[1]),-1)
    closest_third = np.arange(int(closest_third[0]),int(closest_third[1]),-1)


    for a in agents:
        if a.row in inner_third:
            if a.column_index <3:
                a.boarding_group = 0
            else:
                a.boarding_group = 2

        if a.row in middle_third:
            if a.column_index<3:
                a.boarding_group = 4
            else:
                a.boarding_group = 1

        if a.row in closest_third:
            if a.column_index<3:
                a.boarding_group = 3
            else:
                a.boarding_group = 5

    agents.sort(key=lambda p: (p.boarding_group, random.random()))
    return agents

#### Not working right now
# def reversed_pyramid_method(seats, spawn_loc):
#     agents = [Agent(seat, spawn_loc) for seat in seats]

#     # column groups: 0=window, 1=middle, 2=aisle (same idea as WILMA)
#     col_priority = {
#         0: 0, 6: 0,   # windows
#         1: 1, 5: 1,   # middle
#         2: 2, 4: 2,   # aisle
#     }

#     max_row = max(a.row for a in agents)

#     def row_zone(row):
#         # split cabin into 3 zones
#         if row > max_row * 2 / 3:
#             return 0  # back
#         elif row > max_row / 3:
#             return 1  # middle
#         else:
#             return 2  # front

#     for a in agents:
#         zone = row_zone(a.row)
#         col = col_priority.get(a.column_index, 2)
#         a.boarding_group = zone * 2 + min(col, 1)  # 6 groups total

#     agents.sort(key=lambda p: (p.boarding_group, random.random()))
#     return agents


def steffen_method(seats,spawn_loc):
    left_window_odd_seats = []
    left_window_even_seats = []

    right_window_odd_seats = []
    right_window_even_seats = []

    left_middle_odd_seats = []
    left_middle_even_seats = []

    right_middle_odd_seats = []
    right_middle_even_seats = []

    left_aisle_odd_seats = []
    left_aisle_even_seats = []

    right_aisle_even_seats = []
    right_aisle_odd_seats = []

    counter = 0
    for i in seats:
        row = int(i[:-1])
        seat_letter = i[-1]

        #Check if the row is odd or even to determine where the agent goes
        is_odd_row = (row % 2 == 1)

        # window seats, labled with A and F 
        if seat_letter in ("A", "F"):
            if is_odd_row:
                if seat_letter == "A":
                    left_window_odd_seats.append(i)
                elif seat_letter == "F":
                    right_window_odd_seats.append(i)
            else:
                if seat_letter == "A":
                    left_window_even_seats.append(i)
                elif seat_letter == "F":
                    right_window_even_seats.append(i)

        # Middle seats has the letter B and E
        elif seat_letter in ("B", "E"):
            if is_odd_row:
                if seat_letter == "B":
                    left_middle_odd_seats.append(i)
                elif seat_letter == "E":
                    right_middle_odd_seats.append(i)
            else:
                if seat_letter == "B":
                    left_middle_even_seats.append(i)
                elif seat_letter == "E":
                    right_middle_even_seats.append(i)

        # Aisle seats had C and D
        elif seat_letter in ("C", "D"):
            if is_odd_row:
                if seat_letter == "C":
                    left_aisle_odd_seats.append(i)
                elif seat_letter == "D":
                    right_aisle_odd_seats.append(i)
            else:
                if seat_letter == "C":
                    left_aisle_even_seats.append(i)
                elif seat_letter == "D":
                    right_aisle_even_seats.append(i)
        counter += 1


    merged_list_window = (list(reversed(right_window_odd_seats)) + list(reversed(left_window_odd_seats)) + list(reversed(right_window_even_seats)) + list(reversed(left_window_even_seats)))

    merged_list_middle = (list(reversed(right_middle_odd_seats)) + list(reversed(left_middle_odd_seats)) + list(reversed(right_middle_even_seats)) + list(reversed(left_middle_even_seats)))

    merged_list_aisle = (list(reversed(right_aisle_odd_seats)) + list(reversed(left_aisle_odd_seats)) + list(reversed(right_aisle_even_seats)) + list(reversed(left_aisle_even_seats)))

    merged_list = merged_list_window + merged_list_middle + merged_list_aisle
    agents = [Agent(seat, spawn_loc) for seat in merged_list]
    return agents