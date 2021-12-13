from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel

import numpy as np
from math import pi, sin, cos, atan


class ModelSolver:

    def __init__(self, theta=0.0, fps=1):
        self.theta = np.array([theta, 0.0])
        self.x = np.array([0.0, 0.0])
        self.u = 0.0
        self.fps = fps

        self.h = 0.001
        self.M = 0.38
        self.m = 0.23
        self.g = -9.81
        self.L = 0.33
        self.d = 1

        self.frozen = False

    def reset(self, theta):
        self.theta = np.array([theta, 0.0])
        self.x = np.array([0.0, 0.0])

    def f_x(self, pos, t, u):
        return np.array([pos[1],
                         (self.m * sin(t[0]) * (self.L * t[1] ** 2 - self.g * cos(t[0])) - self.d * pos[1] - u)
                         / (self.M + self.m * sin(t[0]) ** 2)])

    def f_theta(self, t, pos, u):
        return np.array([t[1],
                         ((self.m + self.M) * self.g * sin(t[0]) - cos(t[0])
                          * (self.m * self.L * t[1] ** 2 * sin(t[0]) - self.d * pos[1] + u))
                         / (self.L * (self.M + self.m * sin(t[0]) ** 2))])

    def next(self):
        if self.frozen:
            return
        i = 0
        while i < self.fps:
            x = self.x
            theta = self.theta
            self.x = x + self.h * self.f_x(x, theta, self.u)
            self.theta = theta + self.h * self.f_theta(theta, x, self.u)
            i = i + self.h


class Simulation(App):

    def build(self):
        fps = 1 / 60
        system = SystemWidget(fps)
        Clock.schedule_interval(lambda *args: system.update(), fps)
        return system


class SystemWidget(Widget):

    def __init__(self, fps, **kwargs):
        super().__init__(**kwargs)
        self.length = 150
        self.model_solver = ModelSolver(theta=1 / 15 * pi, fps=fps)

    def draw(self):
        x = Window.size[0] // 2
        y = Window.size[1] // 2
        theta = self.model_solver.theta[0] - (pi / 2)
        pos = np.array([cos(theta), sin(theta)]) * self.length

        with self.canvas:
            self.canvas.clear()
            Color(1, 1, 1, 0.5)
            Line(points=[x - self.length * 10, y, x + self.length * 10, y], width=1)

            Color(1, 1, 1, 1)
            for i in range(-10, 11):
                xp = x + self.model_solver.x[0] * 100 + i * 100
                Line(points=[xp, y + 30, xp, y + 40], width=1)
                core_l = CoreLabel(text=str(float(i)))
                core_l.refresh()
                Rectangle(texture=core_l.texture, pos=(xp - core_l.size[0] // 2, y + 40), size=core_l.size)

            Line(rectangle=[x - 20, y - 10, 40, 20], width=1)
            Line(points=[x, y, x + pos[0], y + pos[1]], width=1)
            Ellipse(pos=(x - 7 + pos[0], y - 7 + pos[1]), size=(13, 13))

            x, y = x + x // 2, y + y // 2
            Line(points=[x + 20, y + 20, x + 30, y + 30, x + 20, y + 40], width=1)
            x, y = x - Window.size[0] // 2, y
            Line(points=[x - 20, y + 20, x - 30, y + 30, x - 20, y + 40], width=1)

            text = "θ = %+.*f" % (4, self.model_solver.theta[0]) + \
                   "\nx = %+.*f" % (4, self.model_solver.x[0]) + \
                   "\nu = %+.*f" % (4, self.model_solver.u)
            Label(text=text)

    def on_touch_down(self, touch):
        if touch.y < Window.size[1] // 2:
            self.model_solver.frozen = True
            self.on_touch_move(touch)
        else:
            x = touch.x - Window.size[0] // 2
            self.model_solver.u = x / 100

    def on_touch_up(self, touch):
        self.model_solver.frozen = False
        self.model_solver.u = 0

    def on_touch_move(self, touch):
        if touch.y < Window.size[1] // 2:
            x = touch.x - Window.size[0] // 2
            y = self.length
            self.model_solver.reset(atan(x / y))

    def update(self):
        self.model_solver.next()
        self.draw()


Simulation().run()
