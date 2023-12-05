import pygame
import math
import help
import random

constants = {
    "gravity": 0.5,
    "max_bounce": 10,
    "randomizer": 1,
}

window = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()


class Node(object):
    nodes = []

    @staticmethod
    def nodes_in_triangle(a: list, b: list, c: list):
        node_list = []
        for node in Node.nodes:
            if help.point_in_triangle(node.position, a, b, c):
                node_list.append(node)
        return node_list

    def __init__(self, position: list, velocity=(0, 0), color=(0, 0, 0), size=5,
                 projection_length=0, projection_color=(0, 0, 0), static=False, gravity=True):
        self.position = [position[0]+random.random()*constants["randomizer"]-constants["randomizer"]/2,
                         position[1]+random.random()*constants["randomizer"]-constants["randomizer"]/2]
        self.velocity = [velocity[0], velocity[1]]
        self.color = color
        self.size = size
        self.projection_length = projection_length
        self.projection_color = projection_color
        self.static = static
        self.gravity = gravity

        self.last_frame = self.position

        Node.nodes.append(self)

    def update(self):
        # print(self.position)
        self.draw()

        if not self.static:
            if self.gravity:
                self.velocity[1] += constants["gravity"]

            start_pos = list(self.position)
            end_pos = (start_pos[0] + self.velocity[0], start_pos[1] + self.velocity[1])

            excluded_walls = []
            for i in range(constants["max_bounce"]+1):
                wall = Wall.get_intersected_wall(self.position, end_pos, excluded_walls)
                if wall is None:
                    break
                elif i >= constants["max_bounce"]:
                    print("exceeded max_bounce")
                    break
                else:
                    excluded_walls.append(wall)
                    angle = wall.angle_between(start_pos, end_pos)
                    # print(math.degrees(angle))
                    self.bounce(-angle)
                    self.velocity[0] *= wall.dampening
                    self.velocity[1] *= wall.dampening

                    old_end_pos = end_pos
                    end_pos = wall.reflection_point(start_pos, end_pos)
                    start_pos = old_end_pos

                    # end_pos = [end_pos[0] + self.velocity[0], end_pos[1] + self.velocity[1]]

            self.last_frame = self.position
            self.position = end_pos

    def bounce(self, angle):
        # Adjust Velocity
        x = self.velocity[0]*math.cos(angle) - self.velocity[1]*math.sin(angle)
        y = self.velocity[0]*math.sin(angle) + self.velocity[1]*math.cos(angle)
        self.velocity = [x, y]
        # print(self.velocity)

    def draw(self):
        # if self.draw_projection:
        #     wall = self.get_intersected_wall(get_mouse_pos())
        #     if wall is not None:
        #         wall.color = (0, 0, 255)

        if self.projection_length > 0:
            if self.static:
                mouse = get_mouse_pos()
                self.draw_refection(help.angle_of_line(self.position, mouse),
                                    self.projection_length, constants["max_bounce"])
            else:
                self.draw_refection(math.atan2(-self.velocity[0], -self.velocity[1]),
                                    self.projection_length, constants["max_bounce"])

        pygame.draw.circle(window, (0, 0, 0), self.position, self.size+2)
        pygame.draw.circle(window, self.color, self.position, self.size)

    def draw_refection(self, direction, distance, refection_count):
        start_point = list(self.position)

        x = start_point[0] + (math.cos(-direction-math.radians(90)) * distance)
        y = start_point[1] + (math.sin(-direction-math.radians(90)) * distance)
        end_point = x, y

        excluded = None

        for i in range(refection_count + 1):
            if i > refection_count:
                print("Exceeded Refection Count")
                break

            wall = Wall.get_intersected_wall(start_point, end_point, [excluded])
            if wall is not None:
                reflection_point = wall.reflection_point(start_point, end_point)
                end_point = wall.intersection_point(start_point, end_point)
                excluded = wall
                pygame.draw.line(window, self.projection_color, start_point, end_point, 2)
                start_point = end_point
                end_point = reflection_point
            else:
                pygame.draw.line(window, self.projection_color, start_point, end_point, 2)
                break

    # @staticmethod
    # def get_bounce_point(start_pos, end_pos: list, excluded=None, index=None):
    #     if excluded is None:
    #         excluded = []
    #     if index is None:
    #         index = 0
    #     elif index >= constants["max_bounce"]:
    #         warnings.warn("exceeded Max_Bounce")
    #         return None
    #
    #     wall = Wall.get_intersected_wall(start_pos, end_pos, excluded)
    #     if wall is not None:
    #         reflection_pos = wall.reflection_point(start_pos, end_pos)
    #         intersection_pos = wall.intersection_point(start_pos, end_pos)
    #
    #         if Wall.get_intersected_wall(intersection_pos, reflection_pos, [wall]) is not None:
    #             end_point = Node.get_bounce_point(intersection_pos, reflection_pos, [wall], index+1)
    #
    #             pygame.draw.line(window, (0, 255, 255), intersection_pos, end_point, 3)
    #         else:
    #             pygame.draw.line(window, (0, 255, 255), intersection_pos, reflection_pos, 3)
    #         return intersection_pos


class Wall(object):
    walls = []

    @staticmethod
    def get_intersected_wall(start_pos, end_pos, excluded=None):
        selected_distance = None
        selected_wall = None

        if excluded is None:
            excluded = []

        for wall in Wall.walls:
            if wall not in excluded:
                if wall.intersects(start_pos, end_pos):
                    intersection_point = wall.intersection_point(start_pos, end_pos)
                    distance = help.distance_between(start_pos, intersection_point)
                    if selected_distance is None or distance < selected_distance:
                        selected_distance = distance
                        selected_wall = wall

        return selected_wall

    def __init__(self, start_point: list, end_point: list, dampening=1, thickness=5,
                 color=(0, 0, 0), spin=0.0, velocity=(0, 0)):
        self.start = [start_point[0], start_point[1]]
        self.end = [end_point[0], end_point[1]]
        self.dampening = dampening
        self.thickness = thickness
        self.spin = spin
        self.velocity = velocity
        self.color = color

        self.center = (0.0, 0.0)
        self.radius = 0.0
        self.angle = 0.0
        self.set_vars()

        # self.test_node = Node(start_point[0], start_point[1], True)

        Wall.walls.append(self)

    def set_vars(self):
        self.center = ((self.start[0]+self.end[0])/2, (self.start[1]+self.end[1])/2)
        self.radius = help.distance_between(self.start, self.end) / 2
        self.angle = help.angle_of_line(self.start, self.end)

    def move_to(self, angle: float, center=(), radius=()):
        if center == ():
            center = self.center
        if radius == ():
            radius = self.radius

        # print(math.degrees(angle))

        start_pos = (math.sin(angle)*radius+center[0], math.cos(angle)*radius+center[1])
        end_pos = (math.sin(angle)*-radius+center[0], math.cos(angle)*-radius+center[1])

        nodes_hit = self.check_intersected(start_pos, end_pos)

        for node in nodes_hit:
            if node.static:
                nodes_hit.remove(node)
            else:
                print(node.color, ", ", end="", sep="")

        if len(nodes_hit) == 0:
            self.start = start_pos
            self.end = end_pos
            self.set_vars()
        else:
            # TODO: come up with better solution than to just skip it
            # self.spin *= -1
            print()

    def check_intersected(self, start_pos, end_pos):
        first_triangle = Node.nodes_in_triangle(start_pos, self.start, end_pos)
        second_triangle = Node.nodes_in_triangle(end_pos, self.end, self.start)

        nodes_hit = []
        if len(first_triangle) > 0:
            nodes_hit.extend(first_triangle)

        if len(second_triangle) > 0:
            nodes_hit.extend(second_triangle)

        return nodes_hit

    def intersects(self, start_pos: list, end_pos: list) -> bool:
        if (help.orientation(self.start, self.end, start_pos) != help.orientation(self.start, self.end, end_pos)) and \
                (help.orientation(start_pos, end_pos, self.start) != help.orientation(start_pos, end_pos, self.end)):
            return True
        else:
            return False

    def distance_from_point(self, p: list) -> float:
        x0 = p[0]
        y0 = p[1]
        x1 = self.start[0]
        y1 = self.start[1]
        x2 = self.end[0]
        y2 = self.end[1]
        return math.fabs((x2-x1)*(y1-y0)-(x1-x0)*(y2-y1))/math.sqrt((x2-x1)**2+(y2-y1)**2)

    def intersection_point(self, start_point: list, end_point: list) -> list:
        x1 = self.start[0]
        y1 = self.start[1]
        x2 = self.end[0]
        y2 = self.end[1]
        x3 = start_point[0]
        y3 = start_point[1]
        x4 = end_point[0]
        y4 = end_point[1]

        divisor = ((x1-x2)*(y3-y4) - (y1-y2)*(x3-x4))

        if divisor != 0:
            x = ((x1*y2-y1*x2)*(x3-x4) - (x1-x2)*(x3*y4-y3*x4)) / divisor
            y = ((x1*y2-y1*x2)*(y3-y4) - (y1-y2)*(x3*y4-y3*x4)) / divisor
        else:
            print("parallel")  # TODO: wall glitch error
            x = 0
            y = 0

        return [x, y]

    def angle_between(self, start_pos: list, end_pos: list) -> float:
        return (self.angle - help.angle_of_line(start_pos, end_pos)) * 2

    def reflection_point(self, start_pos: list, end_pos: list) -> list:
        rotation_point = self.intersection_point(start_pos, end_pos)
        position = (end_pos[0]-rotation_point[0], end_pos[1]-rotation_point[1])
        angle = self.angle_between(start_pos, end_pos)

        x = position[0]*math.cos(angle) + position[1]*math.sin(angle)
        y = -position[0]*math.sin(angle) + position[1]*math.cos(angle)

        return [x+rotation_point[0], y+rotation_point[1]]

    def update(self):
        self.draw()

        if self.spin != 0 or self.velocity[0] != 0 or self.velocity[1] != 0:
            x = self.center[0] + self.velocity[0]
            y = self.center[1] + self.velocity[1]
            self.move_to(self.angle + math.radians(-self.spin), (x, y))

    def draw(self):
        # start_pos = (main_node.position[0], main_node.position[1])
        # end_pos = get_mouse_pos()

        # if self.intersects(start_pos, end_pos):
        #     # self.test_node.position = self.intersection_point(start, end)
        #     self.test_node.position = self.reflection_point(start_pos, end_pos)
        #     pygame.draw.line(window, (0, 255, 255), self.intersection_point(start_pos, end_pos),
        #                      self.test_node.position, 3)
        # else:
        #     self.test_node.position = (-100, -100)

        pygame.draw.line(window, self.color, self.start, self.end, self.thickness)
        #
        # if self.intersects(start_pos, end_pos):
        #     self.color = (255, 0, 0)
        # else:
        #     self.color = (0, 0, 0)


def start():
    Wall([50, 600], [850, 600])
    Wall([100, 100], [600, 600])
    Wall([250, 100], [250, 600])
    Wall([750, 100], [750, 600])
    Wall([50, 100], [850, 100])
    Wall([600, 200], [600, 400], spin=2)

    node1 = Node([400, 250], [-2, -1], (255, 0, 0), projection_length=100)
    node2 = Node([700, 225], [20, -3], (255, 191, 0), projection_length=100)
    node3 = Node([550, 275], [7, -5], (255, 255, 0), projection_length=100)
    node4 = Node([650, 350], [-3, 2], (0, 255, 0), projection_length=100)
    node5 = Node([350, 125], [0, 0], (0, 0, 255), projection_length=100)
    node6 = Node([275, 125], [4, -7], (0, 255, 255), projection_length=100)

    # floating_node = Node((650, 250), (7, 12), (0, 0, 0), 5, 100, False, False)
    # static_node = Node((300, 150), (5, 5), (0, 0, 0), 5, 1000, True, False)


def update():
    window.fill((191, 127, 255))
    update_classes()
    check_events()
    pygame.display.update()


def update_classes():
    for wall in Wall.walls:
        wall.update()

    for node in Node.nodes:
        node.update()


def check_events():
    global run
    global key_delay
    keys = pygame.key.get_pressed()

    if key_delay <= 0:
        if keys[pygame.K_j]:
            # spinning_wall.update()
            key_delay = 5
    else:
        key_delay -= 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    # start_pos = main_node.position
    #
    # distance = math.hypot(math.fabs(start_pos[0] - x), math.fabs(start_pos[1] - y))
    #
    # if distance != 0:
    #     multiplier = 1000/distance
    #     x = ((x - start_pos[0]) * multiplier) + start_pos[0]
    #     y = ((y - start_pos[1]) * multiplier) + start_pos[1]

    return [x, y]


def round_pos(position: list, places=2):
    return position[0].__round__(places), position[1].__round__(places)


key_delay = 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Pygame Physics Engine")

    start()
    # main loop
    run = True
    while run:
        clock.tick(30)
        update()

    pygame.quit()
