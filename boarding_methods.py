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
    agents.sort(key=lambda p: (priority.get(p.column_index, 3), random.random()))
    return agents

def get_priority(num):
    return (num - 1) // 5

def btf_method(seats,spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    max_seat = agents[-1].row
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