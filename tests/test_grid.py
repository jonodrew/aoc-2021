from helpers.grid import theoretical_cardinal_neighbour_coords


def test_theoretical_cardinal_neighbour_coords():
    neighbour_coords = list(theoretical_cardinal_neighbour_coords((0, 0)))
    assert len(neighbour_coords) == 4
