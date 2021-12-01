from day_01.source import *
from helpers import current_path, stream_data


def data_stream():
    return cast_data_to_int(stream_data(current_path(__file__)))


print(f"Part one: {compare_measurements(data_stream())}")
print(f"Part two: {compare_measurements(generate_three_measurements(data_stream()))}")
