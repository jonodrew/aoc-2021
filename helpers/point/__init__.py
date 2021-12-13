from helpers.point.point import Point


def construct_point_from_string(coords_string="") -> Point:
    return Point(*map(int, coords_string.split(",")))
