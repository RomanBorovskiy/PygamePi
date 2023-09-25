import math

import pygame

from constants import BLACK, BLUE, GREEN, RED


class Caption:
    """
    Надпись в рамке.

    caption:str  - текст рамки
    rect: pygame.Rect - размер и положение рамки

    draw(screen: pygame.Surface) - Для отрисовки на поверхности screen
    set_caption(new_caption: str) - для изменения текста на new_caption
    """

    font_size = 15  # рaзмер шрифта
    font_color = BLACK  # цвет шрифта
    back_color = BLUE  # цвет фона

    def __init__(self, caption: str, rect: pygame.Rect):
        self.caption = caption
        self.surface = pygame.Surface(rect.size)
        self.rect = rect
        self.set_caption(caption)

    def set_caption(self, new_caption: str):
        self.caption = new_caption
        font = pygame.font.Font(pygame.font.get_default_font(), self.font_size)
        text_surface = font.render(self.caption, True, self.font_color)
        text_rect = text_surface.get_rect(center=(self.rect.width // 2, self.rect.height // 2))

        self.surface.fill(self.back_color)
        self.surface.blit(text_surface, text_rect)
        pygame.draw.rect(self.surface, BLACK, self.surface.get_rect(), width=1)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)


class Diagram:
    """
    Вертикальная диаграмма.
    Масштаб автоматически подстраивается под текущий максимум и минимум
    rect: pygame.Rect - границы диаграммы

    add_value(value: float) - добавляет новое значение к диаграмме. Показываются только последние значения
    draw(screen: pygame.Surface, central_pi: bool = True) -  Для отрисовки на поверхности screen.
    central_pi определяет будет ли диаграмма центроваться относительно Пи

    """

    line_width = 2  # толщина одного бара (линии) на диаграмме
    back_color = GREEN  # цвет фона
    line_color = RED  # цвет бара (линии)

    def __init__(self, rect: pygame.Rect):
        self.rect = rect
        self.surface = pygame.Surface(rect.size)
        self.surface.fill(self.back_color)
        self.values = []

    def add_value(self, value: float):
        self.values.append(value)

    def draw(self, screen: pygame.Surface, central_pi: bool = True):
        def method_movable_pi(values_list: list[float]):
            min_val = min(math.pi, min(values_list))
            max_val = max(math.pi, max(values_list))

            delta = max_val - min_val
            k = (self.rect.width - 1) / delta

            for i, val in enumerate(values_list):
                value = val - min_val
                width = int(k * value) + 1

                pygame.draw.line(
                    self.surface,
                    self.line_color,
                    (0, i * self.line_width),
                    (width, i * self.line_width),
                    width=self.line_width,
                )

            width = int(k * (math.pi - min_val))
            pygame.draw.line(self.surface, BLUE, (width, 0), (width, self.rect.height), width=2)

        def method_central_pi(values_list: list[float]):
            min_val = min(values_list)
            max_val = max(values_list)

            delta = max(abs(min_val - math.pi), abs(max_val - math.pi))
            k = self.rect.width / (2 * delta)

            for i, val in enumerate(values_list):
                value = val - math.pi
                width = int(k * value) + self.rect.width // 2

                pygame.draw.line(
                    self.surface,
                    self.line_color,
                    (0, i * self.line_width),
                    (width, i * self.line_width),
                    width=self.line_width,
                )

            pygame.draw.line(
                self.surface, BLUE, (self.rect.width // 2, 0), (self.rect.width // 2, self.rect.height), width=2
            )

        self.surface.fill(self.back_color)
        diagram_line_count = self.rect.height // self.line_width

        if self.values:
            show_values = self.values[-diagram_line_count:]
            if central_pi:
                method_central_pi(show_values)
            else:
                method_movable_pi(show_values)

        pygame.draw.rect(self.surface, BLACK, self.surface.get_rect(), width=1)
        screen.blit(self.surface, self.rect)


class MonteCarlo:
    """
    Класс для расчета числа Пи и отображения процесса на экране
    число точек попавшие в окружность/всего точек = pi*r2/4*r2 = pi/4
    top_left: tuple[int, int] - координаты верхнего левого угла
    radius: int - радиус окружности

    set_point(x: int, y: int) - добавляет точку на схему, пересчитывает значение
    draw(screen: pygame.Surface) -  для отрисовки на поверхности screen.
    """

    back_color = GREEN  # цвет фона
    in_color = RED  # цвет точки, попавшей в круг
    out_color = BLUE  # цвет точки, не попавшей в круг

    def __init__(self, top_left: tuple[int, int] = (10, 50), radius: int = 250):
        self.surface = pygame.Surface((radius * 2, radius * 2))
        self.surface.fill(GREEN)
        self.rect = self.surface.get_rect(topleft=top_left)
        self.radius = radius
        pygame.draw.circle(self.surface, BLACK, (radius, radius), radius, 1)
        pygame.draw.rect(self.surface, BLACK, (0, 0, radius * 2, radius * 2), 1)
        self.in_circle = 0
        self.count = 0
        self.pi = 0
        self.error = 0

    def set_point(self, x: int, y: int):
        dist = (x - self.radius) ** 2 + (y - self.radius) ** 2
        if dist <= self.radius**2:
            self.surface.set_at((x, y), self.in_color)
            self.in_circle += 1
        else:
            self.surface.set_at((x, y), self.out_color)

        self.count += 1

        # pi: s_circle/s_rect = pi*r2/4*r2 = pi/4
        self.pi = 4 * self.in_circle / self.count
        self.error = abs(self.pi - math.pi) * 100 / math.pi

    def draw(self, screen: pygame.Surface):
        screen.blit(self.surface, self.rect)
