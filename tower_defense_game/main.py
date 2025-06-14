from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Line, Color, Rectangle, InstructionGroup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import time
import requests
from enemy import Enemy
from tower import Tower
from soldier import Soldier

class GameUI(BoxLayout):
    money = NumericProperty(200)
    health = NumericProperty(100)
    wave = NumericProperty(1)
    score = NumericProperty(0)
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
           
    def show_game_over(self):
        Clock.unschedule(self.spawn_enemy_in_wave)
        self.enemies.clear()
        game_over_popup = ModalView(size_hint=(0.5, 0.3), auto_dismiss = False)
        label = Label(text= "Game Over", font_size = "24", size_hint = (0.9, 0.2))
        ui = App.get_running_app().root
        score_label = Label(text = f"Score: {ui.score}", size_hint = (0.9, 0.2))
        name_textbox = TextInput(hint_text = "Enter your name", multiline=False, size_hint= (0.9, 0.2))
        submit_btn = Button(text = "Submit", size_hint = (0.9, 0.2))
        
        layout = BoxLayout(orientation = "vertical", spacing=10, padding=10)
        layout.add_widget(label)
        layout.add_widget(score_label)
        layout.add_widget(name_textbox)
        layout.add_widget(submit_btn)
        
        game_over_popup.add_widget(layout)
        
        def submit_action(instance):
            name = name_textbox.text.strip()
            if name:
                with open("highscores.csv", "a", encoding="utf-8") as f:
                    f.write(name + ";" + str(ui.score) + ";" + str(time.time()) + "\n")
                url = "https://vincebence-500c0-default-rtdb.europe-west1.firebasedatabase.app/highscores.json"
                data = {
                    "username": name,
                    "score": ui.score,
                    "timestamp": time.time()
                }
                try:
                    response = requests.post(url, json=data)
                    if response.status_code == 200:
                        print("Score submitted to the databse.")
                    else:
                        print("Error when submitting the score.")
                        print("Status code:", response.status_code)
                        print(response.text)
                except Exception as e:
                    print("Error:", e)
            game_over_popup.dismiss()
            print("game_over closed")
            self.show_highscores()
        submit_btn.bind(on_release=submit_action)
        
        game_over_popup.open()
    
    def show_highscores(self):
        highscores_popup = ModalView(size_hint=(0.5, 0.8), auto_dismiss = False)
        
        layout = BoxLayout(orientation="vertical")
        
        url = "https://vincebence-500c0-default-rtdb.europe-west1.firebasedatabase.app/highscores.json"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            else:
                print("Status code error:", response.status_code)
        except Exception as e:
            print(e)
        
        label = Label(text=f"TOP 10", font_size = 30)
        layout.add_widget(label)
        sorted_scores = sorted(data.items(), key = lambda x: x[1]["score"], reverse = True)
        i = 0
        while i < 10 and i < len(sorted_scores):
            key, entry = sorted_scores[i]
            label = Label(text=f"{i+1}. {entry["username"]}: {entry["score"]}", font_size = "24")
            layout.add_widget(label)
            i += 1
        highscores_popup.add_widget(layout)
        restart_btn = Button(text="Restart")
        quit_btn = Button(text = "Quit")
        
        #layout.add_widget(restart_btn)
        layout.add_widget(quit_btn)
        
        def restart_game(instance):
            App.get_running_app().stop()
            TowerDefenseApp.run()
            
        restart_btn.bind(on_relese=restart_game)
        quit_btn.bind(on_release= lambda x: App.get_running_app().stop())
        
        
        highscores_popup.open()
        
        
        
    def start_first_wave(self, dt):
        app = App.get_running_app()
        ui = app.root
        
        self.wave_in_progress = True
        self.enemies_to_spawn = 5
        ui.wave = 1
        
        Clock.schedule_interval(self.spawn_enemy_in_wave, 0.5)
        
    def spawn_enemy_in_wave(self, dt):
        ui = App.get_running_app().root
        if self.enemies_to_spawn > 0:
            self.enemies.append(Enemy(
                self, self.path_points,
                speed = ui.wave // 4 + 1,
                max_hp = ui.wave * 5 + 30,
                damage = max(ui.wave * 2, 5),
                value = max(20 - ui.wave, 1)
            ))
            self.enemies_to_spawn -= 1
        elif len(self.enemies) == 0:
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