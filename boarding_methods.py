from agent import *
import random

def wilma_method_seatinput(seats,spawn_loc):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    priority = {
        0: 0, 6: 0,
        1: 1, 5: 1,
        2: 2, 4: 2}
    for a in agents:
        a.boarding_group = priority.get(a.column_index, 3)
    agents.sort(key=lambda p: (priority.get(p.column_index, 3), random.random()))
    return agents

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


    merged_list_window = (right_window_odd_seats + left_window_odd_seats + right_window_even_seats + left_window_even_seats)

    merged_list_middle = (right_middle_odd_seats + left_middle_odd_seats + right_middle_even_seats + left_middle_even_seats)

    merged_list_aisle = (right_aisle_odd_seats + left_aisle_odd_seats + right_aisle_even_seats + left_aisle_even_seats)

    merged_list = merged_list_window + merged_list_middle + merged_list_aisle
    agents = [Agent(seat, spawn_loc) for seat in merged_list]
    return agents