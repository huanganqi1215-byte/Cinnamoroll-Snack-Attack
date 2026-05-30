import pygame
import random

pygame.init()
pygame.mixer.init()

# COLOURS - (R, G, B)
# CONSTANTS ALL HAVE CAPS FOR THEIR NAMES
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (237, 190, 176)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
BG_COLOUR = (18, 69, 89)

# CONSTANTS
WIDTH = 800
HEIGHT = 600
SIZE = (WIDTH, HEIGHT)

NUM_INITIAL_ENEMIES = 5
NUM_INITIAL_FOOD = 3


class Player(pygame.sprite.Sprite):
    def __init__(self):
        """Player"""
        super().__init__()

        self.image = pygame.image.load("Images/player.webp")
        self.image = pygame.transform.scale(self.image, (80, 60))

        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 30

        self.x_vel = 0
        self.y_vel = 0
        self.health = 3

    def jump(self):
        """Player jumps"""
        self.y_vel = -17

    def go_left(self):
        """Move left speed"""
        self.x_vel = -5

    def go_right(self):
        """Move right speed"""
        self.x_vel = 5

    def stop(self):
        """Stop moving"""
        self.x_vel = 0

    def update(self):
        """Update player position"""
        self.rect.x += self.x_vel

        self.y_vel += 0.6
        self.rect.y += self.y_vel

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.y_vel = 0

        if self.rect.top < 0:
            self.rect.top = 0
            self.y_vel = 0


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """Create a bullet at given x and y"""
        super().__init__()

        self.image = pygame.image.load("Images/bullet.png")
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

        self.y_vel = -10

    def update(self):
        """Moves from bottom to top"""
        self.rect.y += self.y_vel


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        """Enemy"""
        super().__init__()

        self.image = pygame.image.load("Images/enemy.png")
        self.image = pygame.transform.scale(self.image, (65, 50))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y

        self.x_vel = 3
        self.y_vel = 2
        self.hp = 2

    def update(self):
        """Move and bounce off the screen"""
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.x_vel = -self.x_vel

        if self.rect.left <= 0:
            self.rect.left = 0
            self.x_vel = -self.x_vel

        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.y_vel = -self.y_vel

        if self.rect.top <= 0:
            self.rect.top = 0
            self.y_vel = -self.y_vel


class Food(pygame.sprite.Sprite):
    def __init__(self):
        """food"""
        super().__init__()

        self.image = pygame.image.load("Images/food.png")
        self.image = pygame.transform.scale(self.image, (28, 28))

        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-HEIGHT, 0)

        self.y_vel = 3

    def update(self):
        """Move food from top to bottom"""
        self.rect.y += self.y_vel

        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-HEIGHT, 0)


def main():
    # Creating the Screen
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Cinnamoroll Snack Attack")

    bg = pygame.image.load("Images/BG.jpg")
    bg = pygame.transform.scale(bg, SIZE)

    # Sounds
    start_sound = pygame.mixer.Sound("Sounds/game_start.mp3")
    eat_sound = pygame.mixer.Sound("Sounds/eating.mp3")
    shoot_sound = pygame.mixer.Sound("Sounds/bullet.mp3")
    lose_sound1 = pygame.mixer.Sound("Sounds/game_over1.mp3")
    lose_sound2 = pygame.mixer.Sound("Sounds/game_over2.mp3")

    # BGM
    pygame.mixer.music.load("Sounds/background_music.MP3")

    # Variables
    done = False
    game_over = False
    win = False
    score = 0
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    bullet_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    food_sprites = pygame.sprite.Group()

    # Create player
    player = Player()
    all_sprites.add(player)

    # Create food
    for _ in range(NUM_INITIAL_FOOD):
        food = Food()
        all_sprites.add(food)
        food_sprites.add(food)

    # Create enemies
    for i in range(NUM_INITIAL_ENEMIES):
        enemy = Enemy(80 + i * 140, 50)
        all_sprites.add(enemy)
        enemy_sprites.add(enemy)

    # Start sounds
    start_sound.play()
    pygame.mixer.music.play()

    # MAIN GAME LOOP
    while not done:
        # MAIN EVENT LISTENER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if not game_over and not win:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.go_left()

                    if event.key == pygame.K_RIGHT:
                        player.go_right()

                    if event.key == pygame.K_UP:
                        player.jump()

                    if event.key == pygame.K_SPACE:
                        player_x = player.rect.centerx
                        player_y = player.rect.top

                        bullet = Bullet(player_x, player_y)
                        all_sprites.add(bullet)
                        bullet_sprites.add(bullet)

                        shoot_sound.play()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and player.x_vel < 0:
                        player.stop()

                    if event.key == pygame.K_RIGHT and player.x_vel > 0:
                        player.stop()

        # GAME LOGIC
        if not game_over and not win:
            all_sprites.update()

            # Collision between player and food
            foods_hit = pygame.sprite.spritecollide(player, food_sprites, False)

            for food in foods_hit:
                score += 1
                food.rect.x = random.randrange(0, WIDTH - food.rect.width)
                food.rect.y = random.randrange(-HEIGHT, 0)
                eat_sound.play()

            if score >= 8:
                win = True

            # Collision between bullet and enemy
            for bullet in bullet_sprites:
                enemy_hit = pygame.sprite.spritecollide(
                    bullet, enemy_sprites, False
                )

                for enemy in enemy_hit:
                    enemy.hp -= 1

                    if enemy.hp == 0:
                        all_sprites.remove(enemy)
                        enemy_sprites.remove(enemy)

                if bullet.rect.bottom < 0 or enemy_hit:
                    bullet_sprites.remove(bullet)
                    all_sprites.remove(bullet)

            # Collision between player and enemy
            enemy_hit = pygame.sprite.spritecollide(player, enemy_sprites, False)

            for enemy in enemy_hit:
                player.health -= 1
                all_sprites.remove(enemy)
                enemy_sprites.remove(enemy)

            if player.health <= 0:
                game_over = True
                pygame.mixer.music.stop()
                lose_sound1.play()
                lose_sound2.play()

        # DRAWING TO SCREEN
        screen.blit(bg, (0, 0))
        all_sprites.draw(screen)

        score_text = font.render(f"Food: {score}/8", True, WHITE)
        health_text = font.render(f"Health: {player.health}", True, WHITE)

        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 45))

        if game_over:
            text = big_font.render("GAME OVER", True, RED)

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )

        if win:
            text = big_font.render("WIN", True, WHITE)

            screen.blit(
                text,
                (
                    WIDTH // 2 - text.get_width() // 2,
                    HEIGHT // 2 - text.get_height() // 2,
                ),
            )

        # Update screen
        pygame.display.flip()

        # CLOCK TICK
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()