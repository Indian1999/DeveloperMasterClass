from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector

class Soldier:
    def __init__(self, widget, path_points):
        self.widget = widget
        self.path = path_points[::-1]
        self.current_index = 0 # Hanyadik path pointnál jár?
        self.speed = 2
        self.size = (30, 30)
        self.pos = list(self.path[0])   # [0, 200]
        self.health = 100
        self.damage = 10
        self.value = 50
        self.moving = True
        
        with widget.canvas:
            Color(0.4,0.1,0.7)
            self.rect = Rectangle(pos=self.pos, size = self.size)
            
        self.alive = True    
        Clock.schedule_interval(self.move, 1/60)
    
    def destroy(self):
        if hasattr(self, "rect") and self.rect in self.widget.canvas.children:
            self.widget.canvas.remove(self.rect)
        try:
            self.widget.soldiers.remove(self)
        except:
            pass
        del self
    
    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.destroy()
        
    def move(self, deltaTime):
        if self.current_index >= len(self.path)-1:
            self.destroy()
            return # Kilépünk, mert elértük a célt
        
        close_enemy = False
        for enemy in self.widget.enemies:
            if self.distance_to(enemy.pos[0], enemy.pos[1]) < 35:
                close_enemy = True
                
        close_soldier = False
        index = self.widget.soldiers.index(self)
        if index != 0:
            soldier_ahead = self.widget.soldiers[index - 1]
            if self.distance_to(soldier_ahead.pos[0], soldier_ahead.pos[1]) < 35:
                close_soldier = True
            
        self.moving = not close_enemy and not close_soldier
        if self.moving:       
            target = self.path[self.current_index + 1]
            direction = Vector(*target) - Vector(*self.pos)
            if direction.length() < self.speed:
                self.current_index += 1
            else:
                step = direction.normalize() * self.speed
                self.pos[0] += step.x
                self.pos[1] += step.y
                self.rect.pos = self.pos
    
    def distance_to(self, x0, y0):
        return ((self.pos[0] - x0) ** 2 + (self.pos[1] - y0) ** 2)**(1/2)