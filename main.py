from agent import *
import scipy as sci
import time
from Visual import Visuals
def generate_manifest(rows, left_col, right_col):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # left block: A, B, C
    left = [letters[i] for i in range(left_col)]

    # right block: next letters: D, E, F
    right = [letters[i + left_col] for i in range(right_col)]

    all_letters = left + right

    manifest = []
    for r in range(1, rows + 1):
        for L in all_letters:
            manifest.append(f"{r}{L}")

    return manifest



def steffen_method(rows,left_col,right_col):
    seats = generate_manifest(rows,left_col,right_col)

    left_window_odd_seats = []
    left_window_even_seats = []

    right_window_odd_seats = []
    right_window_even_seats = []


    left_middle_odd_seats = []
    left_middle_even_seats = []

    right_middle_odd_seats = []
    right_middle_even_seats = []

    left_aisle_odd_seats = []
    right_aisle_even_seats = []

    counter = 0
    for i in seats:
        #window seats, and also check even or odd number
        if counter == 0 or counter%6 == 0:
            if counter%2 ==0:
                if "A" in i:
                    left_window_even_seats.append(i)
                elif "F" in i:
                    right_window_even_seats.append(i)
                else: print("Seems to be wrong in the even window seating")
            else:
                if "A" in i:
                    left_window_odd_seats.append(i)
                elif "F" in i:
                    right_window_odd_seats.append(i)
                else: print("Seems to be wrong in the odd window seating")


        #Middle seats, and also check even or odd number
        if counter == 1 or (counter-1)%6==0:
            if counter%2 ==0:
                if "B" in i:
                    left_middle_even_seats.append(i)
                elif "E" in i:
                    right_middle_even_seats.append(i)
                else:
                    print("No B or E in middle even seats")
            else:
                if "B" in i:
                    left_window_odd_seats.append(i)
                elif "E" in i:
                    right_window_odd_seats.append(i)
                else:    
                    print("No B or E in middle odd seats")



            if "B" in i:
                left_middle_seats.append(i)
            else:
                right_middle_seats.append(i)
        if counter ==2 or counter-2%6 == 0:
            if "C" in i:
                left_aisle_seats.append(i)
            else:
                right_aisle_seats.append(i)
    merged_list = left_window_seats+right_window_seats+        

    



    return

# Parameterss
rows = 10
left_col = 3
right_col = 3
column = left_col + right_col
n_passengers = column * rows
spawn_loc = [0, 3]



manifest = generate_manifest(rows, left_col, right_col)
agents = [Agent(seat, spawn_loc) for seat in manifest]


import random

agents.sort(key=lambda p: (-p.row, random.random()))

#Main loop


visual_system = Visuals(rows, column, amount_of_ailes=1, corridor_row=1, ailes_width=1)
visual_system.update_passengers(passenger_list = agents)
visual_system.draw_grid()
not_all_seated = True
while not_all_seated:
    # sortera så att agenter närmast gången flyttas först.
    # Om lägre x betyder närmare gången: använd key=lambda p: p.x
    # Om omvänt, använd key=lambda p: -p.x
    agents.sort(key=lambda p: p.x)

    for i, a in enumerate(agents):
        visual_system.canvas.delete(a.tinkerobject, a.tinkertext)
        others = agents[:i] + agents[i+1:]
        a.move(other_agents = others)

    time.sleep(0.5)
    visual_system.update_passengers(passenger_list = agents)
    visual_system.root.update_idletasks()
    visual_system.root.update()



visual_system.root.update_idletasks()
visual_system.root.update()
visual_system.root.mainloop()