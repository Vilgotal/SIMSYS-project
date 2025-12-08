from agent import *
import scipy as sci
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
agents = [Agent(seat, spawn_loc) for seat in manifest]

# Main loop


window = ["A", "F"]
middle = ["B", "E"]
aisle  = ["C", "D"]

# 1. Generate all agents
agents = [
    Agent(f"{row}{L}")
    for row in range(1, rows + 1)
    for L in (window + middle + aisle)
]

# 2. Assign boarding groups (lower number boards first)
for a in agents:
    if a.column_letter in window:
        a.set_boarding_group(1)
    elif a.column_letter in middle:
        a.set_boarding_group(2)
    else:
        a.set_boarding_group(3)

# 3. Sort agents by boarding group (and optionally row)
agents.sort(key=lambda a: (a.boarding_group, a.row))
