from agent import *
import scipy as sci
import time
from Visual import Visuals
import random
from boarding_methods import *
import matplotlib.pyplot as plt

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




# question = True
# while question:
#     print("Press 1+ enter to simulate Wilma method")
#     print("Press 2 + enter to simulate Steffen method")
#     print("Press 3 + enter to simulate Back-to-Front method")
#     method = int(input('Which method do you want to simulate?'))

#     if method == 1:
#         agents = wilma_method_seatinput(seats,spawn_loc)
#         question = False
#     elif method == 2:
#         agents = steffen_method(seats,spawn_loc)
#         question = False
#     elif method == 3:
#         agents = btf_method(seats,spawn_loc)
#         question = False

#     else: 
#         print("wrong input you need to press 1 or 2!")

# WILMA, BTF, RANDOM, STEFFEN METHOD
methods_list = [wilma_method, vilgot_method, random_order_method, wilma_method, btf_method, steffen_method]

methods_steps = []

#Main loop
for f in methods_list:
    steps_list = []
    print(str(f.__name__))
    for i in range(0,10):
        agents = f(seats,spawn_loc)
        visual_system = Visuals(rows, column, amount_of_ailes=1, method_name = f.__name__, corridor_row=1)
        visual_system.update_passengers(passenger_list = agents)
        visual_system.draw_grid()
        steps = 0
            
        while not all(a.seated for a in agents):
            # sortera så att agenter närmast gången flyttas först.
            # Om lägre x betyder närmare gången: använd key=lambda p: p.x
            # Om omvänt, använd key=lambda p: -p.x
            agents.sort(key=lambda p: p.x)

            for i, a in enumerate(agents):
                visual_system.canvas.delete(a.tinkerobject, a.tinkertext)
                others = agents[:i] + agents[i+1:]
                a.move(other_agents = others)

            time.sleep(0.04)
            visual_system.update_passengers(passenger_list = agents)
            visual_system.root.update_idletasks()
            visual_system.root.update()
            steps += 1
        visual_system.root.destroy()
        steps_list.append(steps)
    methods_steps.append(steps_list)

means = []
errors = []

for i, f in enumerate(methods_list):
    # data = methods_steps[i]
    # means.append(np.mean(data))
    # errors.append(np.std(data))   # or std/np.sqrt(n) for SEM
    data = methods_steps[i]
    mean = np.mean(data)
    err = np.std(data)

    plt.errorbar(
        i, [mean], yerr=[err],
        fmt='o', capsize=5, label=f.__name__
    )
    
# x = range(len(methods_list))

# plt.errorbar(x, means, yerr=errors, fmt='o', capsize=5)
# plt.xticks(x, methods_list)
# plt.xlabel("Boarding Method")
# plt.ylabel("Timesteps")
# plt.title("Boarding Time Comparison")
# plt.show()


plt.xticks([])  # no x-axis labels
plt.ylabel("Timesteps")
plt.title("Boarding Time Comparison")
plt.legend(loc="best")
plt.show()