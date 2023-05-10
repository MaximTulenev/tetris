import pygame, random, sys, time
from pygame.locals import *

# цвета

BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (30, 30, 255)
LIGHT_GREEN = (50, 255, 50)
LIGHT_RED = (255, 30, 30)
LIGHT_YELLOW = (255, 255, 30)
WHITE = (255, 255, 255)
GRAY = (185, 185, 185)
BLACK = (0, 0, 0)

brd_color = WHITE
txt_color = WHITE
bg_color = BLACK
title_color = YELLOW
info_color = BLUE

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

window_line_1 = pygame.draw.line(window_full, WHITE, (side_margin, window_H), (side_margin, window_H - top_margin * 2), 2),
window_line_2 = pygame.draw.line(window_full, WHITE, (side_margin + cup_W * block, window_H - top_margin * 2), (side_margin + cup_W * block, window_H), 2)
window_line_3 = pygame.draw.line(window_full, WHITE, (side_margin, window_H - top_margin * 2), (side_margin + cup_W * block, window_H - top_margin * 2), 2)

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
        pygame.display.update()
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
    falling_fig, next_fig = get_new_fig()

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
        fps_clock.tick(fps)




# другие функции

