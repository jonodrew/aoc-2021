from day_04.bingo_functions import (
    parse_data,
    solve_bingo_part_two,
    solve_bingo_part_one,
)

print(f"Part one: {solve_bingo_part_one(parse_data('./'))}")
print(f"Part two: {solve_bingo_part_two(parse_data('./'))}")
