from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, InstructionGroup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty

from enemy import Enemy
from tower import Tower
from soldier import Soldier

class GameUI(BoxLayout):
    money = NumericProperty(200)
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
        Window.bind(mouse_pos=self.on_mouse_move)
        self.enemies = []
        self.soldiers = []
        self.towers = []
        self.draw_path()
        self.wave_in_progress = False
        self.enemies_to_spawn = 0
        self.basic_ghost_tower = None
        #self.towers.append(Tower(self, (500, 500)))
        #Clock.schedule_interval(self.spawn_enemy, 5)
        Clock.schedule_once(self.start_first_wave, 2)
           
    def start_first_wave(self, dt):
        app = App.get_running_app()
        ui = app.root
        
        self.wave_in_progress = True
        self.enemies_to_spawn = 5
        ui.wave = 1
        
        Clock.schedule_interval(self.spawn_enemy_in_wave, 0.5)
        
    def spawn_enemy_in_wave(self, dt):
        if self.enemies_to_spawn > 0:
            self.spawn_enemy()
            self.enemies_to_spawn -= 1
        else:
            Clock.unschedule(self.spawn_enemy_in_wave)
            self.wave_in_progress = False
            self.schedule_next_wave()
            
    def schedule_next_wave(self):
        Clock.schedule_once(self.start_next_wave, 10) # 10 mp downtime 2 wave között
    
    def start_next_wave(self, dt):
        app = App.get_running_app()
        ui = app.root
        
        ui.wave += 1
        self.wave_in_progress = True
        self.enemies_to_spawn = ui.wave * 5
        
        Clock.schedule_interval(self.spawn_enemy_in_wave, 0.5)
        
    def summon_soldier(self):
        app = App.get_running_app()
        ui = app.root
        if ui.money >= 50:
            self.soldiers.append(Soldier(self, self.path_points))
            ui.money -= 50
    
    def is_valid_tower_position(self, x, y):
        for i in range(len(self.path_points) - 1):
            A = self.path_points[i]
            B = self.path_points[i + 1]
            if self.segment_point_distance(A, B, (x, y)) < 50:
                return False
        return True
            
    def segment_point_distance(self, A, B, P):
        def point_distance(A, B):
            return (  (A[0]-B[0])**2 + (A[1]-B[1])**2    )**(1/2)
        (x1, y1) = A    
        (x2, y2) = B
        (xp, yp) = P
        # A->B vektor
        vx = x2 - x1
        vy = y2 - y1
        wx = xp - x1    
        wy = yp - y1   
        
        s1 = vx * wx + vy * wy # v * w (Skaláris szorzat)
        s2 = vx * vx + vy * vy # v * v
        
        t = s1/s2
        if t < 0:
            return point_distance(A, P)
        elif t > 1:
            return point_distance(B, P)
        else:
            qx = x1 + t*vx
            qy = y1 + t*vy
            return point_distance((qx, qy), P)
        
        # Ha t < 0, akkor a legközelebbi pont a szakasz A pontja
        # Ha t > 1, akkor a legközelebbi pont a szakasz B pontja
        # ha t >= 0 és t <= 1, akkor valahol a szakasz közepént
        # Legközelebbi pont: Q = A + t * AB(vektor)
            
    def on_touch_down(self, touch):
        app = App.get_running_app()
        ui = app.root
        if ui.placing_basic_tower and self.is_valid_tower_position(touch.x, touch.y):
            self.towers.append(Tower(self, (touch.x, touch.y)))
            ui.finish_basic_tower_placement()
            self.remove_basic_ghost_tower()
        
    def on_mouse_move(self, window, pos):
        app = App.get_running_app()
        ui = app.root
        if ui.placing_basic_tower:
            self.show_basic_ghost_tower(pos[0], pos[1])
        return True    
        
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
            

    def spawn_enemy(self, deltaTime = None):
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