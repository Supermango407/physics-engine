import math


def distance_between(start_position: list[float, float], end_position: list[float, float]) -> float:
    """
    get the distance from one point in to another. (2D only)

    :param start_position: first point
    :param end_position: second point
    :return: distance between
    """
    return math.hypot(start_position[0]-end_position[0], start_position[1]-end_position[1])


def in_triangle(p: list[float, float], a: list[float, float],
                b: list[float, float], c: list, threshold=0.001) -> bool:
    """
    tell if a given point is in triangle. (2D only)

    :param p: point checking
    :param a: triangle point
    :param b: triangle point
    :param c: triangle point
    :param threshold: how much to round by.
    :return:  True if point p is in triangle abc, otherwise returns false
    """
    full_area = triangle_area(a, b, c)

    area1 = triangle_area(p, a, b)
    area2 = triangle_area(p, b, c)
    area3 = triangle_area(p, a, c)

    # print([full_area, area1 + area2 + area3])

    if full_area-threshold <= area1 + area2 + area3 <= full_area+threshold:
        return True
    else:
        return False


def triangle_area(a: list[float, float], b: list[float, float],
                  c: list[float, float]) -> float:
    """
    gets the area of triangle abc. (2D only)

    :param a: triangle point 1
    :param b: triangle point 2
    :param c: triangle point 3
    :return: area
    """
    return math.fabs((a[0]*(b[1]-c[1]) + b[0]*(c[1]-a[1]) + c[0]*(a[1]-b[1]))/2.0)


def lines_intersects(line1: list[list[float, float], list[float, float]],
                     line2: list[list[float, float], list[float, float]]) -> bool:
    """
    get whether two points intersect on the coordinate plane. (2D only)
    :param line1: the first line.
    :param line2: the second line.
    :return: Returns True if the intersect, Returns False if they don't.
    """
    if (orientation(line1[0], line1[1], line2[0]) != orientation(line1[0], line1[1], line2[1])) and \
            (orientation(line2[0], line2[1], line1[0]) != orientation(line2[0], line2[1], line1[1])):
        return True
    else:
        return False


def orientation(p1: list[float, float], p2: list[float, float], p3: list[float, float]) -> int:
    """
    tells whether triangle p1, p2, p3(ORDER MATTERS), is clock wise or counter clockwise. (2D only)

    :param p1: first point
    :param p2:  first point
    :param p3:  first point
    :return: 1 if triangle is clockwise, -1 if triangle is counterclockwise.
    """
    val = ((p2[1]-p1[1]) * (p3[0]-p2[0]) - ((p2[0]-p1[0]) * (p3[1]-p2[1])))

    if val > 0:
        return 1
    else:
        return -1


def angle_of_line(start_position: list[float, float], end_position: list[float, float]) -> float:
    """
    get the rotation of a line, defined by start_position and end_position(ORDER MATTERS). (2D only)

    :param start_position: starting point of line
    :param end_position: end point of line
    :return: angle in radians
    """
    return math.atan2(start_position[0]-end_position[0], start_position[1]-end_position[1])
