import pygame
import pygame_menu
import random
import os
from pygame.math import Vector2
import datetime
import psycopg2

pygame.init()
cell_size = 30
cell_num = 20

playb = [[i for i in range(0, cell_num)] for j in range(0, cell_num)]


class Constants:
    UP = Vector2(0, -1)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    RIGHT = Vector2(1, 0)
    fruits = {1: "apple", 2: "banana", 3: "strawberry"}


class DBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def checkIfExists(self, table_name):
        query = f"""
            SELECT *
            FROM INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'test'
            AND TABLE_NAME = '{table_name}'
            """

        self.cursor.execute(query)
        output = self.cursor.fetchone()
        print(output)
        return bool(output)

    def getRecords(self):
        query = """SELECT * FROM lab10.test.snake ORDER BY points DESC"""
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def insertIfNotExists(self, username):
        query = f"""INSERT INTO lab10.test.snake(name, points, level)
                SELECT '{username}', 0, 0
                WHERE NOT EXISTS (SELECT 1 FROM lab10.test.snake WHERE name = '{username}')
                """
        self.cursor.execute(query)
        self.commit()

    def updateIfBest(self, username, points, level):
        query = f"""UPDATE lab10.test.snake 
                    SET points = GREATEST(points, {points}), 
                        level = GREATEST(level, {level}) 
                    WHERE name = '{username}'"""
        self.cursor.execute(query)
        self.commit()

    def createTable(self):
        query = """
            CREATE TABLE lab10.test.snake(
                id SERIAL,
                points INTEGER,
                level INTEGER,
                name VARCHAR(255)
            )
            """

        self.cursor.execute(query)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()

    def connect(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="lab10",
            user="postgres",
            port="5432",
            password="Dias2004")
        self.cursor = self.conn.cursor()

        if not self.checkIfExists("snake"):
            print("Not exists")
            self.createTable()
            self.commit()


class GameObject:
    def draw(self, where: pygame.Surface):
        pass

    def move(self):
        pass

    def get_pos(self) -> tuple[float, float]:
        pass


class Obstacle(GameObject):

    def __init__(self):
        self.blocks = []

    def draw(self, where: pygame.Surface):
        for block in self.blocks:
            rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(where, (78, 76, 77), rect)

    def move(self):
        # spawn only in free space
        y = random.choice([i for i in range(1, cell_num - 2) if 0 in playb[i]])
        x = random.choice([i for i in range(1, cell_num - 2) if playb[y][i] == 0])

        self.blocks.append(Vector2(x, y))
        playb[y][x] = 1


class Snake(GameObject):
    def __init__(self):
        # head of the snake is at body[0]
        self.body = [Vector2(6, 0), Vector2(5, 0), Vector2(4, 0)]
        self.direction = Constants.RIGHT

    def draw(self, where):
        for idx, block in enumerate(self.body):
            if idx == 0:
                rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
                pygame.draw.rect(where, (39, 145, 10), rect)
            else:
                rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
                pygame.draw.rect(where, (36, 92, 20), rect)

    def move(self):
        copy = self.body[:-1]
        copy.insert(0, self.body[0] + self.direction)  # first block of body becomes head, move head
        self.body = copy

        # add new position in matrix
        for i in range(0, len(playb)):
            for j in range(0, len(playb)):
                coor = Vector2(j, i)
                if coor in self.body:
                    playb[i][j] = 2
                else:
                    playb[i][j] = 0

    def get_pos(self) -> tuple[float, float]:
        return self.body[0].x, self.body[0].y

    def extend(self):
        copy = self.body[:]
        copy.insert(0, self.body[0] + self.direction)  # first block of body becomes head, move head
        self.body = copy


class Fruit(GameObject):

    def __init__(self):
        self.weight = 1
        self.position = Vector2(random.randint(1, cell_num - 3), random.randint(1, cell_num - 3))
        self.image = pygame.transform.scale(pygame.image.load(os.path.abspath(
            f"snake_assets/{Constants.fruits[self.weight]}.png")).convert_alpha(),
                                            (cell_size, cell_size))
        self.timestamp = datetime.datetime.now()

    def setTimer(self):
        now = datetime.datetime.now()
        if (now - self.timestamp).seconds.real >= 5:
            self.move()

    def draw(self, where):
        self.setTimer()
        rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        where.blit(self.image, rect)

    def move(self):
        # remove previous position in matrix
        playb[int(self.position.y)][int(self.position.x)] = 0

        # prevent from spawning inside the wall
        y = random.choice([i for i in range(1, cell_num - 2) if 0 in playb[i]])
        x = random.choice([i for i in range(1, cell_num - 2) if playb[y][i] == 0])

        self.position = Vector2(x, y)
        self.weight = random.randint(1, 3)
        self.image = pygame.transform.scale(pygame.image.load(os.path.abspath(
            f"snake_assets/{Constants.fruits[self.weight]}.png")).convert_alpha(),
                                            (cell_size, cell_size))
        self.timestamp = datetime.datetime.now()
        # add new position in matrix
        playb[int(self.position.y)][int(self.position.x)] = 3

    def get_pos(self) -> tuple[float, float]:
        return self.position.x, self.position.y


class RecordsMenu:
    def drawMenu(self, where, data):
        theme = pygame_menu.themes.THEME_BLUE.copy()
        theme.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND  # cursor on scroll
        recordsMenu = pygame_menu.Menu(title='RECORDS', width=450, height=300, enabled=False,
                                       theme=theme, onclose=lambda: recordsMenu.disable())
        recordsMenu.enable()
        recordsMenu.add.vertical_margin(20)  # Adds margin
        table = recordsMenu.add.table()
        max_cell_length = 12
        table.add_row((f"Name{' ' * 8}", f"Points{' ' * 6}", f"Level{' ' * 7}"), cell_font_size=25)
        # recordsMenu.add.label(title=f"Name:{' '*8}Points:{' '*8}Level:{' '*8}", font_size = 25)

        for i in data:
            name = i[3] if len(i[3]) < 9 else i[3][:8] + "..."
            points = str(i[1]) + ' ' * (max_cell_length - len(str(i[1])))
            level = str(i[2]) + ' ' * (max_cell_length - len(str(i[2])))
            table.add_row((name, points, level), cell_font_size=20)

        recordsMenu.mainloop(where)


class PauseMenu:
    def __init__(self, onPlay, onRecord, onQuit):
        self.menu = pygame_menu.Menu('PAUSE', 400, 300, enabled=False,
                                     theme=pygame_menu.themes.THEME_BLUE)
        self.menu.add.button('Play', onPlay)
        self.menu.add.button('Records', onRecord)
        self.menu.add.button("Quit", onQuit)

    def drawMenu(self, where, ):
        self.menu.enable()
        self.menu.mainloop(where)


class Game:

    def __init__(self, db: DBManager):
        # db
        self.name = ""
        self.dbManager = db

        # menu
        self.pauseMenu = None
        self.recordsMenu = None

        # display
        self.SIZE = (cell_num * cell_size, cell_num * cell_size)
        self.screen = pygame.display.set_mode(self.SIZE)

        # Game objects
        self.obstacle = None
        self.snake = None
        self.fruit = None

        # game state
        self.running = True
        self.isPause = False
        self.gameOver = False
        self.TICK = 150
        self.collectedPoints = 0
        self.currLevel = 1
        self.font = pygame.font.SysFont("Arial", 16)

    def setScreenColor(self):
        self.screen.fill((109, 181, 83))

    def checkForFail(self):
        head = self.snake.get_pos()
        # check for the wall
        if not (0 <= head[0] < cell_num):
            self.gameOver = True
            self.dbManager.updateIfBest(self.name, self.collectedPoints, self.currLevel)
        if not (0 <= head[1] < cell_num):
            self.gameOver = True
            self.dbManager.updateIfBest(self.name, self.collectedPoints, self.currLevel)

        # check if we hit outselves
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.gameOver = True
                self.dbManager.updateIfBest(self.name, self.collectedPoints, self.currLevel)

        # check if we hit obstacles
        if self.snake.body[0] in self.obstacle.blocks:
            self.gameOver = True
            self.dbManager.updateIfBest(self.name, self.collectedPoints, self.currLevel)

    def renderGameInfo(self):
        level = self.font.render(f"Level {self.currLevel}", True, (0, 0, 0))
        score = self.font.render(f"Score {self.collectedPoints}", True, (0, 0, 0))
        self.screen.blit(level, ((cell_num - 3) * cell_size, 20.0))
        self.screen.blit(score, ((cell_num - 3) * cell_size, 40.0))

    def increaseLevel(self):
        self.currLevel += 1
        self.obstacle.move()
        self.obstacle.move()

        if self.TICK > 40:
            self.TICK -= 10

    def checkForCollision(self, MOVEMENT):
        headC = self.snake.get_pos()
        appleC = self.fruit.get_pos()
        if appleC == headC:
            self.collectedPoints += self.fruit.weight
            self.fruit.move()
            self.snake.extend()

            if self.collectedPoints >= 2 and self.collectedPoints / 3 > self.currLevel:
                self.increaseLevel()
                pygame.time.set_timer(MOVEMENT, self.TICK)

    def updateScreen(self, user_event):
        self.setScreenColor()
        self.fruit.draw(self.screen)
        self.snake.draw(self.screen)
        self.obstacle.draw(self.screen)
        self.checkForCollision(user_event)
        self.checkForFail()
        self.renderGameInfo()

    def unpause(self):
        self.isPause = False
        self.pauseMenu.menu.disable()

    def pause(self):
        self.isPause = True

    def quit(self):
        self.running = False
        self.pauseMenu.disable()
        self.dbManager.close()

    def drawPlayBtn(self):
        restartImg = pygame.image.load(os.path.abspath("snake_assets/restart.png")).convert_alpha()
        restartImg = pygame.transform.scale(restartImg, (100, 100))
        restartBtn = self.screen.blit(restartImg,
                                      ((self.screen.get_width() / 2 - 50), (self.screen.get_height() / 2 - 50)))
        pygame.display.flip()
        return restartBtn

    def drawMenuBtn(self):
        menuImg = pygame.image.load(os.path.abspath("snake_assets/menu.png")).convert_alpha()
        menuImg = pygame.transform.scale(menuImg, (40, 40))
        menuImg = self.screen.blit(menuImg, (30, 30))
        return menuImg

    def drawPauseMenu(self):
        self.pauseMenu.drawMenu(where=self.screen)

    def drawRecordsDialog(self):
        self.recordsMenu = RecordsMenu()
        data = self.dbManager.getRecords()
        self.recordsMenu.drawMenu(self.screen, data)

    def restart(self, user_event):
        self.fruit = Fruit()
        self.snake = Snake()
        self.obstacle = Obstacle()
        self.currLevel = 1
        self.TICK = 150
        self.collectedPoints = 0
        self.updateScreen(user_event)
        self.gameOver = False

        MOVEMENT = pygame.USEREVENT
        pygame.time.set_timer(MOVEMENT, self.TICK)

    def startGame(self):
        # Game objects
        self.fruit = Fruit()
        self.snake = Snake()
        self.obstacle = Obstacle()

        # UI
        restartBtn = None
        menuBtn = None
        self.pauseMenu = PauseMenu(
            onPlay=lambda: self.unpause(),
            onRecord=lambda: self.drawRecordsDialog(),
            onQuit=lambda: self.quit())

        # Events
        MOVEMENT = pygame.USEREVENT
        pygame.time.set_timer(MOVEMENT, self.TICK)

        while self.running:
            if not self.gameOver and not self.isPause:
                self.updateScreen(MOVEMENT)
                menuBtn = self.drawMenuBtn()
                pygame.display.flip()
            elif self.gameOver and not self.isPause:
                restartBtn = self.drawPlayBtn()
            elif self.isPause and not self.gameOver:
                self.drawPauseMenu()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    self.dbManager.close()
                if event.type == MOVEMENT:
                    self.snake.move()

                # update movement
                if event.type == pygame.KEYDOWN and not self.gameOver:
                    if event.key == pygame.K_UP and self.snake.direction is not Constants.DOWN:
                        self.snake.direction = Constants.UP
                    if event.key == pygame.K_DOWN and self.snake.direction is not Constants.UP:
                        self.snake.direction = Constants.DOWN
                    if event.key == pygame.K_LEFT and self.snake.direction is not Constants.RIGHT:
                        self.snake.direction = Constants.LEFT
                    if event.key == pygame.K_RIGHT and self.snake.direction is not Constants.LEFT:
                        self.snake.direction = Constants.RIGHT

                # handle btns
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.gameOver and restartBtn is not None:
                        if restartBtn.collidepoint(pos):
                            self.restart(MOVEMENT)
                    if menuBtn is not None:
                        if menuBtn.collidepoint(pos):
                            self.pause()
                            self.pauseMenu.menu.enable()

            if self.pauseMenu.menu.is_enabled():
                self.pauseMenu.menu.update(pygame.event.get())
                self.pauseMenu.menu.draw(self.screen)

    def checkForUser(self, username, startMenu):
        self.name = str(username.get_value())
        self.dbManager.insertIfNotExists(self.name)
        self.startGame()
        startMenu.disable()

    def start(self):
        menu = pygame_menu.Menu('Welcome', 400, 300,
                                theme=pygame_menu.themes.THEME_BLUE)

        username_bx = menu.add.text_input('Name :', default='Username')
        menu.add.button('Play', lambda: snakeGame.checkForUser(username_bx, menu))
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.screen)


dbManager = DBManager()
dbManager.connect()
snakeGame = Game(dbManager)
snakeGame.start()
