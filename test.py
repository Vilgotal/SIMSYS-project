from agent import * 
import random

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

rows = 10
left_col = right_col = 3


def wilma_method_seatinput(seats):
    agents = [Agent(seat, spawn_loc) for seat in seats]
    priority = {
        0: 0, 6: 0,
        1: 1, 5: 1,
        2: 2, 4: 2}

    agents.sort(key=lambda p: (priority.get(p.column_index, 3), random.random()))
    return agents


spawn_loc = [0, 3] 


manifest = generate_manifest(rows, left_col, right_col)
wm = wilma_method_seatinput(manifest)

for i in wm:
    print(i.seat)