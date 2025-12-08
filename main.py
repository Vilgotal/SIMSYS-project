from agent import *
import scipy as sci
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




# Parameterss
rows = 30
left_col = 3
right_col = 3
pass_per_row = left_col + right_col
n_passengers = pass_per_row * rows
spawn_loc = [-3, 3]



manifest = generate_manifest(rows, left_col, right_col)
#agents = [Agent(seat, spawn_loc) for seat in manifest]

test1 = Agent(seat = "13B", spawn = [0,3])

# Main loop


visual_system = Visuals(rows=30, columns=6, amount_of_ailes=1, ailes_width=1)
visual_system.update(passengers = [test1])

