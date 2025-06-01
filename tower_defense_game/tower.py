from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.vector import Vector
from bullet import Bullet

class Tower:
    def __init__(self, widget, position, range = 150):
        self.widget = widget
        self.pos = position
        self.range = range
        self.size = (40, 40)
        self.bullets = []
        self.damage = 10
        with widget.canvas:
            Color(0,0,1)
            self.rect = Rectangle(pos=self.pos, size = self.size)
        Clock.schedule_interval(self.attack, 0.5)
        
    def attack(self, deltaTime):
        for enemy in self.widget.enemies:
            if self.is_in_range(enemy):
                self.bullets.append(Bullet(self.widget, self, enemy, self.damage))
                break # Kilépónk a ciklusból, hogy csak 1 ellenséget támadjon
    
    def is_in_range(self, enemy):
        dist =  Vector(*self.pos).distance(Vector(*enemy.pos))
        return dist <= self.range
        
    