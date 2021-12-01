from day_01.source import *
from helpers import current_path, stream_data


def data_stream():
    return cast_data_to_int(stream_data(current_path(__file__)))


print(solve_part_one(data_stream()))
print(solve_part_two(data_stream()))
