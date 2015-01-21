# !/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import random
import time
import threading

class Snake(object):
    UP, DOWN, LEFT, RIGHT = -1,1,-2,2
    def __init__(self, x=0, y=0, length=5):
        # Initialize a snake
        # Attributes
        self.length = length
        self.x = x
        self.y = y
        self.direction = Snake.RIGHT # up, down, left, right: 0,1,2,3
        self.trace = []
        self.speed = 1 # This should be a constant. Only the 'game speed' changes
        self.__init_trace()
        self.print_init()
    # -----------------  Public methods  -----------------------
    def grow(self):
        self.length += 1
    def turn(self, direction):
        if self.direction + direction != 0:
            self.direction = direction
    def move(self):
        if self.direction == Snake.UP:
            self.y += self.speed
        elif self.direction == Snake.DOWN:
            self.y -= self.speed
        elif self.direction == Snake.LEFT:
            self.x -= self.speed
        elif self.direction == Snake.RIGHT:
            self.x += self.speed
        # Renew trace
        # Do not delete the last point of trace when moving
        if self.length == len(self.trace):
            self.trace.pop()
        self.trace.insert(0, [self.x, self.y])
    # -----------------  Private methods  -----------------------
    def __init_trace(self):
        for i in range(self.length):
            self.trace.append([self.x - i, self.y])
    # -----------------  Debug methods  -----------------------
    def print_init(self):
        print 'Initialize a snake:'
        print '  self.trace=', self.trace
        print '  self.len=', self.length
        print '  self.directrion=', self.direction
    def print_snake(self):
        print 'self.trace=', self.trace
        #print 'self.len=', self.length
        #print 'self.directrion=', self.direction
    
class Food(object):
    def __init__(self, x=0, y=0):
        # Initialize a food
        # Attributes
        self.x = x
        self.y = y
        self.print_init()
    def renew(self, x, y):
        self.x = x
        self.y = y
    # -----------------  Debug methods  -----------------------
    def print_init(self):
        print "Initialize a food: \n  x=%d, y=%d" % (self.x, self.y)
    def print_food(self):
        print "Food: x=%d, y=%d" % (self.x, self.y)

class GameMap(object):
    def __init__(self, x_max, x_min ,y_max, y_min):
        self.x_max = x_max
        self.x_min = x_min
        self.y_max = y_max
        self.y_min = y_min
        self.print_init()
    def print_init(self):
        print "Initialize a map:"
        print "  x_max=%d, y_max=%d" % (self.x_max,self.y_max)
        print "  x_min=%d, y_min=%d" % (self.x_min,self.y_min)

class GamePaint(object):
    def __init__(self, handler):
        self.draw_handler = handler
    def draw_snake(self, snake):
        #snake.print_snake()
        for i in range(0, snake.length-2):
            p1 = snake.trace[i]
            p2 = snake.trace[i+1]
            self.draw_handler.draw_line(p1, p2)
    def draw_food(self, food):
        #food.print_food()
        self.draw_handler.draw_point([food.x, food.y])
    def draw_map(self, m):
        # p11        p12
        #
        # p22        p21
        p11 = [m.x_min, m.y_max]
        p12 = [m.x_max, m.y_max]
        p21 = [m.x_max, m.y_min]
        p22 = [m.x_min, m.y_min]
        self.draw_handler.draw_line(p11, p12)
        self.draw_handler.draw_line(p12, p21)
        self.draw_handler.draw_line(p21, p22)
        self.draw_handler.draw_line(p11, p22)
    def repaint(self):
        self.draw_handler.clear_buf()
    def paint(self):
        self.draw_handler.paint()

class ConsolePaintHandler(object):
    def __init__(self, x_max=50, x_min=0, y_max=50, y_min=0, scale = 1):
        # y
        #  ^
        #  |
        #  |
        #  |
        #  |
        # O`-------------------> x
        self.x_max = x_max+1
        self.x_min = x_min
        self.y_max = y_max+1
        self.y_min = y_min
        self.scale = scale
        self.buf = [' '] * self.y_max
        for i in range(self.y_max):
            self.buf[i] = [' '] * self.x_max
    def clear_buf(self):
        for i in range(self.y_max):
            for j in range(self.x_max):
                self.buf[i][j] = ' '
    def draw_line(self, p1, p2):
        if p1[0] == p2[0]:
            # Horizontal
            x = p1[0]
            y_min = min(p1[1], p2[1])
            y_max = max(p1[1], p2[1])
            for yi in range(y_min, y_max+1):
                self.draw_point([x, yi])
        elif p1[1] == p2[1]:
            # Vertical
            y = p1[1]
            x_min = min(p1[0], p2[0])
            x_max = max(p1[0], p2[0])
            for xi in range(x_min, x_max+1):
                self.draw_point([xi, y])
        else:
            # Otherwise
            pass
    def draw_point(self, p):
        self.buf[p[1]][p[0]] = '*'
    def paint(self):
        import platform
        import os
        plat_os = platform.system()
        if plat_os == 'Windows':
            os.system("cls")
        else:
            os.system("clear")
        
        if plat_os != 'Windows':
            os.system("stty cbreak -echo")
        count = len(self.buf)
        for i in range(count):
            print ''.join(self.buf[count - i - 1])
        if plat_os != 'Windows':
            os.system("stty -cbreak echo")

class QtPaintHandler(object):
    pass

class GameSnake(object):
    M_X_MAX = 30
    M_X_MIN = 0
    M_Y_MAX = 20
    M_Y_MIN = 0
    S_INIT_X = 8
    S_INIT_Y = 1
    S_INIT_L = 7
    def __init__(self):
        # Initialize the game
        self.snake = Snake(
                GameSnake.S_INIT_X, 
                GameSnake.S_INIT_Y, 
                GameSnake.S_INIT_L)
        self.game_map = GameMap(
                GameSnake.M_X_MAX,
                GameSnake.M_X_MIN,
                GameSnake.M_Y_MAX,
                GameSnake.M_Y_MIN)
        self.food = Food(
                (GameSnake.M_X_MAX + GameSnake.M_X_MIN)/2,
                (GameSnake.M_Y_MAX + GameSnake.M_Y_MIN)/2)
        self.game_paint = GamePaint(
                ConsolePaintHandler(
                    GameSnake.M_X_MAX,
                    GameSnake.M_X_MIN,
                    GameSnake.M_Y_MAX,
                    GameSnake.M_Y_MIN))
        self.start = False
        self.pause = False
    def game_start(self):
        self.start = True
        print "Game Start!"
    def game_pause(self):
        self.pause = True
        print "Game Pause!"
    def game_over(self):
        self.start = False
        print "Game Over!"
        h_s = self.game_getscore()
        s = self.snake.length
        if h_s < s:
            self.game_log()
            h_s = s
        print "Score:", s
        print "Highest Score:", h_s
        print "Press any key to exit"
    def game_getscore(self):
        try:
            f = open("log", "rU")
            lines = f.readlines()
            if lines != []:
                return int(lines[0])
            else:
                return 0
            f.close()
        except:
            return 0
    def game_log(self):
        f = open("log", "w")
        f.write(str(self.snake.length))
        f.close()
    def main_thread(self):
        count = 0
        while True:
            if self.start == True and self.pause == False:
                # Paint first !
                self.game_paint.repaint()
                self.game_paint.draw_map(self.game_map)
                self.game_paint.draw_food(self.food)
                self.game_paint.draw_snake(self.snake)
                self.game_paint.paint()
                # Snake move
                self.snake.move()
                # Dead ?
                if self.snake.trace[0][0] in \
                       [self.game_map.x_max, self.game_map.x_min] or \
                   self.snake.trace[0][1] in \
                       [self.game_map.y_max, self.game_map.y_min] or \
                   self.snake.trace[0] in self.snake.trace[1:]:
                    break
                # Grow ?
                if self.snake.trace[0] == [self.food.x, self.food.y]:
                    self.snake.grow()
                    # Renew food
                    x_new = random.randint(
                            self.game_map.x_min+1, 
                            self.game_map.x_max-1)
                    y_new = random.randint(
                            self.game_map.y_min+1, 
                            self.game_map.y_max-1)
                    while [x_new, y_new] in self.snake.trace:
                        x_new = random.randint(
                                self.game_map.x_min+1, 
                                self.game_map.x_max-1)
                        y_new = random.randint(
                                self.game_map.y_min+1, 
                                self.game_map.y_max-1)
                    self.food.renew(x_new, y_new)
                # Delay
                time.sleep(0.1)
        self.game_over()
    def paint_thread(self):
        while self.start == True:
            # Paint first !
            self.game_paint.repaint()
            self.game_paint.draw_map(self.game_map)
            self.game_paint.draw_food(self.food)
            self.game_paint.draw_snake(self.snake)
            self.game_paint.paint()
            # Delay
            time.sleep(0.1)
    def key_thread(self):
        import getkey
        getch = getkey.Getch()
        while self.start == True:
            key = None
            c = getch()
            if c == 'w':
                key = Snake.UP
            elif c == 'd':
                key = Snake.RIGHT
            elif c == 's':
                key = Snake.DOWN
            elif c == 'a':
                key = Snake.LEFT
            # Turn ?
            if key != None:
                self.snake.turn(key)
            time.sleep(0.1)
def main():
    game = GameSnake()
    game.game_start()
    threading.Thread(target = game.key_thread).start() 
    threading.Thread(target = game.main_thread).start()
if __name__ == '__main__':
    main()
