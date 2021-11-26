from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
import numpy as np
from math import pi, sin, cos, atan


class ModelSolver:

    def __init__(self, theta=0.0):
        self.theta = np.array([theta, 0.0])
        self.x = np.array([0.0, 0.0])
        self.u = 0

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

    def f_x(self, v, t, u):
        return np.array([v[1], 1 / (self.M + self.m * sin(t[0]) ** 2) * (
                self.m * sin(t[0]) * (self.L * t[1] ** 2 - self.g * cos(t[0])) - self.d * v[
            1] - u)])

    def f_theta(self, t, v, u):
        return np.array([t[1], 1 / (self.L * (self.M + self.m * sin(t[0]) ** 2)) * (
                (self.m + self.M) * self.g * sin(t[0]) - cos(t[0]) * (
                self.m * self.L * t[1] ** 2 * sin(t[0]) - self.d * v[1] + u))])

    def next(self, fps):
        if self.frozen:
            return
        i = 0
        while i < fps:
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
        self.fps = fps
        self.length = 150
        self.model_solver = ModelSolver(theta=1 / 15 * pi)

    def draw(self):
        u = self.model_solver.u
        theta = self.model_solver.theta[0] - (pi / 2)
        pos = np.array([cos(theta), sin(theta)]) * self.length

        with self.canvas:
            self.canvas.clear()

            center_x = Window.size[0] // 2 + u
            center_y = Window.size[1] // 2

            Color(1, 1, 1, 1)
            Line(points=[center_x, center_y, center_x + pos[0], center_y + pos[1]], width=1)

            size = 40
            Line(rectangle=[center_x - size // 2, center_y - size // 4, size, size // 2], width=1)

            size = 15
            dif = (size + 1) // 2
            Ellipse(pos=(center_x - dif + pos[0], center_y - dif + pos[1]), size=(size, size))

            text = "θ = %+.*f" % (4, self.model_solver.theta[0]) + \
                   "\nx = %+.*f" % (4, self.model_solver.x[0]) + \
                   "\nu = %+.*f" % (4, self.model_solver.u)
            Label(text=text)

    def on_touch_down(self, touch):
        if touch.y < Window.size[1] // 2:
            self.model_solver.frozen = True
            self.on_touch_move(touch)

    def on_touch_up(self, touch):
        self.model_solver.frozen = False
        self.model_solver.u = 0

    def on_touch_move(self, touch):
        x = touch.x - Window.size[0] // 2
        if touch.y < Window.size[1] // 2:
            y = self.length
            self.model_solver.reset(atan(x / y))
        else:
            self.model_solver.u = x / 100

    def update(self):
        self.model_solver.next(self.fps)
        self.draw()


Simulation().run()
