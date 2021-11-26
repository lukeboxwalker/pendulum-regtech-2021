from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Color, Line, Ellipse
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.widget import Widget
import numpy as np
from math import pi, sin, cos, exp


class Simulation(App):

    def build(self):
        ui = SystemWidget()
        Clock.schedule_interval(ui.update, 1 / 60)
        return ui


class SystemWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.length = 150
        self.theta = np.array([1, 0])
        self.start_time = Clock.get_time()

    def get_time(self):
        return Clock.get_time() - self.start_time

    def draw_figure(self):
        theta = self.theta[1] - (pi / 2)
        pos = np.array([cos(theta), sin(theta)]) * self.length
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1, 1)
            center_x = Window.size[0] // 2
            center_y = Window.size[1] // 2
            Line(points=[center_x, center_y, center_x + pos[0], center_y + pos[1]], width=1)

            size = 15
            dif = (size + 1) // 2
            Color(1, 1, 1, 1)
            Ellipse(pos=(center_x - dif + pos[0], center_y - dif + pos[1]), size=(size, size))

    def update(self, *args):

        def f(x):
            return np.array([x[1], -9.81/self.length * sin(x[0])])

        h = 0.1
        theta = self.theta
        self.theta = (theta + h * f(theta))

        self.draw_figure()


Simulation().run()
