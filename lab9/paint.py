import os.path

import pygame, sys
from collections import namedtuple

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
points = []


class ColorMode:
    RED = "red"
    BLACK = "black"
    WHITE = "white"
    GREEN = "green"
    BLUE = "blue"

    colors = [RED, BLACK, GREEN, BLUE]


class Mode:
    BRUSH = "brush"
    ERASER = "eraser"
    RECT = "rectangle"
    CIRCLE = "oval"
    SQUARE = "square"
    RIGHT_TRL = "right_triangle"
    EQ_TRL = "eq_trl"
    RHOMB = "rhomb"

    figures = [RECT, CIRCLE, SQUARE, RIGHT_TRL, EQ_TRL, RHOMB, BRUSH, ERASER]

    END = "end"
    START = "start"


class Point:
    def __init__(self, x, y, radius, color, mode):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mode = mode
        self.status = Mode.START


class Brush:
    def __init__(self):
        self.pos = pygame.mouse.get_pos()
        self.mode = Mode.BRUSH
        self.icon = "brush"
        self.image = pygame.transform.scale(pygame.image.load('paint_assets/brush.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
        self.width = 15
        self.color_mode = ColorMode.RED
        self.points = []

    # render new position of the brush
    def update(self):
        self.pos = pygame.mouse.get_pos()
        self.image = pygame.transform.scale(pygame.image.load(f'paint_assets/{self.icon}.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos

    # adding points into the dataSet
    def add_points(self):
        if 50 <= self.pos[1] <= 500:
            color = self.color_mode if self.mode != Mode.ERASER else ColorMode.WHITE
            p = Point(x=self.pos[0], y=self.pos[1], radius=self.width, color=color, mode=self.mode)
            self.points = self.points + [p]

    # drawing line between two points => creating a series of points => one straight line
    def draw_line_between(self, surf, start, end):
        dx = start.x - end.x
        dy = start.y - end.y
        iterations = max(abs(dx), abs(dy))
        # 1) check if the points have only brush or eraser mode
        # 2) check for the new lines
        if ((start.mode == Mode.BRUSH and end.mode == Mode.BRUSH) or (
                start.mode == Mode.ERASER and end.mode == Mode.ERASER)) and not (
                start.status == Mode.END and end.status == Mode.START):
            for i in range(iterations):
                progress = 1.0 * i / iterations
                aprogress = 1 - progress
                x = int(aprogress * start.x + progress * end.x)
                y = int(aprogress * start.y + progress * end.y)
                if start.mode == Mode.BRUSH or start.mode == Mode.ERASER:
                    pygame.draw.circle(surf, start.color, (x, y), start.radius)

    # constantly updating info on self.points and calling necessary methods
    def draw_points(self, surf):
        i = 0
        while i < len(self.points) - 1:
            if self.points[i].mode == Mode.BRUSH or self.points[i].mode == Mode.ERASER:
                self.draw_line_between(surf, self.points[i], self.points[i + 1])

            if self.points[i + 1].mode == Mode.RECT:
                rect = pygame.Rect(self.points[i + 1].x, self.points[i + 1].y, 200, 130)
                pygame.draw.rect(surf, self.points[i + 1].color, rect, rect.width)

            if self.points[i + 1].mode == Mode.CIRCLE:
                pygame.draw.circle(surf, self.points[i + 1].color, (self.points[i + 1].x, self.points[i + 1].y), 40)

            if self.points[i + 1].mode == Mode.SQUARE:
                rect = pygame.Rect(self.points[i + 1].x, self.points[i + 1].y, 150, 150)
                pygame.draw.rect(surf, self.points[i + 1].color, rect, rect.width)

            if self.points[i + 1].mode == Mode.RIGHT_TRL:
                pygame.draw.polygon(surf, self.points[i + 1].color, ((self.points[i + 1].x, self.points[i + 1].y),
                                                                     (self.points[i + 1].x, self.points[i + 1].y - 100),
                                                                     (self.points[i + 1].x + 100, self.points[i + 1].y)
                                                                     ))

            if self.points[i + 1].mode == Mode.EQ_TRL:
                pygame.draw.polygon(surf, self.points[i + 1].color, ((self.points[i + 1].x, self.points[i + 1].y),
                                                                     (self.points[i + 1].x + 50,
                                                                      self.points[i + 1].y - 100),
                                                                     (self.points[i + 1].x + 100, self.points[i + 1].y)
                                                                     ))

            if self.points[i + 1].mode == Mode.RHOMB:
                pygame.draw.polygon(surf, self.points[i + 1].color, ((self.points[i + 1].x, self.points[i + 1].y),
                                                                     (self.points[i + 1].x - 25,
                                                                      self.points[i + 1].y - 50),
                                                                     (self.points[i + 1].x, self.points[i + 1].y - 100),
                                                                     (self.points[i + 1].x + 25,
                                                                      self.points[i + 1].y - 50)
                                                                     ))
            i += 1

    def pick_color_menu(self, surf):
        x = 0
        y = 0
        for i in ColorMode.colors:
            rect = pygame.draw.rect(surf, i, pygame.Rect(x, y, 40, 40))

            pos = pygame.mouse.get_pos()
            presses = pygame.mouse.get_pressed()
            if rect.collidepoint(pos) and presses[0]:
                self.color_mode = i
            x += 40

    def pick_figure_menu(self, surf):
        x = 0
        y = 510
        for i in Mode.figures:
            img = pygame.transform.scale(pygame.image.load(os.path.abspath(f"paint_assets/{i}.png")), (80, 80))
            rect = surf.blit(img, (x, y))

            pos = pygame.mouse.get_pos()
            presses = pygame.mouse.get_pressed()
            if rect.collidepoint(pos) and presses[0]:
                self.mode = i
                if i != Mode.ERASER:
                    self.icon = "brush"
                    if self.color_mode == ColorMode.WHITE:
                        self.color_mode = ColorMode.RED
                else:
                    self.icon = "eraser"
                    self.color_mode = ColorMode.WHITE
            x += 90

    def erase_all(self):
        self.points = []


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Paint")
    fps = pygame.time.Clock()

    brush = Brush()

    pygame.mouse.set_visible(False)

    while True:
        fps.tick(60)

        pressed_keys = pygame.key.get_pressed()
        alt_key = pressed_keys[pygame.K_LALT] and pressed_keys[pygame.K_RALT]
        ctrl_key = pressed_keys[pygame.K_LCTRL] and pressed_keys[pygame.K_RCTRL]
        screen.fill((255, 255, 255))

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and ctrl_key:
                    return
                if event.key == pygame.K_F4 and alt_key:
                    return
                if event.key == pygame.K_ESCAPE:
                    return

                if event.key == pygame.K_UP:
                    brush.width += 5
                if event.key == pygame.K_DOWN:
                    brush.width -= 5
                if event.key == pygame.K_BACKSPACE:
                    brush.erase_all()

            # placing figure on the screen
            if event.type == pygame.MOUSEBUTTONDOWN and (brush.mode != Mode.BRUSH and brush.mode != Mode.ERASER):
                if brush.color_mode == ColorMode.WHITE:
                    brush.color_mode = ColorMode.RED
                brush.add_points()

            # set the end of the line
            if event.type == pygame.MOUSEBUTTONUP and len(brush.points) > 1:
                brush.points[-1].status = Mode.END

            if event.type == pygame.MOUSEMOTION and (event.buttons[0] == 1):
                if brush.mode == Mode.BRUSH or brush.mode == Mode.ERASER:
                    brush.add_points()

        brush.update()

        brush.draw_points(screen)
        brush.pick_color_menu(screen)
        brush.pick_figure_menu(screen)
        screen.blit(brush.image, brush.rect)
        pygame.display.flip()


if __name__ == "__main__":
    main()
