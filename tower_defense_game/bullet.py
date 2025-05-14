from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.vector import Vector

class Bullet:
    def __init__(self, widget, tower, target):
        self.widget = widget
        self.tower = tower
        self.pos = list(tower.pos)
        self.target = target
        self.speed = 8
        self.size = (6,6)
        with widget.canvas:
            Color(0, 1, 1)
            self.rect = Rectangle(pos=self.pos, size = self.size)
        self.alive = True
        Clock.schedule_interval(self.move, 1/60)
        
    def move(self, deltaTime):
        if not self.alive or self.target == None or not self.target.alive:
            self.destroy()
            return
        
        direction = Vector(*self.target.pos) - Vector(*self.pos)
        if direction.length() <= self.speed:
            self.target.destroy()
            self.destroy()
        else:
            step = direction.normalize() * self.speed
            self.pos[0] += step.x
            self.pos[1] += step.y
            self.rect.pos = self.pos
    
    def destroy(self):
        if hasattr(self, "rect") and self.rect in self.widget.canvas.children:
            self.widget.canvas.remove(self.rect)
        self.tower.bullets.remove(self)
        del self