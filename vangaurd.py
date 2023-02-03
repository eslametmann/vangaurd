import pygame
import random
import math
from pygame import mixer

pygame.init()
# create the screen
screen = pygame.display.set_mode((800, 600))

# title and icon
pygame.display.set_caption("Vangaurd")
icon = pygame.image.load("space-shuttle.png")
pygame.display.set_icon(icon)

# back_ground
back_ground = pygame.image.load("space.png")

# sound
mixer.music.load("epic.mp3")
mixer.music.play(-1)

# player
player_image = pygame.image.load("fighter.png")
playerX = 380
playerY = 470
playerX_change = 0
playerY_change = 0

# bullets
missile_img = pygame.image.load("missile.png")
missileX = 380
missileY = 470
missileY_change = -10
missile_state = "ready"

enemy1_img = pygame.image.load("enemy1.png")
enemy2_img = pygame.image.load("enemy2.png")
enemy3_img = pygame.image.load("enemy3.png")
enemy4_img = pygame.image.load("enemy4.png")
enemy5_img = pygame.image.load("enemy5.png")
enemy6_img = pygame.image.load("enemy6.png")

enemy_img = [enemy1_img, enemy2_img, enemy3_img, enemy4_img, enemy5_img, enemy6_img]
enemy1X = []
enemy1Y = []
enemy1Y_change = []
enemy1X_change = []
num_of_enemies = 6

# enemies
for i in range(num_of_enemies):
    enemy1X.append(400)
    enemy1Y.append(0)
    enemy1Y_change.append(2)
    enemy1X_change.append(2)

score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
scoreX = 10
scoreY = 10


def show_score(x, y):
    text = font.render("score is : " + str(score), True, (255, 255, 255))
    screen.blit(text, (x, y))


def player(x, y):
    screen.blit(player_image, (x, y))


def fire_missile(x, y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_img, (x + 20, y + 10))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (enemy1X[i], enemy1Y[i]))


def collision(enemyX, enemyY, missileX, missileY):
    distance = math.sqrt((math.pow(enemyX - missileX, 2)) + (math.pow(enemyY - missileY, 2)))
    if distance <= 30:
        return True
    else:
        return False


def game_over(enemy1X, enemy1Y, playerX, playerY):
    distance = math.sqrt((math.pow(enemy1X - playerX, 2)) + (math.pow(enemy1Y - playerY, 2)))
    if distance <= 36:
        return True
    else:
        return False


font_over = pygame.font.Font("freesansbold.ttf", 70)


def game_over_text():
    over_text = font_over.render("GAME OVER !", True, (255, 255, 255))
    screen.blit(over_text, (290, 270))


# game loop to keep running and listen to quit
running = True
while running:
    # screen background and update
    screen.fill((0, 0, 0))
    screen.blit(back_ground, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_UP:
                playerY_change = -4
            if event.key == pygame.K_DOWN:
                playerY_change = 4
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    launch = mixer.Sound("launch.mp3")
                    launch.play()
                    missileX = playerX
                    missileY = playerY
                    fire_missile(missileX, missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    if playerY <= 100:
        playerY = 100
    elif playerY >= 536:
        playerY = 536
    for i in range(num_of_enemies):
        over = game_over(enemy1X[i], enemy1Y[i], playerX, playerY)
        if over:
            for j in range(num_of_enemies):
                enemy1Y_change[j] = 0
                enemy1Y[j] = 599
                enemy1X_change[j] = 0
            game_over_text()
            break


        enemy1Y[i] += enemy1Y_change[i]
        enemy1X[i] += enemy1X_change[i]
        if enemy1X[i] <= 0:
            enemy1X_change[i] = 2
        elif enemy1X[i] >= 736:
            enemy1X_change[i] = -2

        if enemy1Y[i] >= 800:
            enemy1Y[i] = 0
            enemy1X[i] = random.randrange(20, 736)
            enemy1X_change[i] = random.choices([1, 2, 3, -2, -1, -3])[0]
            enemy1Y_change[i] = random.choices([1, 2, 3])[0]

        coll = collision(enemy1X[i], enemy1Y[i], missileX, missileY)
        if coll:
            boom = mixer.Sound("boom.mp3")
            boom.play()
            score += 1
            enemy1Y[i] = 0
            enemy1X[i] = random.randrange(0, 800)
            enemy1X_change[i] = random.choices([1, -1])[0]
            missile_state = "ready"

        enemy(enemy1X[i], enemy1Y[i], i)

    if missile_state == "fire":
        fire_missile(missileX, missileY)
        missileY += missileY_change
    if missileY <= 0:
        missile_state = "ready"

    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()

