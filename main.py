from agent import *





# Parameterss
rows = 30
left_col = 3
right_col = 3
pass_per_row = left_col + right_col
test1 = Agent(seat="25C")
test2 = Agent(seat="25A")

test1.move([test2])

print(test1.position)
print(test2.aisle_indices)

# Main loop