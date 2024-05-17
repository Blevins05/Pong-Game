import pygame, sys, random, time 
pygame.init()

def draw(surface, rectangle):
    screen.blit(surface, rectangle)

def draw_line(screen, color, start_pos, end_pos, width):
    pygame.draw.line(screen, color, start_pos, end_pos, width)

def player_animation():
    player_paddle.y += player_speed
    if player_paddle.top < 0:
        player_paddle.top = 0
    if player_paddle.bottom >= screen_height:
        player_paddle.bottom = screen_height

def update_speed():
    global ball_speed_x, ball_speed_y
    ball_speed_y *=1.0005
    ball_speed_x *=1.0005

def opponent_ai():
    if opponent_paddle.top < ball_rect.y:
        opponent_paddle.y += opponent_speed
    if opponent_paddle.bottom > ball_rect.y:
        opponent_paddle.y -= opponent_speed

    if opponent_paddle.top <= 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom >= screen_height:
        opponent_paddle.bottom = screen_height

def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, n_collisions
    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y
    if ball_rect.top <= 0 or ball_rect.bottom >= screen_height:
        ball_speed_y *= -1
    
    # Player scores
    if ball_rect.left <= 0:
        player_score += 1
        pygame.mixer.Sound.play(score_sound)
        ball_restart()
    
    # Opponent scores
    if ball_rect.right >= screen_width:
        opponent_score += 1
        pygame.mixer.Sound.play(score_sound)
        ball_restart()
        
    # Ball collisions with paddles
    if ball_rect.colliderect(player_paddle) and ball_speed_x > 0:
        if ball_rect.right >= player_paddle.left:  # Check if ball is penetrating paddle
            ball_rect.right = player_paddle.left  # Adjust ball position
            ball_speed_x *= -1
    if ball_rect.colliderect(opponent_paddle) and ball_speed_x < 0:
        if ball_rect.left < opponent_paddle.right:  # Check if ball is penetrating paddle
            ball_rect.left = opponent_paddle.right  # Adjust ball position
            ball_speed_x *= -1
    if ball_rect.colliderect(player_paddle) or ball_rect.colliderect(opponent_paddle):
        ball_speed_x *= -1
        n_collisions += 1
def reset_point():
    ball_rect.center = (starting_ball_x, starting_ball_y)
    pass

def ball_restart():
    global ball_speed_x, ball_speed_y
    ball_rect.center = (starting_ball_x, starting_ball_y)
    ball_speed_y = 7 * random.choice((1, -1))
    ball_speed_x = 7 * random.choice((1, -1))


def display_score(score, text, x_pos, y_pos):
    font = pygame.font.SysFont('sans serif', 30)
    score_surf = font.render(f'{text}: {score}', False, white)
    score_rect = score_surf.get_rect(center=(x_pos, y_pos))
    draw(score_surf, score_rect)

def menu():
    title_font = pygame.font.SysFont('sans serif', 100)
    msg_font = pygame.font.SysFont('sans serif', 45)
    title = title_font.render('Pong Game',False, black)
    title_rect = title.get_rect(center = (375, 90))
    pong = pygame.image.load('pongpaddle.jpg').convert_alpha()
    smaller_pong = pygame.transform.rotozoom(pong, 315, 2/5)
    pong_rect = smaller_pong.get_rect(center = (365, 380))
    msg = msg_font.render('Player vs AI: Press space to start', False, black)
    msg_rect = msg.get_rect(center = (375, 165))
    pause_msg = msg_font.render('-Use escape to pause', False, black)
    pause_msg_rect = pause_msg.get_rect(center = (360, 200))
    draw(smaller_pong, pong_rect)
    draw(title, title_rect)
    draw(msg, msg_rect)
    draw(pause_msg, pause_msg_rect)
def game_won():
    global game_active
    winner = ''
    player = 'Player'
    opponent = 'AI'
    win_font = pygame.font.SysFont('sans serif', 80)
    
    if opponent_score == 10:
        winner = opponent
    elif player_score == 10:
        winner = player
    
    if winner:
        win = win_font.render(f'{winner} wins!', False, cyan)
        win_rect = win.get_rect(center=(375, 250))
        draw(win, win_rect)
        pygame.display.flip()
        time.sleep(1.5)
        pygame.quit()
        sys.exit()

def toggle_pause():
    global game_paused
    game_paused = not game_paused

### ----- ###

clock = pygame.time.Clock()
screen_width, screen_height = 750, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')

game_active = False
game_paused = False
framerate = 60  # ingame fps
n_collisions = 0

# game colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
grey = (128, 128, 128)
light_grey = (200, 200, 200)
cyan = (0, 255, 255)
bg_color = pygame.Color('grey12')

# game rectangles
starting_ball_x, starting_ball_y = 368, 250
ball_surface = pygame.image.load('Ball.png').convert_alpha()
ball_smaller = pygame.transform.rotozoom(ball_surface, 0, 0.5)
ball_rect = ball_smaller.get_rect(center=(starting_ball_x, starting_ball_y))

player_paddle = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
opponent_paddle = pygame.Rect(10, screen_height / 2 - 70, 10, 140)

# game variables
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

player_score, opponent_score = 0, 0

# sounds
score_sound = pygame.mixer.Sound('score.ogg')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_speed -= 7
            if event.key == pygame.K_DOWN:
                player_speed += 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_speed += 7
            if event.key == pygame.K_DOWN:
                player_speed -= 7
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_paused:
                game_active = True
            if event.key == pygame.K_ESCAPE:  # toggle pause with 'ESC' key
                toggle_pause()
                
    if not game_paused:
        screen.fill(bg_color)
        if game_active:
            # ingame logic
            player_animation()
            ball_animation()
            opponent_ai()
            update_speed()
            # drawing the court
            draw(ball_surface, ball_rect)
            draw_line(screen, white, (375, 0), (375, 500), 1)

            # draw paddles

            pygame.draw.rect(screen, light_grey, player_paddle)
            pygame.draw.rect(screen, light_grey, opponent_paddle)

            # display scores
            display_score(player_score, 'Player', screen_width - 60, 25)
            display_score(opponent_score, 'AI', 60, 25)

            # checking 
            game_won()
        else:
            screen.fill(white)
            menu()
    else:
        font = pygame.font.SysFont('sans serif', 80)
        pause_surf = font.render('Paused', False, red)
        pause_rect = pause_surf.get_rect(center=(screen_width/2, screen_height/2))
        draw(pause_surf, pause_rect)
    pygame.display.flip()
    clock.tick(framerate)