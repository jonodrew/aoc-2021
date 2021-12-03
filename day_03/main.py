import day_03.functions as functions
from helpers import stream_data, current_path

print(
    f"Part one: {functions.solve_part_one(functions.gamma_rate(stream_data(current_path(__file__))), functions.epsilon_rate)}"
)
print(f"Part two: {functions.solve_part_two(stream_data(current_path(__file__)))}")
