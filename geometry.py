import pygame
from pygame import Vector2
import help
import math

fps = 30

window = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()


def start():
    """called once at beginning of program."""
    # Wall(window, [100, 100], [100, 500], 2)
    # Wall(window, [100, 500], [500, 500], 2)
    # Wall(window, [500, 500], [500, 100], 2)
    # Wall(window, [500, 100], [100, 100], 2)

    # Circle(window, [300, 300], 250, filled=False)

    Circle(window, [300, 150], 10, gravity=1000)
    Circle(window, [200, 250], 10, vel=(65, 0))
    Circle(window, [400, 250], 10, vel=(-50, 0))
    Circle(window, [200, 200], 10, vel=(100, 50))

    Rectangle(window, [500, 300], [750, 500], filled=False)
    Rectangle(window, [250, 150], [100, 25], rotation=45)
    Rectangle(window, [350, 350], [200, 50], spin=10)
    Rectangle(window, [750, 250], [150, 100])


def update():
    """called once a frame"""
    global run
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    window.fill((100, 100, 100))
    for shape_updating in Shape.shapes:
        shape_updating.update()

    pygame.display.update()


class Shape(object):
    shapes = []

    def __init__(self, win, position, rotation=0.0, color=(0, 0, 0), vel=(0, 0), spin=0.0,
                 static=False, gravity=0.0, collider=False):
        self.window = win
        self.position = Vector2(position[0], position[1])
        self.rotation = rotation
        self.color = color
        self.velocity = Vector2(vel[0], vel[1])
        self.spin = spin

        self.static = static
        self.gravity = gravity
        self.collider = collider

        self.collider = None

        Shape.shapes.append(self)

    def update(self):
        """run once a frame"""
        self.draw()

        if not self.static:
            if self.gravity != 0:
                self.velocity[1] += self.gravity/fps

            self.move(self.position + self.velocity/fps, self.rotation+self.spin/fps)

    def draw(self):
        """draw shape, at current position"""
        pygame.draw.circle(self.window, self.color, self.position, 1)

    def move(self, moving_to: Vector2, rotation=None):
        """try moving the shape to a given position and rotation."""
        if self.velocity != Vector2(0, 0) and self.collides(moving_to):
            self.velocity *= -1
        else:
            self.position = moving_to
            if self.collider:
                self.update_collider()

        if rotation is not None:
            self.rotation = rotation

    def update_collider(self):
        """move collider to shapes position and rotation"""
        self.collider.set_position(self.position)

    def collides(self, end_point):
        """check if shape will collided if moves to give position."""
        return len(Collider.colliders_between(self.position, end_point, self.collider)) > 0


class Circle(Shape):
    circles = []

    def __init__(self, win, position, radius, collider=True, filled=True, width=None, **kwargs):
        super().__init__(win, position, **kwargs)
        self.radius = radius
        self.filled = filled

        if width is None:
            if filled:
                self.width = 0
            else:
                self.width = 1

        if collider:
            self.collider = CircleCollider(position, radius, hollow=not filled)

        Circle.circles.append(self)

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.position, self.radius, width=self.width)
        # if self.velocity != Vector2(0, 0):
        #     collision_surface = self.velocity.normalize()*self.radius
        #     pygame.draw.line(self.window, (255, 255, 255), collision_surface+self.position,
        #                      collision_surface+(self.velocity / fps)+self.position)

    def update_collider(self):
        self.collider.set_location(self.position)

    def collides(self, end_point):
        collision_surface = (end_point-self.position).normalize()*self.radius
        return len(Collider.colliders_between(collision_surface+self.position, collision_surface+end_point, self)) > 0


class Rectangle(Shape):
    rectangle = []

    def __init__(self, win, position, size, rotation=0.0, collider=True, filled=True, width=None, **kwargs):
        super().__init__(win, position, rotation, **kwargs)

        self.size = [size[0], size[1]]

        if width is None:
            if filled:
                self.width = 0
            else:
                self.width = 1

        if collider:
            self.collider = BoxCollider(position, size, self.rotation, hollow=not filled)

        Rectangle.rectangle.append(self)

    def get_rect(self):
        """gets the rectangle in pygame's draw format."""
        return [self.position[0]-self.size[0]/2, self.position[1]-self.size[1]/2, self.size[0], self.size[1]]

    def draw(self):
        if self.rotation == 0:
            pygame.draw.rect(self.window, self.color, self.get_rect(), width=self.width)
        else:
            top_left = Vector2(-self.size[0]/2, -self.size[1]/2).rotate(self.rotation) + self.position
            top_right = Vector2(self.size[0]/2, -self.size[1]/2).rotate(self.rotation) + self.position
            bottom_right = Vector2(self.size[0]/2, self.size[1]/2).rotate(self.rotation) + self.position
            bottom_left = Vector2(-self.size[0]/2, self.size[1]/2).rotate(self.rotation) + self.position

            pygame.draw.polygon(self.window, self.color, (top_left, top_right, bottom_right, bottom_left),
                                width=self.width)

    def update_collider(self):
        self.collider.set_location(self.position, self.rotation)

    def collides(self, end_point):
        return len(Collider.colliders_between(self.position, end_point, self)) > 0


class Wall(Shape):
    walls = []

    def __init__(self, win, start_point, end_point, width=1, collider=True, **kwargs):
        self.start_point = Vector2(start_point)
        self.end_point = Vector2(end_point)
        self.center = (self.start_point + self.end_point)/2

        super().__init__(win, self.center, collider=collider, **kwargs)

        self.width = width

        if collider:
            self.collider = WallCollider(start_point, end_point)

        Wall.walls.append(self)

    def update_collider(self):
        self.collider.start_point = self.start_point
        self.collider.end_point = self.end_point

    def draw(self):
        pygame.draw.line(self.window, self.color, self.start_point, self.end_point, self.width)


class Collider(object):

    def __init__(self, center, rotation=0.0):
        self.center = center
        self.rotation = rotation

    def line_collides(self, start_point, end_point):
        """if given line crosses collider."""
        return False

    def set_location(self, position, rotation=None):
        """sets the position and rotation of the collider"""
        self.center = position
        if rotation is not None:
            self.rotation = rotation

    @staticmethod
    def colliders_between(start_point, end_point, excluded=None):
        """
        gets a list of the colliders between start point and end point.
        :param start_point: the start point of line checking.
        :param end_point: the end point of line checking
        :param excluded: colliders to not include in list
        """
        colliders = []
        if excluded is None:
            excluded = []
        elif not hasattr(excluded, '__iter__'):  # if not list, make it a list
            excluded = [excluded]

        for shape in Shape.shapes:
            if shape not in excluded and shape.collider and shape.collider.line_collides(start_point, end_point):
                colliders.append(shape)

        # print(colliders)
        return colliders


class WallCollider(Collider):

    def __init__(self, start_point, end_point):
        self.start_point = Vector2(start_point)
        self.end_point = Vector2(end_point)
        center = (self.start_point + self.end_point)/2
        super().__init__(center, help.angle_of_line(start_point, end_point))

        self.start = start_point
        self.end = end_point

    def line_collides(self, start_point, end_point):
        return help.lines_intersects([start_point, end_point], [self.start, self.end])


class CircleCollider(Collider):

    def __init__(self, position, radius, hollow=False):
        super().__init__(position)
        self.radius = radius
        self.hollow = hollow

    def line_collides(self, start_point, end_point):
        return help.circle_line_intersection(self.center, self.radius, start_point, end_point, hollow=self.hollow)


class BoxCollider(Collider):

    def __init__(self, position, size, rotation=0.0, hollow=False):
        super().__init__(position, rotation)
        self.size = [size[0], size[1]]
        self.hollow = hollow

    def line_collides(self, start_point, end_point):
        return help.rectangle_line_intersection(self.center, self.size, math.radians(self.rotation),
                                                start_point, end_point, hollow=self.hollow)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("geometry test")

    start()
    # main loop
    run = True
    while run:
        clock.tick(fps)
        update()

    pygame.quit()
