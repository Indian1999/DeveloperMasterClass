from kivy.app import App
from kivy.uix.widget import Widget

class GameWidget(Widget):
    def __init__(self, **kwarg):
        super().__init__()


class TowerDefenseApp(App):
    def build(self):
        return GameWidget()
    
if __name__ == "__main__":
    TowerDefenseApp().run()