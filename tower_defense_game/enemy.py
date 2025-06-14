from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector

class Enemy:
    def __init__(self, widget, path_points):
        self.widget = widget
        self.path = path_points
        self.current_index = 0 # Hanyadik path pointnál jár?
        self.speed = 20
        self.size = (30, 30)
        self.pos = list(self.path[0])   # [0, 200]
        self.max_hp = 50
        self.health = self.max_hp
        self.damage = 50
        self.value = 15
        self.moving = True
        
        with widget.canvas:
            Color(1,0,0) #Piros
            self.rect = Rectangle(pos=self.pos, size = self.size)
            Color(1,1,1)
            self.hp_bar = Rectangle(pos=self.pos, size = (self.size[0], 5))
            
        self.alive = True    
        Clock.schedule_interval(self.move, 1/60)
        Clock.schedule_interval(self.attack, 0.5)
    
    def attack(self, dt):
        for soldier in self.widget.soldiers:
            if self.distance_to(soldier.pos[0], soldier.pos[1]) < 36:
                soldier.takeDamage(self.damage)
    
    def destroy(self):
        if hasattr(self, "rect") and self.rect in self.widget.canvas.children:
            self.widget.canvas.remove(self.rect)
        if hasattr(self, "hp_bar") and self.hp_bar in self.widget.canvas.children:
            self.widget.canvas.remove(self.hp_bar)
        try:
            self.widget.enemies.remove(self)
        except:
            pass
        del self
    
    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.widget.parent.parent.money += self.value
            self.widget.parent.parent.score += self.value
            self.destroy()
        self.hp_bar.size = (self.health/self.max_hp * self.size[0],5)
        
        
    def move(self, deltaTime):
        if self.current_index >= len(self.path)-1:
            self.widget.parent.parent.health -= self.damage
            if self.widget.parent.parent.health <= 0:
                self.widget.show_game_over()
            self.destroy()
            return # Kilépünk, mert elértük a célt
        
        close_soldier = False
        for soldier in self.widget.soldiers:
            if self.distance_to(soldier.pos[0], soldier.pos[1]) < 35:
                close_soldier = True
                
        
        close_enemy = False
        try:
            index = self.widget.enemies.index(self)
        except:
            return
        if index != 0:
            enemy_ahead = self.widget.enemies[index - 1]
            if self.distance_to(enemy_ahead.pos[0], enemy_ahead.pos[1]) < 35:
                close_enemy = True
            
        self.moving = not close_enemy and not close_soldier
        if self.moving:
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
                self.hp_bar.pos = self.pos
        
    
    def distance_to(self, x0, y0):
        return ((self.pos[0] - x0) ** 2 + (self.pos[1] - y0) ** 2)**(1/2)