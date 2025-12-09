from agent import *
import scipy as sci
import time
from Visual import Visuals
import random
from boarding_methods import *

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



# Parameterss
rows = 30 
left_col = 3
right_col = 3
column = left_col + right_col



# n_passengers = column * rows
spawn_loc = [0, 3]

seats = generate_manifest(rows, left_col, right_col)




question = True
while question:
    print("Press 1+ enter to simulate Wilma method")
    print("Press 2 + enter to simulate Steffen method")
    method = int(input('Which method do you want to simulate?'))

    if method == 1:
        agents = wilma_method_seatinput(seats,spawn_loc)
        question = False
    elif method == 2:
        agents = steffen_method(seats,spawn_loc)
        quesiotn = False

    else: 
        print("wrong input you need to press 1 or 2!")


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

    time.sleep(0.3)
    visual_system.update_passengers(passenger_list = agents)
    visual_system.root.update_idletasks()
    visual_system.root.update()




visual_system.root.update_idletasks()
visual_system.root.update()
visual_system.root.mainloop()