from day_02.source import *
from helpers import current_path, stream_data


def data_stream():
    return stream_data(current_path(__file__))


print(f"Part one: {solve_part_one(data_stream())}")
print(f"Part two: {solve_part_two(data_stream())}")
