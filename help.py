import math


class Line(object):
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point

    def center(self) -> list[float, float]:
        """returns the center of the line."""
        x = (self.start_point[0] + self.end_point[0])/2
        y = (self.start_point[1] + self.end_point[1])/2
        return [x, y]

    def length(self) -> float:
        """returns the length of the line."""
        return distance_between(self.start_point, self.end_point)

    def radius(self) -> float:
        """returns half the length of the line."""
        return distance_between(self.start_point, self.end_point)/2

    def angle(self) -> float:
        """returns the angle between the line and the y axis(angled up), in radians."""
        return angle_of_line(self.start_point, self.end_point)

    def slope(self) -> float:
        """returns the slope of the line."""
        x = self.start_point[0] - self.end_point[0]
        y = self.start_point[1] - self.end_point[1]

        if x == 0:
            print("Invalid Slope")
            return math.inf
        else:
            return y / x

    def y_intercept(self) -> float:
        """returns where a infinite line would cross the y axis."""
        return self.start_point[1] - self.slope()*self.start_point[0]

    def scaled_line(self, multiplier: float) -> list[list[float, float], list[float, float]]:
        """
        returns the start and end points of a copy of the line, multiplied by a given value.
        :param multiplier: the amount to multiply by.
        """
        start = [self.start_point[0] - self.center()[0], self.start_point[1] - self.center()[1]]
        end = [self.end_point[0] - self.center()[0], self.end_point[1] - self.center()[1]]

        start[0] *= multiplier
        start[1] *= multiplier
        end[0] *= multiplier
        end[1] *= multiplier

        start[0] += self.center()[0]
        start[1] += self.center()[1]
        end[0] += self.center()[0]
        end[1] += self.center()[1]

        return [start, end]

    def flip_line(self):
        """sets the start_point of the line to the end_point, and the end_point to the start_point."""
        start = self.start_point
        self.start_point = self.end_point
        self.end_point = start

    def list(self) -> list[list[float, float], list[float, float]]:
        """returns the start and end points of the line as a list."""
        return [self.start_point, self.end_point]


def distance_between(start_position: list[float, float], end_position: list[float, float]) -> float:
    """
    get the distance from one point in to another. (2D only)

    :param start_position: first point
    :param end_position: second point
    :return: distance between
    """
    return math.hypot(start_position[0]-end_position[0], start_position[1]-end_position[1])


def mount(x, scale):
    """a function that when graphed looks like a mountain range. (don't know the actual name of function)"""
    return math.fabs(x % (2*scale) - scale)


def semi_circle_curve(x, r=1.0):
    """a function that when graphed looks like a half a circle."""
    if -r <= x <= r:
        return r-math.sqrt(r**2 - x**2)
    else:
        return 0


def rotate_point_around(point: list[float, float], anchor: list[float, float], angle: float) -> list[float, float]:
    """
    returns a copy of a point rotated around another, by given angle.
    :param point: point rotation.
    :param anchor: point rotating around.
    :param angle: the amount rotated by in radians.
    :return:
    """
    x, y = [point[0] - anchor[0], point[1] - anchor[1]]
    sin = math.sin(angle)
    cos = math.cos(angle)
    new_x = x*cos - y*sin
    new_y = x*sin + y*cos

    return[new_x+anchor[0], new_y+anchor[1]]


def point_in_triangle(p: list[float, float], a: list[float, float],
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
    get whether two lines intersect on the coordinate plane. (2D only)
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


def line_to_point_distance(line: list[list[float, float], list[float, float]], p: list[float, float]) -> float:
    """
    get the shortest distance, from point, to line. (2D only)

    :param line: infinite line, defined by to points
    :param p: point measuring from
    :return: the length of a perpendicular line, from point p to line. AKA the shortest distance.
    """
    x0 = p[0]
    y0 = p[1]
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[1][0]
    y2 = line[1][1]

    divisor = math.sqrt((x2-x1)**2+(y2-y1)**2)
    if divisor != 0:
        return math.fabs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/divisor
    else:
        print("Line_to_point_distance, division by zero")
        return False


def circle_line_intersection(position: list[float, float], radius: float, start_point: list[float, float],
                             end_point: list[float, float], hollow=False) -> bool:
    """
    tells if line intersects circle. (2D only)
    :param position: center of circle
    :param radius: radius of circle
    :param start_point: first point of line segment
    :param end_point: second point of line segment
    :param hollow: exclude collision where whole line is inside circle.
    :return: true if line touches circle, otherwise false.
    """
    line = Line(start_point, end_point)

    # if line not pointing at circle, return False
    if line_to_point_distance(line.list(), position) > radius:
        return False

    start_point_in_circle = distance_between(start_point, position) <= radius
    end_point_in_circle = distance_between(end_point, position) <= radius
    # if hollow check to see if the whole line is in circle. if so return False.
    if hollow and start_point_in_circle and end_point_in_circle:
        return False

    # if inside circle, return true
    if start_point_in_circle or end_point_in_circle:
        return True

    # if the line cutts through the whole circle, return True
    rotate_angle = line.angle() + math.radians(90)
    rotated_line_start = rotate_point_around(line.start_point, position, rotate_angle)
    rotated_line_end = rotate_point_around(line.end_point, position, rotate_angle)
    if rotated_line_start[0] >= position[0] >= rotated_line_end[0] or\
            rotated_line_start[0] < position[0] < rotated_line_end[0]:
        return True
    return False


def rectangle_line_intersection(center: list[float, float], size: list[float, float], rotation: float,
                                start_point: list[float, float], end_point: list[float, float], hollow=False) -> bool:
    """
    tells if line intersects rectangle. (2D only)
    :param center: the center of rectangle.
    :param size: the width, and height of rectangle.
    :param rotation: rotation of the rectangle, in radians.
    :param start_point: the first point of line.
    :param end_point: the second point of line.
    :param hollow: exclude collision where whole line is inside retangle.
    :return: returns True if line touches rectangle, otherwise returns false.
    """
    # rotate line to keep equations simpler
    line = Line(rotate_point_around(start_point, center, -rotation), rotate_point_around(end_point, center, -rotation))

    # if hollow and both points are in rectangle, return False.
    if hollow and point_in_rect(line.start_point, center, size) and point_in_rect(line.end_point, center, size):
        return False

    # if start or end point is in rectangle, return True.
    if point_in_rect(line.start_point, center, size) or point_in_rect(line.end_point, center, size):
        return True
#
    # if line cuts through the rectangle, return True
    rotate_angle = line.angle() + math.radians(90)
    rotated_line = Line(rotate_point_around(line.start_point, center, rotate_angle),
                        rotate_point_around(line.end_point, center, rotate_angle))

    corners = [
        [center[0]+size[0]/2, center[1]+size[1]/2],
        [center[0]-size[0]/2, center[1]+size[1]/2],
        [center[0]-size[0]/2, center[1]-size[1]/2],
        [center[0]+size[0]/2, center[1]-size[1]/2],
    ]  # the corners of the square
    edges = [
        Line(corners[0], corners[1]),
        Line(corners[1], corners[2]),
        Line(corners[2], corners[3]),
        Line(corners[3], corners[0]),
    ]  # the edges of the square

    # if line intersects any edge, return True
    for edge in edges:
        if lines_intersects(line.list(), edge.list()):
            return True

    # if none of the above, return False
    return False


def point_in_rect(point: list[float, float], center: list[float, float], size: list[float, float]) -> bool:
    """
    tell if a given point is in rectangle. (2D only)
    :param point: point's position.
    :param center: center of the rectangle.
    :param size: the width and height of the rectangle, as a list.
    :return:
    """
    return center[0]-size[0]/2 <= point[0] <= center[0] + size[0]/2 and \
        center[1]-size[1]/2 <= point[1] <= center[1] + size[1]/2
