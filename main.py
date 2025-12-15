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




methods_list = [Random_order_method, Wilma_method, Btf_method, Modified_block_method, Steffen_method, Reversed_pyramid_method]

methods_steps = []

#Main loop
for f in methods_list:
    steps_list = []
    print(str(f.__name__))
    for i in range(0,20):
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

            time.sleep(0.05)
            visual_system.update_passengers(passenger_list = agents)
            visual_system.root.update_idletasks()
            visual_system.root.update()
            steps += 1
        #visual_system.root.destroy()
        steps_list.append(steps)
    methods_steps.append(steps_list)



method_names = [m.__name__.replace("_", " ").replace("method","") for m in methods_list]


for i, f in enumerate(methods_list):
    data = methods_steps[i]
    mean = np.mean(data)
    err = np.std(data)

    plt.errorbar(
        i, mean, yerr=err,
        fmt='o', capsize=5, label=method_names
    )

# Korrekt sätt att sätta etiketterna
plt.xticks(
    ticks=range(len(methods_list)),
    labels=method_names,
    rotation=-30,fontsize = 10
)

plt.ylabel("Timesteps")
plt.xlabel("Boarding methods")
plt.title("Boarding Time Comparison")
plt.tight_layout()
plt.grid()
plt.show()