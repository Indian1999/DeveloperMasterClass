from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.vector import Vector

class Tower:
    def __init__(self, widget, position, range = 150):
        self.widget = widget
        self.pos = position
        self.range = range
        self.size = (40, 40)
        with widget.canvas:
            Color(0,0,1)
            self.rect = Rectangle(pos=self.pos, size = self.size)
        Clock.schedule_interval(self.attack, 0.5)
        
    def attack(self, deltaTime):
        for enemy in self.widget.enemies:
            if self.is_in_range(enemy):
                print("attack") #TODO
    
    def is_in_range(self, enemy):
        dist =  Vector(*self.pos).distance(Vector(*enemy.pos))
        return dist <= self.range
        
    