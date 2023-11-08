import pygame
import random
class Point:
    def __init__(self, x, y, brain=None, cell_size=20):
        self.x = x
        self.y = y
        self.cell_size = cell_size
        if brain is None:
            self.left_chance = random.randint(0, 100)
            self.right_chance = random.randint(0, 100)
            self.up_chance = random.randint(0, 100)
            self.down_chance = random.randint(0, 100)
            self.stay = random.randint(0, 100)
        else:
            self.left_chance = brain[0]
            self.right_chance = brain[1]
            self.up_chance = brain[2]
            self.down_chance = brain[3]
            self.stay = brain[4]
        self.color = (-self.left_chance + 150 + self.right_chance,  -self.up_chance + self.down_chance + 150, 100 + self.stay)
        while (self.x, self.y) in [(p.x, p.y) for p in points]:
            self.x = random.randint(0, num_cells_x - 1) * self.cell_size
            self.y = random.randint(0, num_cells_y - 1) * self.cell_size


    def move(self):

        go = [{'left': random.randint(0, self.left_chance)},
              {'right': random.randint(0, self.right_chance)},
              {'up': random.randint(0, self.up_chance)},
              {'down': random.randint(0, self.down_chance)},
              {'stay': random.randint(0, self.stay)}]
        max_go = max(go, key=lambda x: list(x.values())[0])
        max_key = list(max_go.keys())[0]

        direction_x = 0
        direction_y = 0
        if max_key == 'left':

            direction_x = -1
            direction_y = 0
        if max_key == 'right':
            direction_x = 1
            direction_y = 0
        if max_key == 'up':
            direction_x = 0
            direction_y = -1
        if max_key == 'down':
            direction_x = 0
            direction_y = 1


        new_x = self.x + direction_x * self.cell_size
        new_y = self.y + direction_y * self.cell_size
        if (new_x, new_y) in cells and (new_x, new_y) not in [(p.x, p.y) for p in points] and (new_x, new_y) not in walls:
            self.x = new_x
            self.y = new_y


    def draw(self, screen):
        point_color = (0, 0, 0)
        pygame.draw.circle(screen, self.color, (self.x + self.cell_size // 2, self.y + self.cell_size // 2), self.cell_size // 4)


# Инициализация Pygame
pygame.init()
population_size = 400
gen = 0
# Определение размера экрана
screen_width = 800
screen_height = 600

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))

# Определение размера клетки
cell_size = 20

# Определение количества клеток по горизонтали и вертикали
num_cells_x = screen_width // cell_size
num_cells_y = screen_height // cell_size

# Создание списка всех клеток
cells = []
walls = []
for y in range(num_cells_y):
    for x in range(num_cells_x):
        cells.append((x * cell_size, y * cell_size))

# Создание списка точек
points = []
for i in range(population_size):
    x = random.randint(0, num_cells_x - 1)
    y = random.randint(0, num_cells_y - 1)
    points.append(Point(x * cell_size, y * cell_size))

# Создание списка красных клеток
red_cells = []
num_red_cells = 100 # количество красных клеток
for i in range(num_cells_x//5):
    for j in range(num_cells_y):
        red_cells.append(((num_cells_x - i) * cell_size, j * cell_size))
        # red_cells.append((i * cell_size, j * cell_size))

# Определение скорости движения точек
speed = cell_size

# Определение цветов
background_color = (255, 255, 255)
cell_color = (200, 200, 200)
point_color = (0, 0, 0)
red_color = (255, 0, 0)


def shuffle_pos():
    occupied_positions = set()

    for point in points:
        occupied_positions.add((point.x, point.y))

    for point in points:
        occupied_positions.remove((point.x, point.y))
        new_x = random.randint(0, num_cells_x - 1) * point.cell_size
        new_y = random.randint(0, num_cells_y - 1) * point.cell_size

        while (new_x, new_y) in occupied_positions:
            new_x = random.randint(0, num_cells_x - 1) * point.cell_size
            new_y = random.randint(0, num_cells_y - 1) * point.cell_size

        point.x, point.y = new_x, new_y
        occupied_positions.add((new_x, new_y))
        # print(len(set(points)))





# Определение функции для отрисовки клеток
def draw_cells():
    for cell in cells:
        pygame.draw.rect(screen, (0,0,0), (cell[0], cell[1], cell_size, cell_size))

# Определение функции для отрисовки точек
def draw_points():
    for point in points:
        point.draw(screen)

# Определение функции для отрисовки красной клетки
def draw_red_cell():
    for red_cell in red_cells:
        pygame.draw.rect(screen, red_color, (red_cell[0], red_cell[1], cell_size, cell_size))
def draw_walls():
    for wall in walls:
        pygame.draw.rect(screen, (50, 50, 50), (wall[0], wall[1], cell_size, cell_size))

# Определение функции для обновления положения точек
def update_points():

    for point in points:

        point.move()


# Определение функции для запуска генетического алгоритма
def mutate(point):
    choice = ['left_chance', 'right_chance','up_chance', 'down_chance', 'stay']
    what = random.choice(choice)
    point.__setattr__(what, random.randint(0, 100))

def run_genetic_algorithm():
    dead = 0
    same_pos = []
    global gen
    gen += 1
    print('Gen:', gen)
    for point in points:
        same_pos.append((point.x, point.y))
        mutation = random.randint(0, 50)
        x, y = point.x, point.y
        for red_cell in red_cells:
            if x == red_cell[0] and y == red_cell[1]:

                points.remove(point)
                dead += 1

        if mutation == 25:
            mutate(point)
            print('mutation appeared')
    print('Dead:', dead,' ',dead/200*100, '%')
    # if gen == 20:
    #     for i in range(num_cells_x // 6):
    #         for j in range(num_cells_y):
    #             red_cells.append(((i) * cell_size, j * cell_size))
    if population_size > len(points):
        while population_size > len(points):
            to_add = random.choice(points)

            points.append(Point(to_add.x, to_add.y, brain=[to_add.left_chance,to_add.right_chance,to_add.up_chance,to_add.down_chance,to_add.stay]))
            # print(to_add)
    # print(points[190])
    shuffle_pos()





# Основной цикл
clock = pygame.time.Clock()
generation_time = 1000 # время в миллисекундах
last_generation_time = pygame.time.get_ticks()

while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:

            # Добавление красной клетки или стены при клике мыши
            mouse_pos = pygame.mouse.get_pos()
            cell_x = (mouse_pos[0] // cell_size) * cell_size
            cell_y = (mouse_pos[1] // cell_size) * cell_size
            if (cell_x, cell_y) not in red_cells:
                if pygame.mouse.get_pressed()[0]:
                    red_cells.append((cell_x, cell_y))
                elif pygame.mouse.get_pressed()[2]:
                    walls.append((cell_x, cell_y))

    # Очистка экрана
    screen.fill((0, 0, 0))
    # Отрисовка клеток и точек
    draw_cells()

    draw_red_cell()
    draw_walls()
    update_points()

    draw_points()



    # Запуск генетического алгоритма каждые 3 секунды
    current_time = pygame.time.get_ticks()
    if current_time - last_generation_time >= generation_time:
        run_genetic_algorithm()
        last_generation_time = current_time



    # Обновление экрана
    pygame.display.update()

    # Ограничение количества кадров в секунду
    clock.tick(60)  # 60 FPS