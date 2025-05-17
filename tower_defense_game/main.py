from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, InstructionGroup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty



from enemy import Enemy
from tower import Tower

class GameUI(BoxLayout):
    money = NumericProperty(500)
    health = NumericProperty(100)
    wave = NumericProperty(1)
    placing_basic_tower = BooleanProperty(False)
    
    def building_basic_tower(self):
        if (self.money >= 150):
            self.placing_basic_tower = True
        else:
            print("Not enough money!")
    
    def finish_basic_tower_placement(self):
        if self.placing_basic_tower:
            self.money -= 150
            self.placing_basic_tower = False
    
    def summon_soldier(self):
        pass

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
        self.basic_ghost_tower = None
        self.towers.append(Tower(self, (500, 500)))
        Clock.schedule_interval(self.spawn_enemy, 5)
        
        
    def on_touch_down(self, touch):
        app = App.get_running_app()
        ui = app.root
        if ui.placing_basic_tower:
            self.towers.append(Tower(self, (touch.x, touch.y)))
            ui.finish_basic_tower_placement()
            self.remove_basic_ghost_tower()
            
    def on_touch_move(self, touch):
        app = App.get_running_app()
        ui = app.root
        if ui.placing_basic_tower:
            self.show_basic_ghost_tower(touch.x, touch.y)
        
    def show_basic_ghost_tower(self, x, y):
        if self.basic_ghost_tower:
            self.canvas.remove(self.basic_ghost_tower)
        self.basic_ghost_tower = InstructionGroup()
        self.basic_ghost_tower.add(Color(0, 0, 1, 0.2))
        self.basic_ghost_tower.add(Rectangle(pos = (x, y), size = (40,40)))
        self.canvas.add(self.basic_ghost_tower)
        
    def remove_basic_ghost_tower(self):
        if self.basic_ghost_tower:
            self.canvas.remove(self.basic_ghost_tower)
            self.basic_ghost_tower = None
            
        
            
          
    def spawn_enemy(self, deltaTime):
        self.enemies.append(Enemy(self, self.path_points))
        
    def draw_path(self):
        with self.canvas:
            Color(0.6, 0.4, 0.2) # Barna
            Line(points=sum(self.path_points, ()), width=40, cap = "round")
        
    
class TowerDefenseApp(App):
    def build(self):
        return GameUI()
    
if __name__ == "__main__":
    TowerDefenseApp().run()