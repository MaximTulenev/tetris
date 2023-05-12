import pygame, random, sys, time
from pygame.locals import *

# цвета

# синий, зелёный, красный, жёлтый
colors = [(0, 0, 255),
          (0, 255, 0),
          (255, 0, 0),
          (255, 255, 0)]

# порядок цветов тот же, что и в прошлом массиве, отличие в том, что здесь цвета светлые
light_colors = [(30, 30, 255),
                (50, 255, 50),
                (255, 30, 30),
                (255, 255, 30)]

WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)

brd_color = WHITE
txt_color = WHITE
bg_color = BLACK
title_color = colors[3]
info_color = colors[0]

# окно

window_W = 990
window_H = 650
cup_W = 15
cup_H = 20
block = 20
window_full = pygame.display.set_mode((window_W, window_H))
pygame.display.set_caption('Tetris')

side_margin = int((window_W - cup_W * block) / 2)
top_margin = int((window_H - cup_H * block))

side_move = 0.15
down_move = 0.1

# window_line_1 = pygame.draw.line(window_full, WHITE, (side_margin, window_H), (side_margin, window_H - top_margin * 2), 2),
# window_line_2 = pygame.draw.line(window_full, WHITE, (side_margin + cup_W * block, window_H - top_margin * 2), (side_margin + cup_W * block, window_H), 2)
# window_line_3 = pygame.draw.line(window_full, WHITE, (side_margin, window_H - top_margin * 2), (side_margin + cup_W * block, window_H - top_margin * 2), 2)

# шаблоны фигур

fig_w = 5
fig_h = 5
empty = '-'

figures = {'S': [['-----',
                  '-----',
                  '--xx-',
                  '-xx--',
                  '-----'],
                 ['-----',
                  '--x--',
                  '--xx-',
                  '---x-',
                  '-----']],
           'Z': [['-----',
                  '-----',
                  '-xx--',
                  '--xx-',
                  '-----'],
                 ['-----',
                  '--x--',
                  '-xx--',
                  '-x---',
                  '-----']],
           'J': [['-----',
                  '-x---',
                  '-xxx-',
                  '-----',
                  '-----'],
                 ['-----',
                  '--xx-',
                  '--x--',
                  '--x--',
                  '-----'],
                 ['-----',
                  '-----',
                  '-xxx-',
                  '---x-',
                  '-----'],
                 ['-----',
                  '--x--',
                  '--x--',
                  '-xx--',
                  '-----']],
           'L': [['-----',
                  '---x-',
                  '-xxx-',
                  '-----',
                  '-----'],
                 ['-----',
                  '--x--',
                  '--x--',
                  '--xx-',
                  '-----'],
                 ['-----',
                  '-----',
                  '-xxx-',
                  '-x---',
                  '-----'],
                 ['-----',
                  '-xx--',
                  '--x--',
                  '--x--',
                  '-----']],
           'I': [['--x--',
                  '--x--',
                  '--x--',
                  '--x--',
                  '-----'],
                 ['-----',
                  '-----',
                  'xxxx-',
                  '-----',
                  '-----']],
           'O': [['-----',
                  '-----',
                  '-xx--',
                  '-xx--',
                  '-----']],
           'T': [['-----',
                  '--x--',
                  '-xxx-',
                  '-----',
                  '-----'],
                 ['-----',
                  '--x--',
                  '--xx-',
                  '--x--',
                  '-----'],
                 ['-----',
                  '-----',
                  '-xxx-',
                  '--x--',
                  '-----'],
                 ['-----',
                  '--x--',
                  '-xx--',
                  '--x--',
                  '-----']]}

# экран паузы

def pause_screen():
    p_scr = pygame.Surface((990, 650), pygame.SRCALPHA)
    p_scr.fill((0, 0, 0, 127))
    window_full.blit(p_scr, (0, 0))

# основная функция игры

def main():
    global fps_clock, basic_font, big_font
    pygame.init()
    fps_clock = pygame.time.Clock()
    basic_font = pygame.font.SysFont('arial', 20)
    big_font = pygame.font.SysFont('verdana', 45)
    show_text('TETRIS')
    while True:
        # pygame.display.update()
        global fps
        fps = 25
        pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        run_tetris()
        pause_screen()
        show_text('Игра закончена')

# функция с процессом игры

def run_tetris():
    cup = empty_cup()
    last_move_down = time.time()
    last_move_side = time.time()
    last_fall = time.time()
    going_down = False
    going_left = False
    going_right = False
    score = 0
    level, fall_speed = calc_speed(score)
    falling_fig = get_new_fig()
    next_fig = get_new_fig()

    while True:
        if falling_fig == None:
            falling_fig = next_fig
            last_fall = time.time()

            if not check_position(cup, falling_fig):
                quit_game()

        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause_screen()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_move_side = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and check_position(cup, falling_fig, adjX=-1):
                    falling_fig['x'] += 1
                    going_left = True
                    going_right = False
                    last_move_side = time.time()
                elif event.key == K_RIGHT and check_position(cup, falling_fig, adjX=1):
                    falling_fig['x'] += 1
                    going_left = False
                    going_right = True
                    last_move_side = time.time()
                elif event.key == K_UP:
                    falling_fig['rotation'] = (falling_fig['rotation'] + 1) % len(figures[falling_fig['shape']])
                    if not check_position(cup, falling_fig):
                        falling_fig['rotation'] = (falling_fig['rotation'] - 1) % len(figures[falling_fig['shape']])
                elif event.key == K_DOWN:
                    going_down = True
                    if check_position(cup, falling_fig, adjY=1):
                        falling_fig['y'] += 1
                    last_move_down = time.time()
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_H):
                        if not check_position(cup, falling_fig, adjY=i):
                            break
                    falling_fig['y'] += i - 1
        if (going_left or going_right) and time.time() - last_move_side > side_move:
            if going_left and check_position(cup, falling_fig, adjX=-1):
                falling_fig['x'] -= 1
            elif going_right and check_position(cup, falling_fig, adjX=1):
                falling_fig['x'] += 1
            last_move_side = time.time()

        if going_down and time.time() -last_move_down > down_move and check_position(cup, falling_fig, adjY=1):
            falling_fig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:
            if not check_position(cup, falling_fig, adjY=1):
                add_to_cup(cup, falling_fig)
                score += clear_completed(cup)
                level, fall_speed = calc_speed(score)
                falling_fig = None
            else:
                falling_fig['y'] += 1
                last_fall = time.time()

        window_full.fill(bg_color)
        draw_title()
        gamecup(cup)
        draw_info(score, level)
        draw_next_fig(next_fig)
        if falling_fig != None:
            draw_fig(falling_fig)
        pygame.display.update()
        fps_clock.tick(fps)




# второстепенные функции

def txt_objects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()

def stop_game():
    return pygame.quit(), sys.exit()

def check_keys():
    quit.game()
    for event in pygame.event.get():
        if event.type == K_SPACE:
            continue
        return event.key
    return None

def show_text(text):
    title_surf, title_rect = txt_objects(text, big_font, title_color)
    title_rect.center = (int(window_W / 2) - 3, int(window_H / 2) - 3)
    window_full.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = txt_objects('Нажмите пробел для продолжения', basic_font, title_color)
    press_key_rect.center = (int(window_W / 2), int(window_H / 2) + 100)
    window_full.blit(press_key_surf, press_key_rect)

def quit_game():
    for event in pygame.event.get(QUIT):
        stop_game()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop_game()
        pygame.event.post(event)

def calc_speed(score):
    level = int(score / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed

def get_new_fig():
    shape = random.choice(list(figures.keys()))
    new_figure = {'shape': shape,
                  'rotation': random.randint(0, len(figures[shape]) - 1),
                  'x': int(cup_W / 2) - int(fig_h / 2),
                  'y': -2,
                  'color': random.randint(0, len(colors) - 1)}
    return new_figure

def add_to_cup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']

def empty_cup():
    cup = []
    for i in range(cup_W):
        cup.append([empty] * cup_H)
    return cup

def in_cup(x, y):
    return x >= 0 and x < cup_W and y < cup_H

def check_position(cup, fig, adjX=0, adjY=0):
    for x in range(fig_w):
        for y in range(fig_h):
            above_cup = y + fig['y'] + adjY < 0
            if above_cup or figures[fig['shape']][fig['rotation']][y][x] == empty:
                continue
            if not in_cup(x + fig['x'] + adjX, y + fig['y'] + adjY):
                return False
            if cup[x + fig['x'] + adjX][y + fig['y'] + adjY] != empty:
                return False
    return True

def is_completed(cup, y):
    for x in range(cup_W):
        if cup[x][y] == empty:
            return False
        return True

def clear_completed(cup):
    removed_lines = 0
    y = cup_H - 1
    while y >= 0:
        if is_completed(cup, y):
            for push_down_y in range(y, 0, -1):
                for x in range(cup_W):
                    cup[x][0] = empty
                removed_lines += 1
            else:
                y -= 1
    return removed_lines

def convert_coordinates(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))

def draw_block(block_x, block_y, color, pixelx=None, pixely=None):
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixel_y = convert_coordinates(block_x, block_y)
    pygame.draw.rect(window_full, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pygame.draw.rect(window_full, light_colors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pygame.draw.rect(window_full, colors[color], (pixelx + block / 2, pixely + block / 2), 5)

def gamecup(cup):
    pygame.draw.rect(window_full, brd_color, (side_margin - 4, top_margin - 4, (cup_W * block) + 8, (cup_H * block) + 8), 5)
    pygame.draw.rect(window_full, bg_color, (side_margin, top_margin, block * cup_W, block * cup_H))
    for x in range(cup_W):
        for y in range(cup_H):
            draw_block(x, y, cup[x][y])

def draw_title():
    title_surf = big_font.render('ТЕТРИС', True, title_color)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (window_W - 425, 30)
    window_full.blit(title_surf, title_rect)

def draw_info(score, level):
    score_surf = basic_font.render(f'Баллы: {score}', True, txt_color)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (window_W - 550, 180)
    window_full.blit(score_surf, score_rect)

    level_surf = basic_font.render(f'Уровень: {level}', True, txt_color)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (window_W - 550, 250)
    window_full.blit(level_surf, level_rect)

    pause_surf = basic_font.render(f'Пауза - пробел', True, info_color)
    pause_rect = pause_surf.get_rect()
    pause_rect.topleft = (window_W - 550, 420)
    window_full.blit(pause_surf, pause_rect)

    escb_surf = basic_font.render(f'Выход - Esc', True, info_color)
    escb_rect = escb_surf.get_rect()
    escb_rect.topleft = (window_W - 550, 450)
    window_full.blit(escb_surf, escb_rect)

def draw_fig(fig, pixelx=None, pixely=None):
    fig_to_draw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_coordinates(fig['x'], fig['y'])
    for x in range(fig_w):
        for y in range(fig_h):
            if fig_to_draw[y][x] != empty:
                draw_block(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))

def draw_next_fig(fig):
    next_surf = basic_font.render('Следующая: ', True, txt_color)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (window_W - 150, 180)
    draw_fig(fig, pixelx=window_W-150, pixely=230)

main()
