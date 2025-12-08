from agent import *





# Parameters
rows = 30
left_col = 3
right_col = 3
pass_per_row = left_col + right_col
test1 = Agent(seat="25C", grid_width = 7, grid_height=30)
test2 = Agent(seat="25A", grid_width=7, grid_height=30)
print(test1.position)

print(test2.aisle_indices)

# Main loop