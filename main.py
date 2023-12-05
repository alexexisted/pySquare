import pygame as pg
import pymunk.pygame_util
from random import randrange


pymunk.pygame_util.positive_y_is_up = False

#настройки pygame
RES = WIDTH, HEIGHT = 900, 720
FPS = 60

pg.init()
surface = pg.display.set_mode(RES)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)

#настройки pymunk
space = pymunk.Space()
space.gravity = 0, 8000

# отрисовка платформы
# статический объект (сам не двигается, но может взаимодействовать с другими телами)
segment_shape = pymunk.Segment(space.static_body, (1, HEIGHT), (WIDTH, HEIGHT), 26)
space.add(segment_shape) # добавляем в пространство объект
segment_shape.elasticity = 0.4 # коэфицент упругости
segment_shape.friction = 1.0 # коэфицент трения


# создаем тело квадратной формы
def create_square(space, pos):
    square_mass, square_size = 1, (60, 60) # масса и размер квадрата
    square_moment = pymunk.moment_for_box(square_mass, square_size) # автоматически расчитываем момент инерции
    # с помощью массы и размера
    square_body = pymunk.Body(square_mass, square_moment) # экземпляр тела
    square_body.position = pos # появление на месте курсора
    square_shape = pymunk.Poly.create_box(square_body, square_size)
    square_shape.elasticity = 0.8
    square_shape.friction = 1.0
    square_shape.color = [randrange(256) for i in range(4)]
    space.add(square_body, square_shape)


def create_circle(space, pos):
    circle_mass, circle_radius = 1, 30
    circle_moment = pymunk.moment_for_circle(circle_mass, 0, circle_radius)
    circle_body = pymunk.Body(circle_mass, circle_moment)
    circle_body.position = pos
    circle_shape = pymunk.Circle(circle_body, circle_radius)
    circle_shape.elasticity = 0.8
    circle_shape.friction = 1.0
    circle_shape.color = [randrange(256) for i in range(4)]
    space.add(circle_body, circle_shape)


while True:
    surface.fill(pg.Color('black'))

    for i in pg.event.get():
        if i.type == pg.QUIT:
            exit()
        # спавн кубов
        if i.type == pg.MOUSEBUTTONDOWN:
            if i.button == 1:
                create_square(space, i.pos)
                create_circle(space, i.pos)
                print(i.pos)
        pg.display.flip()
        clock.tick(FPS)

    space.step(1 / FPS)
    space.debug_draw(draw_options)

    pg.display.flip()
    clock.tick(FPS)

