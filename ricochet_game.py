import pygame
import physics_engine as physics
import random
import math

window = physics.window
pygame.display.set_caption("Ricochet")

level = {
    "turret_pos": (100, 100),
    "score_lines": [((650, 650), (850, 650))],
    "delete_lines": [],
    "map_size": (1000, 800),
    "game_seed": 1,
    "star_seed": 7,
    "star_count": 1000
}

constants = {
    "shoot_speed": 100,
    "screen_box": 100
}

star_randomizer = random.Random(level["star_seed"])
game_randomizer = random.Random(level["game_seed"])


def update():
    check_events()

    window.fill((63, 63, 63))
    draw_space()

    # Draw Game Lines
    for line in level["score_lines"]:
        pygame.draw.line(window, (0, 255, 0), line[0], line[1])
    for line in level["delete_lines"]:
        pygame.draw.line(window, (255, 0, 0), line[0], line[1])

    physics.update_classes()
    pygame.display.update()

    # delete walls if off screen
    for wall in physics.Wall.walls:
        x = wall.center[0]
        y = wall.center[1]
        size = wall.radius
        if x-size > level["map_size"][0]+constants["screen_box"] or \
                y-size > level["map_size"][1]+constants["screen_box"] or \
                x+size < -constants["screen_box"] or \
                y+size < -constants["screen_box"]:

            physics.Wall.walls.remove(wall)
            del wall

    for node in physics.Node.nodes:
        # check off screen
        x = node.position[0]
        y = node.position[1]
        size = node.size

        if x-size > level["map_size"][0]+constants["screen_box"] or \
                y-size > level["map_size"][1]+constants["screen_box"] or \
                x+size < -constants["screen_box"] or \
                y+size < -constants["screen_box"]:

            physics.Node.nodes.remove(node)
            del node
        else:
            # Check Game Line Intersect
            for line in level["score_lines"]:
                if physics.lines_intersects((node.last_frame, node.position), line):
                    print("Win")
            for line in level["delete_lines"]:
                if physics.lines_intersects((node.last_frame, node.position), line):
                    print("Die")
                    physics.Node.nodes.remove(node)
                    del node
                    break

    # Check Generate Random Wall
    if game_randomizer.random() <= 0.03:
        generate_random_wall()


def draw_space():
    pygame.draw.rect(window, (0, 0, 0), ((0, 0), level["map_size"]))
    star_randomizer.seed(level["star_seed"])

    for i in range(level["star_count"]):
        x = star_randomizer.randrange(0, level["map_size"][0])
        y = star_randomizer.randrange(0, level["map_size"][1])
        size = star_randomizer.random()
        color = int(255*(size**2))

        if random.random() < 0.005:
            twinkle = 0.75
        else:
            twinkle = 1
        pygame.draw.circle(window, (color*twinkle, color*twinkle, color*twinkle), (x, y), size+1)


def check_events():
    global run
    global key_delay

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            shoot()

    keys = pygame.key.get_pressed()
    if key_delay <= 0:
        if keys[pygame.K_j]:
            print("Test")
            key_delay = 5
    else:
        key_delay -= 1


def shoot():
    mouse = physics.get_mouse_pos()
    x = mouse[0] - turret.position[0]
    y = mouse[1] - turret.position[1]
    magnitude = math.hypot(x, y)

    velocity = (x*constants["shoot_speed"]/magnitude, y*constants["shoot_speed"]/magnitude)
    physics.Node(level["turret_pos"], velocity, (0, 255, 255), gravity=False)


def generate_random_wall():
    wall = game_randomizer.randint(0, 3)  # 0:top, 1:right: 2:bottom, 3:left
    axis_direction = ((wall//2)*2)-1  # 1 if wall is a positive axis, -1 if its negative

    direction = math.radians(game_randomizer.randrange(0, 360))
    speed = (game_randomizer.random()-0.5) * 2
    angle = game_randomizer.randrange(0, 360)
    spin = (game_randomizer.random()-0.5)

    x_vel = math.cos(direction)*speed
    y_vel = math.sin(direction)*speed
    if wall % 2 == 0:  # if on top or bottom wall
        y_vel = math.fabs(y_vel) * -axis_direction
        x_pos = game_randomizer.randrange(0, level["map_size"][0])
        if axis_direction > 0:
            y_pos = level["map_size"][1] + constants["screen_box"]
        else:
            y_pos = -constants["screen_box"]
    else:
        x_vel = math.fabs(x_vel) * -axis_direction
        y_pos = game_randomizer.randrange(0, level["map_size"][1])
        if axis_direction > 0:
            x_pos = level["map_size"][0] + constants["screen_box"]
        else:
            x_pos = -constants["screen_box"]

    wall = physics.Wall((x_pos-50, y_pos), (x_pos+50, y_pos), color=(127, 127, 127), velocity=(x_vel, y_vel), spin=spin)
    wall.move_to(angle)


turret = physics.Node(level["turret_pos"], (0, 0), (0, 0, 255), projection_length=5000, projection_color=(0, 255, 255), static=True)
physics.Wall((650, 650), (650, 450), color=(127, 127, 127))

# main loop
key_delay = 0
run = True
while run:
    physics.clock.tick(30)
    update()

pygame.quit()

