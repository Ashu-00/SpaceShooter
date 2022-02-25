import random
import pygame
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()

BEEP = pygame.mixer.Sound("sound.mp3")
LASER = pygame.mixer.Sound("laser.mp3")

WIDTH = 500
HEIGHT = 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Game")

FPS = 50

AST = pygame.image.load("asteroid.png").convert_alpha()
ASTEROID = pygame.transform.scale(AST, (30, 30))
ASTEROID_VEL = 9

SPACESHIP = pygame.transform.scale(
    pygame.image.load("Spaceship.png").convert_alpha(), (60, 60)
)
SHIP_VEL = 10

BULLET_VEL = 11

BACKGROUND = pygame.transform.scale(
    pygame.image.load("Background.png").convert(), (WIDTH, HEIGHT)
)

FONT1 = pygame.font.SysFont("fixedsys", 20)
FONT2 = pygame.font.SysFont("fixedsys", 50)


def draw(ship_rec, bullets, asteroids, health, points):
    WIN.fill((0, 0, 0))
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(SPACESHIP, (ship_rec.x, ship_rec.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, (255, 255, 0), bullet)

    for asteroid in asteroids:
        WIN.blit(ASTEROID, (asteroid.x, asteroid.y))
    text1 = FONT1.render("Health:" + str(health), 1, (255, 0, 0))
    text2 = FONT1.render("Score:" + str(points), 1, (0, 255, 0))
    WIN.blit(text2, (0, 0))
    WIN.blit(text1, (WIDTH - text1.get_width(), 0))

    pygame.display.update()


def handle_ship(ship_rec, keys_pressed):

    if keys_pressed[pygame.K_RIGHT] and ship_rec.x + SPACESHIP.get_width() <= WIDTH:
        ship_rec.x += SHIP_VEL

    if keys_pressed[pygame.K_LEFT] and ship_rec.x >= 0:
        ship_rec.x -= SHIP_VEL


def handle_bullets(bullets):
    for bullet in bullets:
        bullet.y -= BULLET_VEL


def handle_asteroids(asteroids):
    for asteroid in asteroids:
        asteroid.y += ASTEROID_VEL


def check_coll(ship_rec, bullets, asteroids, health, points):
    for asteroid in asteroids:
        if asteroid.colliderect(ship_rec):
            health -= 1
            asteroids.remove(asteroid)
            BEEP.play()

    for asteroid in asteroids:
        for bullet in bullets:
            if bullet.colliderect(asteroid):
                bullets.remove(bullet)
                asteroids.remove(asteroid)
                points += 1
                BEEP.play()

    return health, asteroids, bullets, points


def check_level(points, health, level):
    if points > 50 and level == 2:
        textB = FONT2.render("LEVEL 3", 1, (0, 0, 0))
        textA = FONT2.render("Your Score:" + str(points), 1, (0, 0, 0))
        WIN.blit(textB, ((WIDTH - textB.get_width()) / 2, 0))
        WIN.blit(textA, ((WIDTH - textA.get_width()) / 2, textB.get_height() + 5))
        pygame.display.update()

        pygame.time.delay(5000)
        level += 1
        health = 15

    elif points > 15 and level == 1:
        textB = FONT2.render("LEVEL 2", 1, (0, 0, 0))
        textA = FONT2.render("Your Score:" + str(points), 1, (0, 0, 0))
        WIN.blit(textB, ((WIDTH - textB.get_width()) / 2, 0))
        WIN.blit(textA, ((WIDTH - textA.get_width()) / 2, textB.get_height() + 5))
        pygame.display.update()

        pygame.time.delay(5000)
        level += 1
        health = 15
    return points, health, level


def main():
    clock = pygame.time.Clock()
    run = True
    pygame.mixer.music.load("background.mp3")
    pygame.mixer.music.play(-1, 0, 0)

    ship_rec = pygame.Rect(
        (WIDTH - SPACESHIP.get_width()) / 2,
        HEIGHT - 10 - SPACESHIP.get_height(),
        SPACESHIP.get_width(),
        SPACESHIP.get_height(),
    )
    bullets = []
    asteroids = []
    health = 15
    points = 0
    t = time.time()
    level = 1

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(
                        ship_rec.x + (SPACESHIP.get_width()) / 2, ship_rec.y + 10, 5, 10
                    )
                    bullets.append(bullet)
                    LASER.play()

        if level == 1:
            n = 0.7
        elif level == 2:
            n = 0.4
        elif level == 3:
            global ASTEROID_VEL
            ASTEROID_VEL = 15

        if (time.time() - t) >= n:
            asteroid = pygame.Rect(
                random.uniform(0, WIDTH - ASTEROID.get_width()),
                0 - ASTEROID.get_height(),
                ASTEROID.get_width(),
                ASTEROID.get_height(),
            )
            asteroids.append(asteroid)
            t = time.time()

        if health == 0:
            textB = FONT2.render("GAME OVER", 1, (0, 0, 0))
            textA = FONT2.render("Your Score:" + str(points), 1, (0, 0, 0))
            WIN.blit(textB, ((WIDTH - textB.get_width()) / 2, 0))
            WIN.blit(textA, ((WIDTH - textA.get_width()) / 2, textB.get_height() + 5))
            pygame.display.update()

            pygame.time.delay(5000)
            break

        points, health, level = check_level(points, health, level)
        keys_pressed = pygame.key.get_pressed()
        handle_ship(ship_rec, keys_pressed)
        handle_bullets(bullets)
        handle_asteroids(asteroids)
        health, asteroids, bullets, points = check_coll(
            ship_rec, bullets, asteroids, health, points
        )

        draw(ship_rec, bullets, asteroids, health, points)

    pygame.quit()


if __name__ == "__main__":
    main()
