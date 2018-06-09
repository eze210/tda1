from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.filechooser import FileChooser, FileChooserIconView

from shipPlayer import *


class ShipButton(Button):

    def __init__(self, ship, game, **kwargs):
        super(ShipButton, self).__init__(**kwargs)
        self.ship = ship
        self.game = game

    def on_press(self):
        super(ShipButton, self).on_press()
        game.selectRow(self.ship.identifier)
        self.parent.update()


class GridView(GridLayout):

    def __init__(self, game, **kwargs):
        super(GridView, self).__init__(**kwargs)
        self.game = game
        self.buttons = {}
        ships = game.shipPlayer.getShips()
        self.rows = len(ships)
        for ship in ships:
            label = Label(halign='center', text="Vida restante:\n{}".format(ship.health))
            self.add_widget(label)
            for turn, d in enumerate(ship.damageList):
                if turn not in self.buttons:
                    self.buttons[turn] = []

                button = ShipButton(ship, game, text="{}".format(d))
                self.add_widget(button)
                self.buttons[turn].append(button)

        self.update()

    def update(self):
        currentTurn = self.game.getCurrentTurn()
        for turn, buttons in self.buttons.items():
            for button in buttons:
                if turn is currentTurn % len(self.buttons):
                    button.disabled = False
                else:
                    button.disabled = True


class GameView(GridLayout):

    def __init__(self, game, **kwargs):
        super(GameView, self).__init__(**kwargs)
        self.gridView = GridView(game)

        self.cols = 1
        self.add_widget(self.gridView)


class GameApp(App):

    def __init__(self, game):
        self.game = game
        App.__init__(self)

    def build(self):
        return GameView(self.game)

if __name__ == '__main__':
    if len(argv) < 2:
        print("Uso: python {} <shipfile>".format(argv[0]))
        exit(1)
    fileName = argv[1]
    print("Cargando {0}".format(fileName))
    game = loadGame(fileName)

    GameApp(game).run()
