#!/usr/bin/python
# -*- coding: utf-8 -*-

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
        self.buf = ['  '] * self.y_max
        for i in range(self.y_max):
            self.buf[i] = ['  '] * self.x_max
    def clear_buf(self):
        for i in range(self.y_max):
            for j in range(self.x_max):
                self.buf[i][j] = '  '
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
        self.buf[p[1]][p[0]] = '* '
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
