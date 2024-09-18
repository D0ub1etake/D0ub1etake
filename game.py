import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
WHITE = (255, 255, 255)
BG_COLOR = (200, 200, 200)
DIFFICULTY_LEVELS = {
    'easy': (120, 60),  # 时间限制，基础分数
    'normal': (90, 90),
    'hard': (60, 120)
}
TIME_LIMIT = 60  # 默认游戏时间限制，单位秒

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("消除游戏")

# 加载背景图像
background_image = pygame.image.load('background.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.jpg") for i in range(1, 10)]  # 更新为9种图案
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 创建游戏板和消除计数器
board = [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]
eliminate_count = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# 初始化得分和倒计时
score = 0
start_time = time.time()

# 游戏状态
game_state = 'menu'  # 'menu', 'playing', 'game_over', 'victory'

# 初始化选中的图案列表
selected = []


def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))


def check_match():
    global score
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2] and eliminate_count[r1][c1] < 3 and eliminate_count[r2][c2] < 3:
            eliminate_count[r1][c1] += 1
            eliminate_count[r2][c2] += 1
            board[r1][c1] = None
            board[r2][c2] = None
            score += 10  # 每次匹配成功增加得分
            selected.clear()
            if check_victory():
                game_state = 'victory'


def fill_board():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is None and eliminate_count[row][col] < 3:
                board[row][col] = random.choice(patterns)


def check_victory():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] is not None:
                return False
    return True


def draw_score_and_time():
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    time_elapsed = time.time() - start_time
    time_left = max(TIME_LIMIT - time_elapsed, 0)
    time_text = font.render(f"Time: {int(time_left)}s", True, WHITE)
    screen.blit(score_text, (10, 10))  # 绘制得分
    screen.blit(time_text, (WIDTH - 200, 10))  # 绘制时间


def draw_menu():
    screen.blit(background_image, (0, 0))  # 绘制背景图
    font = pygame.font.Font(None, 48)
    start_text = font.render("Click to Start", True, WHITE)
    exit_text = font.render("Click to Exit", True, WHITE)
    screen.blit(start_text, (WIDTH / 2 - start_text.get_width() / 2, HEIGHT / 2 - start_text.get_height() / 2 - 50))
    screen.blit(exit_text, (WIDTH / 2 - exit_text.get_width() / 2, HEIGHT / 2 + start_text.get_height() / 2 + 50))


def draw_difficulty_selection():
    screen.blit(background_image, (0, 0))  # 绘制背景图
    font = pygame.font.Font(None, 48)
    easy_text = font.render("Easy (120s, 60pts)", True, WHITE)
    normal_text = font.render("Normal (90s, 90pts)", True, WHITE)
    hard_text = font.render("Hard (60s, 120pts)", True, WHITE)
    screen.blit(easy_text, (WIDTH / 2 - easy_text.get_width() / 2, HEIGHT / 2 - 120))
    screen.blit(normal_text, (WIDTH / 2 - normal_text.get_width() / 2, HEIGHT / 2-30))
    screen.blit(hard_text, (WIDTH / 2 - hard_text.get_width() / 2, HEIGHT / 2 + 100))


def draw_game_over():
    screen.blit(background_image, (0, 0))  # 绘制背景图
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over!", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2 - 20))
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH / 2 - score_text.get_width() / 2, HEIGHT / 2))
    retry_text = font.render("Click to Retry", True, WHITE)
    exit_text = font.render("Click to Exit", True, WHITE)
    screen.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 2 + 50))
    screen.blit(exit_text, (WIDTH / 2 - exit_text.get_width() / 2, HEIGHT / 2 + 100))


def draw_victory():
    screen.blit(background_image, (0, 0))  # 绘制背景图
    font = pygame.font.Font(None, 48)
    text = font.render("Victory!", True, WHITE)
    screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    retry_text = font.render("Click to Retry", True, WHITE)
    exit_text = font.render("Click to Exit", True, WHITE)
    screen.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 2 + 50))
    screen.blit(exit_text, (WIDTH / 2 - exit_text.get_width() / 2, HEIGHT / 2 + 100))


# 主游戏循环
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_state == 'menu':
                if HEIGHT / 2 - 100 < y < HEIGHT / 2:
                    game_state = 'difficulty_selection'
                elif HEIGHT / 2 < y < HEIGHT / 2 + 100:
                    running = False
            elif game_state == 'difficulty_selection':
                if HEIGHT / 2 - 200 < y < HEIGHT / 2 - 100:
                    TIME_LIMIT, score = DIFFICULTY_LEVELS['easy']
                    game_state = 'playing'
                    start_time = time.time()  # 重置时间
                    score = 60  # 设置基础分数
                    selected.clear()
                    # 重新填充游戏板
                    for row in range(ROWS):
                        for col in range(COLS):
                            board[row][col] = random.choice(patterns)
                            eliminate_count[row][col] = 0
                elif HEIGHT / 2 - 100 < y < HEIGHT / 2:
                    TIME_LIMIT, score = DIFFICULTY_LEVELS['normal']
                    game_state = 'playing'
                    start_time = time.time()  # 重置时间
                    score = 90  # 设置基础分数
                    selected.clear()
                    # 重新填充游戏板
                    for row in range(ROWS):
                        for col in range(COLS):
                            board[row][col] = random.choice(patterns)
                            eliminate_count[row][col] = 0
                elif HEIGHT / 2 + 100 < y < HEIGHT / 2 + 200:
                    TIME_LIMIT, score = DIFFICULTY_LEVELS['hard']
                    game_state = 'playing'
                    start_time = time.time()  # 重置时间
                    score = 120  # 设置基础分数
                    selected.clear()
                    # 重新填充游戏板
                    for row in range(ROWS):
                        for col in range(COLS):
                            board[row][col] = random.choice(patterns)
                            eliminate_count[row][col] = 0
            elif game_state == 'playing':
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= col < COLS and 0 <= row < ROWS:
                    if board[row][col] is not None:
                        if len(selected) < 2:
                            selected.append((row, col))
                        if len(selected) == 2:
                            check_match()
                            fill_board()  # 重新填充空白位置
                            selected.clear()
            elif game_state == 'game_over' or game_state == 'victory':
                if HEIGHT / 2 - 100 < y < HEIGHT / 2 + 100:
                    game_state = 'menu'
                    score = 0
                    selected.clear()
                    for row in range(ROWS):
                        for col in range(COLS):
                            board[row][col] = random.choice(patterns)
                            eliminate_count[row][col] = 0
                elif HEIGHT / 2 + 50 < y < HEIGHT / 2 + 150:
                    running = False

    screen.fill(BG_COLOR)
    if game_state == 'menu':
        draw_menu()
    elif game_state == 'difficulty_selection':
        draw_difficulty_selection()
    elif game_state == 'playing':
        draw_board()
        draw_score_and_time()
    elif game_state == 'game_over':
        draw_game_over()
    elif game_state == 'victory':
        draw_victory()

    pygame.display.flip()

    # 检查游戏是否结束
    if game_state == 'playing' and current_time - start_time >= TIME_LIMIT:
        game_state = 'game_over'

pygame.quit()