import pygame
import time
import random

# I built this game with the help of 2 tutorials, combined with my own ideas.
# The tutorials are from:
# Tech with Tim https://www.youtube.com/watch?v=Q-__8Xw9KTM
# buildwithpython (via freeCodeCamp.org) https://www.youtube.com/watch?v=FfWpgLFMI7w
# Many thanks to these guys for their great lessons! :)

# Initialize the pygame.
pygame.init()

# Create the screen.
W = 800
H = 600
SCREEN = pygame.display.set_mode((W, H))

# Images
# BACKGROUND image 'Futuristic city on other planet' created by vectorpocket https://www.freepik.com/vectors/background
BACKGROUND = pygame.image.load('background.jpg')
# PLAYER icon made by Pixel Buddha https://www.flaticon.com/authors/pixel-buddha
PLAYER = pygame.image.load('player.png')
# ENEMY and ENEMY_HIT icon made by Smashicons https://www.flaticon.com/authors/smashicons
ENEMY = pygame.image.load('enemy.png')
ENEMY_HIT = pygame.image.load('enemy_hit.png')
# BULLET and ENEMY_BULLET icon made by Darius Dan https://www.flaticon.com/authors/darius-dan
BULLET = pygame.image.load('bullet.png')
ENEMY_BULLET = pygame.image.load('bullet_enemy.png')

# Title
pygame.display.set_caption("Space Invaders")

# Game Over Text / You Won Text
over_font = pygame.font.Font('freesansbold.ttf', 64)
won_font = pygame.font.Font('freesansbold.ttf', 64)


# Create class HealthBar that displays the health of the player
# The health bar has 5 circles that represent the health the player has left
# I learned how to create this class from Peter Collingridge
# http://www.petercollingridge.co.uk/tutorials/pygame-physics-simulation/drawing-circles/
class HealthBar:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 255, 205)

    def display(self):
        pygame.draw.circle(SCREEN, self.colour, (self.x, self.y), self.size)


health1 = HealthBar(780, 580, 10)
health2 = HealthBar(780, 555, 10)
health3 = HealthBar(780, 530, 10)
health4 = HealthBar(780, 505, 10)
health5 = HealthBar(780, 480, 10)


# Create parent class Spaceship.
# pygame.mask is to determine pixel-precise collision, idea from Tech with Tim
class Spaceship:
    def __init__(self, image, x, y, speed):
        self.image = image
        self.x = x
        self.y = y
        self.speed = speed
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self):
        # to draw the image on the screen, blit means draw
        SCREEN.blit(self.image, (self.x, self.y))


# Create child class Player
class Player(Spaceship):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.health = 10
        self.max_health = 10  # Used to calculate health percentage
        self.health_bar = [health1, health2, health3, health4, health5]


# Create child class Enemy
class Enemy(Spaceship):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.health = 2
        self.bullets = []


class PlayerBullet(Spaceship):
    pass


class EnemyBullet(Spaceship):
    pass


# This piece of code is from Tech with Tim's tutorial
def collision(object1, object2):
    offset_x = object2.x - object1.x
    offset_y = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (offset_x, offset_y)) is not None


# Function to run main game loop
def main():
    run = True
    # fps = frames per second
    fps = 60

    # create clock
    clock = pygame.time.Clock()

    # create instance of Player
    player = Player(PLAYER, 370, 480, 3)

    # create instances of Enemy
    enemies = []
    num_enemies = 10
    for i in range(num_enemies):
        enemy = Enemy(ENEMY, random.randint(10, W - 70),  random.randint(10, 50), 2)
        enemies.append(enemy)

    # create list of bullets
    player_bullets = []

    # Game over or won?
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    game_over = False
    won_text = won_font.render("YOU WON!!", True, (255, 255, 255))
    you_won = False
    countdown = 0

    # Function to redraw window and objects during the game.
    # Idea to put this function in main function is from Tech with Tim.
    def redraw_window():
        SCREEN.blit(BACKGROUND, (0, 0))
        for item in player.health_bar:
            item.display()
        player.draw()
        for enemy in enemies:
            enemy.draw()
            for enemy_bullet in enemy.bullets:
                enemy_bullet.draw()
        for player_bullet in player_bullets:
            player_bullet.draw()
        if game_over:
            SCREEN.blit(over_text, (200, 250))
        if you_won:
            SCREEN.blit(won_text, (200, 250))
        pygame.display.update()

    while run:
        clock.tick(fps)
        redraw_window()

        # End game if game over
        # The message 'Game over' of 'You won' is displayed for 3 seconds.
        # This piece of code is from Tech with Tim.
        if game_over or you_won:
            countdown += 1
            if countdown > fps * 3:
                run = False
            else:
                continue

        # End game if user clicks cross.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Player movement and player shooting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.speed > 0:
            player.x -= player.speed
        if keys[pygame.K_RIGHT] and player.x + player.speed + player.width < W:
            player.x += player.speed
        if keys[pygame.K_UP] and player.y - player.speed > 0:
            player.y -= player.speed
        if keys[pygame.K_DOWN] and player.y + player.speed + player.height < H:
            player.y += player.speed
        if keys[pygame.K_SPACE]:
            if len(player_bullets) < 1:
                player_bullet = PlayerBullet(BULLET, player.x, player.y, 10)
                player_bullets.append(player_bullet)

        # Player bullets movement
        for player_bullet in player_bullets:
            player_bullet.y -= player_bullet.speed
            if player_bullet.y <= 0:
                player_bullets.remove(player_bullet)

        # Enemy movement
        for enemy in enemies:
            enemy.x += enemy.speed
            if enemy.x <= 0:
                enemy.speed = 2
                if enemy.y <= 400:
                    enemy.y += 30
            elif enemy.x >= W - enemy.width:
                enemy.speed = -2
                if enemy.y <= 400:
                    enemy.y += 30

            # Enemy shooting
            # Enemies shoot at random times, about once every 2 seconds
            if random.randrange(0, 2 * 60) == 1: # this piece of code is from Tech with Tim
                # Every enemy has only 1 bullet at a time.
                # After the bullet is removed, a new one is created and added to the list.
                if len(enemy.bullets) < 1:
                    enemy_bullet = EnemyBullet(ENEMY_BULLET, enemy.x + 10, enemy.y + 25, 8)
                    enemy.bullets.append(enemy_bullet)

        # Move enemy bullets and check collision with player
        for enemy in enemies:
            for enemy_bullet in enemy.bullets:
                enemy_bullet.y += enemy_bullet.speed
                if collision(player, enemy_bullet):
                    # enemy bullet is removed if there is collision
                    enemy.bullets.remove(enemy_bullet)

                    # lower player health
                    if player.health > 1:
                        player.health -= 1
                        # Percentage of maximum health is represented in health bar
                        player.perc_health = player.health / player.max_health * 100
                        if 80 < player.perc_health < 100 and len(player.health_bar) > 4:
                            player.health_bar.pop()
                        if 60 < player.perc_health <= 80 and len(player.health_bar) > 3:
                            player.health_bar.pop()
                        if 40 < player.perc_health <= 60 and len(player.health_bar) > 2:
                            player.health_bar.pop()
                        if 20 < player.perc_health <= 40 and len(player.health_bar) > 1:
                            player.health_bar.pop()
                        if 0 < player.perc_health <= 20 and len(player.health_bar) == 1:
                            player.health_bar.pop()
                    else:
                        game_over = True

                # enemy bullet is removed if it leaves the screen
                if enemy_bullet.y >= H:
                    enemy.bullets.remove(enemy_bullet)

            # Enemy being hit
            for player_bullet in player_bullets:
                if collision(enemy, player_bullet):
                    player_bullets.remove(player_bullet)
                    enemy.health -= 1
                    # Enemy needs to be shot twice to disappear
                    if enemy.health == 1:
                        # Enemy becomes half-transparent after first shot
                        enemy.image = ENEMY_HIT
                    elif enemy.health == 0:
                        enemies.remove(enemy)
                        if len(enemies) == 0:
                            you_won = True

    menu()


# Main menu of the game
def menu():
    title_font = pygame.font.Font('freesansbold.ttf', 32)
    title_text = title_font.render("Can you stop the Space Invaders?", True, (255, 255, 255))
    start_font = pygame.font.Font('freesansbold.ttf', 40)
    start_text = start_font.render("Press the space bar to find out...", True, (255, 255, 255))
    run_menu = True
    while run_menu:
        SCREEN.fill((0, 0, 0))
        SCREEN.blit(title_text, (120, 80))
        SCREEN.blit(start_text, (95, 250))
        SCREEN.blit(PLAYER, (int((W / 2 - 16)), 450))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
    pygame.quit()
    exit()


menu()
