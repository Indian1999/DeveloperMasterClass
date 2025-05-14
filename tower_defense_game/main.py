from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from enemy import Enemy
from tower import Tower

class GameWidget(Widget):
    def __init__(self, **kwarg):
        super().__init__()
        self.path_points = [
            (0, Window.height // 5), 
            (Window.width // 4, Window.height // 5),
            (Window.width // 4, Window.height // 5 * 4),
            (Window.width // 4 * 3, Window.height // 5 * 4),
            (Window.width // 4 * 3, 0)
        ]
        self.enemies = []
        self.towers = []
        self.draw_path()
        self.towers.append(Tower(self, (100, 200)))
        Clock.schedule_interval(self.spawn_enemy, 5)
        
    def spawn_enemy(self, deltaTime):
        self.enemies.append(Enemy(self, self.path_points))
        
    def draw_path(self):
        with self.canvas:
            Color(0.6, 0.4, 0.2) # Barna
            Line(points=sum(self.path_points, ()), width=40, cap = "round")
        
    
class TowerDefenseApp(App):
    def build(self):
        return GameWidget()
    
if __name__ == "__main__":
    TowerDefenseApp().run()