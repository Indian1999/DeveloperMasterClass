from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector

class Enemy:
    def __init__(self, widget, path_points):
        self.widget = widget
        self.path = path_points
        self.current_index = 0 # Hanyadik path pointnál jár?
        self.speed = 2
        self.size = (30, 30)
        self.pos = list(self.path[0])   # [0, 200]
        self.health = 50
        
        with widget.canvas:
            Color(1,0,0) #Piros
            self.rect = Rectangle(pos=self.pos, size = self.size)
            
        self.alive = True    
        Clock.schedule_interval(self.move, 1/60)
    
    def destroy(self):
        if hasattr(self, "rect") and self.rect in self.widget.canvas.children:
            self.widget.canvas.remove(self.rect)
        try:
            self.widget.enemies.remove(self)
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
        
        target = self.path[self.current_index + 1]
        direction = Vector(*target) - Vector(*self.pos)
        # target = (50, 100)
        # *target -> 50, 100
        # Vector(target), akkor egy tuple-t adok át a Vector konstruktorának (HIBÁT okozna)
        # Vector(*target), akkor több egyszerű paramétert adok át
        # * kicsomagoló operátor pythonban
        if direction.length() < self.speed:
            self.current_index += 1
        else:
            step = direction.normalize() * self.speed
            self.pos[0] += step.x
            self.pos[1] += step.y
            self.rect.pos = self.pos
        