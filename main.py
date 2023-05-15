import pygame
import random, time, sys
from pygame.locals import *

fps = 25
window_w = 600
window_h = 500
block = 20
cup_h, cup_w = 20, 10

side_freq, down_freq = 0.15, 0.1  # передвижение в сторону и вниз

side_margin = (window_w - cup_w * block) / 2
top_margin = window_h - (cup_h * block) - 5

# цвета

colors = ((0, 0, 225), (0, 225, 0), (225, 0, 0), (225, 225, 0))  # синий, зеленый, красный, желтый
lightcolors = ((30, 30, 255), (50, 255, 50), (255, 30, 30), (255, 255, 30))  # светло-синий, светло-зеленый, светло-красный, светло-желтый

white, gray, black = (255, 255, 255), (185, 185, 185), (0, 0, 0)
brd_color, bg_color, txt_color, title_color, info_color = white, black, white, colors[3], colors[0]

fig_w, fig_h = 5, 5
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


def pause_screen():
    pause = pygame.Surface((600, 500), pygame.SRCALPHA)
    pause.fill((0, 0, 255, 127))
    display_surf.blit(pause, (0, 0))


def main():
    global fps_clock, display_surf, basic_font, big_font
    pygame.init()
    fps_clock = pygame.time.Clock()
    display_surf = pygame.display.set_mode((window_w, window_h))
    basic_font = pygame.font.SysFont('arial', 20)
    big_font = pygame.font.SysFont('verdana', 45)
    pygame.display.set_caption('Тетрис Lite')
    show_text('Тетрис Lite')
    while True:  # начинаем игру
        run_tetris()
        pause_screen()
        show_text('Игра закончена')


def run_tetris():
    cup = emptycup()
    last_move_down = time.time()
    last_side_move = time.time()
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
            # если нет падающих фигур, генерируем новую
            falling_fig = next_fig
            next_fig = get_new_fig()
            last_fall = time.time()

            if not check_position(cup, falling_fig):
                return  # если на игровом поле нет свободного места - игра закончена
        quit_game()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    pause_screen()
                    show_text('Пауза')
                    last_fall = time.time()
                    last_move_down = time.time()
                    last_side_move = time.time()
                elif event.key == K_LEFT:
                    going_left = False
                elif event.key == K_RIGHT:
                    going_right = False
                elif event.key == K_DOWN:
                    going_down = False

            elif event.type == KEYDOWN:
                # перемещение фигуры вправо и влево
                if event.key == K_LEFT and check_position(cup, falling_fig, adjX=-1):
                    falling_fig['x'] -= 1
                    going_left = True
                    going_right = False
                    last_side_move = time.time()

                elif event.key == K_RIGHT and check_position(cup, falling_fig, adjX=1):
                    falling_fig['x'] += 1
                    going_right = True
                    going_left = False
                    last_side_move = time.time()

                # поворачиваем фигуру, если есть место
                elif event.key == K_UP:
                    falling_fig['rotation'] = (falling_fig['rotation'] + 1) % len(figures[falling_fig['shape']])
                    if not check_position(cup, falling_fig):
                        falling_fig['rotation'] = (falling_fig['rotation'] - 1) % len(figures[falling_fig['shape']])

                # ускоряем падение фигуры
                elif event.key == K_DOWN:
                    going_down = True
                    if check_position(cup, falling_fig, adjY=1):
                        falling_fig['y'] += 1
                    last_move_down = time.time()

                # мгновенный сброс вниз
                elif event.key == K_RETURN:
                    going_down = False
                    going_left = False
                    going_right = False
                    for i in range(1, cup_h):
                        if not check_position(cup, falling_fig, adjY=i):
                            break
                    falling_fig['y'] += i - 1

        # управление падением фигуры при удержании клавиш
        if (going_left or going_right) and time.time() - last_side_move > side_freq:
            if going_left and check_position(cup, falling_fig, adjX=-1):
                falling_fig['x'] -= 1
            elif going_right and check_position(cup, falling_fig, adjX=1):
                falling_fig['x'] += 1
            last_side_move = time.time()

        if going_down and time.time() - last_move_down > down_freq and check_position(cup, falling_fig, adjY=1):
            falling_fig['y'] += 1
            last_move_down = time.time()

        if time.time() - last_fall > fall_speed:  # свободное падение фигуры
            if not check_position(cup, falling_fig, adjY=1):  # проверка "приземления" фигуры
                add_to_cup(cup, falling_fig)  # фигура приземлилась, добавляем ее в содержимое стакана
                score += clear_completed(cup)
                level, fall_speed = calc_speed(score)
                falling_fig = None
            else:  # фигура пока не приземлилась, продолжаем движение вниз
                falling_fig['y'] += 1
                last_fall = time.time()

        # рисуем окно игры со всеми надписями
        display_surf.fill(bg_color)
        draw_title()
        game_cup(cup)
        draw_info(score, level)
        draw_next_fig(next_fig)
        if falling_fig != None:
            draw_fig(falling_fig)
        pygame.display.update()
        fps_clock.tick(fps)


def txt_objects(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def stop_game():
    pygame.quit()
    sys.exit()


def check_keys():
    quit_game()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
        if event.type == KEYDOWN:
            continue
        return event.key
    return None


def show_text(text):
    title_surf, title_rect = txt_objects(text, big_font, title_color)
    title_rect.center = (int(window_w / 2) - 3, int(window_h / 2) - 3)
    display_surf.blit(title_surf, title_rect)

    press_key_surf, press_key_rect = txt_objects('Нажмите любую клавишу для продолжения', basic_font, title_color)
    press_key_rect.center = (int(window_w / 2), int(window_h / 2) + 100)
    display_surf.blit(press_key_surf, press_key_rect)

    while check_keys() == None:
        pygame.display.update()
        fps_clock.tick()


def quit_game():
    for event in pygame.event.get(QUIT):  # проверка всех событий, приводящих к выходу из игры
        stop_game()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            stop_game()
        pygame.event.post(event)


def calc_speed(score):
    # вычисляет уровень
    level = int(score / 10) + 1
    fall_speed = 0.27 - (level * 0.02)
    return level, fall_speed


def get_new_fig():
    # возвращает новую фигуру со случайным цветом и углом поворота
    shape = random.choice(list(figures.keys()))
    new_figure = {'shape': shape,
                 'rotation': random.randint(0, len(figures[shape]) - 1),
                 'x': int(cup_w / 2) - int(fig_w / 2),
                 'y': -2,
                 'color': random.randint(0, len(colors) - 1)}
    return new_figure


def add_to_cup(cup, fig):
    for x in range(fig_w):
        for y in range(fig_h):
            if figures[fig['shape']][fig['rotation']][y][x] != empty:
                cup[x + fig['x']][y + fig['y']] = fig['color']


def emptycup():
    # создает пустой стакан
    cup = []
    for i in range(cup_w):
        cup.append([empty] * cup_h)
    return cup


def in_cup(x, y):
    return x >= 0 and x < cup_w and y < cup_h


def check_position(cup, fig, adjX=0, adjY=0):
    # проверяет, находится ли фигура в границах стакана, не сталкиваясь с другими фигурами
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
    # проверяем наличие полностью заполненных рядов
    for x in range(cup_w):
        if cup[x][y] == empty:
            return False
    return True


def clear_completed(cup):
    # Удаление заполенных рядов и сдвиг верхних рядов вниз
    removed_lines = 0
    y = cup_h - 1
    while y >= 0:
        if is_completed(cup, y):
            for push_down_y in range(y, 0, -1):
                for x in range(cup_w):
                    cup[x][push_down_y] = cup[x][push_down_y - 1]
            for x in range(cup_w):
                cup[x][0] = empty
            removed_lines += 1
        else:
            y -= 1
    return removed_lines


def convert_coords(block_x, block_y):
    return (side_margin + (block_x * block)), (top_margin + (block_y * block))


def draw_block(block_x, block_y, color, pixelx=None, pixely=None):
    # отрисовка квадратных блоков, из которых состоят фигуры
    if color == empty:
        return
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_coords(block_x, block_y)
    pygame.draw.rect(display_surf, colors[color], (pixelx + 1, pixely + 1, block - 1, block - 1), 0, 3)
    pygame.draw.rect(display_surf, lightcolors[color], (pixelx + 1, pixely + 1, block - 4, block - 4), 0, 3)
    pygame.draw.circle(display_surf, colors[color], (pixelx + block / 2, pixely + block / 2), 5)


def game_cup(cup):
    # граница игрового поля-стакана
    pygame.draw.rect(display_surf, brd_color, (side_margin - 4, top_margin - 4, (cup_w * block) + 8, (cup_h * block) + 8), 5)

    # фон игрового поля
    pygame.draw.rect(display_surf, bg_color, (side_margin, top_margin, block * cup_w, block * cup_h))
    for x in range(cup_w):
        for y in range(cup_h):
            draw_block(x, y, cup[x][y])


def draw_title():
    title_surf = big_font.render('Тетрис Lite', True, title_color)
    title_rect = title_surf.get_rect()
    title_rect.topleft = (window_w - 425, 30)
    display_surf.blit(title_surf, title_rect)


def draw_info(score, level):
    score_surf = basic_font.render(f'Баллы: {score}', True, txt_color)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (window_w - 550, 180)
    display_surf.blit(score_surf, score_rect)

    level_surf = basic_font.render(f'Уровень: {level}', True, txt_color)
    level_rect = level_surf.get_rect()
    level_rect.topleft = (window_w - 550, 250)
    display_surf.blit(level_surf, level_rect)

    pauseb_surf = basic_font.render('Пауза: пробел', True, info_color)
    pauseb_rect = pauseb_surf.get_rect()
    pauseb_rect.topleft = (window_w - 550, 420)
    display_surf.blit(pauseb_surf, pauseb_rect)

    escb_surf = basic_font.render('Выход: Esc', True, info_color)
    escbR_rect = escb_surf.get_rect()
    escbR_rect.topleft = (window_w - 550, 450)
    display_surf.blit(escb_surf, escbR_rect)


def draw_fig(fig, pixelx=None, pixely=None):
    fig_to_draw = figures[fig['shape']][fig['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convert_coords(fig['x'], fig['y'])

    # отрисовка элементов фигур
    for x in range(fig_w):
        for y in range(fig_h):
            if fig_to_draw[y][x] != empty:
                draw_block(None, None, fig['color'], pixelx + (x * block), pixely + (y * block))


def draw_next_fig(fig):  # превью следующей фигуры
    next_surf = basic_font.render('Следующая:', True, txt_color)
    next_rect = next_surf.get_rect()
    next_rect.topleft = (window_w - 150, 180)
    display_surf.blit(next_surf, next_rect)
    draw_fig(fig, pixelx=window_w - 150, pixely=230)


if __name__ == '__main__':
    main()
