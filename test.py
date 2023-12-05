import pygame
import help
import math

window = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
clock = pygame.time.Clock()

fps = 30


def rectangle_intersection_test():
    position = [350+offsets[1]/5, 350+offsets[0]/-5]
    size = [500+offsets[3]/5, 50+offsets[2]/5]
    rotation = math.radians(offsets[4]/10)

    min_size = min(size[0]/2, size[1]/2)
    max_size = max(size[0]/2, size[1]/2)
    rect = [position[0]-size[0]/2, position[1]-size[1]/2, size[0], size[1]]

    # mouse_line = help.Line([750, 350], get_mouse_pos())
    mouse_line = help.Line(last_clicked, get_mouse_pos())
    print(math.degrees(mouse_line.angle()))
    crosses = help.rectangle_line_intersection(position, size, rotation, mouse_line.start_point, mouse_line.end_point)
    if crosses:
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)

    top_left = help.rotate_point_around([(position[0] - size[0]/2), (position[1] - size[1]/2)], position, rotation)
    top_right = help.rotate_point_around([(position[0] - size[0]/2), (position[1] + size[1]/2)], position, rotation)
    bottom_right = help.rotate_point_around([(position[0] + size[0]/2), (position[1] + size[1]/2)], position, rotation)
    bottom_left = help.rotate_point_around([(position[0] + size[0]/2), (position[1] - size[1]/2)], position, rotation)
    pygame.draw.polygon(window, (0, 0, 0), (top_left, top_right, bottom_right, bottom_left))

    pygame.draw.circle(window, (255, 255, 255), position, 5)
    pygame.draw.circle(window, (255, 255, 255), position, min_size, width=2)
    pygame.draw.circle(window, (255, 255, 255), position, max_size, width=2)

    pygame.draw.rect(window, (255, 255, 255), rect, width=2)

    rotate_angle = mouse_line.angle() + math.radians(90)
    rotated_line_start = help.rotate_point_around(mouse_line.start_point, position, rotate_angle)
    rotated_line_end = help.rotate_point_around(mouse_line.end_point, position, rotate_angle)
    pygame.draw.line(window, (127, 0, 255), rotated_line_start, rotated_line_end, width=2)
    pygame.draw.circle(window, (127, 0, 255), rotated_line_start, 4)

    top_left = help.rotate_point_around([(position[0] - size[0]/2), (position[1] - size[1]/2)], position, rotate_angle)
    top_right = help.rotate_point_around([(position[0] - size[0]/2), (position[1] + size[1]/2)], position, rotate_angle)
    bottom_right = help.rotate_point_around([(position[0] + size[0]/2), (position[1] + size[1]/2)], position, rotate_angle)
    bottom_left = help.rotate_point_around([(position[0] + size[0]/2), (position[1] - size[1]/2)], position, rotate_angle)
    pygame.draw.polygon(window, (0, 255, 255), (top_left, top_right, bottom_right, bottom_left), width=2)

    infinite_line_start = mouse_line.scaled_line(10000)[0]
    infinite_line_end = mouse_line.scaled_line(10000)[1]

    pygame.draw.line(window, (255, 255, 0), help.rotate_point_around(mouse_line.start_point, position, -rotation),
                     help.rotate_point_around(mouse_line.end_point, position, -rotation), width=2)

    above = rotated_line_start[1] < position[1]  # if rotate line is above rectangle
    points = [
        help.rotate_point_around([(position[0] - size[0]/2), (position[1] - size[1]/2)], position, rotate_angle),
        help.rotate_point_around([(position[0] - size[0]/2), (position[1] + size[1]/2)], position, rotate_angle),
        help.rotate_point_around([(position[0] + size[0]/2), (position[1] + size[1]/2)], position, rotate_angle),
        help.rotate_point_around([(position[0] + size[0]/2), (position[1] - size[1]/2)], position, rotate_angle)
    ]
    closest_point = None
    if above:
        distance_to_beat = math.inf
        for point in points:
            if point[1] < distance_to_beat:
                distance_to_beat = point[1]
                closest_point = point
    else:
        distance_to_beat = 0
        for point in points:
            if point[1] > distance_to_beat:
                distance_to_beat = point[1]
                closest_point = point
    pygame.draw.circle(window, (0, 0, 255), closest_point, 5)
    # if math.degrees(rotation+rotate_angle) % 360 > 180:
    #     print(True)
    vertical_length = size[1]/math.cos(rotation+rotate_angle)
    # print(vertical_length)
    pygame.draw.circle(window, (0, 0, 255), [closest_point[0], closest_point[1]+vertical_length], 5)

    pygame.draw.line(window, (0, 0, 255), infinite_line_start, infinite_line_end, width=2)
    pygame.draw.line(window, color, mouse_line.start_point, mouse_line.end_point, width=4)


def circle_intersection_test():
    center = [350+offsets[1]/5, 350+offsets[0]/-5]
    radius = 200+offsets[2]/5
    # mouse_line = help.Line([750, 350], get_mouse_pos())
    mouse_line = help.Line(last_clicked, get_mouse_pos())

    crosses = help.circle_line_intersection(center, radius, mouse_line.start_point, get_mouse_pos())
    if crosses:
        color = (255, 0, 0)
    else:
        color = (0, 255, 0)

    pygame.draw.circle(window, (0, 0, 0), center, radius)

    perpendicular_line = help.Line(mouse_line.center(), center)
    infinite_line_start = mouse_line.scaled_line(10000)[0]
    infinite_line_end = mouse_line.scaled_line(10000)[1]
    pygame.draw.circle(window, (0, 0, 255), mouse_line.center(), mouse_line.radius(), width=2)
    pygame.draw.line(window, (0, 0, 255), infinite_line_start, infinite_line_end, width=2)

    pygame.draw.line(window, (255, 255, 0), mouse_line.center(), center, width=2)
    pygame.draw.line(window, color, mouse_line.start_point, mouse_line.end_point, width=4)

    circle_edge = [center[0], center[1] + radius]
    tangent_line = help.rotate_point_around(circle_edge, center, -perpendicular_line.angle())
    pygame.draw.line(window, (0, 255, 255), center, tangent_line, width=4)

    rotate_angle = mouse_line.angle() + math.radians(90)
    rotated_line_start = help.rotate_point_around(mouse_line.start_point, center, rotate_angle)
    rotated_line_end = help.rotate_point_around(mouse_line.end_point, center, rotate_angle)
    pygame.draw.line(window, (127, 0, 255), rotated_line_start, rotated_line_end, width=2)

    # circle_offset = help.semi_circle_curve(get_mouse_pos()[1] - center[1], radius)
    # # print(circle_offset)
    # intersection_point = [550 - circle_offset, get_mouse_pos()[1]]
    # pygame.draw.circle(window, (128, 0, 255), intersection_point, 5)


def start():
    pass


def update():
    check_events()
    draw()
    pygame.display.update()


def draw():
    window.fill((100, 100, 100))
    rectangle_intersection_test()


def check_events():
    global run
    global offsets
    global key_delay
    global last_clicked

    keys = pygame.key.get_pressed()

    if key_delay <= 0:
        if keys[pygame.K_j]:
            print("key_ pressed")
            key_delay = 5
    else:
        key_delay -= 1

    if keys[pygame.K_UP]:
        offsets[0] += fps
    if keys[pygame.K_DOWN]:
        offsets[0] -= fps
    if keys[pygame.K_RIGHT]:
        offsets[1] += fps
    if keys[pygame.K_LEFT]:
        offsets[1] -= fps
    if keys[pygame.K_w]:
        offsets[2] += fps
    if keys[pygame.K_s]:
        offsets[2] -= fps
    if keys[pygame.K_d]:
        offsets[3] += fps
    if keys[pygame.K_a]:
        offsets[3] -= fps
    if keys[pygame.K_e]:
        offsets[4] += fps
    if keys[pygame.K_q]:
        offsets[4] -= fps

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            last_clicked = get_mouse_pos()


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


offsets = [0, 0, 0, 0, 0]
last_clicked = [750, 350]
key_delay = 0

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Pygame Physics Engine")

    start()
    # main loop
    run = True
    while run:
        clock.tick(fps)
        update()

    pygame.quit()
