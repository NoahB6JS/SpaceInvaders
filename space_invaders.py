import pygame 
import sys
import random

pygame.init()
pygame.mixer.init()

# ------------------ IMAGES ------------------
player_img = pygame.image.load("app&webdev/spaceinvaders/images/player.png")
life_icon = pygame.transform.scale(player_img, (20, 20)) 

# ------------------ SOUNDS ------------------

shoot_sound = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/invaderkilled.wav")
shoot_sound.set_volume(0.3)


enemy_collision_sound = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/invaderkilled.wav")
shoot_sound.set_volume(0.4)


pygame.mixer.music.load("app&webdev/spaceinvaders/sound/soundtrack.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

fast1 = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/fastinvader1.wav")
fast2 = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/fastinvader2.wav")
fast3 = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/fastinvader3.wav")

explosion_sound = pygame.mixer.Sound("app&webdev/spaceinvaders/sound/explosion.wav")

# ------------------ CLASSES ------------------

class Player:
    def __init__(self, x, y, img, l, h, score):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (l, h))
        self.l = l
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        self.score = score
        self.lives = 3  
    
    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)

class Invader:
    def __init__(self, x, y, img, l, h):
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (l, h))
        self.l = l
        self.h = h
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)
        self.speed = 0.75
        self.direction = -1  # Add this

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.l, self.h)

class Bullet:
    def __init__(self, x, y, w, h, s):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = s
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class EnemyBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 4
        self.h = 10
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def update(self):
        self.y += self.speed
        self.rect.topleft = (self.x, self.y)


# Screen setup
SCREEN_HEIGHT = 500
SCREEN_WIDTH = 500
screen = pygame.display.set_mode([SCREEN_HEIGHT, SCREEN_WIDTH])

clock = pygame.time.Clock()
FPS = 60

bg = pygame.image.load("app&webdev/spaceinvaders/images/bg.jpg")

font_path = "app&webdev/spaceinvaders/fonts/PressSTart2P.ttf"
font = pygame.font.SysFont(font_path, 20)
lives_font = pygame.font.SysFont(font_path, 20)

invader_startrow = 10
invader_endrow = 300
invader_startcol = 100
invader_endcol = 400 

score = 0
invaders = []

invader_image = pygame.image.load("app&webdev/spaceinvaders/images/defender.png")


player = Player((SCREEN_WIDTH/2)-(35/2), SCREEN_HEIGHT - 100,
                pygame.image.load("app&webdev/spaceinvaders/images/player.png"),
                35, 30, score)

bullet = Bullet(player.x, player.y, 3, 8, 10)
fired = False
collide = False

enemy_bullets = []


# ------------------ SCREENS ------------------

def start_screen():

    font_path = "app&webdev/spaceinvaders/fonts/PressStart2P.ttf"

    # Load the actual TTF file directly
    title_font = pygame.font.Font(font_path, 60)
    info_font = pygame.font.Font(font_path, 30)


    font_path = "app&webdev/spaceinvaders/fonts/PressSTart2P.ttf"
    font = pygame.font.SysFont(font_path, 20)

    title_font = pygame.font.Font(font, 60)
    info_font = pygame.font.Font(None, 30)

    title_text = title_font.render("SPACE INVADERS", True, (255, 255, 255))
    info_text = info_font.render("Press SPACE to Start", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        
        screen.blit(bg, (0, 0))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 150))
        screen.blit(info_text, (SCREEN_WIDTH//2 - info_text.get_width()//2, 300))
        pygame.display.update()


def end_screen():
    end_font = pygame.font.Font(None, 60)

    end_text = end_font.render("GAME OVER", True, (255, 255, 255))
    score_text_render = end_font.render(f"Final Score: {score}", True, (255, 255, 255))
    back_text = end_font.render("Press SPACE to Restart", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        screen.blit(bg, (0, 0))
        screen.blit(end_text, (SCREEN_WIDTH//2 - end_text.get_width()//2, 120))
        screen.blit(score_text_render, (SCREEN_WIDTH//2 - score_text_render.get_width()//2, 230))
        screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, 340))
        pygame.display.update()

def win_screen():
    end_font = pygame.font.Font(None, 60)

    end_text = end_font.render("WINNER!!", True, (255, 255, 255))
    score_text_render = end_font.render(f"Final Score: {score}", True, (255, 255, 255))
    back_text = end_font.render("Press SPACE to Restart", True, (255, 255, 255))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        screen.blit(bg, (0, 0))
        screen.blit(end_text, (SCREEN_WIDTH//2 - end_text.get_width()//2, 120))
        screen.blit(score_text_render, (SCREEN_WIDTH//2 - score_text_render.get_width()//2, 230))
        screen.blit(back_text, (SCREEN_WIDTH//2 - back_text.get_width()//2, 340))
        pygame.display.update()


# ------------------ GAME RESET ------------------

def draw_invaders():
    invaders.clear()

    invader_image = pygame.image.load("app&webdev/spaceinvaders/images/defender.png")

    start_x = 100
    start_y = 30
    rows = 5
    cols = 8
    spacing_x = 40
    spacing_y = 55

    for r in range(rows):
        for c in range(cols):
            x = start_x + c * spacing_x
            y = start_y + r * spacing_y
            invaders.append(Invader(x, y, invader_image, 30, 30))


def reset_game():
    global score, invaders, fired, collide, enemy_bullets, invader_startrow, invader_endrow, invader_startcol, invader_endcol

    score = 0
    fired = False
    collide = False
    enemy_bullets.clear()

    player.x = (SCREEN_WIDTH/2)-(35/2)
    player.y = SCREEN_HEIGHT - 100
    player.lives = 3
    player.update()

    bullet.x = -10
    bullet.y = -10



    invaders.clear()
    draw_invaders()


# Start game
draw_invaders()
start_screen()


# ------------------ MAIN GAME LOOP ------------------

running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fired = True
                collide = False
                bullet.x = player.x + player.l // 2
                bullet.y = player.y
                shoot_sound.play()
    
    if len(invaders) == 0:
        win_screen()
        reset_game()


    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player.x -= 7

    if keys[pygame.K_RIGHT]:
        player.x += 7

    player.update()
    

   

    # -------- DRAW EVERYTHING --------
    screen.blit(bg, (0, 0))
    screen.blit(player.img, (player.x, player.y))


    # Score & lives
    screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    for i in range(player.lives):
    # Space out each icon horizontally
        x = 390 + i * 40  # 20px padding + 50px between each icon
        y = 10
        screen.blit(life_icon, (x, y))


    # -------- DRAW INVADERS --------
    for inv in invaders:
        screen.blit(inv.img, (inv.x, inv.y))
        inv.update()

    # -------- PLAYER BULLET --------
    if fired:
        pygame.draw.rect(screen, (255, 0, 0), bullet.rect)
        bullet.y -= bullet.speed
        bullet.update()

        if bullet.y < 0:
            fired = False


        # -------- BULLET COLLISION --------
    for invader in invaders[:]:
        if bullet.rect.colliderect(invader.rect) and not collide:
            invaders.remove(invader)
            enemy_collision_sound.play()
            score += 1
            if score >= 35:
                for i in invaders:
                    i.speed = 2.5
                    if score == 35:
                        fast3.play()
            elif score >= 25:
                for i in invaders:
                    i.speed = 2
                    if score == 25:
                        fast3.play()
            elif score >= 15:
                for i in invaders:
                    i.speed = 1.5
                    if score == 15:
                        fast2.play
            elif score >= 5:
                for i in invaders:
                    i.speed = 1
                    if score == 5:
                        fast1.play()

            collide = True
            bullet.x = -10
            bullet.y = -10


    # -------- ENEMY SHOOTING --------
    if len(invaders) > 0:
        if random.randint(1, 120) == 1:
            shooter = random.choice(invaders)
            enemy_bullets.append(
                EnemyBullet(shooter.x + shooter.l//2, shooter.y + shooter.h)
            )

    # -------- ENEMY BULLET UPDATE --------
    for eb in enemy_bullets[:]:
        pygame.draw.rect(screen, (255, 255, 0), eb.rect)
        eb.update()

        if eb.y > SCREEN_HEIGHT:
            enemy_bullets.remove(eb)

        if eb.rect.colliderect(player.rect):
            enemy_bullets.remove(eb)
            player.lives -= 1
            explosion_sound.play()

            if player.lives <= 0:
                end_screen()
                reset_game()

    # -------- MOVE INVADERS -------
    for inv in invaders:
        inv.x += inv.speed * inv.direction
        inv.update()

    for inv in invaders:
        if inv.x <= 0 or inv.x + inv.l >= SCREEN_WIDTH:
            for i in invaders:
                i.direction *= -1  
                i.y += 10
                if i.y + i.h >= player.y:
                    end_screen()
                    reset_game()
            break

    pygame.display.flip()
    clock.tick(FPS)
