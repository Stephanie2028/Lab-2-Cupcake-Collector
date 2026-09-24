import sys
import random
import pygame

pygame.init()

pygame.display.set_caption('cow paradise')
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

grass = pygame.image.load('grassbot.png')
grass = pygame.transform.scale(grass, (640, 60))

skyBG = pygame.image.load('sky.png')
skyBG = pygame.transform.scale(skyBG, (640, 480))

cloudSPR = pygame.image.load('cloud.png')
cloudSPR = pygame.transform.scale(cloudSPR, (180, 84))

cowSPR = pygame.image.load('cow.png')
cowSPR = pygame.transform.scale(cowSPR, (70, 70))

cupcake1 = pygame.image.load('cupcake1.png')
cupcake2 = pygame.image.load('cupcake2.png')
cupcake3 = pygame.image.load('cupcake3.png')

cupcake1 = pygame.transform.scale(cupcake1, (40, 40))
cupcake2 = pygame.transform.scale(cupcake2, (40, 40))
cupcake3 = pygame.transform.scale(cupcake3, (40, 40))

cupcake_images = [cupcake1, cupcake2, cupcake3]

cowSPRx = 0
cowSPRy = 410

speed = 3

gravity = 0.5
jump_strength = -13
vertical_speed = 0

on_ground = True
cow_facing_right = True

clouds = [
    [50, 50],
    [100, 350],
    [350, 280],
    [150, 200],
    [450, 120]
]

cupcakes_collected = 0
cupcakes = []

def spawn_cupcake():
    cupcake_image = random.choice(cupcake_images)

    if random.choice([True, False]):
        x = random.randint(0, 600)
        y = 440
    else:
        cloud = random.choice(clouds)

        cloud_x = cloud[0]
        cloud_y = cloud[1]

        x = random.randint(cloud_x, cloud_x + 140)
        y = cloud_y - 40

    cupcakes.append([cupcake_image, x, y])

for i in range(6):
    spawn_cupcake()

running = True

while running:
    screen.fill((0, 0, 0))
    screen.blit(skyBG, [0, 0])
    screen.blit(grass, [0, 445])

    for cloud in clouds:
        screen.blit(cloudSPR, cloud)

    for cupcake in cupcakes:
        screen.blit(cupcake[0], [cupcake[1], cupcake[2]])

    if cow_facing_right:
        cowSPR_flipped = cowSPR
    else:
        cowSPR_flipped = pygame.transform.flip(cowSPR, True, False)

    screen.blit(cowSPR_flipped, [cowSPRx, cowSPRy])

    font = pygame.font.Font(None, 32)

    score_text = font.render(
        "Cupcakes collected: " + str(cupcakes_collected),
        True,
        (255, 255, 255)
    )

    screen.blit(score_text, [10, 10])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                vertical_speed = jump_strength
                on_ground = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT]:
        cowSPRx += speed
        cow_facing_right = True

    if keys[pygame.K_LEFT]:
        cowSPRx -= speed
        cow_facing_right = False

    oldCowY = cowSPRy

    vertical_speed += gravity
    cowSPRy += vertical_speed

    on_ground = False

    for cloud in clouds:
        cloud_x = cloud[0]
        cloud_y = cloud[1]

        cow_left = cowSPRx
        cow_right = cowSPRx + 70
        cow_bottom = cowSPRy + 70

        cloud_left = cloud_x
        cloud_right = cloud_x + 180
        cloud_top = cloud_y

        if vertical_speed >= 0:
            if oldCowY + 70 <= cloud_top and cow_bottom >= cloud_top:
                if cow_right > cloud_left and cow_left < cloud_right:
                    cowSPRy = cloud_top - 70
                    vertical_speed = 0
                    on_ground = True

    if cowSPRy >= 410:
        cowSPRy = 410
        vertical_speed = 0
        on_ground = True

    if cowSPRx < 0:
        cowSPRx = 0

    if cowSPRx > 570:
        cowSPRx = 570

    cow_rect = pygame.Rect(
        cowSPRx,
        cowSPRy,
        70,
        70
    )

    for cupcake in cupcakes[:]:
        cupcake_rect = pygame.Rect(
            cupcake[1],
            cupcake[2],
            40,
            40
        )

        if cow_rect.colliderect(cupcake_rect):
            cupcakes.remove(cupcake)
            cupcakes_collected += 1
            spawn_cupcake()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
