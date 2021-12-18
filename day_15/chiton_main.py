from day_15.chiton import gen_reference_grid, dijkstras_algorithm


def main():
    return dijkstras_algorithm(gen_reference_grid(), 5).cost

main()
