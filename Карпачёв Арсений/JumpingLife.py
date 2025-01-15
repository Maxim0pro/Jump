# TODO: Добавить классы
# TODO: Раскидать все по папкам и модулям (файлам) +-
# TODO: Загрузить все на GitHub +

# L = length - длина
# B = breadth - ширина
# W = width - ширина
# H = height - высота

# Хочу сделать:
# 1. Бесконечное кол-во труб.
# 2. При столкновении основного объекта (лысый) с второстепенными объектами (трубы) всё
# останавливалось и на главном экране появлялось дополнительное окно с надписью "Проигрыш".

import pygame as pg  # Импорт библиотеки pygame
import random as rd  # Импорт библиотеки random

pg.init()  # Инициализация Pygame

W = 360  # Ширина окна
H = 640  # Высота окна
isJump = False  # Флаг для прыжка
bg = pg.image.load('images/fon.png')  # Загрузка фонового изображения
bald_image = pg.image.load('images/bald.png')  # Загрузка изображения персонажа
tube_image = pg.image.load('images/tube0.png')  # Загрузка изображения трубы
new_image = pg.transform.scale(bald_image, (100, 100))  # Масштабирование изображения персонажа
new_image_2 = pg.transform.scale(tube_image, (250, 400))  # Масштабирование изображения трубы

speed = 3  # Скорость движения объектов
xCord = -45  # x-координата персонажа
y1 = 323  # y-координата персонажа

# Загрузка музыки
menu_sound = pg.mixer.Sound('sounds/menu.mp3')  # Загрузка музыки для меню
bg_sound = pg.mixer.Sound('sounds/background.wav')  # Загрузка музыки для игры
current_music = menu_sound  # Установка текущей музыки как музыки меню
current_music.play(loops=-1)  # Запуск музыки меню в бесконечном цикле

clock = pg.time.Clock()  # Создание объекта для управления временем
win = pg.display.set_mode((W, H), flags=pg.NOFRAME)  # Создание окна игры без рамки
pg.display.set_caption('Jumping Life')  # Установка заголовка окна

# Цвета
BLACK = (0, 0, 0)  # Черный цвет
WHITE = (255, 255, 255)  # Белый цвет
GREEN = (0, 255, 0)  # Зеленый цвет

# Параметры кнопки
button_width = 200  # Ширина кнопки
button_height = 50  # Высота кнопки
button_x = W // 2 - button_width // 2  # x-координата кнопки
button_y = H // 2 - button_height // 2  # y-координата кнопки
button_color = GREEN  # Цвет кнопки
button_text_color = BLACK  # Цвет текста кнопки
font = pg.font.Font(None, 36)  # Шрифт текста кнопки
button_text = font.render('Start game', True, button_text_color)  # Создание текста кнопки
button_text_rect = button_text.get_rect(
    center=(button_x + button_width // 2, button_y + button_height // 2))  # Создание прямоугольника текста кнопки

# Состояние игры
game_started = False  # Флаг для состояния игры (меню или игра)


class Pipe:  # Класс для трубы
    def __init__(self, img, x, y, flipped=False):  # Конструктор класса Pipe
        self.img = img  # Изображение трубы
        if flipped:  # Если труба перевернута
            self.img = pg.transform.flip(img, False, True)  # Переворот изображения
        self.x = x  # x-координата трубы
        self.y = y  # y-координата трубы
        self.width = img.get_width()  # Ширина трубы
        self.height = img.get_height()  # Высота трубы

    def render(self, win):  # Метод для отрисовки трубы
        win.blit(self.img, (self.x, self.y))  # Отрисовка трубы в окне

    def update(self):  # Метод для обновления позиции трубы
        self.x -= speed  # Уменьшение x-координаты трубы


# Создаем список для хранения труб
pipes = []  # Список для хранения объектов труб


# Функция создания новой пары труб
def create_pipe():  # Функция для создания новой пары труб
    pipe_gap = 200  # Расстояние между трубами
    pipe_height = new_image_2.get_height()  # Высота трубы

    # Случайная позиция для верхней трубы
    # Установка верхней трубы рандомно сверху экрана
    y_top = rd.randint(-pipe_height + 50, 0)  # Случайная y-координата верхней трубы
    y_bottom = y_top + pipe_height + pipe_gap  # y-координата нижней трубы

    return {  # Возвращает словарь с верхней и нижней трубами
        'top': Pipe(new_image_2, W, y_top, flipped=True),  # Верхняя труба (перевернутая)
        'bottom': Pipe(new_image_2, W, y_bottom)  # Нижняя труба
    }


# Основной игровой цикл
running = True  # Флаг для работы игрового цикла
while running:  # Начало игрового цикла
    for event in pg.event.get():  # Обработка событий
        if event.type == pg.QUIT:  # Если пользователь закрыл окно
            running = False  # Завершение игрового цикла
        if event.type == pg.MOUSEBUTTONDOWN and not game_started:  # Если нажата кнопка мыши и игра не начата
            mouse_x, mouse_y = event.pos  # Получение координат мыши

            if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:  # Если нажата кнопка "Start game"
                game_started = True  # Установка флага начала игры

    # Главное меню
    if not game_started:  # Если игра не начата (меню)
        if current_music != menu_sound:  # Если текущая музыка не музыка меню
            current_music.stop()  # Останавливаем текущую музыку
            current_music = menu_sound  # Меняем на музыку меню
            current_music.play(loops=-1)  # Запускаем музыку меню
        win.fill('green')  # Заливка окна зеленым цветом
        pg.draw.rect(win, button_color, (button_x, button_y, button_width, button_height))  # Отрисовка кнопки
        win.blit(button_text, button_text_rect)  # Отрисовка текста кнопки
    # Игровой процесс
    else:  # Если игра начата
        if current_music != bg_sound:  # Если текущая музыка не музыка игры
            current_music.stop()  # Останавливаем текущую музыку
            current_music = bg_sound  # Меняем на музыку игры
            current_music.play(loops=-1)  # Запускаем музыку игры
        # Очищаем экран и рисуем фон
        win.blit(bg, (0, 0))  # Отрисовка фона

        # Рисуем персонажа
        win.blit(new_image, (xCord, y1))  # Отрисовка персонажа

        # Управление трубами
        if len(pipes) == 0 or pipes[-1]['top'].x < W - 300:  # Если нет труб или последняя труба достаточно далеко
            pipes.append(create_pipe())  # Добавление новой пары труб

        # Обновление и отрисовка труб
        for pipe_pair in pipes[:]:  # Проходим по всем трубам
            pipe_pair['top'].render(win)  # Отрисовка верхней трубы
            pipe_pair['bottom'].render(win)  # Отрисовка нижней трубы
            pipe_pair['top'].update()  # Обновление позиции верхней трубы
            pipe_pair['bottom'].update()  # Обновление позиции нижней трубы

            # Удаляем трубы, ушедшие за экран
            if pipe_pair['top'].x < -pipe_pair['top'].width:  # Если труба ушла за левый край экрана
                pipes.remove(pipe_pair)  # Удаление трубы из списка

        # Обработка клавиш
        keys = pg.key.get_pressed()  # Получение нажатых клавиш
        if keys[pg.K_a]:  # Если нажата клавиша "A"
            xCord -= 3  # Уменьшение x-координаты персонажа
        if keys[pg.K_d]:  # Если нажата клавиша "D"
            xCord += 3  # Увеличение x-координаты персонажа
        if not (isJump):  # Если персонаж не прыгает
            if keys[pg.K_UP]:  # Если нажата клавиша "UP"
                y1 -= 3  # Уменьшение y-координаты персонажа
            if keys[pg.K_DOWN]:  # Если нажата клавиша "DOWN"
                y1 += 3  # Увеличение y-координаты персонажа

        # Проверка границ
        if xCord > 370:  # Если персонаж ушел за правый край экрана
            xCord = -80  # Перемещение персонажа на левый край
        if y1 >= 468:  # Если персонаж ушел за нижний край экрана
            y1 = 468  # Установка y-координаты в нижний край
        if y1 <= -3:  # Если персонаж ушел за верхний край экрана
            y1 = -3  # Установка y-координаты в верхний край

    # Обновление экрана
    pg.display.flip()  # Обновление всего экрана
    clock.tick(40)  # Управление частотой кадров (40 кадров в секунду)
pg.quit()  # Завершение Pygame
