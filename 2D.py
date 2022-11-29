import pygame

WIDTH = 360  # ширина игрового окна
HEIGHT = 480 # высота игрового окна
FPS = 30 # частота кадров в секунду
GRAY = (127, 127, 127)

def game1():
    # создаем игру и окно
    pygame.init()
    print(pygame.image.get_extended())
    pygame.mixer.init()  # для звука
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    # Цикл игры
    running = True
    while running:
        # держим цикл на правильной скорости
        clock.tick(FPS)
        # Ввод процесса (события)
        for event in pygame.event.get():
            # проверить закрытие окна
            if event.type == pygame.QUIT:
                running = False

        # Обновление

        # Рендеринг
        screen.fill(GRAY)
        # после отрисовки всего, переворачиваем экран
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    print("This is not app!")
