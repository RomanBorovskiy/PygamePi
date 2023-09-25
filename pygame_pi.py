import random

import pygame

from components import Caption, Diagram, MonteCarlo
from config import (app_height, app_width, diagram_central_pi, radius,
                    random_fill, value_for_every)
from constants import WHITE


def main():
    pygame.init()
    pygame.display.set_caption('Pi Monte Carlo method')

    screen = pygame.display.set_mode((app_width, app_height))

    mc_window = MonteCarlo((10, 50), radius)

    caption_rect = pygame.Rect(0, 0, radius * 2, 30)

    caption_rect.bottomleft = mc_window.rect.topleft
    caption_rect.move_ip(0, -2)

    window_caption = Caption('Monte Carlo', caption_rect)

    diagram_rect = pygame.Rect(0, 0, 200, radius * 2)
    diagram_rect.bottomleft = mc_window.rect.bottomright
    diagram_rect.move_ip(40, 0)

    diagram = Diagram(diagram_rect)

    caption_rect = pygame.Rect(0, 0, 200, 30)
    caption_rect.bottomleft = diagram_rect.topleft
    caption_rect.move_ip(0, -2)

    diagram_caption = Caption('Pi value', caption_rect)

    random.seed()

    running = True
    while running:
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

        if random_fill:
            #  выбор случайных значений
            x = random.randint(0, radius * 2 - 1)
            y = random.randint(0, radius * 2 - 1)
        else:
            # сплошная заливка всех точек последовательно
            if mc_window.count >= 4 * radius * radius:
                continue

            x = mc_window.count // (radius * 2)
            y = mc_window.count % (radius * 2)

        mc_window.set_point(x, y)

        # не будем прорисовывать каждый цикл, так получается быстрее
        if mc_window.count % value_for_every != 0:
            continue

        diagram.add_value(mc_window.pi)

        screen.fill(WHITE)
        info_str = f' pi:{mc_window.pi: .5f} count: {mc_window.count: 6d} error: {mc_window.error:2.2f}%'
        window_caption.set_caption(info_str)
        window_caption.draw(screen)
        mc_window.draw(screen)

        diagram.draw(screen, central_pi=diagram_central_pi)
        diagram_caption.draw(screen)

        pygame.display.flip()

    print(f'last pi: {mc_window.pi}')
    pygame.quit()


if __name__ == '__main__':
    main()
